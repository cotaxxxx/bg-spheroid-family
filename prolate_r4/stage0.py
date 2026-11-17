"""D-PRO R4 fixed-denominator 35-coefficient spatial validation.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. A single cell, not full box2.

Tensor Simpson quadrature with a rigorously bounded fourth derivative in each
spatial direction. No zero-order spatial range integral for coefficients.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, os, resource, time
from pathlib import Path
import flint
from flint import arb, fmpq as Q, ctx

STATUS = "DIAGNOSTIC_ONLY / NOT_EVIDENCE"
DEG = 4
ALPHAS = sorted((a for a in itertools.product(range(5), repeat=3)
                 if sum(a) <= 4), key=lambda a: (sum(a), a))
ZERO = (0,0,0)
RC, TC, QC = Q(3,4), Q(256,4225), Q(512,2559)**2
TF = lambda x: 4*x*x/(1+x*x)**2
RAD = (Q(1,128), max(TC-TF(Q(15,128)), TF(Q(17,128))-TC),
       max(QC-Q(1,25), Q(256,1279)**2-QC))
CENTRE = (RC, TC, QC)
# Stage 0 cell, matching Codex R4 v2: theta=pi*v/2, v=[1/4,3/8].
CELL = ((Q(0),Q(1,8)), (Q(1,4),Q(3,8)), (Q(1,4),Q(3,8)))

def iv(lo, hi): return arb(lo).union(arb(hi))
def low(x): return x.lower().fmpq()
def high(x): return x.upper().fmpq()
def mag(x): return max(abs(low(x)), abs(high(x)))
def ser(x): return [str(low(x)), str(high(x))]
def positive_interval(x, lower):
    """Preserve independently established strict lower bound using rational ends."""
    if not x.is_finite(): raise ArithmeticError('nonfinite denominator')
    lo, hi = max(Q(lower), low(x)), high(x)
    if lo <= 0 or lo > hi: raise ArithmeticError('invalid positive denominator enclosure')
    return lo, hi

class J:
    """Univariate factorial-normalized Taylor jet over Arb for space variable."""
    __slots__ = ('c',)
    order = 0
    def __init__(self, c):
        self.c = tuple(arb(x) for x in c) + (arb(0),)*(J.order+1-len(c))
        assert len(self.c) == J.order+1
    @staticmethod
    def lift(x): return x if isinstance(x,J) else J([x])
    @staticmethod
    def var(x, deriv=False): return J([x,1] if deriv else [x])
    def __add__(self,x):
        a=J.lift(x); return J([p+q for p,q in zip(self.c,a.c)])
    __radd__=__add__
    def __neg__(self): return J([-x for x in self.c])
    def __sub__(self,x): return self+-J.lift(x)
    def __rsub__(self,x): return J.lift(x)+-self
    def __mul__(self,x):
        a=J.lift(x)
        return J([sum((self.c[j]*a.c[k-j] for j in range(k+1)),arb(0)) for k in range(J.order+1)])
    __rmul__=__mul__
    def __pow__(self,n):
        if not isinstance(n,int) or n<0: raise ValueError('positive integer power')
        r=J.lift(1); x=self
        while n:
            if n&1:r=r*x
            n>>=1
            if n:x=x*x
        return r
    def inverse(self,positive_lower):
        a,b=positive_interval(self.c[0],positive_lower)
        inv=iv(1/b,1/a)
        out=[inv]
        for k in range(1,J.order+1):
            out.append(-inv*sum((self.c[j]*out[k-j] for j in range(1,k+1)),arb(0)))
        return J(out)
    def sincos(self):
        z=J((arb(0),)+self.c[1:]); zz=z*z
        cosine=J.lift(1); sine=J.lift(0)
        zpow=J.lift(1)
        for k in range(1,J.order+1):
            zpow=zpow*z
            if k%2==0: cosine+=(-1)**(k//2)*zpow*Q(1,math.factorial(k))
            else: sine+=(-1)**((k-1)//2)*zpow*Q(1,math.factorial(k))
        c=self.c[0].cos(); s=self.c[0].sin()
        return s*cosine+c*sine,c*cosine-s*sine
    def cos(self): return self.sincos()[1]

class O:
    """Sparse outer Taylor algebra (R,t,q), coefficient ring J."""
    __slots__=('c',)
    def __init__(self,c): self.c={k:J.lift(v) for k,v in c.items()}
    @staticmethod
    def lift(x): return x if isinstance(x,O) else O({ZERO:J.lift(x)})
    def __add__(self,x):
        x=O.lift(x)
        return O({a:self.c.get(a,J.lift(0))+x.c.get(a,J.lift(0)) for a in self.c.keys()|x.c.keys()})
    __radd__=__add__
    def __neg__(self): return O({a:-v for a,v in self.c.items()})
    def __sub__(self,x): return self+-O.lift(x)
    def __rsub__(self,x): return O.lift(x)+-self
    def __mul__(self,x):
        x=O.lift(x); out={}
        for a,c in self.c.items():
            for b,d in x.c.items():
                ab=tuple(i+j for i,j in zip(a,b))
                if sum(ab)<=DEG: out[ab]=out.get(ab,J.lift(0))+c*d
        return O(out)
    __rmul__=__mul__
    def __pow__(self,n):
        r=O.lift(1); x=self
        while n:
            if n&1:r=r*x
            n>>=1
            if n:x=x*x
        return r
    def reciprocal(self,lower):
        if ZERO not in self.c: raise ArithmeticError('zero constant')
        inv=self.c[ZERO].inverse(lower)
        out={ZERO:inv}
        for alpha in ALPHAS[1:]:
            tot=J.lift(0)
            for beta,c in self.c.items():
                if beta==ZERO or not all(i<=j for i,j in zip(beta,alpha)):
                    continue
                rem=tuple(j-i for i,j in zip(beta,alpha))
                tot+=c*out.get(rem,J.lift(0))
            out[alpha]=-inv*tot
        return O(out)

def polys(R,t,q,h,v2,w):
    """CW7/CW4 rational identities, using only exact one-half."""
    sig=(1-R)**2+2*R*(1-h); k=1-R*h; d=1-q
    aa=(h-R)**2; uc=(1-t)*v2+t*aa; vc=(1-t)*v2-t*aa
    ac=q*sig+d*uc; B0=1-d*((1-t)*v2+t*h*h)
    cross=(h-R)*h*v2
    pp=ac*B0-4*d*d*t*(1-t)*cross
    pt=d*(aa-v2)*B0-ac*d*(h*h-v2)-4*d*d*(1-2*t)*cross
    c=q*q*sig*sig+2*q*d*sig*uc+d*d*vc*vc
    ct=2*q*d*sig*(aa-v2)+2*d*d*vc*(-v2-aa)
    bs=q+d*(1-h*h-v2); ub=(1-t)*h*h+t*v2; vb=(1-t)*h*h-t*v2
    b=bs*bs+2*bs*d*ub+d*d*vb*vb
    bt=2*bs*d*(v2-h*h)+2*d*d*vb*(-h*h-v2)
    delta=c*b; dt=ct*b+c*bt
    a=k*k*(1-w*w)
    ss=q*q*a*a+2*q*a*w*w*pp+w**4*delta
    nn=q*a*dt*Q(1,2)+w*w*(pp*dt-delta*pt)
    return 2*q*k**3*nn,delta,ss

def geometric_bounds(cell):
    h,v,w=(iv(*x) for x in cell)
    vv2=(1-h*h)*(arb.pi()*v/2).cos()**2
    sig=(1-arb(RC))**2+2*arb(RC)*(1-h)
    siglow=max((1-RC)**2,low(sig))
    klow=max(1-RC,low(1-arb(RC)*h))
    dlower=QC**4*siglow**2
    slower=QC**2*min(klow**2,QC*siglow)**2
    rr,tt,qq=map(arb,CENTRE); dd=1-qq
    yy=(1-h*h)*(arb.pi()*v/2).sin()**2
    aa=(h-rr)**2; uc=(1-tt)*vv2+tt*aa; vc=(1-tt)*vv2-tt*aa
    bs=qq+dd*yy; ub=(1-tt)*h*h+tt*vv2; vb=(1-tt)*h*h-tt*vv2
    cp=qq**2*sig**2+2*qq*dd*sig*uc+dd**2*vc**2
    bp=bs**2+2*bs*dd*ub+dd**2*vb**2
    cl=max(QC**2*siglow**2,low(cp)); bl=max(QC**2,low(bp))
    dlower=max(dlower,cl*bl)
    pp=bs*(qq*sig+dd*uc)+qq*sig*dd*ub+dd**2*(tt*(1-tt)*(h*(h-rr)-vv2)**2+vv2*((1-tt)*h-tt*(h-rr))**2)
    pl=max(QC**2*siglow,low(pp))
    al=max(Q(0),low((1-rr*h)**2*(1-w*w)))
    w2l=max(Q(0),low(w**2))
    slower=max(slower,QC**2*al**2+2*QC*al*w2l*pl+w2l**2*dlower)
    return dlower,slower

def coefficients(h,v,w,cell,active=None,derivative_order=0):
    J.order=derivative_order
    hs,vs,ws= (J.var(z,active==label) for z,label in zip((h,v,w),('h','v','w')))
    v2=(1-hs**2)*(vs*J.lift(arb.pi()/2)).cos()**2
    vars=[]
    for i,(c,r) in enumerate(zip(CENTRE,RAD)):
        a=tuple(int(k==i) for k in range(3))
        vars.append(O({ZERO:J.lift(arb(c)),a:J.lift(arb(r))}))
    u,d,s=polys(*vars,O.lift(hs),O.lift(v2),O.lift(ws))
    dl,sl=geometric_bounds(cell)
    f=u * (vars[0]**2).reciprocal(RC**2) * d.reciprocal(dl) * s.reciprocal(sl)
    return [f.c.get(a,J.lift(0)) for a in ALPHAS]

def simpson(cell):
    a,b,c=cell
    nodes=[(x[0],(x[0]+x[1])/2,x[1]) for x in cell]
    weights=(Q(1,6),Q(4,6),Q(1,6))
    acc=[arb(0) for _ in ALPHAS]
    start=time.monotonic()
    for i,j,k in itertools.product(range(3),repeat=3):
        vals=coefficients(arb(nodes[0][i]),arb(nodes[1][j]),arb(nodes[2][k]),cell)
        wt=weights[i]*weights[j]*weights[k]*Q(1,2)
        for z,q in enumerate(vals): acc[z]+=q.c[0]*arb(wt)
    lens=[x[1]-x[0] for x in cell]
    vol=arb(math.prod(lens)/2)
    acc=[v*vol*2 for v in acc]  # Q weights normalized to one; 1/2 factor already used.
    node_time=time.monotonic()-start
    bounds=[Q(0) for _ in ALPHAS]
    derivative_breakdown={}
    for z,axis in enumerate(('h','v','w')):
        start=time.monotonic()
        J.order=4
        interval_values=[iv(*x) for x in cell]
        derivs=coefficients(*interval_values,cell,active=axis,derivative_order=4)
        # Simpson fourth-derivative bound E <= L^5/120*|jet4|,
        # since f''''=4!*jet4, and the normalized tensor integral has
        # volume*(L^4/120)*|jet4|.
        eb=[mag(j.c[4]) * lens[z]**4 / 120 for j in derivs]
        bounds=[v+w for v,w in zip(bounds,eb)]
        derivative_breakdown[axis]={'elapsed_seconds':time.monotonic()-start,
            'normalized_error_upper_sum':str(sum(eb,Q(0))),
            'max_derivative_jet4':str(max((mag(j.c[4]) for j in derivs),default=Q(0)))}
    intervals=[a+iv(-v,v)*vol for a,v in zip(acc,bounds)]
    return {'intervals':intervals,'quadrature':acc,
            'errors':[vol*arb(x) for x in bounds],
            'node_time':node_time,'derivatives':derivative_breakdown}

def run(output,reference=None,split=1):
    ctx.prec=128
    if flint.__version__ != '0.8.0':
        raise RuntimeError('expected python-flint 0.8.0, got '+flint.__version__)
    start=time.monotonic()
    if split < 1 or split > 16: raise ValueError('split must be 1..16')
    slices = [tuple((a+(b-a)*Q(i,split), a+(b-a)*Q(i+1,split))
               for i in range(split)) for a,b in CELL]
    x={'intervals':[arb(0) for _ in ALPHAS],
       'quadrature':[arb(0) for _ in ALPHAS],
       'errors':[arb(0) for _ in ALPHAS],
       'node_time':0.0, 'derivatives':{axis:0.0 for axis in ('h','v','w')}}
    for ijk in itertools.product(range(split),repeat=3):
        sub=tuple(slices[i][j] for i,j in enumerate(ijk))
        y=simpson(sub)
        x['intervals']=[a+b for a,b in zip(x['intervals'],y['intervals'])]
        x['quadrature']=[a+b for a,b in zip(x['quadrature'],y['quadrature'])]
        x['errors']=[a+b for a,b in zip(x['errors'],y['errors'])]
        x['node_time']+=y['node_time']
        for axis in x['derivatives']:
            x['derivatives'][axis]+=y['derivatives'][axis]['elapsed_seconds']
    errs=[high(e) for e in x['errors']]
    width=[high(i)-low(i) for i in x['intervals']]
    # Stage-0 budget: sum of 35 interval radii <= 1/100000 (cell integral).
    budget=Q(1,100000)
    uncertainty=sum(width,Q(0))/2
    obj={'status':STATUS,'scope':'stage0-single-cell-only','method':'tensor Simpson with interval fourth derivative',
        'precision_bits':128,'flint':flint.__version__,
        'outer_center':[str(a) for a in CENTRE], 'outer_radii':[str(a) for a in RAD],
        'cell':[[str(a),str(b)] for a,b in CELL],'spatial_subdivisions_per_axis':split,'spatial_cells':split**3,
        'coefficients':[{'alpha':list(a),'integral':ser(b),'width':str(w),'derivative_bound_upper':str(e)}
                         for a,b,w,e in zip(ALPHAS,x['intervals'],width,errs)],
        'total_halfwidth_sum':str(uncertainty),'stage0_budget':str(budget),
        'stage0_width_result':'PASS' if uncertainty<=budget else 'FAIL',
        'timing':{'nodes_seconds':x['node_time'],'derivatives':x['derivatives'],
                  'wall_seconds':time.monotonic()-start},
        'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'stage1_executed':False, 'box2_W_enclosure':None,
        'note':'Independent 50-digit mpmath reference comparison is a separate diagnostic.'}
    if reference is not None:
        ref=json.loads(Path(reference).read_text())
        arr=ref['coefficients']; mismatches=[]
        for a,r in zip(x['intervals'],arr):
            # diagnostic only; strict comparison with 50-digit text through arb
            p=arb(r['value']);
            if p<a.lower() or p>a.upper(): mismatches.append(r['alpha'])
        obj['reference50']={'file':str(reference),'contains_all':not mismatches,'mismatches':mismatches}
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='coefficients'},indent=2,ensure_ascii=False))
    return obj

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--reference');p.add_argument('--split',type=int,default=1);args=p.parse_args();run(args.output,args.reference,args.split)
