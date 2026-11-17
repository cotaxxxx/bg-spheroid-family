"""50-decimal-working-digit independent numerical reference for Stage 0.
DIAGNOSTIC_ONLY / NOT_EVIDENCE; Gaussian quadrature is NOT a rigorous bound.
Uses the geometrically positive p polynomial, independently of CW7 simplified p.
"""
from __future__ import annotations
import argparse,itertools,json,time
from pathlib import Path
import mpmath as mp
mp.mp.dps=60
ALPHAS=sorted((a for a in itertools.product(range(5),repeat=3) if sum(a)<=4),key=lambda a:(sum(a),a))
Z=(0,0,0)
Q=mp.mpf
RC=Q(3)/4; TC=Q(256)/4225; QC=(Q(512)/2559)**2
TF=lambda x:4*x*x/(1+x*x)**2
RAD=(Q(1)/128,max(TC-TF(Q(15)/128),TF(Q(17)/128)-TC),max(QC-Q(1)/25,(Q(256)/1279)**2-QC))
CENTER=(RC,TC,QC)
CELL=((Q(0),Q(1)/8),(Q(1)/4,Q(3)/8),(Q(1)/4,Q(3)/8))

class O:
    __slots__=('c',)
    def __init__(self,c):self.c={a:mp.mpf(v) for a,v in c.items()}
    @staticmethod
    def lift(v):return v if isinstance(v,O) else O({Z:v})
    def __add__(self,x):
        x=O.lift(x);return O({a:self.c.get(a,Q(0))+x.c.get(a,Q(0)) for a in self.c.keys()|x.c.keys()})
    __radd__=__add__
    def __neg__(self):return O({a:-v for a,v in self.c.items()})
    def __sub__(self,x):return self+-O.lift(x)
    def __rsub__(self,x):return O.lift(x)+-self
    def __mul__(self,x):
        x=O.lift(x);out={}
        for a,u in self.c.items():
            for b,v in x.c.items():
                ab=tuple(i+j for i,j in zip(a,b))
                if sum(ab)<=4:out[ab]=out.get(ab,Q(0))+u*v
        return O(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=O.lift(1);cur=self
        while n:
            if n&1:out=out*cur
            n>>=1
            if n:cur=cur*cur
        return out
    def reciprocal(self):
        inv=1/self.c[Z];out={Z:inv}
        for a in ALPHAS[1:]:
            t=Q(0)
            for b,u in self.c.items():
                if b==Z or not all(k<=v for k,v in zip(b,a)):continue
                r=tuple(v-k for k,v in zip(b,a))
                t+=u*out.get(r,Q(0))
            out[a]=-inv*t
        return O(out)

def polys_independent(R,t,q,h,z,w):
    sig=(1-R)**2+2*R*(1-h);k=1-R*h;d=1-q
    aa=(h-R)**2;uc=(1-t)*z+t*aa;vc=(1-t)*z-t*aa
    bs=q+d*(1-h*h-z);ub=(1-t)*h*h+t*z;vb=(1-t)*h*h-t*z
    c=q*q*sig*sig+2*q*d*sig*uc+d*d*vc*vc
    ct=2*q*d*sig*(aa-z)+2*d*d*vc*(-z-aa)
    b=bs*bs+2*bs*d*ub+d*d*vb*vb
    bt=2*bs*d*(z-h*h)+2*d*d*vb*(-h*h-z)
    cross=h*(h-R)-z
    angle=(1-t)*h-t*(h-R)
    p=bs*(q*sig+d*uc)+q*sig*d*ub+d*d*(t*(1-t)*cross**2+z*angle**2)
    pt=bs*d*(aa-z)+q*sig*d*(z-h*h)+d*d*((1-2*t)*cross**2-2*z*angle*(2*h-R))
    delta=c*b;dt=ct*b+c*bt
    a=k*k*(1-w*w)
    s=q*q*a*a+2*q*a*w*w*p+w**4*delta
    u=2*q*k**3*(q*a*dt*Q("0.5")+w*w*(p*dt-delta*pt))
    return u,delta,s

def point(h,v,w):
    z=(1-h*h)*mp.cos(mp.pi*v/2)**2
    vars=[]
    for i,(c,r) in enumerate(zip(CENTER,RAD)):
        axis=tuple(int(k==i) for k in range(3))
        vars.append(O({Z:c,axis:r}))
    U,D,S=polys_independent(*vars,h,z,w)
    f=U*(vars[0]**2).reciprocal()*D.reciprocal()*S.reciprocal()
    return [f.c.get(a,Q(0)) for a in ALPHAS]

def gauss_tensor(n):
    raw,wts=mp.gauss_quadrature(n,'legendre'); nodes=[];weights=[]
    for l,r in CELL:
        nodes.append([(l+r)/2+(r-l)*raw[i]/2 for i in range(n)])
        weights.append([(r-l)*wts[i]/2 for i in range(n)])
    sums=[Q(0) for _ in ALPHAS]
    for i,j,k in itertools.product(range(n),repeat=3):
        vals=point(nodes[0][i],nodes[1][j],nodes[2][k]);weight=weights[0][i]*weights[1][j]*weights[2][k]/2
        for t,v in enumerate(vals):sums[t]+=v*weight
    return sums

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=6);ap.add_argument('--n-compare',type=int,default=8);args=ap.parse_args()
    st=time.monotonic();lo=gauss_tensor(args.n);t1=time.monotonic()-st
    hi=gauss_tensor(args.n_compare);t2=time.monotonic()-st-t1
    obj={'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','method':'mpmath 60-dps Gauss-Legendre tensor reference; no error guarantee',
         'n':args.n,'n_compare':args.n_compare,'elapsed_seconds':[t1,t2],
         'max_difference_between_grids':mp.nstr(max(abs(a-b) for a,b in zip(lo,hi)),22),
         'coefficients':[{'alpha':list(a),'value':mp.nstr(x,62),'difference_from_coarse':mp.nstr(abs(x-y),20)} for a,x,y in zip(ALPHAS,hi,lo)]}
    Path(args.output).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='coefficients'},indent=2))
if __name__=='__main__':main()
