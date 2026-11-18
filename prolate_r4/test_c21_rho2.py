"""Compare derived rho2 kernel with pinned R3's physical fxx at s=1.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Shares R3 geometric upstream for checking.
"""
import json,resource
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import Domain,evaluate
from prolate_r1.intervals import bounds
from .c21_special import rr
PARAMS=((Q(1,2),Q(1,2),Q(2)),(Q(1,64),Q(1,2),Q(5)),(Q(1,2),Q(63,64),Q(5)))
SPACE=((Q(1,4),Q(1,4)),(Q(1,2),Q(1,2)),(Q(7,8),Q(3,4)))
def run():
 ctx.prec=128
 outcomes=[]
 for R,tau,L in PARAMS:
  dom=Domain((R,R),(L,L),Q(0),"equator")
  p=tuple(map(arb,(R,tau,L)))
  for u,v in SPACE:
   u,v=arb(u),arb(v)
   one=rr(u,v,arb(1),p,dom)[0].c[0]
   other=evaluate(u,v,p,dom,(),(0,),"physical")[3].c[0]
   a,b=bounds(one);c,d=bounds(other)
   outcomes.append({"R":str(R),"tau":str(tau),"lambda":str(L),
       "u":str(u),"v":str(v),"overlap":bool(a<=d and c<=b),
       "midpoint_difference_display":abs(float(one.mid())-float(other.mid()))})
 assert all(x["overlap"] for x in outcomes)
 return {"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
         "test":"rho2 derived vs pinned R3 fxx, 9 fixed samples",
         "overlap":sum(x["overlap"] for x in outcomes),
         "total":len(outcomes),
         "max_midpoint_diff":max(x["midpoint_difference_display"] for x in outcomes),
         "limits":"not spatial integration audit", "samples":outcomes}
if __name__=="__main__":print(json.dumps(run(),indent=2))
