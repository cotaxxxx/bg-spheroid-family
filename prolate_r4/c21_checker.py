"""Independent exact-rational OUTPUT CONTRACT checker for C21 representative pilot.
DIAGNOSTIC_ONLY / NOT_EVIDENCE; not an independent quadrature audit.
"""
import json
from pathlib import Path
from fractions import Fraction as F
from .c21_special import BOXES
BASE=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
NAMES=["G2","G35","AX","EQ","CE","BD"]+[f"STRIP_{i:02}" for i in range(16)]+["LW"]
def ends(x):return F(x["lower"]),F(x["upper"])
def do():
 results=[];bad=[]
 for name in NAMES:
  j=json.loads((BASE/(name+".json")).read_text())
  if "H_interval" not in j:
   results.append({"name":name,"state":"OPEN","contract":"uncomputed"});continue
  assert j["status"]=="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
  box=j["input_box"]
  for key,expected in zip(("R","tau","lambda"),BOXES[name]):
   assert tuple(map(F,box[key]))==tuple(F(str(q)) for q in expected),(name,key)
  hlo,hhi=ends(j["H_interval"])
  p0,p1=ends(j.get("center_point",j.get("H_center_point")))
  if "outer_correction" in j:c0,c1=ends(j["outer_correction"])
  else:c0,c1=ends(j["H_outer_correction"])
  if "cap_correction" in j:k0,k1=ends(j["cap_correction"])
  else:k0,k1=F(0),F(0)
  assert hlo<=p0+c0+k0,(name,"bad lower")
  assert hhi>=p1+c1+k1,(name,"bad upper")
  assert (hlo<=0<=hhi)==j["zero_included_RECORD_ONLY"]
  assert abs((hhi-hlo)/2-F(str(j["H_interval"]["halfwidth"])))<F(1,10**5)
  for _,d in j["directional_contributions"].items():
   x=d.get("outer_halfwidth_contribution",d.get("halfwidth_contribution"))
   lo,hi=ends(x)
   assert lo<=0<=hi
  results.append({"name":name,"state":"CHECKED","halfwidth":float((hhi-hlo)/2),
                  "zero_included":hlo<=0<=hhi})
 assert len(results)==23
 obj={"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
      "scope":"exact JSON endpoint/metadata contract, NOT mathematical source verification",
      "evaluated":len([x for x in results if x["state"]=="CHECKED"]),
      "open":len([x for x in results if x["state"]=="OPEN"]),
      "no_synthetic_enclosures_for_open":True,"rows":results}
 (BASE/"contract_checker.json").write_text(json.dumps(obj,indent=2)+"\n")
 print(json.dumps({"evaluated":obj["evaluated"],"open":obj["open"],
                  "status":"CONTRACT_PASS"},indent=2))
if __name__=="__main__":do()
