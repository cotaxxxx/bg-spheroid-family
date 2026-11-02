"""V6-B7 cached global priority diagnostic runner. NOT an independent certificate.
Outer boxes are universal (min), inner leaves integrated (sum). Exact rational
geometry and outward 2**128 dyadic interval arithmetic. No source rewriting.
"""
import argparse, hashlib, heapq, json, os, time
from fractions import Fraction as Q
from pathlib import Path
from v3_fixed_128 import I,S
from v6_b7_adaptive_128 import bounds,bisect,choose,grid
from b7_constants_v3 import KQ, P0, SIGMA0

YEDGES=[Q(0),Q(1,10**10),Q(1,10**9),Q(1,10**8),Q(1,10**7),Q(1,10**6),Q(1,10**5),Q(1,10**4),Q(1,10**3),Q(1,10**2),Q(1,10),Q(1)]
PEDGES=[P0]+[p for p in (Q(1,10**7),Q(1,10**6),Q(1,10**5),Q(1,10**4),Q(1,10**3),Q(1,10**2),Q(1)) if p>P0]

def intervals(edges):return list(zip(edges[:-1],edges[1:]))
def inner_grid():
    for y in intervals(YEDGES):
        for p in intervals(PEDGES):
            for ti in range(8):
                for ui in range(8):
                    yield (y,p,(Q(ti,8),Q(ti+1,8)),(Q(ui,8),Q(ui+1,8)))

def fracpair(pair):return [str(x) for x in pair]
def encode_cell(cell):return [fracpair(pair) for pair in cell]
def low(v):return Q(v.lo,S)
def up(v):return Q(v.hi,S)
def lower_text(q):return str(q)

def contact(outer):return 2*outer[0][1]*KQ*SIGMA0

def prefactor_lower(s,outer):
    # 7/11 <= 2/pi <= 2/3, all lambda positive
    return s*outer[0][0]*Q(7,11) if s>=0 else s*outer[0][1]*Q(2,3)

def evaluate(outer,cell,depth,uid):
    main,rem,total=bounds(outer,cell)
    axis=choose(rem,cell)
    # priority by largest scaled negative remainder, independent of total sign
    score=max(0,-rem[axis].lo)
    return {'uid':uid,'cell':cell,'depth':depth,'main':main,'rem':rem,'total':total,'axis':axis,'score':score}

def certify_outer(outer,cells,max_leaves,max_depth,trace_path=None,checkpoint_every=100,diagnostic=False):
    """Cache each evaluated leaf; each split evaluates ONLY two new children.
    A limit means LIMIT_REACHED, not a mathematical counterexample.
    """
    heap=[]; active={}; serial=0; n_evals=0; counts=[0]*4
    main_lo=0;rem_lo=[0]*4; total_lo=0
    trace=open(trace_path,'w') if trace_path else None
    try:
        for cell in cells:
            leaf=evaluate(outer,cell,0,serial);serial+=1;n_evals+=1
            active[leaf['uid']]=leaf
            main_lo+=leaf['main'].lo;total_lo+=leaf['total'].lo
            for i in range(4):rem_lo[i]+=leaf['rem'][i].lo
            if max_depth>0:heapq.heappush(heap,(-leaf['score'],leaf['uid']))
        initial=len(active)
        loss=contact(outer)
        def current():return Q(total_lo,S) if diagnostic else prefactor_lower(Q(total_lo,S),outer)-loss
        status='LIMIT_REACHED';splits=0
        if current()>0:status='PASS'
        while status!='PASS' and len(active)<max_leaves and heap:
            negscore,uid=heapq.heappop(heap)
            if uid not in active:continue
            old=active.pop(uid)
            if old['depth']>=max_depth:
                active[uid]=old
                continue
            left,right=bisect(old['cell'],old['axis'])
            children=[]
            for cell in (left,right):
                child=evaluate(outer,cell,old['depth']+1,serial);serial+=1;n_evals+=1
                children.append(child)
            main_lo-=old['main'].lo;total_lo-=old['total'].lo
            for i in range(4):rem_lo[i]-=old['rem'][i].lo
            for child in children:
                active[child['uid']]=child
                main_lo+=child['main'].lo;total_lo+=child['total'].lo
                for i in range(4):rem_lo[i]+=child['rem'][i].lo
                if child['depth']<max_depth:heapq.heappush(heap,(-child['score'],child['uid']))
            counts[old['axis']]+=1;splits+=1
            if trace:
                record={'split':splits,'parent_uid':uid,'axis':'yptu'[old['axis']], 'parent_cell':encode_cell(old['cell']), 'score_raw_scaled':str(old['score']),'child_uids':[x['uid'] for x in children], 'total_lower':str(Q(total_lo,S)), 'final_lower':str(current())}
                trace.write(json.dumps(record,sort_keys=True)+'\n')
                if splits%checkpoint_every==0:trace.flush();os.fsync(trace.fileno())
            if current()>0:status='PASS'
        if trace:trace.flush();os.fsync(trace.fileno())
        return {'status':status,'initial_cells':initial,'leaves':len(active),'evaluations':n_evals,'splits':splits,'split_counts':dict(zip('yptu',counts)), 'main_lower':str(Q(main_lo,S)),'remainder_lower':{c:str(Q(r,S)) for c,r in zip('yptu',rem_lo)},'total_lower':str(Q(total_lo,S)),'contact_loss_upper':str(loss),'final_lower':str(current()),'diagnostic_only':diagnostic,'outer':encode_cell(outer),'split_log':str(trace_path) if trace_path else None}
    finally:
        if trace:trace.close()

def delta_grid():return [(Q(3,10**8),Q(1,10**4)),(Q(1,10**4),Q(1,10**2)),(Q(1,10**2),Q(15,64))]

def run():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['representative','full'],default='representative')
    ap.add_argument('--delta',choices=['small','middle','large','all'],default='small')
    ap.add_argument('--max-leaves',type=int,default=32)
    ap.add_argument('--max-depth',type=int,default=10)
    ap.add_argument('--out-dir',default='v6_b7_runs')
    ap.add_argument('--outer-limit',type=int,default=1)
    args=ap.parse_args()
    if args.max_leaves<1 or args.max_depth<0:raise ValueError('invalid limits')
    if args.mode=='full' and args.max_leaves<len(YEDGES[:-1])*len(PEDGES[:-1])*64:raise ValueError('full grid max-leaves below dynamic grid size')
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    deltas=delta_grid();indices={'small':[0],'middle':[1],'large':[2],'all':[0,1,2]}[args.delta]
    boxes=[(f'L{i}_T{j}_D{k}',(lam,tau,deltas[k])) for k in indices for i,lam in enumerate(intervals([Q(2,5),Q(173,400),Q(93,200)])) for j,tau in enumerate(intervals([Q(7,8)+Q(n,32) for n in range(5)]))]
    representative=((Q(1,10),Q(2,10)),(Q(3,10),Q(4,10)),(Q(1,4),Q(3,8)),(Q(1,4),Q(3,8)))
    for key,outer in boxes[:args.outer_limit if args.outer_limit>0 else None]:
        path=out/(key+'_'+args.mode+'.json')
        if path.exists():
            prev=json.loads(path.read_text())
            if prev.get('settings')==vars(args) and prev.get('status') in ('PASS','DIAGNOSTIC_POSITIVE','LIMIT_REACHED','DOMAIN_FAIL'):
                print(key,'SKIPPED',prev['status'],flush=True);continue
            raise RuntimeError('existing result is incompatible with current settings or has an unknown status: '+str(path))
        t0=time.monotonic()
        try:
            cells=[representative] if args.mode=='representative' else inner_grid()
            result=certify_outer(outer,cells,args.max_leaves,args.max_depth,trace_path=out/(key+'_'+args.mode+'.jsonl'),diagnostic=args.mode=='representative')
        except (ValueError,ZeroDivisionError) as exc:
            result={'status':'DOMAIN_FAIL','error':repr(exc),'outer':encode_cell(outer)}
        if args.mode=='representative' and result['status']=='PASS':result['status']='DIAGNOSTIC_POSITIVE'
        result.update({'outer_id':key,'seconds':time.monotonic()-t0,'settings':vars(args),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
        tmp=path.with_suffix('.json.tmp')
        with open(tmp,'w') as f:json.dump(result,f,indent=2,sort_keys=True);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        print(key,result['status'],result.get('final_lower'), 'leaves',result.get('leaves'),flush=True)
if __name__=='__main__':run()
