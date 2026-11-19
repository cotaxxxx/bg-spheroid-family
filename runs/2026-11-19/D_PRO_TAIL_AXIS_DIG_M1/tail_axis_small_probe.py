#!/usr/bin/env python3
"""TAILAX_V1: ε=0 inner H kernel only; rigorous Arb cell range, diagnostic."""
from pathlib import Path
from fractions import Fraction
from time import monotonic
import json,hashlib,traceback,resource
import flint
from flint import fmpq as Q,arb,ctx

ROOT=Path(__file__).resolve().parent
PLAN_SHA="0fb1fbf4e1cfbd77bfb860cb5825217fcc1b7b0975011e978908e1f628cbea86"
if hashlib.sha256((ROOT/"PLAN_TAIL_AXIS_BEFORE_RUN.md").read_bytes()).hexdigest()!=PLAN_SHA:
    raise RuntimeError("FROZEN PLAN CHANGED; refusing all diagnostics")
if flint.__version__!="0.8.0":
    raise RuntimeError("python-flint != 0.8.0")
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
PREC=192;NCELLS=256;TNODES=(8,16,32,64);N=20
A=[Q(1)]
for n in range(21):
    A.append(A[-1]*Q(2*n+2,2*n+3))
B=[A[n]*Q(2*n*n+10*n+10,2*n+3) for n in range(N+1)]

def endpoints(x):
    if not x.is_finite(): raise ArithmeticError("STOP_NONFINITE_INTERVAL")
    return x.lower().fmpq(), x.upper().fmpq()
def exact_hull(a,b):
    if a>b: raise ArithmeticError("STOP_BAD_HULL")
    return arb(a).union(arb(b))
def clipped(x,a,b):
    y=x.intersection(exact_hull(a,b))
    if not y.is_finite(): raise ArithmeticError("STOP_EMPTY_RANGE_INTERSECTION")
    return y
def nonnegative(x):
    lo,hi=endpoints(x)
    if hi<0: raise ArithmeticError("STOP_NEGATIVE_PROVEN_GEOMETRY")
    return clipped(x,Q(0),hi)
def ec(x):
    l,u=endpoints(x)
    return {"lower":str(l),"upper":str(u),
            "lower_float":float(arb(l)),"upper_float":float(arb(u)),
            "halfwidth_float":float(arb((u-l)/2))}
def bounds_Fprime_Q(g):
    h=clipped((1-g)/2,Q(0),Q(1,2))
    p=arb(0);q=arb(0)
    for n in range(N,-1,-1):
        p=p*h+arb(A[n])
        q=q*h+arb(B[n])
    plo=2*p
    phi=plo+4*arb(A[N+1])*h**(N+1)
    qlo=q
    qhi=qlo+arb(2*N+12)*arb(A[N+1])*h**(N+1)
    fp=exact_hull(endpoints(plo)[0],endpoints(phi)[1])
    qc=exact_hull(endpoints(qlo)[0],endpoints(qhi)[1])
    return fp,qc

def values_at_cell(t,j):
    pi=arb.pi()
    # Full angular CELL, not a midpoint evaluation.
    phi=(pi*Q(2*j,NCELLS)).union(pi*Q(2*(j+1),NCELLS))
    x=phi.cos()
    y=phi.sin()
    y2=nonnegative(y*y)
    dx2=nonnegative((x-arb(Q(1,2)))**2)
    t2=arb(Q(t*t))
    D2=t2+arb(Q(5,4))-x
    if endpoints(D2)[0]<=0:
        raise ArithmeticError("STOP_D2_LOWER_NONPOSITIVE")
    D=D2.sqrt()
    invD=arb(1)/D
    invD2=arb(1)/D2
    k=arb(1)-x/2
    if endpoints(k)[0]<=0:
        raise ArithmeticError("STOP_K_LOWER_NONPOSITIVE")
    g=clipped(k*invD,Q(0),Q(1))
    fp,q=bounds_Fprime_Q(g)
    Ay=nonnegative(g*g*(t2+dx2)*invD2)
    fac=1-k*invD2
    C=nonnegative(y2*nonnegative(fac*fac))
    raw=invD*(fp*Ay-q*C)
    # Keep common y² FACTORED with the subtracted log coefficient.
    # c_H(phi)=-2*pi*y² and r=K+2*pi*y²/sqrt(1+t²).
    corrective=2*pi/(arb(1+t*t).sqrt())-q*nonnegative(fac*fac)*invD
    res=invD*fp*Ay+y2*corrective
    return raw,res

def check_axis_symmetry():
    out=[]
    e=Q(1,5)
    for m,z in ((Q(1,4),Q(1,2)),(Q(3,4),Q(1,2))):
        k=lambda u,v: 1-v*u
        d=lambda u,v: (u-v)**2+e*e*(1-u*u)
        b=lambda u: 1-(1-e*e)*u*u
        checks={"k":k(-m,z)==k(m,-z),
                "d2":d(-m,z)==d(m,-z),
                "B":b(-m)==b(m)}
        if not all(checks.values()):
            raise ArithmeticError("STOP_AXIS_RATIONAL_REFLECTION")
        out.append({"mu":str(m),"z":str(z),"eps":"1/5","checks":checks})
    return out

def run():
    out={"classification":STATUS,"plan_sha256":PLAN_SHA,
         "type":"EPSILON_ZERO_INNER_KERNEL_ONLY_NOT_A_GLOBAL_H_BOUND",
         "rho":"1/2","z":"0","epsilon":"0 inner-limit","arb_bits":PREC,
         "N":N,"phi_cells":NCELLS,
         "t_nodes":list(TNODES),"axis_symmetry":check_axis_symmetry(),
         "measurements":[]}
    with ctx.workprec(PREC):
        pi=arb.pi()
        for t in TNODES:
            start=monotonic()
            d={"t":t,"classification":STATUS}
            try:
                raw=arb(0); r=arb(0)
                for j in range(NCELLS):
                    if monotonic()-start>120: raise TimeoutError("STOP_FIXED_NODE_120S")
                    kr,rr=values_at_cell(t,j)
                    raw+=kr/NCELLS
                    r+=rr/NCELLS
                norm=pi/arb(1+t*t).sqrt()
                indirect=raw+norm
                l1,h1=endpoints(r);l2,h2=endpoints(indirect)
                if h1<l2 or h2<l1:
                    raise ArithmeticError("STOP_IDENTITY_INTERVAL_DISJOINT")
                L,U=endpoints(raw)
                raw_abs_lower=Q(0) if L<=0<=U else min(abs(L),abs(U))
                res_abs_upper=max(abs(l1),abs(h1))
                d.update({
                    "status":"COMPLETE","Kbar_interval":ec(raw),
                    "rbar_factored_interval":ec(r),
                    "rbar_indirect_interval":ec(indirect),
                    "mean_subtractor_interval":ec(norm),
                    "rbar_contains_zero":bool(l1<=0<=h1),
                    "residual_abs_max_below_raw_abs_min":bool(res_abs_upper<raw_abs_lower),
                    "raw_abs_min_exact":str(raw_abs_lower),
                    "residual_abs_max_exact":str(res_abs_upper),
                    "t_times_Kbar":ec(t*raw),
                    "t_squared_times_rbar":ec(t*t*r)})
            except Exception as exc:
                d.update({"status":"STOP","stop_reason":repr(exc),"traceback":traceback.format_exc()})
            d["wall_seconds"]=monotonic()-start
            d["peak_RSS_KiB"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            out["measurements"].append(d)
            (ROOT/("PILOT_T%03d.json"%t)).write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
            print("TAILAX_T",t,d["status"],d.get("Kbar_interval"),d.get("rbar_factored_interval"),
                  "seconds",d["wall_seconds"],flush=True)
    (ROOT/"PILOT_RESULT.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    print("PILOT_RECORDS",len(out["measurements"]),"symmetry",out["axis_symmetry"],flush=True)

if __name__=="__main__":run()
