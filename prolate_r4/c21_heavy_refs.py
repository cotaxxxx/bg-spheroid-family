"""Independent primitive-E numerical spot-check of completed H nodes.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No certified quadrature/difference remainder.
"""
from __future__ import annotations
import argparse,json,math,time
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
from . import c21_heavy_cover as cover
OUT=cover.OUT;STATUS=cover.STATUS
mp.mp.dps=30
H=mp.mpf("0.004")
def mpq(x):
 q=F(str(x));return mp.mpf(q.numerator)/q.denominator
GRIDS={}
def rules(n):
 if n not in GRIDS:
  a,w=mp.gauss_quadrature(n,"legendre")
  GRIDS[n]=[((a[k]+1)*mp.pi/2,w[k]*mp.pi/2) for k in range(n)]
 return GRIDS[n]
def E(lam,rho,pz,n):
 grid=rules(n)
 out=mp.mpf(0)
 for th,tw in grid:
  mu=mp.cos(th);sn=mp.sin(th)
  pref=tw*sn
  w=mp.sqrt(lam*lam*sn*sn+mu*mu)
  zterm=(lam*mu-pz)**2
  for ph,pw in grid:
   xi=sn*mp.cos(ph);eta=sn*mp.sin(ph)
   k=lam*(1-rho*xi)-pz*mu
   D=mp.sqrt((xi-rho)**2+eta*eta+zterm)
   arg=k/(w*D)
   if arg>1 and arg-1<mp.mpf("1e-22"):arg=mp.mpf(1)
   if arg<0 and arg< -1 and -1-arg<mp.mpf("1e-22"):arg=mp.mpf(-1)
   if not -1<=arg<=1:raise ArithmeticError("acos_argument_unphysical")
   out+=pref*pw*k*mp.acos(arg)**2
 return mp.re(out/(2*mp.pi*lam))
def Href(R,T,lam,n):
 R=mpq(R);tau=mpq(T);lam=mpq(lam)
 rho=R*(1-tau*tau)/(1+tau*tau)
 z=R*(2*tau)/(1+tau*tau)
 if rho<=mp.mpf("0.008"):return None # avoid stencil crossing rho=0
 pz=lam*z
 val={k:E(lam,rho+k*H,pz,n) for k in (-2,-1,1,2)}
 d1=(8*(val[1]-val[-1])-(val[2]-val[-2]))/(12*H)
 return str(d1/rho)
def sample_nodes():
 st=cover.readstate()
 decided=sorted((x for x in st["terminal"] if x["kind"]=="DECIDED_NONZERO"),
                key=lambda x:x["node"]["id"])
 tubes=sorted((x for x in st["terminal"] if x["kind"]!="DECIDED_NONZERO"),
              key=lambda x:x["node"]["id"])
 good_tube=[x for x in tubes if x.get("H_interval") is not None]
 chosen=[]
 if decided:chosen.append(("DECIDED",decided[len(decided)//2]))
 if good_tube:chosen.append(("EVALUATED_TUBE",good_tube[len(good_tube)//2]))
 elif tubes:chosen.append(("OPEN_TUBE_NO_H_INTERVAL",tubes[0]))
 return chosen
def check(max_s=300.):
 existing=OUT/"E_REFERENCE_RESULTS.json"
 if existing.exists():
  data=json.loads(existing.read_text())
  if data.get("complete") and data.get("status")==STATUS:
   print("E_REFERENCE_ALREADY_COMPUTED",len(data["results"]))
   return data
 pick=sample_nodes()
 t0=time.monotonic()
 rows=[]
 for cat,x in pick:
  n=x["node"];spec=x.get("H_interval")
  lo,hi=map(mpq,(spec["lower"],spec["upper"])) if spec else (None,None)
  R=tuple(mpq(a) for a in n["R"]);T=tuple(mpq(a) for a in n["tau"])
  lam=(mpq(cover.PLATE[0])+mpq(cover.PLATE[1]))/2
  pts=[("mid",(R[0]+R[1])/2,(T[0]+T[1])/2),
       ("lower_corner",R[0],T[0]),("upper_corner",R[1],T[1])]
  for tag,r,t in pts:
   entry={"status":STATUS,"id":n["id"],"category":cat,"sample":tag,
      "R":str(r),"tau":str(t),"lambda":str(lam),
      "box_H_interval":spec,
      "not_a_certified_E_reference":True}
   if time.monotonic()-t0>max_s:
    entry.update({"result":"SKIPPED_TIME_BUDGET"});rows.append(entry);continue
   if r*(1-t*t)/(1+t*t)<=mp.mpf("0.008"):
    entry.update({"result":"SKIPPED_RHO_NEAR_ZERO"});rows.append(entry);continue
   try:
    v24=Href(r,t,lam,24);v40=Href(r,t,lam,40)
    v=[mp.mpf(v24),mp.mpf(v40)]
    entry.update({"result":"NUMERICAL_COMPARE" if spec else "NUMERICAL_REFERENCE_NO_H_INTERVAL",
       "H_primitive_E_n24":v24,"H_primitive_E_n40":v40,
       "inside_Arb_both":(all(lo<=a<=hi for a in v) if spec else None),
       "difference":str(abs(v[0]-v[1]))})
   except Exception as e:
    entry.update({"result":"NUMERICAL_OPEN","reason":type(e).__name__+":"+str(e)[:150]})
   rows.append(entry)
   cover.atomic({"status":STATUS,"results":rows,"complete":False},
      OUT/"E_REFERENCE_RESULTS.json")
 result={"status":STATUS,"sample_rule":"sorted IDs median decided and median available tube, 3 points each",
   "quadrature":"primitive E Gauss-Legendre n=24,40, 5-point physical rho stencil h=0.004",
   "physical_position":"original p_z=lambda*z",
   "results":rows,"complete":True,"n_points":len(rows),
   "interval_comparison_only":"NOT mathematically validated",
   "max_time_budget_s":max_s,"elapsed_s":time.monotonic()-t0}
 cover.atomic(result,OUT/"E_REFERENCE_RESULTS.json")
 print(json.dumps({"status":STATUS,"cases":len(pick),"points":len(rows),
    "compared":sum(x["result"]=="NUMERICAL_COMPARE" for x in rows),
    "inside":sum(x.get("inside_Arb_both") is True for x in rows),
    "not_certified":True}))
 return result
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--max-seconds",type=float,default=300.)
 check(a.parse_args().max_seconds)
