"""Deterministic SECOND-ORDER 12-worker adaptive H slab survey (C21).
DIAGNOSTIC_ONLY / NOT_EVIDENCE. NOT a λ∈[2,5] covering.

State checkpoints at every ordered batch; worker logs and JSON per box.
Terminal tube includes H intervals containing zero at min width, genuine
PER-BOX timeouts, and mathematical/resource exceptions. Unprocessed
pending jobs are NOT called evaluated tube boxes.
"""
from __future__ import annotations
import argparse,collections,concurrent.futures,json,os,resource,subprocess,sys,time
from fractions import Fraction as F
from pathlib import Path
from flint import fmpq as Q
from .c21_slabpart_mvt import route
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
OUT=Path("runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER/STAGE_B")
STATE=OUT/"state.json"
WALL_CAP=86400.0
INITIAL_R_PARTS=16
INITIAL_T_PARTS=64
TARGET_AREA=F(1,4)
MIN_EDGE=F(1,256)
MAX_WORKERS=12
TIME_LIMITS={"GENERAL":1800,"AXIS_MVT":2400,"CENTER_MVT":2400,"SMALL_RHO_MVT":2400}
def q(x):return F(str(x))
def s(x):return str(x)
def area(node):
 return (q(node["R"][1])-q(node["R"][0]))*(q(node["tau"][1])-q(node["tau"][0]))
def revbits(k,bits):
 return int(f"{k:0{bits}b}"[::-1],2)
def mk_id(i,j):
 return f"R{i+16:02d}_T{j:02d}"
def initial():
 tau_seq=[63,0]+sorted((j for j in range(64) if j not in (63,0)),key=lambda j:revbits(j,6))
 rank_t={j:i for i,j in enumerate(tau_seq)}
 rank_r={i:k for k,i in enumerate(sorted(range(16),key=lambda i:revbits(i,4)))}
 nodes=[]
 for i in range(INITIAL_R_PARTS):
  for j in range(INITIAL_T_PARTS):
   name=mk_id(i,j)
   r=rank_r[i];t=rank_t[j]
   node={"id":name,"root":name,"root_order":(t//2)*32+2*r+(t%2),
     "depth":0,"R":[str(F(i+16,64)),str(F(i+17,64))],
     "tau":[str(F(j,64)),str(F(j+1,64))],"parent":None}
   nodes.append(node)
 assert len(nodes)==1024 and len({x["root_order"] for x in nodes})==1024
 assert sum((area(n) for n in nodes),F(0))==TARGET_AREA
 return sorted(nodes,key=priority)
def priority(node):
 return (node["depth"],node["root_order"],node["id"])
def mkstate():
 calibpath=OUT.parent/"STAGE_A_GATE.json"
 if not calibpath.exists():
  raise RuntimeError("STAGE_A_REQUIRED: comparison missing")
 calib=json.loads(calibpath.read_text())
 if calib["stage_B_gate"]!="STAGE_B_ALLOWED" or calib["box_count"]!=8 or calib["worse"]!=0 or calib["open"]!=0:
  raise RuntimeError("STAGE_B_BLOCKED: fixed 8-box gate not met")
 calibration_wall=float(calib["stage_A_wall_s"])
 return {"status":STATUS,
   "schema_version":"c21_second_adaptive_v1",
   "policy":"../PRE_RUN_FREEZE.md",
   "slab_lambda":["1279/256","5"],
   "global_wall_cap_seconds":WALL_CAP,
   "initial_partition":"16x64;R=1/4..1/2",
   "workers":MAX_WORKERS,"min_edge":"1/256",
   "pending":initial(),"inflight":[],
   "terminal":[],"split_events":[],
   "processed_jobs":[],"completed_batches":0,
   "wall_elapsed_cumulative_s":calibration_wall,
   "calibration_wall_s":calibration_wall,
   "H_adaptive_wall_s":0.0,
   "W_sample_wall_s":0.0,
   "session_receipts":[]}
def atomic(obj,path=STATE):
 path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_suffix(path.suffix+".tmp")
 with temp.open("w") as f:
  json.dump(obj,f,indent=2)
  f.write("\n");f.flush();os.fsync(f.fileno())
 os.replace(temp,path)
def load():
 if not STATE.exists():
  st=mkstate();atomic(st);return st
 st=json.loads(STATE.read_text())
 assert st["schema_version"]=="c21_second_adaptive_v1"
 assert st["slab_lambda"]==["1279/256","5"]
 if st["inflight"]:
  known={x["id"] for x in st["pending"]}
  for job in st["inflight"]:
   if job["id"] not in known:st["pending"].append(job)
  st["inflight"]=[];st["pending"].sort(key=priority)
  atomic(st)
 return st
def split(node):
 R=tuple(map(q,node["R"]));T=tuple(map(q,node["tau"]))
 lenR=R[1]-R[0];lenT=T[1]-T[0]
 axis="R" if lenR>=lenT else "tau"
 x=(R if axis=="R" else T);mid=(x[0]+x[1])/2
 childs=[]
 for i,ends in enumerate(((x[0],mid),(mid,x[1]))):
  child=dict(node);child["id"]=node["id"]+f".{axis}{i}"
  child["parent"]=node["id"]
  child["depth"]=node["depth"]+1
  child[axis]=[str(ends[0]),str(ends[1])]
  childs.append(child)
 assert sum(map(area,childs),F(0))==area(node)
 return childs,axis
def timeout_for(node):
 return TIME_LIMITS[route(tuple(map(Q,node["R"])),tuple(map(Q,node["tau"])))]
def get_proc_vmHWM_KiB(pid):
 try:
  with open(f"/proc/{pid}/status") as f:
   for line in f:
    if line.startswith("VmHWM:"):
     return int(line.split()[1])
 except (OSError,ValueError):pass
 return None

def worker(node,remaining_session):
 import re
 name=node["id"];R=node["R"];T=node["tau"]
 kind=route(tuple(map(Q,R)),tuple(map(Q,T)))
 cap=timeout_for(node)
 hard=min(float(cap),float(remaining_session))
 interrupted=hard < float(cap)-1e-6
 logfile=OUT/"logs"/(name+".log")
 jsonfile=OUT/"boxes"/(name+".json")
 logfile.parent.mkdir(exist_ok=True,parents=True)
 jsonfile.parent.mkdir(exist_ok=True,parents=True)
 cmd=[sys.executable,"-u","-m","prolate_r4.c21_second_order",
      "--id",name,"--R",*R,"--tau",*T,"--output",str(jsonfile)]
 start=time.monotonic();peak_sampled=0
 cause=None;completed=False
 try:
  with logfile.open("wb") as f:
   process=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
   try:
    while process.poll() is None:
     vm=get_proc_vmHWM_KiB(process.pid)
     if vm:peak_sampled=max(peak_sampled,vm)
     if time.monotonic()-start>=hard:
      cause=("SESSION_INTERRUPTED" if interrupted else "PER_BOX_TIME_LIMIT")
      process.kill()
      process.wait(timeout=5)
      break
     time.sleep(0.25)
   finally:
    if process.poll() is None:
     process.kill();process.wait(timeout=5)
  if cause is None:
   if process.returncode!=0:
    raise RuntimeError(f"child exit {process.returncode}")
   got=json.loads(jsonfile.read_text())
   assert got["route_from_position"]==kind
   assert got["status"]==STATUS and isinstance(got["H_interval"],dict)
   lo=q(got["H_interval"]["lower"]);hi=q(got["H_interval"]["upper"])
   assert lo<=hi
   zero=bool(lo<=0<=hi)
   result={"status":"EVALUATED","H_interval":got["H_interval"],
     "halfwidth":got["H_interval"]["halfwidth"],
     "zero_included_RECORD_ONLY":zero,"cell_count":got["mesh_cells"],
     "peak_RSS_KiB":got["peak_RSS_KiB"],
     "peak_RSS_source":"child_resource_getrusage_maxrss",
     "source_json":str(jsonfile.relative_to(OUT)),
     "source_log":str(logfile.relative_to(OUT))}
   completed=True
 except Exception as e:
  cause=type(e).__name__+":"+str(e)[:250]
 sec=time.monotonic()-start
 if not completed:
  if jsonfile.exists():jsonfile.unlink()
  # Mesh cell count may be observed before the timeout, even if the
  # full H enclosure cannot be produced.
  try:
   logtxt=logfile.read_text(errors="replace")
   match=re.search(r"MESH\s+\S+\s+(\d+)",logtxt)
   mesh_cells=int(match.group(1)) if match else None
  except OSError:mesh_cells=None
  result={"status":("PENDING_INTERRUPTED" if cause=="SESSION_INTERRUPTED"
           else "OPEN"),"H_interval":None,
          "reason":cause,"cell_count":mesh_cells,
          "peak_RSS_KiB_sampled_lower":peak_sampled or None,
          "peak_RSS_source":"supervisor_proc_VmHWM_sampled_lower_bound",
          "source_log":str(logfile.relative_to(OUT))}
  if cause!="SESSION_INTERRUPTED":
   jsonfile.write_text(json.dumps({
     "status":STATUS,"id":name,"route":kind,
     "R":R,"tau":T,"lambda":["1279/256","5"],
     "H_interval":None,"reason":cause,
     "mesh_cells_observed":mesh_cells,
     "peak_RSS_KiB_sampled_lower":peak_sampled or None,
     "peak_RSS_source":"supervisor_proc_VmHWM_sampled_lower_bound",
     "measurement_wall_s":sec},indent=2)+"\n")
   result["source_json"]=str(jsonfile.relative_to(OUT))
 return {"node":node,"route":kind,"elapsed_s":sec,
         **result}
def settle(st,item):
 node=item["node"];kind=item["route"]
 st["processed_jobs"].append({"id":node["id"],"route":kind,
     "wall_s":item["elapsed_s"],"status":item["status"],
     "depth":node["depth"],"area":str(area(node))})
 if item["status"]=="PENDING_INTERRUPTED":
  st["pending"].append(node);return
 if item["status"]=="OPEN":
  st["terminal"].append({"node":node,"kind":"TUBE_TIMEOUT_OR_ERROR",
    "reason":item["reason"],"route":kind,"elapsed_s":item["elapsed_s"],
    "H_interval":None,"cell_count":item.get("cell_count"),
    "peak_RSS_KiB":item.get("peak_RSS_KiB_sampled_lower"),
    "peak_RSS_type":"sampled_lower_bound",
    "source_json":item.get("source_json"),
    "source_log":item.get("source_log")})
  return
 if not item["zero_included_RECORD_ONLY"]:
  label="DECIDED_NONZERO"
 elif (q(node["R"][1])-q(node["R"][0])<=MIN_EDGE and
       q(node["tau"][1])-q(node["tau"][0])<=MIN_EDGE):
  label="TUBE_AT_MINIMUM"
 else:
  children,axis=split(node)
  st["pending"].extend(children)
  st["split_events"].append({"parent":node["id"],"axis":axis,
    "depth":node["depth"],"parent_area":str(area(node)),
    "children":[x["id"] for x in children],
    "zero_included_RECORD_ONLY":True})
  return
 st["terminal"].append({"node":node,"kind":label,
   "route":kind,"elapsed_s":item["elapsed_s"],
   "H_interval":item["H_interval"],
   "cell_count":item["cell_count"],
   "peak_RSS_KiB":item["peak_RSS_KiB"],
   "peak_RSS_type":item.get("peak_RSS_source"),
   "zero_included_RECORD_ONLY":item["zero_included_RECORD_ONLY"],
   "source_json":item["source_json"],"source_log":item["source_log"]})
def counts(st):
 decided=[e for e in st["terminal"] if e["kind"]=="DECIDED_NONZERO"]
 tube=[e for e in st["terminal"] if e["kind"]!="DECIDED_NONZERO"]
 waiting=st["pending"]+st["inflight"]
 a_dec=sum((area(x["node"]) for x in decided),F(0))
 a_tube=sum((area(x["node"]) for x in tube),F(0))
 a_pending=sum((area(x) for x in waiting),F(0))
 assert a_dec+a_tube+a_pending==TARGET_AREA,{
   "dec":str(a_dec),"tube":str(a_tube),"pending":str(a_pending)}
 route_time=collections.defaultdict(float)
 route_count=collections.Counter()
 depth_processed=collections.Counter()
 for p in st["processed_jobs"]:
  route_time[p["route"]]+=p["wall_s"]
  route_count[p["route"]]+=1
  depth_processed[str(p["depth"])]+=1
 depth_terminal=collections.Counter(str(x["node"]["depth"]) for x in st["terminal"])
 tube_sorted=sorted(tube,key=lambda e:e["node"]["id"])
 return {"status":STATUS,
   "plate_lambda":["1279/256","5"],
   "measured_jobs":len(st["processed_jobs"]),
   "measured_unique_nodes":len({x["id"] for x in st["processed_jobs"]}),
   "split_parents":len(st["split_events"]),
   "terminal_boxes":len(st["terminal"]),
   "decided_count":len(decided),
   "tube_candidate_EVALUATED_count":len(tube),
   "pending_UNEVALUATED_count":len(waiting),
   "area_decided_exact":str(a_dec),
   "area_tube_evaluated_exact":str(a_tube),
   "area_pending_exact":str(a_pending),
   "area_potential_tube_including_pending_exact":str(a_tube+a_pending),
   "area_partition_sum_exact":str(a_dec+a_tube+a_pending),
   "target_subregion_area_exact":str(TARGET_AREA),
   "area_decided_normalized_exact":str(a_dec/TARGET_AREA),
   "area_tube_normalized_exact":str(a_tube/TARGET_AREA),
   "area_pending_normalized_exact":str(a_pending/TARGET_AREA),
   "full_slab_processed":bool(not waiting),
   "full_subregion_processed":bool(not waiting),
   "tube_by_route":dict(collections.Counter(x["route"] for x in tube)),
   "tube_reason_count":dict(collections.Counter(x["kind"] for x in tube)),
   "depth_processed":dict(depth_processed),
   "depth_terminal":dict(depth_terminal),
   "route_worker_seconds_sum":dict(route_time),
   "route_jobs":dict(route_count),
   "total_experiment_wall_s_including_calibration":st["wall_elapsed_cumulative_s"],
   "calibration_wall_s":st.get("calibration_wall_s",0.0),
   "H_adaptive_wall_s":st.get("H_adaptive_wall_s",0.0),
   "W_sample_wall_s":st.get("W_sample_wall_s",0.0),
   "global_remaining_wall_s":max(0,WALL_CAP-st["wall_elapsed_cumulative_s"]),
   "total_wall_elapsed_sessions_s":st["wall_elapsed_cumulative_s"],
   "tube_coordinates":[{"id":x["node"]["id"],
      "R":x["node"]["R"],"tau":x["node"]["tau"],
      "area":str(area(x["node"])),"reason":x["kind"]}
      for x in tube_sorted],
   "unprocessed_pending_coordinates":[{"id":x["id"],
      "R":x["R"],"tau":x["tau"],"area":str(area(x))}
      for x in sorted(waiting,key=priority)],
   "box_count_for_global_extrapolation":"NOT_AVAILABLE_UNTIL_FULL_SLAB_COVER",
   "W_tube_cost":"OPEN_NOT_MEASURED"}
def run_session(session_seconds,max_batches=None,workers=MAX_WORKERS):
 assert 0<session_seconds<=WALL_CAP
 assert 1<=workers<=MAX_WORKERS
 OUT.mkdir(parents=True,exist_ok=True)
 st=load()
 start=time.monotonic()
 st["pending"].sort(key=priority)
 batch_count=0
 while st["pending"] and batch_count!=max_batches:
  elapsed=time.monotonic()-start
  remaining=min(session_seconds-elapsed,
                WALL_CAP-st["wall_elapsed_cumulative_s"]-elapsed)
  if remaining<=0:break
  # For bounded interactive diagnostic runs, do not start a batch that
  # cannot be given at least 20 seconds of worker execution.
  if remaining<20:break
  batch=st["pending"][:workers]
  del st["pending"][:len(batch)]
  st["inflight"]=batch
  atomic(st) # checkpoint BEFORE executing the batch
  with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
   results=list(pool.map(lambda n:worker(n,remaining-2),batch))
  # Process in deterministic submission order, regardless of CPU timing.
  for item in results:settle(st,item)
  st["inflight"]=[]
  st["pending"].sort(key=priority)
  st["completed_batches"]+=1
  batch_count+=1
  live_wall=time.monotonic()-start
  tmp=counts(st)
  tmp["temporary_current_session_elapsed_s"]=live_wall
  atomic(tmp,OUT/"summary.json")
  atomic(st)
  print("BATCH",st["completed_batches"],
    "workers",len(batch),"jobs",tmp["measured_jobs"],
    "terminal",tmp["terminal_boxes"],"pending",tmp["pending_UNEVALUATED_count"],
    "dec_area",tmp["area_decided_exact"],
    "tube_area",tmp["area_tube_evaluated_exact"],
    "elapsed_session",round(live_wall,2),flush=True)
 delta=time.monotonic()-start
 st["wall_elapsed_cumulative_s"]+=delta
 st["H_adaptive_wall_s"]+=delta
 st["session_receipts"].append({"elapsed_s":delta,
   "batches":batch_count,"workers":workers,
   "stop_reason":("COMPLETE" if not st["pending"] else
     "GLOBAL_24H" if st["wall_elapsed_cumulative_s"]>=WALL_CAP else
     "SESSION_BUDGET_OR_BATCH_LIMIT"),
   "remaining_jobs":len(st["pending"]),
   "max_batches_requested":max_batches})
 atomic(st)
 final=counts(st)
 atomic(final,OUT/"summary.json")
 print("SESSION_RESULT",json.dumps({k:final[k] for k in (
    "measured_jobs","decided_count","tube_candidate_EVALUATED_count",
    "pending_UNEVALUATED_count","area_decided_exact",
    "area_tube_evaluated_exact","area_pending_exact",
    "full_subregion_processed","total_wall_elapsed_sessions_s")},indent=2),flush=True)
 return final
def main():
 pa=argparse.ArgumentParser()
 pa.add_argument("--session-seconds",type=float,default=WALL_CAP)
 pa.add_argument("--max-batches",type=int)
 pa.add_argument("--workers",type=int,default=MAX_WORKERS)
 args=pa.parse_args()
 run_session(args.session_seconds,args.max_batches,args.workers)
if __name__=="__main__":main()
