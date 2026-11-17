"""Dig R3 fixed legacy full 23 diagnostic shards; one original test per output.

DOES NOT change test cases, source, settings, or pass criteria.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import concurrent.futures,json,os,pathlib,subprocess,time
R=pathlib.Path('/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117')
SRC=R/'source'
L=R/'logs'/'legacy23_shards'
L.mkdir(parents=True,exist_ok=True)
PY=str(R/'venv311/bin/python')
env=dict(os.environ,PYTHONHASHSEED='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
SEC=210
WORKERS=6

def task(i):
    start=time.monotonic_ns()
    name=f'case_{i:03d}'
    dest=L/(name+'.json')
    cmd=['timeout','--signal=TERM','--kill-after=8s',str(SEC),PY,'-m',
         'prolate_r1.tests.run_tests','--full','--resume','--case',str(i),
         '--out',str(dest)]
    with (L/(name+'.stdout')).open('wb') as out, (L/(name+'.stderr')).open('wb') as err:
        rc=subprocess.run(cmd,cwd=SRC,env=env,stdout=out,stderr=err).returncode
    row={"id":i,"exit":rc,"status":"NO_SNAPSHOT","elapsed_ns":time.monotonic_ns()-start,
         "output":str(dest.relative_to(R)),"status_tag":"DIAGNOSTIC_ONLY / NOT_EVIDENCE"}
    if dest.exists():
        try:
            d=json.loads(dest.read_text())
            assert len(d['tests'])==23
            row['status']=d['tests'][i]['result']
            row['plan_sha']=d['plan_sha256']
            row['case_name']=d['tests'][i]['name']
        except Exception as ex:
            row['status']="SNAPSHOT_ERROR: "+str(ex)
    (L/(name+'.receipt.json')).write_text(json.dumps(row,indent=2)+'\n')
    return row

def main():
    began=time.monotonic_ns()
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for future in concurrent.futures.as_completed([pool.submit(task,i) for i in range(23)]):
            row=future.result();rows.append(row)
            print('CASE',row['id'],row['status'],'exit',row['exit'],
                  'sec',round(row['elapsed_ns']/1e9,1),flush=True)
    rows.sort(key=lambda r:r['id'])
    summary={'source_commit':'fdfb498f2117cc0c5d72e88cc3be05eac9727bd8',
             'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','type':'SHARDED_CASES_NOT_SINGLE_SUITE',
             'workers':WORKERS,'per_case_guard_s':SEC,
             'wall_s':(time.monotonic_ns()-began)/1e9,'results':rows}
    (L/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('COUNTS',{k:sum(r['status']==k for r in rows) for k in ('PASS','FAIL','INTERRUPTED','PENDING','RUNNING','NO_SNAPSHOT')},flush=True)
    print('WALL',round(summary['wall_s'],2),flush=True)

if __name__=='__main__':
    main()
