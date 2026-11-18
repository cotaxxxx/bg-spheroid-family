"""Deterministic 24-case C21 H COST-ONLY runner. No cover or adaptive split.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Preregistered list and caps.
"""
from __future__ import annotations
import concurrent.futures,json,os,re,subprocess,sys,time
from pathlib import Path
from . import c21_cost_plan as plan
STATUS=plan.STATUS
OUT=plan.OUT
STATE=OUT/"STATE.json"
GROUPS=("A_LAMBDA_WIDTH","B_HESSIAN_COARSE","C_SPATIAL_BOX","D_LOW_LAMBDA")
def atomic(obj,path):
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(".tmp")
 with tmp.open("w") as f:
  json.dump(obj,f,indent=2)
  f.write("\n");f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def getstate(doc):
 if not STATE.exists():
  st={"status":STATUS,"schema":"cost_trim_v1",
      "frozen_input":"EXPERIMENTS.json","wall_cap_s":plan.BUDGET,
      "elapsed_wall_s":0.,"finished":[],
      "group_receipts":[],"invalid_geometry":doc["invalid_geometry"],
      "not_run":[],"inflight":[],"is_cover":False}
  atomic(st,STATE);return st
 st=json.loads(STATE.read_text())
 assert st["schema"]=="cost_trim_v1" and st["status"]==STATUS
 # An interrupted group cannot be accepted as completed.
 assert not st["inflight"],"INTERRUPTED_INFLIGHT: inspect logs before manually resuming"
 return st
def hwm(pid):
 try:
  with open(f"/proc/{pid}/status") as f:
   for line in f:
    if line.startswith("VmHWM:"):return int(line.split()[1])
 except (OSError,ValueError):pass
 return 0
def worker(spec,remaining):
 ident=spec["id"];out=OUT/"boxes"/(ident+".json")
 log=OUT/"logs"/(ident+".log")
 out.parent.mkdir(exist_ok=True,parents=True)
 log.parent.mkdir(exist_ok=True,parents=True)
 cmd=[sys.executable,"-u","-m","prolate_r4.c21_cost_box",
      "--id",ident,"--output",str(out)]
 start=time.monotonic();limit=min(spec["per_box_limit_s"],max(1,remaining))
 cap_due_global=remaining<spec["per_box_limit_s"]
 reason=None;peak=0
 with log.open("wb") as f:
  p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,
        cwd=str(plan.ROOT))
  try:
   while p.poll() is None:
    peak=max(peak,hwm(p.pid))
    if time.monotonic()-start>=limit:
     reason=("GLOBAL_SESSION_CAP" if cap_due_global else "PER_BOX_TIMEOUT")
     p.kill();p.wait(timeout=5);break
    time.sleep(.25)
  finally:
   if p.poll() is None:p.kill();p.wait(timeout=5)
 elapsed=time.monotonic()-start
 if reason is None and p.returncode:
  reason="PROCESS_EXIT_"+str(p.returncode)
 if reason is None:
  try:
   result=json.loads(out.read_text())
   assert result["status"]==STATUS and result["id"]==ident
   assert result["experiment_input"]==spec
   assert result["H_interval"]["lower"] and result["H_interval"]["upper"]
   assert result["route_from_position"]==spec["route_expected"]
   assert len(result["gradient"])==3 and len(result["hessian"])==6
   assert result["no_cover"] and result["sign_does_not_control_method"]
   return {"id":ident,"group":spec["group"],"result":"COMPLETED",
      "worker_supervisor_s":elapsed,
      "route":spec["route_expected"],
      "source_json":str(out.relative_to(OUT)),
      "source_log":str(log.relative_to(OUT)),
      "peak_RSS_KiB":result["peak_RSS_KiB"],
      "zero_included_RECORD_ONLY":result["zero_included_RECORD_ONLY"]}
  except (AssertionError,KeyError,ValueError,OSError) as e:
   reason="INVALID_RESULT_"+type(e).__name__+":"+str(e)[:150]
 if out.exists():out.unlink()
 text=""
 try:text=log.read_text(errors="replace")
 except OSError:pass
 m=re.search(r"MESH\s+\S+\s+route\s+(\S+)\s+BASE\s+(\d+)\s+HESS\s+(\d+)",text)
 interim={"status":STATUS,"id":ident,"run_status":"OPEN",
    "H_interval":None,"reason":reason,"worker_supervisor_s":elapsed,
    "peak_RSS_KiB_sampled_lower":peak,
    "mesh_cells_observed":({"base":int(m.group(2)),"hessian":int(m.group(3))} if m else None),
    "experiment_input":spec,"no_cover":True}
 atomic(interim,out)
 return {"id":ident,"group":spec["group"],"result":"OPEN",
    "reason":reason,"route":spec["route_expected"],
    "worker_supervisor_s":elapsed,
    "source_json":str(out.relative_to(OUT)),
    "source_log":str(log.relative_to(OUT)),
    "peak_RSS_KiB_sampled_lower":peak}
def run(max_groups=4):
 assert 1<=max_groups<=4
 doc=plan.frozen_write()
 st=getstate(doc)
 processed={x["id"] for x in st["finished"]}
 start_session=time.monotonic()
 for group in GROUPS[:max_groups]:
  cases=[x for x in doc["jobs"] if x["group"]==group and x["id"] not in processed]
  if not cases:continue
  global_remaining=plan.BUDGET-st["elapsed_wall_s"]-(time.monotonic()-start_session)
  if global_remaining<20:
   break
  start=time.monotonic()
  st["inflight"]=[x["id"] for x in cases]
  atomic(st,STATE)
  # Every group is deterministic and independent of preceding H values.
  with concurrent.futures.ThreadPoolExecutor(max_workers=min(plan.MAX_WORKERS,len(cases))) as pool:
   futures=[pool.submit(worker,item,max(2,global_remaining-2)) for item in cases]
   results=[f.result() for f in futures]
  st["finished"].extend(results);st["inflight"]=[]
  done=time.monotonic()-start
  st["elapsed_wall_s"]+=done
  st["group_receipts"].append({"group":group,"cases":len(cases),
    "completed":sum(x["result"]=="COMPLETED" for x in results),
    "open":sum(x["result"]=="OPEN" for x in results),
    "wall_s":done,"worker_seconds_sum":sum(x["worker_supervisor_s"] for x in results)})
  atomic(st,STATE)
  processed.update(x["id"] for x in results)
  print("GROUP_DONE",group,"completed",st["group_receipts"][-1]["completed"],
      "OPEN",st["group_receipts"][-1]["open"],"wall_s",round(done,3),
      "total_elapsed",round(st["elapsed_wall_s"],3),flush=True)
 all_done=len(st["finished"])==len(doc["jobs"])
 sm={"status":STATUS,"is_cover":False,"full_pilot_finished":all_done,
   "measured_jobs":len(st["finished"]),
   "completed_jobs":sum(x["result"]=="COMPLETED" for x in st["finished"]),
   "open_jobs":sum(x["result"]=="OPEN" for x in st["finished"]),
   "invalid_geometry":len(st["invalid_geometry"]),
   "unrun_valid":len(doc["jobs"])-len(st["finished"]),
   "worker_seconds_sum":sum(x["worker_supervisor_s"] for x in st["finished"]),
   "pilot_wall_s":st["elapsed_wall_s"],"groups":st["group_receipts"],
   "results":st["finished"],
   "out_of_domain":st["invalid_geometry"],
   "no_cover_and_no_sign_decision":True}
 atomic(sm,OUT/"SUMMARY.json")
 print("PILOT_SUMMARY",json.dumps({k:sm[k] for k in
   ("measured_jobs","completed_jobs","open_jobs","invalid_geometry","unrun_valid","pilot_wall_s")}),flush=True)
 return sm
if __name__=="__main__":
 run()
