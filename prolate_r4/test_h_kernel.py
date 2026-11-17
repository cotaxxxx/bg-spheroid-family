"""H kernel cross-check against frozen R3 physical rho derivative.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Not an independent analytic proof:
both constructions share the R3 co-rotating geometry.
"""
import json,time,resource
from flint import arb,ctx,fmpq as Q
from prolate_r1.density import evaluate,Domain
from prolate_r1.intervals import bounds
from .h_box2 import density_H,REFS,RBOX,LBOX,STATUS,check_input
def main():
    ctx.prec=128
    assert check_input()
    dom=Domain(RBOX,LBOX,Q(0),"equator")
    points=((Q(1,8),Q(1,4)),(Q(1,2),Q(1,2)),(Q(7,8),Q(3,4)))
    n=0;worst=0.0
    for param,_ in REFS:
        R,tau,lam=param
        rho=arb(R)*arb((1-tau*tau)/(1+tau*tau))
        p=tuple(map(arb,param))
        for u,v in points:
            u,v=arb(u),arb(v)
            y=density_H(u,v,p,dom)[0].c[0]
            fx=evaluate(u,v,p,dom,(),(0,),mode="physical")[1].c[0]
            y2=fx/rho
            lo,hi=bounds(y);l2,h2=bounds(y2)
            assert lo<=h2 and l2<=hi, ("no overlap",param,u,v)
            delta=abs(float(y.mid())-float(y2.mid()))
            worst=max(worst,delta);n+=1
    print(json.dumps({"status":STATUS,"cross_checks":n,
                      "all_intervals_overlap":True,
                      "max_absolute_midpoint_difference_display":worst,
                      "limit":"shares frozen R3 geometry; no independent cubature audit",
                      "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
if __name__=="__main__":main()
