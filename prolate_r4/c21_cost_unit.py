"""Pure-polynomial signed mixed-Hessian Jet test for C21 cost pilot.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Tests code algebra, not C21 density.
"""
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import seed
from prolate_r1.intervals import bounds
from prolate_r1.quadrature import Cell
from .c21_cost_box import signed_integral
from . import c21_cost_plan as plan
def polynomial(u,v,params,active,orders):
 R,x,lam=[seed(a,n,active,orders) for a,n in
          zip(params,("R","x","lam"))]
 return R*R+3*R*x+2*x*x+5*lam*lam
def main():
 mesh=(Cell((Q(0),Q(1)),(Q(0),Q(1))),)
 cases=[((("R",2),),2),((("R",1),("x",1)),3),
        ((("x",2),),4),((("lam",2),),10)]
 with ctx.workprec(128):
  for order in (2,4):
   params=(arb(1),arb(2),arb(3))
   for directions,expected in cases:
    val=signed_integral(mesh,polynomial,params,("R","x","lam"),
              directions,order)
    assert bounds(val)==(Q(expected),Q(expected)),(directions,bounds(val))
   print("SIGNED_HESSIAN_TOY_ORDER",order,"PASS")
 print(plan.STATUS)
 print("This test is not a mathematical audit of C21 density or coverage.")
if __name__=="__main__":main()
