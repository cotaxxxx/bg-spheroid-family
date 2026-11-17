"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed R3 half-width gates; no sign gate."""
import argparse
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from time import perf_counter_ns
from flint import arb, fmpq as Q, ctx
from .. import Config, angular_raw, angular_quotient, axis_g, equatorial_phi_s
from ..intervals import STATUS, bounds
from .resumable import run_suite, source_identity

LAMBDAS=(Q(2),Q(7,2),Q(5))
def decimal_q(text):
    value=Fraction(text)
    return Q(value.numerator,value.denominator)
POINTS=((Q(1,2),Q(1,2)),(Q(3,4),Q(1,3)),
        (Q(1,2),Q(0)),(Q(1,2),Q(1)))
BOXES=(
    ((Q(63,128),Q(65,128)),(Q(63,128),Q(65,128)),(Q(1791,512),Q(1793,512))),
    ((Q(95,128),Q(97,128)),(Q(15,128),Q(17,128)),(Q(1279,256),Q(5))),
    ((Q(79,128),Q(81,128)),(Q(95,128),Q(97,128)),(Q(2),Q(513,256))))
WREF={
    (Q(2),*POINTS[0]):decimal_q("1.39692515774"),
    (Q(7,2),*POINTS[0]):decimal_q("1.92464766603"),
    (Q(5),*POINTS[0]):decimal_q("1.97011480066"),
    (Q(5),*POINTS[1]):decimal_q("1.92926214675"),
    (Q(5),*POINTS[2]):decimal_q("2.09903813065"),
    (Q(5),*POINTS[3]):decimal_q("1.89316108158")}

class WidthFailure(AssertionError):
    def __init__(self,detail):
        self.diagnostic=detail
        super().__init__("R3 diagnostic gate failed: "+detail["name"]+
                         "; half_width="+detail["half_width"]+
                         "; limit="+str(detail["half_width_limit"]))

@dataclass(frozen=True)
class Case:
    name: str
    kind: str
    args: tuple
    limit: object
    reference: object=None
    tolerance: Q=Q(1,1000000)

def specifications():
    out=[]
    for lam in LAMBDAS:
        for R,T in POINTS:
            out.append(Case("W_point_"+str((lam,R,T)),"W",(R,T,lam),Q(1,20),
                            WREF.get((lam,R,T))))
    for lam,ref in ((Q(2),decimal_q("1.48292942522")),(Q(5),decimal_q("2.09803266086"))):
        out.append(Case("W_center_"+str(lam),"W",(Q(1,32),Q(1,2),lam),Q(1,20),ref))
    # The request did not specify lambda for g/Phi_s. The pre-run plan fixed all three.
    for lam in LAMBDAS:
        for t in (Q(1,32),Q(1,2),Q(7,8)):
            ref=decimal_q("0.905251775196") if (lam,t)==(Q(5),Q(1,2)) else None
            out.append(Case("g_"+str((lam,t)),"g",(t,lam),Q(1,100),ref))
    for lam in LAMBDAS:
        for s in (Q(1,1024),Q(1,4),Q(9,16)):
            ref=({Q(1,1024):decimal_q("-0.226193187473"),Q(1,4):decimal_q("-0.236444996026")}
                 .get(s) if lam==Q(5) else None)
            tol=Q(1,10000) if s==Q(1,1024) else Q(1,1000000)
            out.append(Case("Phi_s_"+str((lam,s)),"phi",(s,lam),Q(1,20),ref,tol))
    for i,box in enumerate(BOXES):
        out.append(Case("W_box_"+str(i+1),"W",box,Q(3,10)))
    out.append(Case("Ebeta_reference_lambda5","raw",(Q(1,2),Q(1,2),Q(5)),None,
                    decimal_q("0.236413776079")))
    return tuple(out)

def measure(case):
    cfg=Config()  # Do not substitute an easier test configuration.
    start=perf_counter_ns()
    if case.kind=="W":
        result=angular_quotient(*case.args,angle_kind="tau",config=cfg)
    elif case.kind=="g":
        result=axis_g(*case.args,config=cfg)
    elif case.kind=="phi":
        result=equatorial_phi_s(*case.args,config=cfg)
    elif case.kind=="raw":
        result=angular_raw(*case.args,angle_kind="tau",config=cfg)
    else:
        raise ValueError("unknown case kind")
    elapsed=perf_counter_ns()-start
    value=result.balls[1] if case.kind=="raw" else result.enclosure
    lo,hi=bounds(value); half=(hi-lo)/2
    width_ok=case.limit is None or half<=case.limit
    # Reference values are non-rigorous diagnostics. A tolerance band need
    # only intersect the enclosure; it is not a certified interval oracle.
    ref_ok=(case.reference is None or
            lo-case.tolerance<=case.reference<=hi+case.tolerance)
    detail={"status":STATUS,"name":case.name,"kind":case.kind,
            "inputs":repr(case.args),"default_config":repr(cfg),
            "half_width":str(half),"half_width_decimal":arb(half).str(12),
            "half_width_limit":None if case.limit is None else str(case.limit),
            "width_pass":bool(width_ok),"reference_pass":bool(ref_ok),
            "reference":None if case.reference is None else str(case.reference),
            "reference_tolerance":str(case.tolerance),
            "reference_status":"NONINTERVAL_DIAGNOSTIC",
            "evaluation_ns":elapsed,"seconds":str(Q(elapsed,1000000000)),
            "result":result.to_json()}
    if not width_ok or not ref_ok:
        raise WidthFailure(detail)
    return detail

def case_list():
    return [(c.name,lambda c=c:measure(c)) for c in specifications()]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",default="prolate_r1/outputs/dig_r3_width.json")
    ap.add_argument("--resume",action="store_true")
    ap.add_argument("--max-cases",type=int)
    ap.add_argument("--case",type=int,action="append",dest="selected")
    ap.add_argument("--retry-failed",action="store_true")
    ap.add_argument("--list-cases",action="store_true")
    args=ap.parse_args(); tests=case_list(); cfg=Config()
    if args.list_cases:
        for i,(name,_) in enumerate(tests): print(i,name)
        return
    root=Path(__file__).resolve().parents[1]
    code=run_suite(tests,"r3_width",args.out,source_identity(root,cfg.precision),
                   resume=args.resume,max_cases=args.max_cases,
                   selected=None if args.selected is None else set(args.selected),
                   retry_failed=args.retry_failed,
                   precision_context=lambda:ctx.workprec(cfg.precision))
    raise SystemExit(code)

if __name__=="__main__": main()
