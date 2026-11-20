"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.

Finite-box calibration of the surface gradient and the angular divided
difference. Binary64 basic operations are widened with nextafter.
The probability sphere integral is evaluated by cell range sums.
No non-interval quadrature is used for the reported enclosures.
"""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import argparse
import csv
import hashlib
import itertools
import json
import math
import multiprocessing as mp
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = 65536
S_CENTERS = [65/64, 5/4, 2, 51/16]
T_CENTERS = [65/64, 3/2, 2, 9/4, 3, 4, 5, 383/64]
LADDER = [64, 128, 256, 512, 1024]
MODES = {
    'G3_123': (1/4, 3/8, 1/2),
    'G3_13': (3/8, 0, 1/2),
    'G3_23': (0, 3/8, 1/2),
    'D12': (1/2, 1/2, 0),
}

def lo(x): return np.nextafter(x, -np.inf)
def hi(x): return np.nextafter(x, np.inf)

class Box:
    __array_priority__ = 1000
    def __init__(self, a, b=None):
        self.a = np.asarray(a, dtype=np.float64)
        self.b = self.a if b is None else np.asarray(b, dtype=np.float64)
    def __add__(self, o):
        o = box(o)
        return Box(lo(self.a+o.a), hi(self.b+o.b))
    __radd__ = __add__
    def __neg__(self): return Box(-self.b, -self.a)
    def __sub__(self, o): return self + -box(o)
    def __rsub__(self, o): return box(o) + -self
    def __mul__(self, o):
        o = box(o)
        v = [self.a*o.a, self.a*o.b, self.b*o.a, self.b*o.b]
        return Box(lo(np.minimum.reduce(v)), hi(np.maximum.reduce(v)))
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = box(o)
        if not np.all(o.a > 0): raise ValueError('nonpositive denominator')
        return self * Box(lo(1/o.b), hi(1/o.a))
    def sq(self):
        a, b = self.a*self.a, self.b*self.b
        return Box(np.where((self.a <= 0) & (self.b >= 0), 0, lo(np.minimum(a,b))), hi(np.maximum(a,b)))
    def sqrt(self):
        if not np.all(self.b >= 0): raise ValueError('negative square root')
        return Box(np.maximum(0, lo(np.sqrt(np.maximum(0,self.a)))), hi(np.sqrt(self.b)))
    def cut(self, a, b):
        lower, upper = np.maximum(self.a,a), np.minimum(self.b,b)
        if not np.all(lower <= upper): raise ValueError('empty intersection')
        return Box(lower,upper)

def box(x): return x if isinstance(x,Box) else Box(x)

def outward_sum(x, upper):
    x = np.asarray(x).ravel()
    if not len(x) or len(x) & (len(x)-1): raise ValueError('power-of-two sum required')
    widen = hi if upper else lo
    while len(x) > 1: x = widen(x[::2]+x[1::2])
    return x[0]

def rational_bounds(f):
    x = float(f)
    return Box(lo(x),hi(x))

@lru_cache(None)
def pi_box():
    # Machin identity pi = 16 atan(1/5) - 4 atan(1/239).
    # Each 24-term alternating sum is a lower bound; add the next term
    # for an upper bound. The complete endpoints are rational.
    def atan_bounds(n):
        total = sum((Fraction((-1)**j,(2*j+1)*n**(2*j+1)) for j in range(24)),Fraction(0))
        return total,total+Fraction(1,49*n**49)
    a,b = atan_bounds(5)
    c,d = atan_bounds(239)
    return Box(float(rational_bounds(16*a-4*d).a),float(rational_bounds(16*b-4*c).b))

TABLE_N = 65536
@lru_cache(None)
def angle_table():
    gamma = Box(np.arange(TABLE_N+1)/TABLE_N)
    z = (1-gamma)/2
    v = Box(0)
    for j in range(54,-1,-1):
        coefficient = rational_bounds(Fraction(math.comb(2*j,j),4**j*(2*j+1)))
        v = coefficient+z*v
    v = v+Box(0,2.**-54)
    P = 2*v/(1-z).sqrt()
    F = 4*z*v.sq()
    R = gamma*P
    J = R-F
    K = gamma.sq()*P
    return {'P':P,'F':F,'R':R,'J':J,'K':K}

def angle_ranges(gamma):
    ia = np.floor(gamma.a*TABLE_N).astype(np.int64)
    ib = np.ceil(gamma.b*TABLE_N).astype(np.int64)
    data=angle_table()
    # R, J and K are increasing on [0,1]; proof in calibration_notes.md.
    return {key: Box(data[key].a[ia],data[key].b[ib]) for key in ['R','J','K']}

def case(shape_id, mode):
    is_,it = divmod(shape_id,len(T_CENTERS))
    sc,tc = round(S_CENTERS[is_]*UNIT),round(T_CENTERS[it]*UNIT)
    q = []
    for x in MODES[mode]:
        c = round(x*UNIT)
        q.append((c-8,c+8) if c else (0,0))
    return {'shape':shape_id,'mode':mode,'slo':sc-16,'shi':sc+16,
            'tlo':tc-16,'thi':tc+16,
            **{f'q{i+1}{side}':q[i][j] for i in range(3) for j,side in enumerate(['lo','hi'])}}

def enclosure(spec, M):
    W=M//2
    s=Box(spec['slo']/UNIT,spec['shi']/UNIT)
    t=Box(spec['tlo']/UNIT,spec['thi']/UNIT)
    q=[Box(spec[f'q{i}lo']/UNIT,spec[f'q{i}hi']/UNIT) for i in range(1,4)]
    A=[Box(1),s.sq(),(s*t).sq()]
    normq=(q[0].sq()+q[1].sq()+q[2].sq()).sqrt()
    if not normq.b < 1: raise ValueError('position box is not internal')
    min_D2=(1-normq).sq().a
    min_B=(Box(1)/A[2]).a
    w=Box(np.arange(W)/W,np.arange(1,W+1)/W)
    den=1+w.sq()
    cosphi=(1-w.sq())/den
    sinphi=2*w/den
    weight=Box(4)/pi_box()/den
    sums=[]
    for start in range(0,M,16):
        j=np.arange(start,start+16)[:,None]
        mu=Box(-1+2*j/M,-1+2*(j+1)/M)
        left=(1-mu.sq()).cut(0,1)
        radial=left.sqrt()
        xi_abs=[radial*cosphi,radial*sinphi,mu]
        total=Box(0)
        for sg1,sg2 in itertools.product([-1,1],repeat=2):
            xi=[sg1*xi_abs[0],sg2*xi_abs[1],mu]
            v=[xi[i]-q[i] for i in range(3)]
            D2=(A[0]*v[0].sq()+A[1]*v[1].sq()+A[2]*v[2].sq()).cut(min_D2,np.inf)
            B=(xi[0].sq()+xi[1].sq()/A[1]+xi[2].sq()/A[2]).cut(min_B,1)
            D,S=D2.sqrt(),B.sqrt()
            k=(1-q[0]*xi[0]-q[1]*xi[1]-q[2]*xi[2]).cut(float((1-normq).a),2)
            gamma=(k/(D*S)).cut(0,1)
            ang=angle_ranges(gamma)
            if spec['mode']=='D12':
                value=k*ang['R']*(v[0]*v[1]/D2-xi[0]*xi[1]/(A[1]*B))/(q[0]*q[1])
            else:
                value=(xi[2]*ang['J']-A[2]*v[2]/D*S*ang['K'])/q[2]
            total=total+value
        weighted=weight*total/4
        sums.append((outward_sum(weighted.a,False),outward_sum(weighted.b,True)))
    a=np.asarray(sums)
    return Box(outward_sum(a[:,0],False),outward_sum(a[:,1],True))/(M*W)

def evaluate_case(task):
    shape_id,mode=task
    spec=case(shape_id,mode)
    rows=[]
    for M in LADDER:
        before=time.perf_counter()
        answer=enclosure(spec,M)
        seconds=time.perf_counter()-before
        lower,upper=float(answer.a),float(answer.b)
        result='positive' if lower>0 else ('negative' if upper<0 else 'unresolved')
        row={**spec,'unit':UNIT,'nmu':M,'nw':M//2,
             'sphere_cells':4*M*(M//2),'lower':lower,'upper':upper,
             'width':upper-lower,'seconds':seconds,'result':result}
        rows.append(row)
        if result=='positive': break
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--stop',type=int,default=32)
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--output',default='calibration.csv')
    args=parser.parse_args()
    if not (0<=args.start<args.stop<=32 and 1<=args.workers<=2): raise ValueError('invalid work range')
    target=ROOT/'out'/args.output
    target.parent.mkdir(exist_ok=True,parents=True)
    tasks=[(i,m) for i in range(args.start,args.stop) for m in MODES]
    keys=list(case(0,'G3_123'))+['unit','nmu','nw','sphere_cells','lower','upper','width','seconds','result']
    with target.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator='\n')
        writer.writeheader()
        with mp.Pool(args.workers) as pool:
            for rows in pool.imap(evaluate_case,tasks):
                writer.writerows(rows);f.flush()
                last=rows[-1]
                print(last['shape'],last['mode'],last['nmu'],last['lower'],last['upper'],last['result'],flush=True)

if __name__=='__main__': main()
