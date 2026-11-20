"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Outward Riemann inclusions for selected triaxial axial roots.
IEEE 754 binary64 assumptions are specified in PLAN_AXIS.md.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import argparse, csv, hashlib, json, math, platform, time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'
DEN = 65536
TABLE_N = 65536

def down(x): return np.nextafter(x, -np.inf)
def up(x): return np.nextafter(x, np.inf)

class Box:
    __array_priority__ = 1000
    def __init__(self, a, b=None):
        self.a = np.asarray(a, dtype=np.float64)
        self.b = self.a if b is None else np.asarray(b, dtype=np.float64)
    def __add__(self, o):
        o = box(o); return Box(down(self.a + o.a), up(self.b + o.b))
    __radd__ = __add__
    def __neg__(self): return Box(-self.b, -self.a)
    def __sub__(self, o): return self + -box(o)
    def __rsub__(self, o): return box(o) + -self
    def __mul__(self, o):
        o = box(o)
        values = [self.a*o.a, self.a*o.b, self.b*o.a, self.b*o.b]
        return Box(down(np.minimum.reduce(np.broadcast_arrays(*values))),
                   up(np.maximum.reduce(np.broadcast_arrays(*values))))
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = box(o)
        if not np.all(o.a > 0): raise ArithmeticError('nonpositive divisor')
        return self * Box(down(1/o.b), up(1/o.a))
    def sq(self):
        low = np.minimum(self.a*self.a, self.b*self.b)
        high = np.maximum(self.a*self.a, self.b*self.b)
        return Box(np.where((self.a <= 0)&(self.b >= 0), 0, down(low)), up(high))
    def sqrt(self):
        if not np.all(self.b >= 0): raise ArithmeticError('negative radicand')
        return Box(np.maximum(0, down(np.sqrt(np.maximum(0, self.a)))), up(np.sqrt(self.b)))
    def cut(self, a, b):
        x, y = np.maximum(self.a, a), np.minimum(self.b, b)
        if not np.all(x <= y): raise ArithmeticError('empty intersection')
        return Box(x, y)
    def intersect(self, other): return self.cut(other.a, other.b)

def box(x): return x if isinstance(x, Box) else Box(x)
def rational(n, d=1):
    v = float(Fraction(n, d)); return Box(down(v), up(v))

def pair_sum(x, upper):
    x = np.asarray(x).ravel()
    if len(x)&(len(x)-1): raise ValueError('balanced sum requires power of two')
    widen = up if upper else down
    while len(x)>1: x = widen(x[::2]+x[1::2])
    return float(x[0])

@lru_cache(None)
def pi_box():
    def atan_bounds(d):
        n=80
        value=sum((Fraction((-1)**k, (2*k+1)*d**(2*k+1)) for k in range(n)), Fraction(0))
        rem=Fraction(1, (2*n+1)*d**(2*n+1))
        return value, value+rem
    a,b=atan_bounds(5); c,d=atan_bounds(239)
    return Box(down(float(16*a-4*d)),up(float(16*b-4*c)))

@lru_cache(None)
def angle_table():
    gamma=np.arange(TABLE_N+1)/TABLE_N
    z=Box((1-gamma)/2)
    p=[]; f=[]; q=[]
    for n in range(55):
        pn=Fraction(4**n * math.factorial(n)**2, math.factorial(2*n+1))
        p.append(rational(2*pn.numerator,pn.denominator))
        fn=4*pn/Fraction(n+1)
        f.append(rational(fn.numerator,fn.denominator))
        qn=2*Fraction(n*n+5*n+5,2*n+3)*pn
        q.append(rational(qn.numerator,qn.denominator))
    def horner(coeff):
        r=Box(0)
        for c in coeff[::-1]: r=c+z*r
        return r
    P=horner(p)+Box(0,2.**-53)
    F=z*horner(f)+Box(0,2.**-53)
    Q=horner(q)+Box(0,116*2.**-54)
    return P,F,Q

def angles(g):
    low=np.floor(g.a*TABLE_N).astype(np.int64)
    high=np.ceil(g.b*TABLE_N).astype(np.int64)
    return tuple(Box(v.a[high],v.b[low]) for v in angle_table())

def shape(which):
    if which=='A': s=Box(81919/DEN,81921/DEN)
    elif which=='B': s=Box(134348/DEN,134350/DEN)
    else: raise ValueError(which)
    t=Box(196607/DEN,196609/DEN)
    return [Box(1),s.sq(),(s*t).sq()]

def integral(which, axis, radius, M, hessian=True):
    """Return g_axis,H_11,H_22,H_33,U_prime inclusions on one shape/radius box."""
    A=shape(which); i=axis; j,k=sorted([v for v in range(3) if v!=i])
    W=M//2
    w=Box(np.arange(W)/W,np.arange(1,W+1)/W)
    wd=1+w.sq(); c=(1-w.sq())/wd; d=2*w/wd
    c2,d2=c.sq(),d.sq()
    # c^2+d^2=1; use the identity as an additional enclosure.
    c2=c2.intersect(1-d2).cut(0,1)
    d2=d2.intersect(1-c2).cut(0,1)
    weight=Box(4)/pi_box()/wd
    C=A[j]*c2+A[k]*d2
    C=C.intersect(A[j]+(A[k]-A[j])*d2)
    r=radius
    total=[[] for _ in range(4 if hessian else 1)]
    for row in range(0,M,32):
        idx=np.arange(row,row+32)[:,None]
        mu=Box(-1+2*idx/M,-1+2*(idx+1)/M)
        m2=mu.sq(); left=(1-m2).cut(0,1)
        sqxi=[None]*3; sqxi[i]=m2; sqxi[j]=left*c2; sqxi[k]=left*d2
        vi=mu-r
        term=[None]*3;term[i]=A[i]*vi.sq();term[j]=A[j]*sqxi[j];term[k]=A[k]*sqxi[k]
        D2=term[i]+left*C
        D2=D2.intersect(sum(term,Box(0)))
        D2=D2.cut(float(down((1-float(r.b))**2)),np.inf)
        B=sum((sqxi[l]/A[l] for l in range(3)),Box(0))
        B=B.cut(float(down(1/float(A[2].b))),1)
        kval=1-r*mu
        DS=D2.sqrt()*B.sqrt()
        gamma=(kval/DS).cut(0,1)
        P,F,Q=angles(gamma)
        zi=left*(A[i]*r+mu*(C-A[i]))/D2
        g=P*gamma*zi-mu*F
        vals=[g]
        if hessian:
            for l in range(3):
                positive=P*kval.sq()*A[l]*sum((term[m] for m in range(3) if m!=l),Box(0))/D2.sq()
                z2=zi.sq() if l==i else sqxi[l]*(1-A[l]*kval/D2).sq()
                vals.append((positive-Q*z2)/DS)
        for dest,val in zip(total,vals):
            v=weight*val
            dest.append((pair_sum(v.a,False),pair_sum(v.b,True)))
    ans=[]
    for cells in total:
        ary=np.asarray(cells)
        ans.append(Box(pair_sum(ary[:,0],False),pair_sum(ary[:,1],True))/(M*W))
    if hessian and float(r.a)>0:
        ans.append((r*ans[i+1]-ans[0])/(2*r.sq()*r))
    return ans

HEADER='run shape axis mode s0 s1 t0 t1 shape_den r0 r1 r_den nmu nw quantity lower upper seconds result'.split()
CASES=[('A',0,3/8,1/2,[-1,1,1]),('A',1,27/32,29/32,[-1,-1,1]),('B',1,7/8,15/16,[-1,-1,1])]

def emit(writer,run,sh,axis,mode,r,M,vals,elapsed,status):
    sints=(81919,81921) if sh=='A' else (134348,134350)
    names=['g','H11','H22','H33','Ux']
    for name,v in zip(names,vals):
        writer.writerow([run,sh,axis+1,mode,*sints,196607,196609,DEN,round(float(r.a)*DEN),round(float(r.b)*DEN),DEN,M,M//2,name,float(v.a),float(v.b),elapsed,status])

def run(output,only=None):
    OUT.mkdir(exist_ok=True)
    with (OUT/output).open('w') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(HEADER)
        for idx,(sh,axis,ra,rb,signs) in enumerate(CASES):
            if only is not None and idx!=only:continue
            label=f'{sh}{axis+1}'
            for endpoint,rval,sgn in [('left',ra,1),('right',rb,-1)]:
                for M in [256,512,1024,2048,4096,8192]:
                    start=time.perf_counter();vals=integral(sh,axis,Box(rval),M,False);elapsed=time.perf_counter()-start
                    good=bool(vals[0].a>0 if sgn>0 else vals[0].b<0)
                    emit(writer,label,sh,axis,endpoint,Box(rval),M,vals,elapsed,'sign' if good else 'unresolved');f.flush()
                    print(label,endpoint,M,float(vals[0].a),float(vals[0].b),elapsed,good,flush=True)
                    if good:break
            done=False
            for n in [8,16,32,64]:
                accepted=0
                for panel in range(n):
                    r=Box(ra+(rb-ra)*panel/n,ra+(rb-ra)*(panel+1)/n)
                    for M in [128,256,512,1024,2048]:
                        start=time.perf_counter();vals=integral(sh,axis,r,M,True);elapsed=time.perf_counter()-start
                        good=all(bool(v.a>0 if s>0 else v.b<0) for v,s in zip(vals[1:4],signs)) and bool(vals[4].b<0)
                        emit(writer,label,sh,axis,f'band_{n}_{panel}',r,M,vals,elapsed,'sign' if good else 'unresolved');f.flush()
                        print(label,'band',n,panel,M,[ (float(x.a),float(x.b)) for x in vals[1:]],elapsed,good,flush=True)
                        if good:accepted+=1;break
                if accepted==n: done=True;break
            print(label,'complete_bracket_derivatives',done,flush=True)
    return output

def centers(output):
    with (OUT/output).open('w') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(HEADER)
        for sh,signs in [('A',[1,1,1]),('B',[-1,1,1])]:
            for M in [128,256,512,1024,2048]:
                start=time.perf_counter();v=integral(sh,0,Box(0),M,True);elapsed=time.perf_counter()-start
                good=all(bool(x.a>0 if s>0 else x.b<0) for x,s in zip(v[1:4],signs))
                emit(writer,sh+'0',sh,0,'center',Box(0),M,v,elapsed,'sign' if good else 'unresolved');f.flush()
                print(sh,'center',M,[(float(x.a),float(x.b)) for x in v],elapsed,good,flush=True)
                if good:break

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int);ap.add_argument('--centers',action='store_true');ap.add_argument('--output',default='axis_bounds.csv');args=ap.parse_args()
    if args.centers: centers(args.output)
    else: run(args.output,args.case)
