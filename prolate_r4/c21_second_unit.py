"""Second-order outer Taylor arithmetic and exact-area controller tests.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No certification of C21 density.
"""
from flint import arb,fmpq as Q,ctx
from fractions import Fraction as F
from prolate_r1.density import seed
from prolate_r1.quadrature import Cell
from prolate_r1.intervals import bounds,midpoint,radius,sym
from .c21_second_order import integral,STATUS
from . import c21_second_cover as B
def kernel(u,v,params,active,orders):
 R,t,lam=(seed(p,axis,active,orders) for p,axis in zip(params,("R","x","lam")))
 return R*R+3*R*t+2*t*t+lam
def run():
 assert STATUS=="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
 nodes=B.initial()
 assert len(nodes)==1024
 assert sum(map(B.area,nodes),F(0))==F(1,4)
 assert len({n["id"] for n in nodes})==1024
 for n in nodes[:30]:
  kids,axis=B.split(n)
  assert len(kids)==2 and sum(map(B.area,kids),F(0))==B.area(n)
  assert axis=="R"
 # The univariate signed Taylor integrator returns the exact polynomial derivatives.
 box=((Q(1,4),Q(5,16)),(Q(1,8),Q(3,16)),(Q(1279,256),Q(5)))
 names=("R","x","lam")
 mesh=(Cell((Q(0),Q(1)),(Q(0),Q(1))),)
 with ctx.workprec(128):
  point=tuple(arb(midpoint(x)) for x in box)
  full=tuple(arb(x[0]).union(arb(x[1])) for x in box)
  center=integral(mesh,kernel,point,names,())
  dR=integral(mesh,kernel,point,names,(("R",1),))
  dt=integral(mesh,kernel,point,names,(("x",1),))
  dl=integral(mesh,kernel,point,names,(("lam",1),))
  hRR=integral(mesh,kernel,full,names,(("R",2),))
  hRt=integral(mesh,kernel,full,names,(("R",1),("x",1)))
  htt=integral(mesh,kernel,full,names,(("x",2),))
  assert bounds(hRR)==(Q(2),Q(2))
  assert bounds(hRt)==(Q(3),Q(3))
  assert bounds(htt)==(Q(4),Q(4))
  assert bounds(dl)==(Q(1),Q(1))
  h=[radius(x) for x in box]
  result=center+dR*sym(h[0])+dt*sym(h[1])+dl*sym(h[2])
  result+=(hRR*arb(0).union(arb(h[0]*h[0]))
        +htt*arb(0).union(arb(h[1]*h[1])))*arb(Q(1,2))
  result+=hRt*sym(h[0]*h[1])
  for R in box[0]:
   for t in box[1]:
    for lam in box[2]:
     exact=R*R+3*R*t+2*t*t+lam
     lo,hi=bounds(result)
     assert lo<=exact<=hi,(R,t,lam,lo,hi)
 print(STATUS)
 print("PASS: 1024 exact nodes, 1/4 area, strict tie-R splits")
 print("PASS: mixed jets, diagonal 2! and cross 1!, outward Taylor corners")
if __name__=="__main__":run()
