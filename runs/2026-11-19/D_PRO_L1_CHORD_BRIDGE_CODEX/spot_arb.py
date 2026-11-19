"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Direct interval evaluation of (C1) on three fixed interior boxes."""
import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from time import perf_counter
from flint import arb, ctx, fmpq

ctx.prec=112
NM,NA,G=256,32,4096
BOXES=[(20480,21504,256,320,1280,1408),(24576,28672,2304,2560,1280,1536),
       (28672,32768,1280,1536,2560,3072)]
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
O,Z=arb(1),arb(0)


def hull(a,b):
    return arb(a).union(arb(b))


def square(x):
    a,b=x.lower(),x.upper()
    low=max(Z,a,-b)
    high=max(abs(a),abs(b))
    return hull((low*low).lower(),(high*high).upper())


def index(x,upper):
    p=x.upper() if upper else x.lower()
    if p<=0:return 0
    if p>=1:return G
    s=(p*G).fmpq()
    return -((-int(s.p))//int(s.q)) if upper else int(s.p)//int(s.q)


def run(args):
    case,box=args
    start=perf_counter()
    fp,qq=[],[]
    for i in range(G+1):
        y=arb(fmpq(i,G))
        if i==G: f=arb(2);q=arb(fmpq(10,3))
        else:
            f=2*y.acos()/(1-y*y).sqrt()
            q=2*f+y*(y*f-2)/(1-y*y)
        fp.append(f.upper());qq.append(q.lower())
    angular=[]
    for a in range(NA):
        lo,hi=arb.pi()*a/(2*NA),arb.pi()*(a+1)/(2*NA)
        angular.append((hull(hi.cos().lower(),lo.cos().upper()),hull(square(lo.sin()).lower(),square(hi.sin()).upper())))
    outer=[]
    for corner in itertools.product((0,1),repeat=3):
        bounds=[]
        for j,half in enumerate(corner):
            low,high=box[2*j:2*j+2]
            mid=(low+high)//2
            u,v=(mid,high) if half else (low,mid)
            bounds.append(hull(fmpq(u,4096),fmpq(v,4096)))
        lam,r,z=bounds
        delta=1-square(r)-square(z)
        if delta.lower()<=0: raise ArithmeticError("expected strict interior")
        eps2=1/square(lam)
        total=arb(0)
        for i in range(NM):
            m=hull(fmpq(i,NM),fmpq(i+1,NM))
            m2=square(m)
            a,b=(1-m2).lower(),(1-m2).upper()
            s=hull(max(Z,a).sqrt().lower(),max(Z,b).sqrt().upper())
            C=1+(square(lam)-1)*m2
            ci=1/C
            invr=ci.sqrt()
            for cs,sn2 in angular:
                j=square(s)*sn2
                for phase in (-1,1):
                    ex=phase*s*cs
                    v=z*m+r*ex
                    d=(delta+square(v)).sqrt()
                    u=v/d
                    bounds_pair=[]
                    for side in (1,-1):
                        length=d-side*v
                        zz=z+side*m*length
                        xx=r+side*ex*length
                        sh=square(xx)+square(length)*j
                        B1=1-(1-eps2)*square(zz)
                        B2=eps2+(1-eps2)*sh
                        B=hull(max(eps2.lower(),B1.lower(),B2.lower()),
                               min(O,B1.upper(),B2.upper()))
                        sb=B.sqrt()
                        gamma=d*invr/sb
                        f=fp[index(gamma,False)];q=qq[index(gamma,True)]
                        pterm=min((f*square(d)*ci/sb).upper(),(2*d*invr).upper())
                        # Starting from the signed two terms in C1 individually.
                        proj=(1-j*ci).upper()
                        neg=(q*j*square(d*(1-ci)-side*v)/sb).lower()
                        ak=((pterm*proj-neg)*invr).upper()
                        whi=min(O,((1-side*u)/2).upper())
                        bounds_pair.append((ak,whi))
                    large,small=sorted(bounds_pair,key=lambda x:x[0],reverse=True)
                    total+=(small[0]+large[1]*(large[0]-small[0])).upper()
        upper=(total/(2*NM*NA)).upper().fmpq()
        outer.append(str(upper))
    return dict(case=case,box=box,subbox_upper=outer,negative=all(fmpq(x)<0 for x in outer),
                wall_seconds=round(perf_counter()-start,3))


if __name__=="__main__":
    print(json.dumps(dict(status=STATUS,prec=ctx.prec,grid=[NM,NA],gamma_bins=G)),flush=True)
    with ProcessPoolExecutor(max_workers=3) as pool:
        for out in pool.map(run,enumerate(BOXES)): print(json.dumps(out),flush=True)
