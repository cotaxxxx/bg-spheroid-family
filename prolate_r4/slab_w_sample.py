"""Three fixed-ID R3 W tube-sample measurements.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No tube-wide W proof.

Select first, middle, last from the SORTED evaluated tube candidates at the
first completed checkpoint with >=3 such candidates. Selection is written
atomically and never silently changed after a resume.
"""
from __future__ import annotations
import argparse,concurrent.futures,json,os,resource,subprocess,sys,time
from pathlib import Path
from fractions import Fraction as F
from .slab_adaptive import OUT,STATE,STATUS,atomic,area,route,counts,WALL_CAP
SAMPLE_FILE=OUT/"W_SELECTION.json"
RESULT_FILE=OUT/"W_SAMPLE_RESULTS.json"
W_CAP=1200.0
def select():
 if SAMPLE_FILE.exists():return json.loads(SAMPLE_FILE.read_text())
 if not STATE.exists():return None
 st=json.loads(STATE.read_text())
 # Freeze samples only at completed slab or the hard 24h experiment cap,
 # not at a deliberately short interactive checkpoint.
 if st["pending"] and st["wall_elapsed_cumulative_s"]<WALL_CAP:return None
 tube=sorted([t for t in st["terminal"] if t["kind"]!="DECIDED_NONZERO"],
   key=lambda t:t["node"]["id"])
 if len(tube)<3:return None
 indices=(0,len(tube)//2,len(tube)-1)
 samples=[{"id":tube[k]["node"]["id"],
           "R":tube[k]["node"]["R"],
           "tau":tube[k]["node"]["tau"],
           "source_kind":tube[k]["kind"]} for k in indices]
 assert len({x["id"] for x in samples})==3
 data={"status":STATUS,"selection_rule":"sorted completed tube candidate IDs, first/median/last at first checkpoint >=3",
       "selection_batch":st["completed_batches"],
       "evaluated_tube_candidates_at_selection":len(tube),
       "selection_not_representative_of_final_tube":bool(st["pending"]),
       "samples":samples,"R3_pin":"fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"}
 atomic(data,SAMPLE_FILE)
 return data
def compute_one(spec):
 from flint import arb,fmpq as Q,ctx
 from prolate_r1.api import angular_quotient
 from prolate_r1.intervals import Config,bounds
 assert tuple(map(Q,spec["R"]))[0]>=0
 config=Config(precision=128,order=4,base_u=16,base_v=32,
   distance_ratio=Q(1,2),kappa=Q(1,4096),
   cap_from=Q(15,16),center_to=Q(1,16),
   max_depth=28,max_cells=40000)
 R=tuple(map(Q,spec["R"]));T=tuple(map(Q,spec["tau"]))
 L=(Q(1279,256),Q(5))
 start=time.monotonic()
 with ctx.workprec(128):
  result=angular_quotient(R,T,L,angle_kind="tau",config=config)
  v=result.enclosure;lo,hi=bounds(v)
  return {"status":STATUS,"id":spec["id"],
   "W_interval":{"lower":str(lo),"upper":str(hi),
     "halfwidth":float(arb((hi-lo)/2))},
   "route":result.route,"mesh_cells":result.cells,
   "W_cap_errors":[str(x) for x in result.cap_errors],
   "wall_s":time.monotonic()-start,
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "note":"one-box R3 quadratic form, no tube W coverage"}
def sample_worker(spec,available_seconds):
 name=spec["id"];path=OUT/"W_samples"/(name+".json")
 log=OUT/"W_samples"/(name+".log")
 path.parent.mkdir(parents=True,exist_ok=True)
 args=[sys.executable,"-u","-m","prolate_r4.slab_w_sample",
       "--one",name,"--output",str(path)]
 start=time.monotonic()
 try:
  with log.open("wb") as f:
   p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,
                   timeout=min(W_CAP,available_seconds),check=False)
  if p.returncode:raise RuntimeError("exit="+str(p.returncode))
  result=json.loads(path.read_text())
  return {"id":name,"status":"COMPLETED","wall_s":time.monotonic()-start,
          "W_halfwidth":result["W_interval"]["halfwidth"],
          "peak_RSS_KiB":result["peak_RSS_KiB"],
          "W_interval":result["W_interval"]}
 except (RuntimeError,subprocess.TimeoutExpired,ValueError,OSError) as ex:
  err=type(ex).__name__+":"+str(ex)[:180]
  if path.exists():path.unlink()
  path.write_text(json.dumps({"status":STATUS,"id":name,
      "W_interval":None,"reason":err},indent=2)+"\n")
  return {"id":name,"status":"OPEN","wall_s":time.monotonic()-start,
          "stop_reason":err,"W_interval":None}
def main():
 pa=argparse.ArgumentParser();pa.add_argument("--one")
 pa.add_argument("--output");args=pa.parse_args()
 if args.one:
  spec=next((x for x in json.loads(SAMPLE_FILE.read_text())["samples"]
        if x["id"]==args.one),None)
  if not spec:raise ValueError("ID not frozen in selection")
  if not args.output:raise ValueError("need output")
  out=compute_one(spec)
  Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
  print("W_RESULT",args.one,out["W_interval"],flush=True);return
 selection=select()
 if selection is None:
  print("W_SAMPLE_OPEN: slab still pending or fewer than three evaluated tube candidates");return
 if RESULT_FILE.exists():
  print("W_SAMPLE_ALREADY_RECORDED; no rerun");return
 state=json.loads(STATE.read_text())
 available=WALL_CAP-float(state["wall_elapsed_cumulative_s"])
 if available<30:
  print("W_SAMPLE_OPEN: global 24h budget exhausted");return
 start=time.monotonic()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  futs=[pool.submit(sample_worker,spec,max(1,available-2)) for spec in selection["samples"]]
  results=[f.result() for f in futs]
 data={"status":STATUS,"method":"frozen R3 angular_quotient quadratic form",
       "selection":selection,"results":results,
       "parallel_wall_s":time.monotonic()-start,
       "total_worker_wall_s":sum(x["wall_s"] for x in results),
       "full_tube_W_computed":False,
       "R3_source_validated_by_prior_V32_only":True}
 atomic(data,RESULT_FILE)
 spent=time.monotonic()-start
 state=json.loads(STATE.read_text())
 state["wall_elapsed_cumulative_s"]+=spent
 state["W_sample_wall_s"]+=spent
 assert state["wall_elapsed_cumulative_s"]<=WALL_CAP+2
 atomic(state,STATE)
 atomic(counts(state),OUT/"summary.json")
 print("W_SUMMARY",json.dumps(data,indent=2),flush=True)
if __name__=="__main__":main()
