"""R2 Dig: aggregate exactly 23 unchanged full cases from separate journals.

This script does not turn 22 partial full-suite snapshots into a single-run
completion. It verifies every fixed case from real saved case records.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import hashlib,json,sys
from pathlib import Path
R=Path('/home/daybreak/D_PRO_R1_COROTATION_R2_DIG_20261117')
LOG=R/'logs'
OUT=LOG/'FULL23_AGGREGATE.json'
STATUS='DIAGNOSTIC_ONLY / NOT_EVIDENCE'

def require(x,msg):
    if not x:
        raise RuntimeError(msg)

def main():
    canonical=json.loads((LOG/'dig_r2_full.json').read_text())
    require(len(canonical['tests'])==23,'canonical suite size')
    require(canonical['status']==STATUS,'canonical status')
    sha=canonical['plan_sha256']
    assert canonical['tests'][0]['result']=='PASS'
    rows=[]
    def load_result(report,i,origin):
        require(report['plan_sha256']==sha,'plan sha mismatch '+str(i))
        require(report['status']==STATUS,'status mismatch '+str(i))
        record=report['tests'][i]
        require(record['id']==i,'case id mismatch')
        require(record['name']==canonical['tests'][i]['name'],'case name mismatch')
        require(record['result']=='PASS','test nonPASS '+str(i))
        attempts=record['attempts']
        require(len(attempts)==1,'unexpected test retry '+str(i))
        require(attempts[0]['result']=='PASS','attempt status '+str(i))
        rows.append({'id':i,'name':record['name'],'result':'PASS',
                     'source_record':origin,'attempts':len(attempts),
                     'plan_sha256':sha,
                     'elapsed_ns':attempts[0].get('elapsed_ns')})
    load_result(canonical,0,'logs/dig_r2_full.json')
    for i in range(1,23):
        path=LOG/'full_shards'/('case_%03d.json'%i)
        require(path.exists(),'missing case snapshot '+str(i))
        x=json.loads(path.read_text())
        require(x['complete'] is False,'unexpected complete single-shard suite')
        receipt=json.loads((LOG/'full_shards'/('case_%03d.receipt.json'%i)).read_text())
        require(receipt['case_id']==i,'receipt id mismatch')
        require(receipt['case_result']=='PASS','receipt nonPASS')
        require(receipt['exit_code']==2,'partial suite should return 2')
        load_result(x,i,str(path.relative_to(R)))
    require(len(set(x['id'] for x in rows))==23,'duplicate case ids')
    result={'status':STATUS,
            'type':'AGGREGATED_PER_CASE_FIXED23_NOT_SINGLE_SUITE_SUCCESS',
            'source_commit':'bc70e1badbd9a89449cae6707ef37f5e69757a11',
            'original_r2_zip_sha256':'1f42136c4d26aca41413806cfb04f91b022ab3bd46b747627f3b20e532b75c7d',
            'identical_plan_sha256':sha,
            'records':rows,
            'case_count':23,'PASS':23,'FAIL':0,'interrupted':0,
            'runner_details':'Case 0 canonical --max-cases=1 output; cases 1..22 individually using --case and 6-worker isolated records; each shard exits 2 because suite not individually complete.',
            'mathematical_sufficiency':'NOT_EVIDENCE'}
    OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('ALL_FIXED_CASES_PASS_23_OF_23')
    print('PLAN_SHA256',sha)
    print('AGGREGATE_SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest())
    print(STATUS)

if __name__=='__main__':
    main()
