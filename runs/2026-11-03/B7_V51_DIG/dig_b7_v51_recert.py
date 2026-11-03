#!/usr/bin/env python3
"""Dig B7 V5.1 checkpoint recertifier. Never modifies the origin.

Creates a NEW V5.1-compatible checkpoint from a byte-for-byte snapshot of a
V4/V4.1 checkpoint. Recomputes EVERY active leaf's K floor and three-way
selected lower bound in exact rationals. It preserves old interval caches
only when the common mathematical kernel sources have matching SHA256.

This transforms computation state; it is NOT an independent proof certificate.
The resulting final leaf file requires independent coverage and kernel audit.

Example:
 python3 dig_b7_v5_recert.py \
   --origin /home/daybreak/B7_work/b7_v41/full_v41_t3/L0_T3_D0_full.checkpoint \
   --origin-version v41 \
   --dest /home/daybreak/B7_work/b7_v5_dig/recertified_t3 \
   --max-leaves 150000 --max-depth 24
"""
import argparse, copy, hashlib, heapq, json, os, pickle, shutil, sys
from fractions import Fraction as Q
from pathlib import Path

S=1<<128
OLD_K=Q(859375,64)
NEW_K=Q(275,4)
P0=Q(1,2000000)
SIGMA0=Q(4000000,4000000000001)
COMMON=(
 'v3_fixed_128.py','v6_b_ad2_128.py','v6_b7_safe_128.py',
 'v6_b7_adaptive_128.py','v6_b7_priority_128.py',
 'v6_b7_hybrid_128.py','v6_b7_delta_local_128.py','b7_constants_v3.py'
)
SOURCE_SHA={
 'v4':'085296d892e111f2dc6c3253edacfc3653eea8b2d0ad3203e0e0d07212f0a16f',
 'v41':'017cf2726efaddbb1716af7e451708a4248ad195ad6581520e48fdc817247dfe',
}
SOURCE_FILES={'v4':'v6_b7_unified_outerrem_v4.py',
              'v41':'v6_b7_unified_outerrem_v41.py',
              'v51':'v6_b7_unified_outerrem_v51.py'}
POLICY_V5='max_midpoint_K_floor_zeroth_outerrem_v5_Astra_F_ge_minus_275_over_4'
POLICY_OLD='max_midpoint_K_floor_zeroth_outerrem_v4_Qhat_ge_minus4'

def die(message):
    raise RuntimeError(message)
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()
def fingerprint(work,version):
    names=('v3_fixed_128.py','v6_b_ad2_128.py','v6_b7_safe_128.py',
      'v6_b7_adaptive_128.py','v6_b7_priority_128.py',
      'v6_b7_hybrid_128.py',SOURCE_FILES[version],
      'v6_b7_delta_local_128.py','b7_constants_v3.py')
    if version=='v51':names+=('b7_constants_v5.py',)
    h=hashlib.sha256()
    for name in names:
        h.update(name.encode())
        with (work/name).open('rb') as f:
            for chunk in iter(lambda:f.read(8*1024*1024),b''):
                h.update(chunk)
    return h.hexdigest()
def k_floor(cell,k):
    (ya,yb),(pa,pb),(ta,tb),(ua,ub)=cell
    sigma=lambda p:2*p/(1+p*p)
    ds=sigma(pb)-sigma(pa)
    db=2*(tb-ta)/(1+ta*ta)
    val=-2*k*ds*db*(yb-ya)*(ub-ua)
    return (val*S).__floor__()
def selected(main,rem,zeroth,kfloor):
    midpoint=main+sum(rem)
    return max((('K_FLOOR',kfloor),('MIDPOINT',midpoint),
                ('ZEROTH',zeroth)),key=lambda x:x[1])
def prefactor(j,cfg):
    llo,lhi=map(Q,cfg['outer'][0])
    val=j*llo*Q(7,11) if j>=0 else j*lhi*Q(2,3)
    return val
def final(j,cfg,k):
    lhi=Q(cfg['outer'][0][1])
    return prefactor(j,cfg)-2*lhi*k*SIGMA0
def atomic_pickle(path,obj):
    temp=path.with_name(path.name+'.tmp')
    with temp.open('wb') as f:
        pickle.dump(obj,f,protocol=4)
        f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
def atomic_json(path,obj):
    temp=path.with_name(path.name+'.tmp')
    with temp.open('w') as f:
        json.dump(obj,f,indent=2,sort_keys=True)
        f.flush();os.fsync(f.fileno())
    os.replace(temp,path)

def run(args):
    root=Path(__file__).resolve().parent
    origin=Path(args.origin).resolve()
    if not origin.is_file():die('missing origin checkpoint')
    work=Path(args.origin_work).resolve() if args.origin_work else origin.parent.parent
    dest=Path(args.dest).resolve()
    if dest == origin.parent or dest == work:
        die('destination must be separate from origin directory')
    if not (origin.name.endswith('_full.checkpoint')):
        die('origin must be a full checkpoint')
    if not work.joinpath(SOURCE_FILES[args.origin_version]).is_file():
        die('missing frozen origin producer source')

    source_sha=sha(work/SOURCE_FILES[args.origin_version])
    if source_sha!=SOURCE_SHA[args.origin_version]:
        die('origin producer source SHA mismatch')
    for name in COMMON:
        if sha(work/name)!=sha(root/name):
            die('common math kernel source changed: '+name)
    expected_origin_fp=fingerprint(work,args.origin_version)
    expected_v5_fp=fingerprint(root,'v51')
    if sha(root/'b7_constants_v5.py') != (
        '3d766084caabc5738ea3de70068d688635e6b565a0a8fbe29d14c18ccec3c9c0'):
        die('V5 mathematical constant source not pinned')

    dest.mkdir(parents=True,exist_ok=True)
    snapshot_dir=dest/'snapshots';snapshot_dir.mkdir(exist_ok=True)
    snapshot=snapshot_dir/(origin.name+'.source_copy')
    if snapshot.exists():
        if sha(snapshot)!=sha(origin):
            die('existing origin snapshot differs; choose a fresh destination')
    else:
        pending=snapshot.with_name(snapshot.name+'.tmp')
        with origin.open('rb') as fi,pending.open('wb') as fo:
            shutil.copyfileobj(fi,fo,8*1024*1024)
            fo.flush();os.fsync(fo.fileno())
        os.replace(pending,snapshot)
    source_copy_sha=sha(snapshot)
    print('SNAPSHOT_SHA256',source_copy_sha,flush=True)
    with snapshot.open('rb') as f:
        saved=pickle.load(f)
    cfg=saved['config'];state=saved['state']
    if cfg['fingerprint']!=expected_origin_fp:die('source fingerprint mismatch')
    if Q(cfg['KQ'])!=OLD_K or cfg['bound_policy']!=POLICY_OLD:
        die('origin floor constant or bound policy does not match known V4/V41')
    if cfg['mode']!='full' or Q(cfg['p_cut'])!=P0 or Q(cfg['sigma_cut'])!=SIGMA0:
        die('unexpected domain or normalization')
    if not state.get('initialized',False):
        die('origin full grid is not completely initialized; cannot recertify yet')
    if len(state['active'])!=cfg['grid_count']+state['splits']:
        die('leaf count differs from grid_count + inner splits')
    if len(state['active'])>args.max_leaves:
        die('new leaf cap smaller than existing active leaves')
    if max(x['depth'] for x in state['active'].values())>args.max_depth:
        die('new depth cap smaller than existing leaf depth')

    active=state['active']
    old_total=0;old_main=0;old_zero=0;old_rem=[0]*4
    new_total=0;new_main=0;new_zero=0;new_rem=[0]*4
    old_count={};new_count={}
    old_heap_ids={uid for _,uid in state['heap'] if uid in active}
    new_heap=[]
    switched=0;resurrected=0;strict_gain=0
    for count,(uid,leaf) in enumerate(active.items(),1):
        cell=leaf['cell']
        if any(a>=b for a,b in cell):die('degenerate leaf cell')
        if leaf['depth']<0:die('negative depth')
        main=leaf['main'];rem=leaf['rem'];zero=leaf['zeroth']
        if any(x.lo>x.hi for x in [main,zero]+rem):die('bad interval')
        # Validating both endpoints prevents accidental use of a stale
        # midpoint/remainder cache after the source switch.
        if main.lo+sum(x.lo for x in rem)!=leaf['midpoint'].lo:
            die('midpoint lower does not match interval components')
        if main.hi+sum(x.hi for x in rem)!=leaf['midpoint'].hi:
            die('midpoint upper does not match interval components')
        if leaf['total'].lo!=leaf['midpoint'].lo or leaf['total'].hi!=leaf['midpoint'].hi:
            die('total stored interval differs from midpoint')
        original_floor=k_floor(cell,OLD_K)
        if leaf['k_floor_raw']!=original_floor:
            die('original floor did not match its mathematical definition')
        src_old,sel_old=selected(leaf['midpoint'].lo,[0],zero.lo,original_floor)
        if leaf['total_lo_selected']!=sel_old or leaf['bound_source']!=src_old:
            die('original bound source or selected value inconsistent')
        old_total+=sel_old;old_main+=main.lo;old_zero+=zero.lo
        for i,v in enumerate(rem):old_rem[i]+=v.lo
        old_count[src_old]=old_count.get(src_old,0)+1

        floor_new=k_floor(cell,NEW_K)
        src_new,sel_new=selected(leaf['midpoint'].lo,[0],zero.lo,floor_new)
        if sel_new<sel_old:die('new selected lower became worse')
        new_total+=sel_new;new_main+=main.lo;new_zero+=zero.lo
        for i,v in enumerate(rem):new_rem[i]+=v.lo
        new_count[src_new]=new_count.get(src_new,0)+1
        if src_new!=src_old:switched+=1
        if sel_new>sel_old:strict_gain+=1
        leaf['k_floor_raw']=floor_new
        leaf['total_lo_selected']=sel_new
        leaf['bound_source']=src_new
        axis=leaf['axis']
        # V4.1 search remains unchanged; only floor-dependent score is
        # recalculated. Raised depth caps can re-enable inner candidates.
        inn=3*max(0,-rem[axis].lo)//4 if leaf['depth']<args.max_depth else 0
        leaf['inner_score']=inn
        score=max(inn,leaf['main_width'],leaf['rem_width'],leaf['zeroth_width'])
        if src_new!='MIDPOINT':score=min(score,abs(sel_new))
        leaf['score']=score
        if score>0:
            new_heap.append((-score,uid))
            if uid not in old_heap_ids:resurrected+=1
        if count%10000==0:
            print('RECALCULATED',count,'of',len(active),flush=True)

    if old_main!=state['main_lo'] or old_zero!=state['zeroth_lo']:
        die('original midpoint/zeroth aggregates do not match leaves')
    if old_rem!=state['rem_lo'] or old_total!=state['total_lo']:
        die('original remainder/selected aggregates do not match leaves')
    assert new_main==old_main and new_zero==old_zero and new_rem==old_rem
    old_j=Q(old_total,S)
    old_final=final(old_j,cfg,OLD_K)
    old_contact=2*Q(cfg['outer'][0][1])*OLD_K*SIGMA0
    if new_total<old_total:die('new aggregate is lower than original')
    heapq.heapify(new_heap)
    state['heap']=new_heap
    state['total_lo']=new_total
    # Other aggregates are mathematically unchanged and already checked.
    cfg['fingerprint']=expected_v5_fp
    cfg['KQ']=str(NEW_K)
    cfg['bound_policy']=POLICY_V5
    cfg['limit']=args.max_leaves
    cfg['depth']=args.max_depth
    new_j=Q(new_total,S)
    new_final=final(new_j,cfg,NEW_K)
    key=cfg['key']
    out_checkpoint=dest/(key+'_full.checkpoint')
    out_report=dest/(key+'_v51_recert_report.json')
    if out_checkpoint.exists() or out_report.exists():
        die('destination output already exists; refusing to overwrite')
    report={
     'schema':'DIG-B7-V51-CHECKPOINT-RECERT-v1',
     'key':key,'version_origin':args.origin_version,
     'origin_checkpoint_path':str(origin),
     'origin_source_copy':str(snapshot),
     'origin_checkpoint_sha256':source_copy_sha,
     'origin_source_sha256':source_sha,
     'origin_fingerprint':expected_origin_fp,
     'v51_fingerprint':expected_v5_fp,
     'v51_producer_sha256':sha(root/SOURCE_FILES['v51']),
     'v51_constants_sha256':sha(root/'b7_constants_v5.py'),
     'v51_constant':str(NEW_K),'old_constant':str(OLD_K),
     'old_leaf_count':len(active),
     'old_heap_live_uids':len(old_heap_ids),'v51_heap_live_uids':len(new_heap),
     'requeued_from_old_heap_absence':resurrected,
     'changed_bound_source':switched,
     'improved_selected_leaves':strict_gain,
     'old_source_counts':old_count,'v51_source_counts':new_count,
     'old_J_exact':str(old_j),'new_J_exact':str(new_j),
     'old_contact_loss_exact':str(old_contact),
     'new_contact_loss_exact':str(2*Q(cfg['outer'][0][1])*NEW_K*SIGMA0),
     'old_final_exact':str(old_final),'new_final_exact':str(new_final),
     'new_final_positive':new_final>0,
     'preliminary_status':'POSITIVE_AWAITING_INDEPENDENT_AUDIT' if new_final>0 else 'OPEN',
     'warning':'This is transformed solver state, not an independently certified PASS; full leaf coverage and kernel intervals require audit.',
    }
    atomic_pickle(out_checkpoint,{'config':cfg,'state':state})
    report['v51_checkpoint_sha256']=sha(out_checkpoint)
    atomic_json(out_report,report)
    print('OUT_CHECKPOINT',out_checkpoint,flush=True)
    print('REPORT',out_report,flush=True)
    print('NEW_FINAL',str(new_final),'PRELIMINARY_STATUS',report['preliminary_status'],flush=True)
    print('OLD->V51',str(old_j),'->',str(new_j),'leaves',len(active),'improved',strict_gain,flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--origin',required=True)
    ap.add_argument('--origin-version',required=True,choices=('v4','v41'))
    ap.add_argument('--origin-work')
    ap.add_argument('--dest',required=True)
    ap.add_argument('--max-leaves',type=int,default=150000)
    ap.add_argument('--max-depth',type=int,default=24)
    args=ap.parse_args()
    if args.max_leaves<1 or args.max_depth<0:ap.error('invalid limits')
    run(args)
if __name__=='__main__':main()