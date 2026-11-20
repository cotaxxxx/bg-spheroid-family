"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. C3: position widths and direct collars."""
from pathlib import Path
import csv,json,time,multiprocessing as mp
from calibration import case,MODES,UNIT,ROOT
from calibration_extended import enclosure

LADDER=[128,256,512,1024]
LIMIT_SECONDS=1200

def make_cases():
    ans=[]
    for ident in [0,7,24,31]:
        for half in [256,1024,4096]:
            for mode in MODES:
                sp=case(ident,mode)
                sc=(sp['slo']+sp['shi'])//2;tc=(sp['tlo']+sp['thi'])//2
                sp.update(slo=max(UNIT,sc-4096),shi=min(209716,sc+4096),
                          tlo=max(UNIT,tc-4096),thi=min(6*UNIT,tc+4096))
                for i in range(1,4):
                    c=(sp[f'q{i}lo']+sp[f'q{i}hi'])//2
                    sp[f'q{i}lo']=c-half if c else 0
                    sp[f'q{i}hi']=c+half if c else 0
                sp.update(experiment='position_width',half=half,domain='ball_interior')
                ans.append(sp)
        for mode in MODES:
            sp=case(ident,mode)
            for i in range(1,4):
                c=(sp[f'q{i}lo']+sp[f'q{i}hi'])//2
                sp[f'q{i}lo']=c-256 if c else 0
                sp[f'q{i}hi']=c+256 if c else 0
            near=1 if mode=='D12' else 3
            sp[f'q{near}lo']=256;sp[f'q{near}hi']=768
            sp.update(experiment='direct_collar',half=256,domain='ball_interior')
            ans.append(sp)
    return ans

def evaluate(spec):
    rows=[]
    for M in LADDER:
        tick=time.perf_counter();value,contact=enclosure(spec,M);elapsed=time.perf_counter()-tick
        lower,upper=float(value.a),float(value.b)
        result='positive' if lower>0 else ('negative' if upper<0 else 'unresolved')
        rows.append({**spec,'unit':UNIT,'nmu':M,'nw':M//2,'sphere_cells':4*M*(M//2),
                     'contact_cells':contact,'lower':lower,'upper':upper,'width':upper-lower,
                     'seconds':elapsed,'result':result})
        if result=='positive':break
    return rows

def main():
    start=time.monotonic();cs=make_cases();completed=[];timeout=False
    path=ROOT/'out/calibration_position.csv'
    fields=list(cs[0])+['unit','nmu','nw','sphere_cells','contact_cells','lower','upper','width','seconds','result']
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader()
        pool=mp.Pool(2)
        try:
            iterator=pool.imap_unordered(evaluate,cs)
            while len(completed)<len(cs):
                left=LIMIT_SECONDS-(time.monotonic()-start)
                if left<=0:timeout=True;break
                try:rows=iterator.next(timeout=left)
                except mp.TimeoutError:timeout=True;break
                writer.writerows(rows);f.flush();last=rows[-1];completed.append(last)
                print(last['shape'],last['experiment'],last['half'],last['mode'],last['nmu'],last['lower'],last['upper'],last['result'],flush=True)
        finally:
            if timeout:pool.terminate()
            else:pool.close()
            pool.join()
    done={(x['shape'],x['mode'],x['experiment'],x['half']) for x in completed}
    missing=[x for x in cs if (x['shape'],x['mode'],x['experiment'],x['half']) not in done]
    (ROOT/'out/calibration_position_run.json').write_text(json.dumps({'label':'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
        'wall_seconds':time.monotonic()-start,'limit_seconds':LIMIT_SECONDS,'timed_out':timeout,
        'planned_cases':len(cs),'completed_cases':len(completed),'unprocessed':missing},indent=2)+'\n')

if __name__=='__main__':main()
