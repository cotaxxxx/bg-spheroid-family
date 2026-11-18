"""Preregistered 8-box Stage-A comparison: first-order vs SECOND-ORDER C21 H.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Stage B launch requires ALL eight improvements.
"""
from __future__ import annotations
import argparse,concurrent.futures,json,os,subprocess,sys,time
from fractions import Fraction as F
from pathlib import Path
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER"
OLD=ROOT/"runs/2026-11-18/D_PRO_C21_SLAB_PART/boxes"
SAMPLES=(
 ("R16_T00","GENERAL"),("R18_T08","GENERAL"),
 ("R20_T48","GENERAL"),("R23_T32","GENERAL"),
 ("R26_T00","GENERAL"),("R28_T32","GENERAL"),
 ("R16_T63","AXIS_MVT"),("R31_T63","AXIS_MVT"))
LIMIT={"GENERAL":1800.0,"AXIS_MVT":2400.0}
CAP=86400.0
def atomic(obj,path):
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+".tmp")
 with tmp.open("w") as f:
  json.dump(obj,f,indent=2)
  f.write("\n");f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def width(interval):
 return (F(interval["upper"])-F(interval["lower"]))/2
def freeze_selection():
 found=[]
 for name,kind in SAMPLES:
  src=OLD/(name+".json")
  d=json.loads(src.read_text())
  assert d["name"]==name and d["route_from_position"]==kind
  assert d["status"]==STATUS
  assert isinstance(d["H_interval"],dict)
  found.append({"id":name,"route":kind,
    "R":d["input_box"]["R"],"tau":d["input_box"]["tau"],
    "lambda":d["input_box"]["lambda"],
    "old_H_interval":d["H_interval"],
    "old_halfwidth_exact":str(width(d["H_interval"])),
    "old_worker_wall_s":d["worker_elapsed_s"],
    "old_cell_count":d["mesh_cells"],
    "original_source":"runs/2026-11-18/D_PRO_C21_SLAB_PART/boxes/"+name+".json"})
 doc={"status":STATUS,"frozen_inputs":"2e3a091ad3c7a98a5962b8c016d2e1fb51bcf0e9",
  "selection":"GENERAL sorted indices 0,11,22,33,44,55 plus AXIS first and last",
  "sample_count":8,"samples":found,"limit_s":LIMIT,
  "max_parallel":8,"global_cap_seconds":CAP,
  "stage_B_gate":"ALL8_COMPLETED_AND_ALL_NEW_HALFWIDTH_LE_OLD"}
 atomic(doc,OUT/"STAGE_A_SELECTION.json")
 return doc
def execute_one(spec):
 name=spec["id"];kind=spec["route"]
 path=OUT/"stage_A_boxes"/(name+".json")
 log=OUT/"stage_A_logs"/(name+".log")
 path.parent.mkdir(parents=True,exist_ok=True)
 log.parent.mkdir(parents=True,exist_ok=True)
 cmd=[sys.executable,"-u","-m","prolate_r4.c21_second_order",
      "--id",name,"--R",*spec["R"],"--tau",*spec["tau"],
      "--output",str(path)]
 start=time.monotonic()
 proc=None;peak_kib=0;cause=None
 with log.open("wb") as f:
  proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,
       cwd=str(ROOT))
  try:
   while proc.poll() is None:
    try:
     with open(f"/proc/{proc.pid}/status") as pf:
      for line in pf:
       if line.startswith("VmHWM:"):
        peak_kib=max(peak_kib,int(line.split()[1]))
        break
    except (OSError,ValueError):pass
    if time.monotonic()-start>=LIMIT[kind]:
     cause="STAGE_A_PER_BOX_TIME_LIMIT"
     proc.kill();proc.wait(timeout=5);break
    time.sleep(.25)
  finally:
   if proc.poll() is None:
    proc.kill();proc.wait(timeout=5)
 seconds=time.monotonic()-start
 if cause is None and proc.returncode!=0:
  cause="PROCESS_EXIT_"+str(proc.returncode)
 if cause is None:
  try:
   obj=json.loads(path.read_text())
   assert obj["status"]==STATUS and obj["route_from_position"]==kind
   assert obj["input_box"]["R"]==spec["R"]
   assert obj["input_box"]["tau"]==spec["tau"]
   assert len(obj["gradient"])==3 and len(obj["hessian"])==6
   newwidth=width(obj["H_interval"])
   oldwidth=F(spec["old_halfwidth_exact"])
   improvement=oldwidth/newwidth if newwidth>0 else None
   verdict="NONWORSE" if newwidth<=oldwidth else "WORSE"
   res={"status":STATUS,"id":name,"route":kind,
     "run_result":"COMPLETED","comparison":verdict,
     "first_order_halfwidth_exact":str(oldwidth),
     "second_order_halfwidth_exact":str(newwidth),
     "halfwidth_ratio_old_over_new_exact":str(improvement),
     "first_order_halfwidth":float(oldwidth),
     "second_order_halfwidth":float(newwidth),
     "first_order_wall_s":spec["old_worker_wall_s"],
     "second_order_worker_wall_s":obj["worker_elapsed_s"] if "worker_elapsed_s" in obj else obj["wall_s"],
     "second_order_parent_wall_s":seconds,
     "point_halfwidth":obj["center_point"]["halfwidth"],
     "linear_halfwidth":obj["linear_correction"]["halfwidth"],
     "quadratic_halfwidth":obj["quadratic_correction"]["halfwidth"],
     "mesh_cells":obj["mesh_cells"],
     "peak_RSS_KiB":obj["peak_RSS_KiB"],
     "historical_worker_cell_count":spec["old_cell_count"],
     "original_json":spec["original_source"],
     "new_json":str(path.relative_to(OUT)),
     "log":str(log.relative_to(OUT))}
   return res
  except (OSError,ValueError,AssertionError,KeyError,ZeroDivisionError) as e:
   cause="OUTPUT_ERROR:"+type(e).__name__+":"+str(e)[:180]
 if path.exists():path.unlink()
 doc={"status":STATUS,"id":name,"run_result":"OPEN",
    "H_interval":None,"reason":cause,"wall_s":seconds,
    "peak_RSS_KiB_sampled_lower":peak_kib,
    "mesh_cells_observed":None}
 try:
  import re
  m=re.search(r"MESH\s+\S+\s+(\d+)",log.read_text(errors="replace"))
  if m:doc["mesh_cells_observed"]=int(m.group(1))
 except OSError:pass
 atomic(doc,path)
 return {"status":STATUS,"id":name,"route":kind,
   "run_result":"OPEN","comparison":"UNRESOLVED",
   "reason":cause,"second_order_parent_wall_s":seconds,
   "first_order_halfwidth_exact":spec["old_halfwidth_exact"],
   "second_order_halfwidth_exact":None,
   "peak_RSS_KiB_sampled_lower":peak_kib,
   "new_json":str(path.relative_to(OUT)),"log":str(log.relative_to(OUT))}
def perform():
 sel=json.loads((OUT/"STAGE_A_SELECTION.json").read_text())
 assert [x["id"] for x in sel["samples"]]==[x[0] for x in SAMPLES]
 if (OUT/"STAGE_A_GATE.json").exists():
  return json.loads((OUT/"STAGE_A_GATE.json").read_text())
 t0=time.monotonic()
 atomic({"status":STATUS,"stage":"A","execution":"RUNNING",
         "selection":"STAGE_A_SELECTION.json","start_time_monotonic_not_persisted":True},
        OUT/"STAGE_A_PROGRESS.json")
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  futures=[pool.submit(execute_one,item) for item in sel["samples"]]
  results=[f.result() for f in futures]
 elapsed=time.monotonic()-t0
 if all(x["run_result"]=="COMPLETED" for x in results):
  gate="STAGE_B_ALLOWED" if all(x["comparison"]=="NONWORSE" for x in results) else "STAGE_B_BLOCKED_WORSE_WIDTH"
 else:gate="STAGE_B_BLOCKED_STAGE_A_OPEN"
 comparison={"status":STATUS,"selection_commit_pinned":True,
   "method":"signed spatial order4, point gradient, interval Hessian Taylor-2",
   "stage_A_wall_s":elapsed,"stage_A_sum_worker_s":sum(x["second_order_parent_wall_s"] for x in results),
   "box_count":len(results),"completed":sum(x["run_result"]=="COMPLETED" for x in results),
   "worse":sum(x.get("comparison")=="WORSE" for x in results),
   "open":sum(x["run_result"]=="OPEN" for x in results),
   "stage_B_gate":gate,"results":results}
 atomic(comparison,OUT/"STAGE_A_GATE.json")
 atomic({"status":STATUS,"stage":"A","execution":"COMPLETED",
         "stage_B_gate":gate,"wall_s":elapsed},OUT/"STAGE_A_PROGRESS.json")
 print(json.dumps(comparison,indent=2),flush=True)
 return comparison
def main():
 pa=argparse.ArgumentParser()
 pa.add_argument("--freeze-selection-only",action="store_true")
 args=pa.parse_args()
 if args.freeze_selection_only:
  print(json.dumps(freeze_selection(),indent=2));return
 perform()
if __name__=="__main__":main()
