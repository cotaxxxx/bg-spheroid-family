#!/usr/bin/env python3
"""Fixed Dig R1 R2 full-suite sharded execution; DIAGNOSTIC_ONLY / NOT_EVIDENCE.
23 case definitions kept byte-for-byte in source. Case 0 already tested
under the canonical resumable suite. Cases 1..22 are run using explicit
--case ID in mutually isolated output paths. This is not one completed
single-suite run; aggregate case-by-case result receipts separately.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone
import json,os,subprocess,time
ROOT=Path('/home/daybreak/D_PRO_R1_COROTATION_R2_DIG_20261117')
SRC=ROOT/'source'
LOG=ROOT/'logs'/'full_shards'
LOG.mkdir(parents=True,exist_ok=True)
PY=str(ROOT/'venv311/bin/python')
ENV=dict(os.environ,PYTHONHASHSEED='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
LIMIT_SEC=240
MAX_WORKERS=6
STATUS='DIAGNOSTIC_ONLY / NOT_EVIDENCE'

def run_case(i):
    t=time.monotonic_ns()
    name=f'case_{i:03d}'
    out=LOG/(name+'.json')
    cmd=['timeout','--signal=TERM','--kill-after=8s',str(LIMIT_SEC),PY,
        '-m','prolate_r1.tests.run_tests','--full','--resume',
        '--case',str(i),'--out',str(out)]
    with (LOG/(name+'.stdout')).open('wb') as stdout,\
         (LOG/(name+'.stderr')).open('wb') as stderr:
        res=subprocess.run(cmd,cwd=SRC,env=ENV,stdout=stdout,stderr=stderr,check=False)
    status='NO_SNAPSHOT';plan=None;row=None
    if out.exists():
        try:
            result=json.loads(out.read_text())
            assert len(result['tests'])==23 and result['status']==STATUS
            plan=result['plan_sha256']
            row=result['tests'][i]
            status=row['result']
        except Exception as exc: status=f'INVALID_SNAPSHOT {exc}'
    report={'case_id':i,'command':cmd,'exit_code':res.returncode,'case_result':status,
            'plan_sha256':plan,'elapsed_ns':time.monotonic_ns()-t,'status':STATUS,
            'case_name':row['name'] if row else None}
    (LOG/(name+'.receipt.json')).write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    start=time.monotonic_ns()
    rows=[]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs={pool.submit(run_case,i):i for i in range(1,23)}
        for f in as_completed(futs):
            r=f.result()
            rows.append(r)
            print('CASE',r['case_id'],r['case_result'],'EXIT',r['exit_code'],
                  'WALL_S',round(r['elapsed_ns']/1e9,3),flush=True)
    rows.sort(key=lambda x:x['case_id'])
    results={'status':STATUS,'mode':'CASE_SHARDED_FIXED23_NO_SINGLE_COMPLETED_FULL_SNAPSHOT',
             'source_commit':'bc70e1badbd9a89449cae6707ef37f5e69757a11',
             'workers':MAX_WORKERS,'case_timeout_seconds':LIMIT_SEC,
             'total_wall_seconds':(time.monotonic_ns()-start)/1e9,'results':rows}
    (LOG/'shard_summary.json').write_text(json.dumps(results,indent=2)+'\n')
    print('TOTAL_SHARDED_CASES',len(rows),flush=True)
    print('RESULT_COUNTS',
          {s:sum(x['case_result']==s for x in rows) for s in ('PASS','FAIL','INTERRUPTED','PENDING')},
          flush=True)
    print('TOTAL_WALL_SECONDS',round(results['total_wall_seconds'],3),flush=True)
    print(STATUS,flush=True)

if __name__=='__main__':
    main()
