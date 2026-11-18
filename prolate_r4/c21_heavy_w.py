"""Three post-terminal tube W timings, frozen sorted first/middle/last.
DIAGNOSTIC_ONLY / NOT_EVIDENCE; not W covering. No early sampling.
"""
from __future__ import annotations
import argparse,json,concurrent.futures,os,subprocess,sys,time
from pathlib import Path
from flint import arb,fmpq as Q,ctx
from prolate_r1.api import angular_quotient
from prolate_r1.intervals import Config,bounds
from . import c21_heavy_cover as cover
STATUS=cover.STATUS;OUT=cover.OUT
SEL=OUT/"W_SELECTION.json"
RESULTS=OUT/"W_RESULTS.json"
def frozen_selection():
 if SEL.exists():return json.loads(SEL.read_text())
 st=cover.readstate()
 ready=not st["pending"] or st["wall_elapsed_cumulative_s"]>=cover.WALL_CAP
 if not ready:return None
 tubes=sorted((t for t in st["terminal"] if t["kind"]!="DECIDED_NONZERO"),
      key=lambda x:x["node"]["id"])
 if len(tubes)<3:return None
 indexes=(0,len(tubes)//2,len(tubes)-1)
 samples=[{"id":tubes[k]["node"]["id"],
   "R":tubes[k]["node"]["R"],"tau":tubes[k]["node"]["tau"],
   "tube_kind":tubes[k]["kind"]} for k in indexes]
 assert len({x["id"] for x in samples})==3
 doc={"status":STATUS,"selection_rule":"first,middle,last lexicographic evaluated tube ID",
      "selected_from_evaluated_only":True,
      "selection_at":"FULL_PLATE" if not st["pending"] else "ACTUAL_36H_CAP",
      "sample_count":3,"samples":samples,"R3_pin":"fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"}
 cover.atomic(doc,SEL)
 return doc
def one(spec):
 start=time.monotonic()
 config=Config(precision=128,order=4,base_u=16,base_v=32,
    distance_ratio=Q(1,2),kappa=Q(1,4096),
    cap_from=Q(15,16),center_to=Q(1,16),
    max_depth=28,max_cells=40000)
 R=tuple(Q(x) for x in spec["R"])
 T=tuple(Q(x) for x in spec["tau"])
 with ctx.workprec(128):
  data=angular_quotient(R,T,(Q(79,16),Q(5)),
     angle_kind="tau",config=config)
  lo,hi=bounds(data.enclosure)
  return {"status":STATUS,"id":spec["id"],
    "W_interval":{"lower":str(lo),"upper":str(hi),
                  "halfwidth":float(arb((hi-lo)/2))},
    "wall_s":time.monotonic()-start,
    "route":data.route,"cells":data.cells,
    "cap_errors":[str(x) for x in data.cap_errors],
    "one_sample_only":True}
def invoke_one(idname,out):
 doc=json.loads(SEL.read_text())
 spec=next((s for s in doc["samples"] if s["id"]==idname),None)
 assert spec is not None,"NOT_REGISTERED_W_ID"
 j=one(spec)
 cover.atomic(j,Path(out))
 print("W",idname,j["W_interval"],flush=True)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--id");p.add_argument("--output")
 a=p.parse_args()
 if a.id:
  assert a.output
  invoke_one(a.id,a.output);return
 doc=frozen_selection()
 if not doc:
  print("W_DEFERRED: plate has pending boxes or fewer than3 evaluated tubes")
  cover.atomic({"status":STATUS,
    "reason":"requires FULL_PLATE or actual 36h cap plus >=3 evaluated tubes",
    "W_interval":None,"full_tube_W":False},OUT/"W_DEFERRED.json")
  return
 if RESULTS.exists():print("W_ALREADY_RUN");return
 st=cover.readstate()
 available=cover.WALL_CAP-st["wall_elapsed_cumulative_s"]
 if available<30:
  cover.atomic({"status":STATUS,"W_interval":None,
      "reason":"GLOBAL_36H_CAP_NO_BUDGET_FOR_W","full_tube_W":False},
         OUT/"W_DEFERRED.json")
  print("W_OPEN: no global budget");return
 begin=time.monotonic()
 results=[]
 for x in doc["samples"]:
  obj=OUT/"W_samples"/(x["id"]+".json")
  log=OUT/"W_samples"/(x["id"]+".log")
  obj.parent.mkdir(parents=True,exist_ok=True)
  cap=min(1200.,max(1,available-2))
  cmd=[sys.executable,"-u","-m","prolate_r4.c21_heavy_w",
       "--id",x["id"],"--output",str(obj)]
  t=time.monotonic()
  with log.open("wb") as f:
   try:
    p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,
      timeout=cap,check=False,cwd=str(cover.ROOT))
    if p.returncode:raise RuntimeError("RETURN_CODE_"+str(p.returncode))
    got=json.loads(obj.read_text())
    results.append({"id":x["id"],"result":"COMPLETED",
     "worker_seconds":time.monotonic()-t,"W_interval":got["W_interval"]})
   except (subprocess.TimeoutExpired,RuntimeError,OSError,ValueError) as e:
    reason=type(e).__name__+":"+str(e)
    cover.atomic({"status":STATUS,"id":x["id"],"W_interval":None,"reason":reason},obj)
    results.append({"id":x["id"],"result":"OPEN",
     "worker_seconds":time.monotonic()-t,"reason":reason})
  available-=time.monotonic()-t
  if available<=3:break
 elapsed=time.monotonic()-begin
 cover.atomic({"status":STATUS,"samples":results,"parallel":False,
   "W_wall_s":elapsed,"full_tube_W":False},RESULTS)
 st=cover.readstate()
 st["wall_elapsed_cumulative_s"]+=elapsed;st["W_wall_s"]+=elapsed
 cover.atomic(st,cover.STATE)
 cover.atomic(cover.counts(st),OUT/"SUMMARY.json")
 print("W_RESULTS",len(results),"wall_s",elapsed)
if __name__=="__main__":main()
