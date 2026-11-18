"""Independent rational accounting and signed-component record audit.
DIAGNOSTIC_ONLY / NOT_EVIDENCE, NOT independent mathematical H proof.
"""
from __future__ import annotations
import json,hashlib,subprocess
from fractions import Fraction as F
from pathlib import Path
from . import c21_heavy_cover as c
STATUS=c.STATUS
OUT=c.OUT
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
GIT=Path("/home/daybreak/bg-spheroid-family")
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
R3FILES=("__init__.py","api.py","center_bounds.py","density.py",
         "jets.py","intervals.py","quadrature.py")
def ends(j):return F(j["lower"]),F(j["upper"])
def includes(whole,parts):
 lo,hi=ends(whole)
 return lo<=sum((ends(p)[0] for p in parts),F(0)) and hi>=sum((ends(p)[1] for p in parts),F(0))
def check():
 r=c.frozen_registry()
 loaded=json.loads((OUT/"REGISTRY.json").read_text())
 assert loaded==r and len(r["roots"])==4096
 st=c.readstate()
 summary=c.counts(st)
 written=json.loads((OUT/"SUMMARY.json").read_text())
 assert {k:summary[k] for k in ("decided_area_exact","tube_area_exact",
    "pending_area_exact","area_total_exact","pending_unprocessed_count")}=={
    k:written[k] for k in ("decided_area_exact","tube_area_exact",
    "pending_area_exact","area_total_exact","pending_unprocessed_count")}
 assert summary["area_total_exact"]=="1"
 assert st["inflight"]==[]
 assert len({x["id"] for x in st["processed"]})==len(st["processed"])
 # Initial root partition and bounds agree with geometry-only frozen registry.
 assert {x["id"] for x in r["roots"]}=={
   f"R{i:02d}_T{j:02d}" for i in range(64) for j in range(64)}
 examined=0;open_nodes=0
 for p in st["processed"]:
  node_id=p["id"]
  path=OUT/"boxes"/(node_id+".json")
  assert path.exists(),node_id
  d=json.loads(path.read_text())
  assert d["status"]==STATUS and d["id"]==node_id
  assert d["input_box"]["R"]==p["R"]
  assert d["input_box"]["tau"]==p["tau"]
  assert d["input_box"]["lambda"]==c.PLATE
  assert c.route_of(p)==p["route"]
  assert (OUT/"logs"/(node_id+".log")).exists()
  if p["status"]=="OPEN":
   assert d["H_interval"] is None and d.get("reason")
   open_nodes+=1;continue
  assert p["status"]=="EVALUATED" and d["route_from_position"]==p["route"]
  assert d["base_mesh"]["order"]==4 and d["hessian_mesh"]["order"]==4
  assert d["base_mesh"]["base_u"]==16 and d["base_mesh"]["base_v"]==32
  assert d["hessian_mesh"]["base_u"]==8 and d["hessian_mesh"]["base_v"]==16
  assert d["base_mesh"]["ratio"]=="1/2" and d["hessian_mesh"]["ratio"]=="1"
  assert d["status"]==STATUS and d["is_diagnostic_only"] and d["no_unsigned_zero_order"]
  assert len(d["gradient"])==3 and len(d["hessian"])==6
  assert includes(d["H_interval"],(d["center_point"],d["linear_correction"],
      d["quadratic_correction"],d["boundary_cap_correction"]))
  assert includes(d["linear_correction"],
      [x["correction"] for x in d["gradient"].values()])
  assert includes(d["quadratic_correction"],
      [x["correction"] for x in d["hessian"].values()])
  for i,a in enumerate(d["outer_axes"]):
   box=tuple(F(v) for v in d["outer_boxes"][a])
   h=(box[1]-box[0])/2
   assert d["gradient"][a]["outer_halfwidth"]==str(h)
   for j in range(i,3):
    b=d["outer_axes"][j];bx=tuple(F(v) for v in d["outer_boxes"][b])
    hb=(bx[1]-bx[0])/2
    k=a+"_"+b;item=d["hessian"][k]
    if i==j:
     assert item["type"]=="diagonal_half"
     assert item["factor"]==["0",str(h*h)]
    else:
     assert item["type"]=="cross"
     assert item["factor"]==[str(-h*hb),str(h*hb)]
  cl,ch=ends(d["boundary_cap_correction"])
  if p["route"]=="BOUNDARY_COLLAR":
   assert cl<=0<=ch and ch>0,"boundary cap must be present"
  else:assert cl==ch==0,"cap must not be inserted on nonboundary"
  lo,hi=ends(d["H_interval"])
  assert (lo<=0<=hi)==d["zero_included_RECORD_ONLY"]
  examined+=1
 for s in st["splits"]:
  assert s["zero_membership_record"] is True
  x=next(p for p in st["processed"] if p["id"]==s["id"])
  parent={"R":x["R"],"tau":x["tau"],"id":x["id"],
    "parent":None,"depth":x["depth"],"rank":0,"root":"fixture"}
  kids,ax=c.split(parent)
  assert ax==s["axis"] and [z["id"] for z in kids]==s["children"]
  assert sum(map(c.area,kids),F(0))==c.area(parent)
 for node in st["terminal"]:
  assert node["kind"] in ("DECIDED_NONZERO","TUBE_MIN","TUBE_OPEN_ERROR")
  if node["kind"]=="TUBE_OPEN_ERROR":
   assert node["reason"]
  if node["kind"]=="TUBE_MIN":
   n=node["node"]
   assert F(n["R"][1])-F(n["R"][0])<=F(1,256)
   assert F(n["tau"][1])-F(n["tau"][0])<=F(1,256)
 for f in R3FILES:
  blob=(R3/f).read_bytes()
  pin=subprocess.check_output(["git","-C",str(GIT),"show",PIN+":prolate_r1/"+f])
  assert blob==pin,("PIN_CHANGE",f)
 result={"status":STATUS,"verdict":"ACCOUNTING_PASS_NOT_CERTIFICATION",
  "checked_completed_H_boxes":examined,"checked_OPEN_boxes":open_nodes,
  "checked_splits":len(st["splits"]),
  "initial_roots":4096,"area_exact":"1",
  "R3_bytewise_pins":len(R3FILES),
  "independent_math_certification":False,
  "no_global_H_cover_claim":True}
 c.atomic(result,OUT/"CHECKER.json")
 print(json.dumps(result,indent=2))
 return result
if __name__=="__main__":check()
