"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. C4: q3-normalized G3 by a Hessian collar."""
import csv,json,time,math,itertools,multiprocessing as mp
from functools import lru_cache
from fractions import Fraction
import numpy as np
from calibration import Box,UNIT,ROOT,TABLE_N,pi_box,rational_bounds,angle_ranges,outward_sum,case

LADDER=[128,256,512,1024,2048]
LIMIT_SECONDS=600

@lru_cache(None)
def q_table():
    z=(1-Box(np.arange(TABLE_N+1)/TABLE_N))/2
    a=Fraction(1);coefficients=[]
    for n in range(81):
        coefficients.append(2*a*Fraction(n*n+5*n+5,2*n+3))
        a*=Fraction(2*(n+1),2*n+3)
    value=Box(0)
    for coeff in reversed(coefficients):value=rational_bounds(coeff)+z*value
    tail=Fraction(2*(80+4),2**80)
    return value+Box(0,float(rational_bounds(tail).b))

def q_range(gamma):
    ia=np.floor(gamma.a*TABLE_N).astype(np.int64)
    ib=np.ceil(gamma.b*TABLE_N).astype(np.int64)
    data=q_table()
    return Box(data.a[ib],data.b[ia])

def make_cases():
    ans=[]
    for ident in [0,7,24,31]:
        for mode in ['G3_123','G3_13','G3_23']:
            sp=case(ident,mode)
            for i in [1,2]:
                c=(sp[f'q{i}lo']+sp[f'q{i}hi'])//2
                sp[f'q{i}lo']=c-256 if c else 0
                sp[f'q{i}hi']=c+256 if c else 0
            sp.update(q3lo=0,q3hi=768,experiment='H33_collar',domain='ball_interior')
            ans.append(sp)
    return ans

def enclosure(spec,M):
    W=M//2;s=Box(spec['slo']/UNIT,spec['shi']/UNIT);t=Box(spec['tlo']/UNIT,spec['thi']/UNIT)
    q=[Box(spec[f'q{i}lo']/UNIT,spec[f'q{i}hi']/UNIT) for i in range(1,4)]
    A=[Box(1),s.sq(),(s*t).sq()]
    normq=(q[0].sq()+q[1].sq()+q[2].sq()).sqrt()
    if not normq.b<1:raise ValueError('Hessian collar is not interior')
    minD=(1-normq).sq().a;minB=(Box(1)/A[2]).a
    w=Box(np.arange(W)/W,np.arange(1,W+1)/W);den=1+w.sq()
    cp=(1-w.sq())/den;sp=2*w/den;weight=Box(4)/pi_box()/den;sums=[]
    for start in range(0,M,16):
        j=np.arange(start,start+16)[:,None];mu=Box(-1+2*j/M,-1+2*(j+1)/M)
        radial=(1-mu.sq()).cut(0,1).sqrt();xa=[radial*cp,radial*sp,mu];total=Box(0)
        for sg1,sg2 in itertools.product([-1,1],repeat=2):
            xi=[sg1*xa[0],sg2*xa[1],mu];v=[xi[i]-q[i] for i in range(3)]
            v12=v[0].sq()+A[1]*v[1].sq();D2=(v12+A[2]*v[2].sq()).cut(minD,np.inf)
            B=(xi[0].sq()+xi[1].sq()/A[1]+xi[2].sq()/A[2]).cut(minB,1);D,S=D2.sqrt(),B.sqrt()
            k=(1-q[0]*xi[0]-q[1]*xi[1]-q[2]*xi[2]).cut(float((1-normq).a),2)
            gamma=(k/(D*S)).cut(0,1);K=angle_ranges(gamma)['K'];Q=q_range(gamma)
            # A3-b3^2 = A3*(v1^2+A2*v2^2)/D2, preserving its nonnegativity.
            transverse=(A[2]*v12/D2).cut(0,float(A[2].b))
            z3=xi[2]-k*A[2]*v[2]/D2
            value=(K*B*transverse-Q*z3.sq())/(D*S)
            total=total+value
        weighted=weight*total/4
        sums.append((outward_sum(weighted.a,False),outward_sum(weighted.b,True)))
    a=np.asarray(sums)
    return Box(outward_sum(a[:,0],False),outward_sum(a[:,1],True))/(M*W)

def evaluate(spec):
    rows=[]
    for M in LADDER:
        tick=time.perf_counter();value=enclosure(spec,M);elapsed=time.perf_counter()-tick
        lower,upper=float(value.a),float(value.b)
        result='positive' if lower>0 else ('negative' if upper<0 else 'unresolved')
        rows.append({**spec,'unit':UNIT,'nmu':M,'nw':M//2,'sphere_cells':4*M*(M//2),
                     'lower':lower,'upper':upper,'width':upper-lower,'seconds':elapsed,'result':result})
        if result=='positive':break
    return rows

def main():
    start=time.monotonic();cs=make_cases();completed=[];timeout=False
    fields=list(cs[0])+['unit','nmu','nw','sphere_cells','lower','upper','width','seconds','result']
    with (ROOT/'out/calibration_normalized.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();pool=mp.Pool(2)
        try:
            iterator=pool.imap_unordered(evaluate,cs)
            while len(completed)<len(cs):
                left=LIMIT_SECONDS-(time.monotonic()-start)
                if left<=0:timeout=True;break
                try:rows=iterator.next(timeout=left)
                except mp.TimeoutError:timeout=True;break
                writer.writerows(rows);f.flush();last=rows[-1];completed.append(last)
                print(last['shape'],last['mode'],last['nmu'],last['lower'],last['upper'],last['result'],flush=True)
        finally:
            if timeout:pool.terminate()
            else:pool.close()
            pool.join()
    done={(x['shape'],x['mode']) for x in completed}
    (ROOT/'out/calibration_normalized_run.json').write_text(json.dumps({'label':'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
       'wall_seconds':time.monotonic()-start,'limit_seconds':LIMIT_SECONDS,'timed_out':timeout,
       'planned_cases':len(cs),'completed_cases':len(completed),
       'unprocessed':[x for x in cs if (x['shape'],x['mode']) not in done]},indent=2)+'\n')

if __name__=='__main__':main()
