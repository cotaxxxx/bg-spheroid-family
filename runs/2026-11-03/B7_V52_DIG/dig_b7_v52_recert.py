#!/usr/bin/env python3
"""Dig V5.1 -> V5.2 checkpoint reauthentication (NOT independent audit).

Copies the source checkpoint atomically into a new destination, checks
original producer+shared source provenance, recomputes every active leaf's
ASTRA3 fourth bound, reselects max of four bounds in exact raw 2^-128
integers, rebuilds the priority heap, and writes a NEW V5.2 checkpoint.

Never changes V5.1 producer/checkpoint. Only use in full production
after chat's independent V5.2 implementation audit.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import heapq
import json
import os
import pickle
import shutil
import sys

ROOT=Path(__file__).resolve().parent
V51=Path('/home/daybreak/B7_work/b7_v51')
EXPECTED_V51_SHA='c6f2a373abb3ef7b472d87ab64071b85285831e29b4c7b30faafc205376d01cf'
EXPECTED_V51_FP='2ad94f8a77652ade494d2ab82fffc4fc86cda0b44097b991dd9358b54029e377'
OLD_POLICY='max_midpoint_K_floor_zeroth_outerrem_v5_Astra_F_ge_minus_275_over_4'
NEW_POLICY='max_midpoint_K_floor_zeroth_ASTRA3_outerrem_v52_rho_G2_T2'
NEW_ASTRA3_POLICY='B3_CELL_8_4_2_GEOMETRIC_DELTA_RHO_G2_T2_WITH_NONNEGATIVE_CUTOFF'
COMMON=('v3_fixed_128.py','v6_b_ad2_128.py','v6_b7_safe_128.py',
        'v6_b7_adaptive_128.py','v6_b7_priority_128.py',
        'v6_b7_hybrid_128.py','v6_b7_delta_local_128.py',
        'b7_constants_v3.py','b7_constants_v5.py')
S=1<<128

sys.path.insert(0,str(ROOT))
from v6_b7_unified_outerrem_v52 import fingerprint,k_floor_raw
from b7_astra3_v52 import astra3_floor_raw


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def atomic(path,obj,json_mode=False):
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('w' if json_mode else 'wb') as f:
        if json_mode:json.dump(obj,f,indent=2,sort_keys=True)
        else:pickle.dump(obj,f,protocol=4)
        f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def prefactor(j,cfg):
    llo,lhi=map(Q,cfg['outer'][0])
    return j*llo*Q(7,11) if j>=0 else j*lhi*Q(2,3)

def final(j,cfg):
    lhi=Q(cfg['outer'][0][1])
    sigma=Q(cfg['sigma_cut'])
    return prefactor(j,cfg)-2*lhi*Q(275,4)*sigma

def select(mid,k,z,astra=None):
    rows=[('K_FLOOR',k),('MIDPOINT',mid),('ZEROTH',z)]
    if astra is not None:rows.append(('ASTRA3',astra))
    return max(rows,key=lambda item:item[1])

def run(args):
    origin=Path(args.origin).resolve()
    dest=Path(args.dest).resolve()
    if not origin.is_file() or not origin.name.endswith('_full.checkpoint'):
        raise RuntimeError('missing or invalid full origin checkpoint')
    if dest==origin.parent or dest==V51 or dest==ROOT:
        raise RuntimeError('destination MUST differ from origin/work roots')
    if sha(V51/'v6_b7_unified_outerrem_v51.py')!=EXPECTED_V51_SHA:
        raise RuntimeError('V5.1 source not pinned; STOP')
    for n in COMMON:
        if sha(V51/n)!=sha(ROOT/n):
            raise RuntimeError('common mathematical kernel changed: '+n)
    if fingerprint()!=args.expected_fp:
        raise RuntimeError('V5.2 fingerprint differs from the predeclared source pin')
    dest.mkdir(parents=True,exist_ok=True)
    snapshot_dir=dest/'snapshots'
    snapshot_dir.mkdir(exist_ok=True)
    snapshot=snapshot_dir/(origin.name+'.source_copy')
    if not snapshot.exists():
        pending=snapshot.with_name(snapshot.name+'.tmp')
        with origin.open('rb') as i,pending.open('wb') as o:
            shutil.copyfileobj(i,o,8*1024*1024)
            o.flush();os.fsync(o.fileno())
        os.replace(pending,snapshot)
    print('SNAPSHOT',snapshot,sha(snapshot),flush=True)

    with snapshot.open('rb') as f: saved=pickle.load(f)
    cfg=saved['config'];state=saved['state']
    if cfg.get('fingerprint')!=EXPECTED_V51_FP or cfg.get('bound_policy')!=OLD_POLICY:
        raise RuntimeError('origin V5.1 fingerprint/policy mismatch')
    if cfg.get('mode')!='full' or Q(cfg['KQ'])!=Q(275,4):
        raise RuntimeError('origin constant or mode mismatch')
    if Q(cfg['p_cut'])!=Q(1,2000000):
        raise RuntimeError('p cut changed')
    if not state.get('initialized'):
        raise RuntimeError('V5.1 checkpoint not initialized')
    active=state['active']
    if len(active)!=cfg['grid_count']+state['splits']:
        raise RuntimeError('coverage leaf count mismatch')
    if len(active)>cfg['limit']:
        raise RuntimeError('origin exceeds leaf cap')
    if max(x['depth'] for x in active.values())>cfg['depth']:
        raise RuntimeError('origin exceeds depth')

    old_total=0;new_total=0
    old_main=0;old_z=0;old_rem=[0,0,0,0]
    count_astra=0;strict=0
    old_count={};new_count={}
    old_active_heap={uid for _,uid in state['heap'] if uid in active}
    new_heap=[]
    for idx,(uid,leaf) in enumerate(active.items(),1):
        if leaf['total'].lo!=leaf['midpoint'].lo or leaf['total'].hi!=leaf['midpoint'].hi:
            raise RuntimeError('bad midpoint alias')
        midpoint=leaf['main'].lo+sum(x.lo for x in leaf['rem'])
        if leaf['midpoint'].lo!=midpoint:
            raise RuntimeError('bad midpoint sum')
        if leaf['k_floor_raw']!=k_floor_raw(leaf['cell']):
            raise RuntimeError('original K floor does not match V5.1')
        old_src,old_sel=select(midpoint,leaf['k_floor_raw'],leaf['zeroth'].lo)
        if (old_src,old_sel)!=(leaf['bound_source'],leaf['total_lo_selected']):
            raise RuntimeError('original selected lower/source mismatch')
        astra=astra3_floor_raw(tuple(tuple(Q(v) for v in pair) for pair in cfg['outer']),leaf['cell'])
        new_src,new_sel=select(midpoint,leaf['k_floor_raw'],leaf['zeroth'].lo,astra)
        if new_sel<old_sel:
            raise RuntimeError('V5.2 selected bound got worse')
        old_total+=old_sel;new_total+=new_sel
        old_main+=leaf['main'].lo;old_z+=leaf['zeroth'].lo
        for j,v in enumerate(leaf['rem']):old_rem[j]+=v.lo
        old_count[old_src]=old_count.get(old_src,0)+1
        new_count[new_src]=new_count.get(new_src,0)+1
        strict+=new_sel>old_sel
        count_astra+=new_src=='ASTRA3'
        leaf['astra3_floor_raw']=astra
        leaf['bound_source']=new_src
        leaf['total_lo_selected']=new_sel
        axis=leaf['axis']
        inner_score=3*max(0,-leaf['rem'][axis].lo)//4 if leaf['depth']<cfg['depth'] else 0
        leaf['inner_score']=inner_score
        score=max(inner_score,leaf['main_width'],leaf['rem_width'],leaf['zeroth_width'])
        if new_src!='MIDPOINT':score=min(score,abs(new_sel))
        leaf['score']=score
        if score>0:new_heap.append((-score,uid))
        if idx%10000==0:
            print('RECERTIFIED',idx,'of',len(active),'ASTRA3_SELECTED',count_astra,flush=True)

    if old_total!=state['total_lo'] or old_main!=state['main_lo'] or old_z!=state['zeroth_lo'] or old_rem!=state['rem_lo']:
        raise RuntimeError('checkpoint aggregate did not equal old per-leaf ledger')
    heapq.heapify(new_heap)
    state['total_lo']=new_total
    state['heap']=new_heap
    cfg['fingerprint']=fingerprint()
    cfg['bound_policy']=NEW_POLICY
    cfg['astra3_policy']=NEW_ASTRA3_POLICY

    key=cfg['key']
    output=dest/(key+'_full.checkpoint')
    report_path=dest/(key+'_v52_recert_report.json')
    if output.exists() or report_path.exists():
        raise RuntimeError('V5.2 destination checkpoint/report already exists')
    old_j=Q(old_total,S);new_j=Q(new_total,S)
    report={'schema':'DIG-B7-V52-CHECKPOINT-RECERT-v1','key':key,
            'origin_snapshot_path':str(snapshot),'origin_snapshot_sha256':sha(snapshot),
            'v51_producer_sha256':EXPECTED_V51_SHA,
            'v51_fingerprint':EXPECTED_V51_FP,'v52_fingerprint':fingerprint(),
            'v52_producer_sha256':sha(ROOT/'v6_b7_unified_outerrem_v52.py'),
            'v52_astra3_helper_sha256':sha(ROOT/'b7_astra3_v52.py'),
            'old_J_exact':str(old_j),'new_J_exact':str(new_j),
            'old_final_exact':str(final(old_j,cfg)),
            'new_final_exact':str(final(new_j,cfg)),
            'improved_leaf_count':strict,
            'astra3_selected_leaves':count_astra,
            'old_source_count':old_count,'new_source_count':new_count,
            'original_heap_live_uids':len(old_active_heap),
            'v52_heap_live_uids':len(new_heap),
            'leaf_count':len(active),
            'warning':'Recertified checkpoint, NOT independent audit. No old source file/checkpoint was altered.'}
    atomic(output,saved)
    report['output_checkpoint_sha256']=sha(output)
    atomic(report_path,report,True)
    print('NEW_CHECKPOINT',output,flush=True)
    print('REPORT',report_path,flush=True)
    print('J_GAIN_EXACT',str(new_j-old_j),'J_OLD',str(old_j),'J_V52',str(new_j),flush=True)
    print('INDEPENDENT_AUDIT_PENDING',flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--origin',required=True)
    ap.add_argument('--dest',required=True)
    ap.add_argument('--expected-fp',required=True,
                    help='predeclared V5.2 source fingerprint')
    args=ap.parse_args()
    run(args)

if __name__=='__main__':main()
