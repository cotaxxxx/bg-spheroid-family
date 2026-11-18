#!/usr/bin/env python3
"""Read-only postrun accounting for original C21 H cover + separate Judge E_z ruling."""
import argparse,json,os
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
STATE=Path('/home/daybreak/D_PRO_C21_H_HEAVY_SLAB_20261118/worktree/runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB/STATE.json')
def area(node):
    r,t=node['R'],node['tau']
    return (F(r[1])-F(r[0]))*(F(t[1])-F(t[0]))
def is_running(pid):
    try: os.kill(pid,0);return True
    except ProcessLookupError:return False
def report():
    st=json.loads(STATE.read_text())
    terminal=st['terminal']
    matches=[t for t in terminal if t['node']['id']=='R63_T63']
    assert len(matches)==1,'Judge-adopted root must appear once in frozen H state'
    found=matches[0]
    assert found['kind']=='TUBE_OPEN_ERROR' and found['node']['R']==['63/64','1'] and found['node']['tau']==['63/64','1']
    assert area(found['node'])==F(1,4096)
    decided=[t for t in terminal if t['kind']=='DECIDED_NONZERO']
    remaining=[t for t in terminal if t['node']['id']!='R63_T63' and t['kind']!='DECIDED_NONZERO']
    pending=st['pending']+st['inflight']
    a,b,c,d=map(lambda seq: sum((area(n['node'] if 'node' in n else n) for n in seq),F(0)),(decided,[found],remaining,pending))
    assert a+b+c+d==1,(a,b,c,d)
    status='IN_PROGRESS' if is_running(1581407) or st['inflight'] else 'RUN_STOPPED'
    rr={'scope':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','status':status,'judge_ruling':'JUDGE_ADOPTED_E_z_STATIONARY_EXCLUSION','full_slab_completed':not pending and status=='RUN_STOPPED','ruling_commit':'546986fa7192e6e91b50cb36dfaef2bb75dd2c2e','H_sign_decided_boxes':len(decided),'H_sign_decided_area_exact':str(a),'E_z_exclusion_box_count':1,'E_z_exclusion_area_exact':str(b),'H_sign_E_z_root':'NOT_EVALUATED','boundary_B':'SEPARATE','remaining_H_tube_or_OPEN_count':len(remaining),'remaining_H_tube_or_OPEN_area_exact':str(c),'unevaluated_count':len(pending),'unevaluated_area_exact':str(d),'area_total_exact':str(a+b+c+d),'original_r63_kind':found['kind'],'processed_nodes':len(st['processed']),'split_parent_count':len(st['splits']),'completed_batches':st['completed_batches'],'completed_sessions':len(st['sessions']),'session_wall_elapsed_committed_s':st['wall_elapsed_cumulative_s'],'finished_naturally':not pending and status=='RUN_STOPPED','note':'Do not count E_z exclusion as an H-sign decision. If run stopped with pending, coverage remains incomplete.'}
    return rr
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    opt=parser.parse_args()
    r=report()
    print(json.dumps(r,indent=2,ensure_ascii=False))
    if opt.write:
        assert r['status']=='RUN_STOPPED','Do not archive final aggregation before heavy run stops'
        (HERE/'POSTRUN_AREA_AGGREGATION.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
