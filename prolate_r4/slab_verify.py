"""External exact-rational audit of adaptive slab runner state and logs.
DIAGNOSTIC_ONLY / NOT_EVIDENCE: consistency, not mathematical correctness
of the underlying Arb quadrature.
"""
import json,collections
from pathlib import Path
from fractions import Fraction as F
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
OUT=Path("runs/2026-11-18/D_PRO_C21_SLAB_ADAPTIVE")
def q(v):return F(v)
def area(node):
 return (q(node["R"][1])-q(node["R"][0]))*(q(node["tau"][1])-q(node["tau"][0]))
def verify():
 st=json.loads((OUT/"state.json").read_text())
 report=json.loads((OUT/"summary.json").read_text())
 terminal=st["terminal"];pending=st["pending"];inflight=st["inflight"]
 all_ids=[x["node"]["id"] for x in terminal]+[x["id"] for x in pending+inflight]
 assert len(all_ids)==len(set(all_ids))
 actual=sum((area(x["node"]) for x in terminal),F(0))
 actual+=sum((area(x) for x in pending+inflight),F(0))
 assert actual==1,"terminal and pending fail exact partition-of-unit check"
 nde=F(0);ntu=F(0);npend=F(0)
 for x in terminal:
  box=x["node"];A=area(box)
  if x["kind"]=="DECIDED_NONZERO":
   assert x["H_interval"] is not None
   lo=q(x["H_interval"]["lower"]);hi=q(x["H_interval"]["upper"])
   assert hi<0 or lo>0
   nde+=A
  else:
   if x["kind"]=="TUBE_AT_MINIMUM":
    assert x["H_interval"] is not None
    lo=q(x["H_interval"]["lower"]);hi=q(x["H_interval"]["upper"])
    assert lo<=0<=hi
    assert q(box["R"][1])-q(box["R"][0])<=F(1,256)
    assert q(box["tau"][1])-q(box["tau"][0])<=F(1,256)
   else:assert x["kind"]=="TUBE_TIMEOUT_OR_ERROR"
   ntu+=A
 for n in pending+inflight:npend+=area(n)
 assert str(nde)==report["area_decided_exact"]
 assert str(ntu)==report["area_tube_evaluated_exact"]
 assert str(npend)==report["area_pending_exact"]
 assert nde+ntu+npend==1
 assert len(st["processed_jobs"])==report["measured_jobs"]
 # Validate all saved successful source JSON endpoints and declared routes.
 seen=0
 for t in terminal:
  if t["H_interval"] is None:continue
  src=OUT/t["source_json"]
  assert src.exists()
  j=json.loads(src.read_text())
  assert j["status"]==STATUS and j["H_interval"]==t["H_interval"]
  assert j["route_from_position"]==t["route"]
  seen+=1
 # Include producer JSON for successful SPLIT PARENTS, not just terminals.
 # Otherwise a run with no DECIDED leaf would check zero numeric sources.
 split_ids={e["parent"] for e in st["split_events"]}
 success_ids=set()
 for job in st["processed_jobs"]:
  name=job["id"];src=OUT/"boxes"/(name+".json")
  assert src.exists(),("missing source JSON",name)
  obj=json.loads(src.read_text())
  assert obj["status"]==STATUS,(name,"wrong status")
  if job["status"]=="EVALUATED":
   assert name not in success_ids
   assert "H_interval" in obj and isinstance(obj["H_interval"],dict)
   lo=q(obj["H_interval"]["lower"]);hi=q(obj["H_interval"]["upper"])
   assert lo<=hi
   success_ids.add(name)
   if name in split_ids:
    assert lo<=0<=hi,(name,"parent split without 0 in interval")
  elif job["status"]=="OPEN":
   assert obj["H_interval"] is None
  else:
   raise AssertionError("unexpected job state: "+job["status"])
 for evt in st["split_events"]:
  assert len(evt["children"])==2
  assert evt["axis"] in ("R","tau")
  assert evt["zero_included_RECORD_ONLY"] is True
  assert evt["parent"] in success_ids
 assert report["full_slab_processed"]==(len(pending+inflight)==0)
 obj={"status":STATUS,"checker":"exact state, disjoint ID, area and source-log contract",
   "verdict":"PASS","area_total_exact":"1",
   "area_decided":str(nde),"area_tube_evaluated":str(ntu),
   "area_pending":str(npend),"terminal_boxes":len(terminal),
   "pending_boxes":len(pending+inflight),"checked_box_sources":len(success_ids),
   "split_parent_records":len(st["split_events"]),
   "not_independent_Arb_numerical_proof":True}
 (OUT/"checker.json").write_text(json.dumps(obj,indent=2)+"\n")
 print(json.dumps(obj,indent=2))
if __name__=="__main__":verify()
