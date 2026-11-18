"""C21 slab-part mean-value horizontal E_rho_rho box enclosure.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No Simpson/s integration.
Extends independent rho' in [0,rho_hi], z in [zlo,zhi].
"""
from __future__ import annotations
import time,resource
import flint
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import Domain,seed
from prolate_r1.jets import Jet,angle
from prolate_r1.quadrature import make_mesh,integrate
from prolate_r1.intervals import Config,bounds,midpoint,radius,sym
from .c21_regular import enc,iv,STATUS,PIN

LAMBDA=(Q(1279,256),Q(5))
BU=16;BV=32;RATIO=Q(1,2);ORDER=4
THRESH=Q(1,16)
def a_fun(t):return (1-t*t)/(1+t*t)
def b_fun(t):return 2*t/(1+t*t)
def extended(R,T,L=LAMBDA):
 assert Q(0)<=R[0]<=R[1]<=Q(1)
 assert Q(0)<=T[0]<=T[1]<=Q(1)
 rh=R[1]*a_fun(T[0])
 zlo=R[0]*b_fun(T[0]);zhi=R[1]*b_fun(T[1])
 # Every input point has 0<=rho<=rh and zlo<=z<=zhi.
 assert Q(0)<=rh and Q(0)<=zlo<=zhi
 assert rh+zhi<1,("OPEN: extended point box needs a stronger radial bound",rh+zhi)
 return (Q(0),rh),(zlo,zhi),L
def route(R,T):
 rh=R[1]*a_fun(T[0])
 if T[1]==Q(1):return "AXIS_MVT"
 if R[0]==Q(0):return "CENTER_MVT"
 if rh<=THRESH:return "SMALL_RHO_MVT"
 return "GENERAL"
def density_rr(u,v,params,dom,chart,active=(),orders=(0,)):
 # Angles are a fixed change of integration variables at chart midpoint
 # tau_chart; no chart derivatives w.r.t the independent rho',z,lambda.
 rho,z,lam=(seed(x,n,active,orders) for x,n in zip(params,("rho","z","lam")))
 U=seed(u,"u",active,orders)
 V=seed(v,"v",active,orders)
 t=chart
 a=a_fun(t);b=b_fun(t)
 q=8*U**2/(1+U**2)**2
 sp=4*U*(1-U**2)/(1+U**2)**2
 ex=1-q;ez=sp*(V*arb.pi()).cos()
 xx=a*ex-b*ez;xz=b*ex+a*ez
 rmax=dom.R[1]; Lmax=dom.lam[1]
 k=(1-rho*xx-z*xz).cap(1-rmax,1+rmax)
 D2=1+rho*rho+z*z-2*rho*xx-2*z*xz+(lam*lam-1)*(xz-z)**2
 d2low=(1-rmax)**2
 if d2low<=0:raise ArithmeticError("OPEN: extended radial distance bound")
 D2=D2.cap(d2low,Lmax**2*(1+rmax)**2)
 D=D2.sqrt()
 invD=D.reciprocal_positive(1-rmax,Lmax*(1+rmax))
 invD2=D2.reciprocal_positive(d2low,Lmax**2*(1+rmax)**2)
 B=(1-(1-1/lam**2)*xz**2).cap(1/Lmax**2,1)
 invsqrtB=B.sqrt().reciprocal_positive(Q(1)/Lmax,Q(1))
 gamma=(k*invD*invsqrtB).cap(0,1)
 G,Rfun,Rfunprime=angle(gamma)
 P=xx-rho
 gamma_r=(-xx+k*P*invD2)*invD*invsqrtB
 gamma_rr=(-2*xx*P-k+3*k*P*P*invD2)*invD*invD2*invsqrtB
 frr=4*xx*Rfun*gamma_r-2*k*(Rfunprime*gamma_r*gamma_r+Rfun*gamma_rr)
 jac=8*U*(1-U*U)/(1+U*U)**3
 return (frr*jac,)
def signed_angular(mesh,params,dom,chart,outer=None):
 if outer is None:
  return integrate(lambda u,v,axis,n:density_rr(
   u,v,params,dom,chart,(axis,),(n,)),mesh,ORDER)[0]
 def cb(u,v,axis,n):
  j=density_rr(u,v,params,dom,chart,(axis,outer),(n,1))[0]
  return (Jet((n,),[j.coeff(k,1) for k in range(n+1)]),)
 return integrate(cb,mesh,ORDER)[0]
def calculate(name,R,T,L=LAMBDA):
 assert flint.__version__=="0.8.0"
 rt=route(R,T)
 assert rt in ("AXIS_MVT","CENTER_MVT","SMALL_RHO_MVT"),rt
 bboxes=extended(R,T,L);rbox,zbox,lbox=bboxes
 if rt=="AXIS_MVT" and rbox[1]>THRESH:
  raise ArithmeticError("OPEN: axis rho_hi exceeds pre-frozen 1/16 bound")
 start=time.perf_counter()
 cfg=Config(precision=128,order=ORDER,base_u=BU,base_v=BV,
            distance_ratio=RATIO,max_cells=40000,max_depth=28)
 rgeom=rbox[1]+zbox[1]
 dom=Domain((Q(0),rgeom),lbox,Q(0),"equator")
 chart=midpoint(T)
 with ctx.workprec(128):
  mesh=make_mesh(dom.R,Q(0),cfg,lam=lbox)
  print("MESH",name,len(mesh),"rgeom",rgeom,"chart",chart,flush=True)
  center=tuple(arb(midpoint(x)) for x in bboxes)
  full=tuple(iv(x) for x in bboxes)
  st=time.perf_counter()
  p=signed_angular(mesh,center,dom,chart)
  print("CENTER",name,enc(p),"time",time.perf_counter()-st,flush=True)
  correction=arb(0);components={}
  for box,axis in zip(bboxes,("rho","z","lam")):
   st=time.perf_counter()
   if radius(box)==0:continue
   d=signed_angular(mesh,full,dom,chart,axis)
   term=d*sym(radius(box))
   correction+=term
   components[axis]={"signed_derivative_integral":enc(d),
      "contribution":enc(term),"wall_s":time.perf_counter()-st}
   print("DERIV",name,axis,enc(term)["halfwidth"],
     "time",time.perf_counter()-st,flush=True)
  H=p+correction
  lo,hi=bounds(H)
  return {"status":STATUS,"name":name,
   "route":"MVT_horizontal_second_rho_independent_extension",
   "route_from_position":rt,"input_box":{
    "R":list(map(str,R)),"tau":list(map(str,T)),
    "lambda":list(map(str,L))},
   "extension":{"rho_prime":list(map(str,rbox)),
     "z":list(map(str,zbox)),"lambda":list(map(str,lbox)),
     "rhohi_plus_zhi":str(rgeom),
     "fixed_angle_chart_tau":str(chart)},
   "H_interval":enc(H),"H_extended_center":enc(p),
   "H_outer_correction":enc(correction),
   "directional_contributions":components,
   "zero_included_RECORD_ONLY":bool(lo<=0<=hi),
   "mesh_cells":len(mesh),
   "mesh":{"order":ORDER,"base_u":BU,"base_v":BV,
           "ratio":str(RATIO),"kappa":"0",
           "s_integral":"NONE_MEAN_VALUE_RANGE"},
   "wall_s":time.perf_counter()-start,
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "pinned_R3_commit":PIN,
   "global_C21_condition":"OPEN"}
