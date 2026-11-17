"""DIAGNOSTIC_ONLY / NOT_EVIDENCE: CW7-style rigorous outer-degree-4 tail.
Only for spatial patches of stage0; never treat partial tail as a box enclosure.
"""
import itertools, json, pathlib, resource, time
from flint import arb, arb_poly, fmpq as Q, ctx
from stage0 import RC,TC,QC,RAD,CELL, iv,low,high,mag,polys, geometric_bounds

def conv(a,b,n):
    return [sum((a[j]*b[k-j] for j in range(max(0,k-len(b)+1),min(k,len(a)-1)+1)),arb(0)) for k in range(n+1)]
def inv_major(a,n):
    out=[arb(1)]
    for k in range(1,n+1):out.append(sum((a[j]*out[k-j] for j in range(1,min(k,len(a)-1)+1)),arb(0)))
    return out

def majorant(cell):
    h,v,w=(iv(*p) for p in cell)
    v2=(1-h*h)*(arb.pi()*v/2).cos()**2
    vars=[arb_poly([arb(c),iv(-r,r)]) for c,r in zip((RC,TC,QC),RAD)]
    U,D,S=polys(*vars,h,v2,w)
    d0,s0=geometric_bounds(cell)
    d0=max(d0,low(D[0]));s0=max(s0,low(S[0]))
    if d0<=0 or s0<=0:raise ArithmeticError('positive denominator not available')
    ad=[arb(0)]+[arb(mag(a)/d0) for a in D.coeffs()[1:]]
    ass=[arb(0)]+[arb(mag(a)/s0) for a in S.coeffs()[1:]]
    r=RAD[0]/RC;ar=list(map(arb,[Q(0),2*r,r*r]))
    arr=[ar,ad,ass]
    sums=[sum(a,arb(0)) for a in arr]
    maxA=max(high(a) for a in sums)
    if any(high(a)>=1 for a in sums):return {'A':maxA,'tail_upper':None,'convergent':False}
    ms=[arb(mag(a)) for a in U.coeffs()]
    full=sum(ms,arb(0))
    for a in sums:full=full/(1-a)
    g=ms
    for a in arr:g=conv(g,inv_major(a,4),4)
    tail=(full-sum(g,arb(0)))/arb(RC**2*d0*s0)
    if high(tail)<0:raise ArithmeticError('negative majorant tail')
    return {'A':maxA,'tail_upper':max(Q(0),high(tail)), 'convergent':True}

def run(out,split=4):
    ctx.prec=128
    start=time.monotonic();slices=[[tuple((a+(b-a)*Q(i,split),a+(b-a)*Q(i+1,split))) for i in range(split)] for a,b in CELL]
    all_a=[];bad=[];tail=Q(0);counts=0
    for idx in itertools.product(range(split),repeat=3):
        cell=tuple(slices[i][j] for i,j in enumerate(idx))
        m=majorant(cell);counts+=1;all_a.append(m['A'])
        if m['A']>Q(1,8) or not m['convergent']:
            bad.append({'index':idx,'max_A':str(m['A']), 'convergent':m['convergent']})
        if m['convergent']:
            measure=Q(1,2)
            for a,b in cell:measure*=b-a
            tail+=measure*m['tail_upper']
    obj={'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE', 'split':split,'cells':counts,
         'majorant_threshold':'1/8','nonconforming_count':len(bad), 'max_A':str(max(all_a)),
         'partial_tail_for_convergent_cells':str(tail),
         'tail_all_cells_available':all(not x for x in [y for y in bad if not y['convergent']]),
         'threshold_met_all_cells':not bad, 'violations':bad,
         'elapsed_seconds':time.monotonic()-start,
         'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    pathlib.Path(out).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='violations'},indent=2))
    return obj
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--split',type=int,default=4);z=p.parse_args();run(z.output,z.split)
