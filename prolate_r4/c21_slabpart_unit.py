"""Pre-run deterministic/pointwise diagnostics for the 1024-box partial slab.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from fractions import Fraction as F
from flint import arb,fmpq as Q,ctx
from . import c21_slabpart_adaptive as S
from . import c21_slabpart_mvt as M
from prolate_r1.density import Domain,evaluate
from prolate_r1.intervals import bounds
def test():
 roots=S.initial()
 assert len(roots)==1024
 assert len({x["id"] for x in roots})==1024
 assert len({x["root_order"] for x in roots})==1024
 assert all(S.area(x)==F(1,4096) for x in roots)
 assert sum((S.area(x) for x in roots),F(0))==F(1,4)
 assert [x["id"] for x in roots[:4]]==["R16_T63","R16_T00","R24_T63","R24_T00"]
 assert S.timeout_for(roots[0])==600
 assert S.timeout_for(roots[1])==180
 st=S.mkstate();assert S.counts(st)["area_partition_sum_exact"]=="1/4"
 assert S.counts(st)["area_pending_normalized_exact"]=="1"
 n=roots[0]
 for _ in range(4):
  a,axis=S.split(n)
  assert sum((S.area(x) for x in a),F(0))==S.area(n)
  n=a[0]
 assert S.area(n)==F(1,4096*16)
 assert S.q(n["R"][1])-S.q(n["R"][0])<=F(1,256)
 assert S.q(n["tau"][1])-S.q(n["tau"][0])<=F(1,256)
 # Three pointwise comparisons to immutable R3 physical fxx.
 # These check the algebra, not the full-box interval quadrature.
 with ctx.workprec(128):
  for R,tau,lam,u,v in (
    (Q(1,128),Q(1,2),Q(5),Q(1,4),Q(1,3)),
    (Q(7,16),Q(127,128),Q(5),Q(1,3),Q(2,3)),
    (Q(7,16),Q(1,16),Q(1279,256),Q(3,4),Q(1,2))):
   a=M.a_fun(tau);b=M.b_fun(tau)
   rho=R*a;z=R*b
   geom=rho+z
   new=M.density_rr(arb(u),arb(v),(arb(rho),arb(z),arb(lam)),
                    Domain((Q(0),geom),(lam,lam)),tau)[0]
   old=evaluate(arb(u),arb(v),(arb(R),arb(tau),arb(lam)),
         Domain((R,R),(lam,lam)),(),(0,),"physical")[3]
   lo,hi=bounds(new.c[0]);x,y=bounds(old.c[0])
   assert max(lo,x)<=min(hi,y),(R,tau,u,v,lo,hi,x,y)
 print("DIAGNOSTIC_ONLY / NOT_EVIDENCE")
 print("PASS: exactly 1024 boxes, target area 1/4, route timing and min-edge")
 print("PASS: 3 pointwise overlaps against immutable R3 physical fxx")
if __name__=="__main__":test()
