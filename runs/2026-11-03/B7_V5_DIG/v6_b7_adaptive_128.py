"""V6-B7 adaptive diagnostic; not a full certificate. Exact rational cell geometry.
Outer boxes are NEVER summed: each must independently pass; inner boxes are summed.
"""
import argparse, json, time, hashlib, os
from fractions import Fraction as Q
from v3_fixed_128 import I,iv,S,mulq_interval
from v6_b7_safe_128 import kernel,centered_main

def frac(x):return Q(str(x))
def bounds(outer,cell):
    mid=[((a+b)/2,(a+b)/2) for a,b in cell]
    main=centered_main(outer,cell)
    vol=Q(1)
    for a,b in cell:vol*=b-a
    ms=mulq_interval(main,vol)
    rem=[]
    for i in range(4):
        h=sum((kernel(outer,cell,e,('inner',i)).d2 for e in (1,-1)),iv(0))
        rem.append(mulq_interval(h,vol*(cell[i][1]-cell[i][0])**2/Q(24)))
    return ms,rem,ms+sum(rem,iv(0))

def tofloat(v):return [v.lo/S,v.hi/S]
def bisect(cell,axis):
    a,b=cell[axis];m=(a+b)/2
    l=list(cell);r=list(cell);l[axis]=(a,m);r[axis]=(m,b)
    return tuple(l),tuple(r)

def choose(rem,cell):
    # Negative contribution in certified scaled remainder, not raw d2.
    scores=[max(0,-r.lo) for r in rem]
    return max(range(4),key=lambda i:(scores[i],-i))

def adaptive(outer,cell,max_leaves=16,max_depth=8):
    leaves=[(tuple(cell),0)];log=[];counts=[0]*4
    while len(leaves)<max_leaves:
        candidates=[]
        for j,(c,depth) in enumerate(leaves):
            if depth>=max_depth:continue
            main,rem,total=bounds(outer,c)
            axis=choose(rem,c)
            candidates.append((-rem[axis].lo,j,axis,main,rem,total))
        if not candidates:break
        _,j,axis,main,rem,total=max(candidates)
        c,depth=leaves.pop(j)
        a,b=bisect(c,axis)
        leaves.extend([(a,depth+1),(b,depth+1)])
        counts[axis]+=1
        log.append({'depth':depth,'axis':'yptu'[axis],'scaled_remainder_lower':tofloat(rem[axis])[0], 'total_lower':tofloat(total)[0]})
    main_total=iv(0);rem_total=[iv(0) for _ in range(4)]
    for c,_ in leaves:
        m,r,_=bounds(outer,c);main_total+=m
        for i in range(4):rem_total[i]+=r[i]
    total=main_total+sum(rem_total,iv(0))
    return {'leaves':len(leaves),'split_counts':dict(zip('yptu',counts)), 'main':tofloat(main_total),'remainder':{n:tofloat(r) for n,r in zip('yptu',rem_total)},'total':tofloat(total),'split_log':log}

def grid(nlam=2,ntau=4,delta=(Q(3,10**8),Q(6,10**8))):
    def parts(a,b,n):return [(a+(b-a)*Q(i,n),a+(b-a)*Q(i+1,n)) for i in range(n)]
    for i,l in enumerate(parts(Q(2,5),Q(93,200),nlam)):
        for j,t in enumerate(parts(Q(7,8),Q(1),ntau)):
            yield f'L{i}_T{j}_D0',(l,t,delta)

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--leaves',type=int,default=4);ap.add_argument('--depth',type=int,default=6)
    ap.add_argument('--delta-upper',default='0.0001');ap.add_argument('--out',default='v6_b7_adaptive.jsonl');ap.add_argument('--all-outer',action='store_true')
    args=ap.parse_args()
    cell=((Q(1,10),Q(2,10)),(Q(3,10),Q(4,10)),(Q(1,4),Q(3,8)),(Q(1,4),Q(3,8)))
    outerboxes=list(grid(delta=(Q(3,10**8),frac(args.delta_upper))))
    if not args.all_outer:outerboxes=outerboxes[:1]
    with open(args.out,'w') as f:
        for key,outer in outerboxes:
            start=time.monotonic()
            try:
                baseline=bounds(outer,cell)
                result=adaptive(outer,cell,args.leaves,args.depth)
                row={'outer_id':key,'outer':[[str(a),str(b)] for a,b in outer], 'inner':[[str(a),str(b)] for a,b in cell], 'baseline_total':tofloat(baseline[2]),'result':result,'seconds':time.monotonic()-start,'status':'DIAGNOSTIC'}
            except (ValueError,ZeroDivisionError) as exc:
                row={'outer_id':key,'status':'DOMAIN_FAIL','error':repr(exc)}
            f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
            print(key,row['status'],row.get('result',{}).get('total'),flush=True)
if __name__=='__main__':run()
