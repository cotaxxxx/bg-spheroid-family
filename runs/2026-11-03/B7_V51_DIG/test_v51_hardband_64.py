#!/usr/bin/env python3
"""B7 V5 -> V5.1 hard-band diagnostic. NO full-domain certificate.

64 = one y band [0.562341...,1] x four p bands [1e-5,1e-4]
     x four t quarters x four u quarters.
Both variants use identical source kernels and 2^-128 arithmetic.
Only test-grid generation and the final stop condition are monkeypatched
in memory. Setting the contact loss to +10 is test-only, FORCING search
to continue until leaf cap; do not use the synthetic 'final_lower' as a theorem.

For a resumability test:
  --phase interrupt exits exactly after durable checkpoint at >=20 inner splits.
  --phase resume uses that checkpoint and completes remaining splits.
  --phase run performs an uninterrupted reference calculation.
"""
import argparse, hashlib, importlib, json, os, sys, time
from fractions import Fraction as Q
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--version',choices=('v5','v51'),required=True)
ap.add_argument('--phase',choices=('run','interrupt','resume'),default='run')
ap.add_argument('--out',required=True)
ap.add_argument('--inner-splits',type=int,default=150)
ap.add_argument('--resume-trigger',type=int,default=20)
ap.add_argument('--test-full-refinement',action='store_true',
                help='enable ordinary outer/delta/rem candidates; slower')
args=ap.parse_args()
assert args.inner_splits>=0
base=Path('/home/daybreak/B7_work')
src=base/('b7_v5_dig' if args.version=='v5' else 'b7_v51')
sys.path.insert(0,str(src))
producer_name='v6_b7_unified_outerrem_'+args.version
w=importlib.import_module(producer_name)
ye=w.geometric_edges(w.YEDGES)
pe=w.geometric_edges(w.P_CUT_EDGES,width_cap=Q(1,8))
yv=next((x for x in w.intervals(ye) if Q(56,100)<x[0]<Q(57,100) and x[1]==1))
pr=[x for x in w.intervals(pe) if Q(1,100000)<=x[0] and x[1]<=Q(1,10000)]
assert len(pr)==4 and pr[0][0]==Q(1,100000) and pr[-1][1]==Q(1,10000)
cells=[(yv,p,(Q(t,4),Q(t+1,4)),(Q(u,4),Q(u+1,4))) for p in pr for t in range(4) for u in range(4)]
assert len(cells)==64
w.inner_grid_v2=lambda:iter(cells)
w.grid_count=lambda:64
normal_cut=w.contact_cut
w.contact_cut=lambda outer:Q(10)
key='L0_T3_D0'
out=Path(args.out).resolve()
out.mkdir(parents=True,exist_ok=True)
fp=w.fingerprint()
if args.test_full_refinement:
    parts=(2,2,4);dmax=16;remmax=4;boxmax=32
else:
    parts=(1,1,1);dmax=1;remmax=1;boxmax=1
job=(key,dict(w.boxes())[key],'full',64+args.inner_splits,16,str(out),10,fp,
     parts,dmax,remmax,boxmax,False)
ckpt=out/(key+'_full.checkpoint')
result=out/(key+'_full.json')
if args.phase=='interrupt':
    assert not ckpt.exists() and not result.exists(),'interrupt requires fresh directory'
    atomic_base=w.atomic
    def hook(path,obj,as_json=False):
        atomic_base(path,obj,as_json)
        if path.suffix=='.checkpoint' and obj['state']['splits']>=args.resume_trigger:
            print('INTERRUPTED_AFTER_DURABLE_CHECKPOINT',
                  'splits',obj['state']['splits'],'active',len(obj['state']['active']),flush=True)
            os._exit(42)  # emulate process loss, after fsync/atomic replace
    w.atomic=hook
elif args.phase=='resume':
    assert ckpt.exists() and not result.exists(),'resume requires checkpoint and no final JSON'
else:
    assert not ckpt.exists() and not result.exists(),'run requires empty directory'

print('START',args.version,args.phase,'fp',fp,'newK',w.KQ,'inner64',
      'hard band y',str(yv),'p',(str(pr[0][0]),str(pr[-1][1])),
      'artificial stop loss=10', 'refinement',parts,dmax,remmax,
      'source_SHA256',hashlib.sha256((src/(producer_name+'.py')).read_bytes()).hexdigest(),
      flush=True)
t0=time.monotonic()
w.worker(job)
data=json.loads(result.read_text())
print('RESULT',args.version,args.phase,'splits',data['splits'],
      'leaves',data['leaves'],'outerref',data['outer_refinements'],
      'deltaref',data['delta_refinements'],'remref',data['outerrem_refinements'],
      'J_exact',data['total_lower'],'J_approx',float(Q(data['total_lower'])),
      'leaf_SHA256',data['leaf_file_sha256'],
      'time_s',round(time.monotonic()-t0,2),flush=True)
assert data['leaves']==64+data['splits']
assert data['splits']<=args.inner_splits
print('WARNING: DIAGNOSTIC BAND ONLY, synthetic contact cutoff; NOT A B7 PROOF.',flush=True)