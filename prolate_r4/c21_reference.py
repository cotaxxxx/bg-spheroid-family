"""Primitive E 25-digit Gauss reference + 5point rho finite difference.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Numerical, NOT interval quadrature.
No E_z or vertical derivative used. Two fixed quadrature rules (24, 40).
"""
import argparse,json,time
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
# Independent raw rational input table; avoids importing the Arb producer.
Fr=F
R0=(Fr(63,128),Fr(65,128));T0=(Fr(63,128),Fr(65,128))
LR=(Fr(1791,512),Fr(1793,512));LHI=(Fr(1279,256),Fr(5))
STRIP_T=(Fr(0),Fr(1,64))
BOXES={
 "G2":(R0,T0,(Fr(2),Fr(513,256))),
 "G35":(R0,T0,LR),
 "EQ":(R0,STRIP_T,LHI),
 "CE":((Fr(0),Fr(1,64)),T0,LHI),
 "BD":((Fr(63,64),Fr(1)),T0,LHI),
 "AX":(R0,(Fr(63,64),Fr(1)),LHI),
 "LW":(R0,T0,(Fr(2),Fr(9,4))),
 "STRIP_00":((Fr(0),Fr(1,16)),STRIP_T,LR),
 "STRIP_08":((Fr(8,16),Fr(9,16)),STRIP_T,LR),
 "STRIP_15":((Fr(15,16),Fr(1)),STRIP_T,LR),
}
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
mp.mp.dps=25
H=mp.mpf("0.004")
def mpq(x):
 q=F(str(x));return mp.mpf(q.numerator)/q.denominator
def rules(n):
 a,w=mp.gauss_quadrature(n,"legendre")
 pi=mp.pi
 # Map x∈[-1,1] to theta, phi∈[0,pi], including Jacobian.
 return [((a[k]+1)*pi/2,w[k]*pi/2) for k in range(n)]
CACHE={}
def E_reference(lam,px,pz,n):
 if n not in CACHE:CACHE[n]=rules(n)
 grid=CACHE[n]
 out=mp.mpf(0)
 for theta,tw in grid:
  mu=mp.cos(theta);st=mp.sin(theta)
  # sin theta Jacobian comes from dmu
  wt=tw*st
  w0=mp.sqrt(lam*lam*st*st+mu*mu)
  zm=(lam*mu-pz)**2
  for phi,pw in grid:
   xi=st*mp.cos(phi);eta=st*mp.sin(phi)
   hh=lam*(1-px*xi)-pz*mu
   D=mp.sqrt((xi-px)**2+eta**2+zm)
   ratio=hh/(w0*D)
   if ratio>1 and ratio-1<mp.mpf("1e-22"):ratio=mp.mpf(1)
   elif ratio<0 and ratio < -1 and -1-ratio<mp.mpf("1e-22"):ratio=mp.mpf(-1)
   if not -1<=ratio<=1:raise ArithmeticError("invalid acos ratio")
   out+=wt*pw*hh*mp.acos(ratio)**2
 return mp.re(out/(2*mp.pi*lam))
def ref_one(name, n):
 rbox,tbox,lbox=BOXES[name]
 R=mpq((rbox[0]+rbox[1])/2)
 tau=mpq((tbox[0]+tbox[1])/2)
 lam=mpq((lbox[0]+lbox[1])/2)
 c=(1-tau*tau)/(1+tau*tau)
 s=2*tau/(1+tau*tau)
 rho=R*c;z=R*s
 if abs(rho)<mp.mpf("1e-12"):raise ValueError("rho numerical stencil needs nonzero midpoint")
 Es={k:E_reference(lam,rho+k*H,z,n) for k in (-2,-1,0,1,2)}
 d1=(8*(Es[1]-Es[-1])-(Es[2]-Es[-2]))/(12*H)
 Href=d1/rho
 return {"E0":str(Es[0]),"H_center_num":str(Href),
         "rho":str(rho),"z":str(z),"lambda":str(lam)}
def run(names,output):
 begin=time.monotonic()
 all_rows=[]
 for name in names:
  print("START",name,flush=True)
  t=time.monotonic()
  r24=ref_one(name,24);r40=ref_one(name,40)
  a=mp.mpf(r24["H_center_num"]);b=mp.mpf(r40["H_center_num"])
  obj_path=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")/(name+".json")
  checked=False;interval=None
  if obj_path.exists():
   j=json.loads(obj_path.read_text())
   if "H_interval" in j:
    interval=j["H_interval"]
    lo=mpq(interval["lower"]);hi=mpq(interval["upper"])
    checked=bool(lo<=a<=hi and lo<=b<=hi)
  entry={"name":name,"method":"primitive E + 5point rho stencil; Gauss-Legendre 24² &40²",
         "precision_decimal_digits":25,
         "h":"0.004","n24":r24,"n40":r40,
         "grid_difference_abs":str(abs(a-b)),
         "both_references_inside_Arb_interval":checked,
         "producer_H_interval":interval,
         "seconds":time.monotonic()-t,
         "warning":"No certified error for finite difference or Gauss integral"}
  all_rows.append(entry)
  # Monotone diagnostic checkpoint: a hard timeout preserves completed cases
  # but NEVER labels uncomputed references as checked.
  Path(output).write_text(json.dumps({"status":STATUS,"complete":False,
       "results":all_rows,"uncomputed":names[len(all_rows):]},indent=2)+"\n")
  print("END",name,"H24",r24["H_center_num"],"H40",r40["H_center_num"],"in",checked,flush=True)
 doc={"status":STATUS,"independent_numerical_reference":True,
      "source":"primitive E in request §4, no z derivative",
      "results":all_rows,"elapsed_seconds":time.monotonic()-begin,
      "claims":"POINT_REFERENCES_ONLY / NOT_EVIDENCE"}
 Path(output).write_text(json.dumps(doc,indent=2)+"\n")
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--names",nargs="+",required=True)
 p.add_argument("--output",required=True);a=p.parse_args()
 run(a.names,a.output)
if __name__=="__main__":main()
