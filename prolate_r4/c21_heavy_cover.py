"""Full R-tau 64x64 adaptive heavy slab H survey, restartable.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Only H-interval zero controls splits.
"""
from __future__ import annotations
import argparse,collections,concurrent.futures,json,os,re,subprocess,sys,time
from fractions import Fraction as F
from pathlib import Path
from flint import fmpq as Q
from .c21_heavy_box import route,L,STATUS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB"
STATE=OUT/"STATE.json"
WALL_CAP=129600.0;BOX_CAP=1200.0;WORKERS=12
MIN=F(1,256);PLATE=["79/16","5"]
PRIME=((0,0),(0,63),(63,0),(63,63),(16,0),(16,63),
       (32,32),(63,32),(32,63),(0,32),(1,1),(62,62))
def q(x):return F(str(x))
def area(n):return (q(n["R"][1])-q(n["R"][0]))*(q(n["tau"][1])-q(n["tau"][0]))
def route_of(n):
 return route(tuple(Q(v) for v in n["R"]),tuple(Q(v) for v in n["tau"]))
def morton(i,j):
 return sum(((i>>b)&1)<<(2*b) | ((j>>b)&1)<<(2*b+1) for b in range(6))
def initial():
 grid=[(i,j) for i in range(64) for j in range(64)]
 ids=list(PRIME)+sorted((p for p in grid if p not in PRIME),
                          key=lambda p:(morton(*p),p))
 assert len(ids)==4096 and len(set(ids))==4096
 nodes=[]
 for rank,(i,j) in enumerate(ids):
  name=f"R{i:02d}_T{j:02d}"
  nodes.append({"id":name,"root":name,"rank":rank,"depth":0,
    "R":[str(F(i,64)),str(F(i+1,64))],
    "tau":[str(F(j,64)),str(F(j+1,64))],
    "parent":None})
 assert sum((area(x) for x in nodes),F(0))==1
 return nodes
def frozen_registry():
 return {"status":STATUS,"initial_count":4096,
   "plate":PLATE,"root_order":"first12 geometry then six-bit interleaved Morton",
   "route_precedence":["AXIS_MVT","CENTER_MVT","BOUNDARY_COLLAR","GENERAL"],
   "max_workers":WORKERS,"global_wall_cap_seconds":WALL_CAP,
   "per_box_cap_seconds":BOX_CAP,"min_edge":"1/256",
   "point_grad_mesh":{"base_u":16,"base_v":32,"ratio":"1/2","order":4},
   "Hessian_mesh":{"base_u":8,"base_v":16,"ratio":"1","order":4},
   "boundary_kappa":"1/4096","tau_and_R_geometry_inclusive":True,
   "sampling_W":"sorted evaluated tubes first/middle/last only at completed slab or genuine 36h cap",
   "sign_only_for_frozen_zero_split":True,
   "roots":[{**x,"route":route_of(x)} for x in initial()]}
def atomic(obj,path):
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+".tmp")
 with tmp.open("w") as f:
  json.dump(obj,f,indent=2)
  f.write("\n");f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
def make_registry():
 reg=frozen_registry()
 p=OUT/"REGISTRY.json"
 if p.exists():assert json.loads(p.read_text())==reg,"FROZEN_REGISTRY_CHANGED"
 else:atomic(reg,p)
 return reg
def make_state():
 reg=make_registry()
 return {"status":STATUS,"schema":"heavy_slab_v1",
   "plate":PLATE,"freeze_file":"PRE_RUN_FREEZE.md",
   "workers":WORKERS,"global_36h_cap_s":WALL_CAP,
   "pending":[{k:v for k,v in x.items() if k!="route"} for x in reg["roots"]],
   "inflight":[],"terminal":[],"splits":[],"processed":[],
   "completed_batches":0,"wall_elapsed_cumulative_s":0.,
   "W_wall_s":0.,"sessions":[],"no_cover_certification":True}
def priority(n):return (n["depth"],n["rank"],n["id"])
def readstate():
 if not STATE.exists():
  st=make_state();atomic(st,STATE);return st
 make_registry()
 st=json.loads(STATE.read_text())
 assert st["schema"]=="heavy_slab_v1" and st["plate"]==PLATE
 if st["inflight"]:
  have={x["id"] for x in st["pending"]}
  recovered=0
  for n in st["inflight"]:
   if n["id"] not in have:
    st["pending"].append(n);recovered+=1
  st["inflight"]=[]
  st["pending"].sort(key=priority)
  st.setdefault("recovery_events",[]).append({"requeued_after_crash":recovered,
     "reason":"incomplete inflight may need replay; previous logs not counted"})
  atomic(st,STATE)
 return st
def split(n):
 R=tuple(q(x) for x in n["R"]);T=tuple(q(x) for x in n["tau"])
 edgeR=R[1]-R[0];edgeT=T[1]-T[0]
 ax="R" if edgeR>=edgeT else "tau"
 rng=R if ax=="R" else T
 mid=(rng[0]+rng[1])/2
 children=[]
 for j,(lo,hi) in enumerate(((rng[0],mid),(mid,rng[1]))):
  child={**n,"id":n["id"]+f".{ax}{j}","parent":n["id"],
         "depth":n["depth"]+1,ax:[str(lo),str(hi)]}
  children.append(child)
 assert sum((area(x) for x in children),F(0))==area(n)
 return children,ax
def max_rss(pid):
 try:
  for line in Path(f"/proc/{pid}/status").read_text().splitlines():
   if line.startswith("VmHWM:"):return int(line.split()[1])
 except (OSError,ValueError):pass
 return 0
def worker(n,available):
 name=n["id"]
 rt=route_of(n)
 log=OUT/"logs"/(name+".log")
 target=OUT/"boxes"/(name+".json")
 log.parent.mkdir(parents=True,exist_ok=True)
 target.parent.mkdir(parents=True,exist_ok=True)
 limit=min(BOX_CAP,max(1.,available-2.))
 is_session_cap=limit<BOX_CAP-1e-5
 command=[sys.executable,"-u","-m","prolate_r4.c21_heavy_box",
   "--id",name,"--R",*n["R"],"--tau",*n["tau"],
   "--output",str(target)]
 t0=time.monotonic();peak=0;cause=None
 with log.open("wb") as f:
  proc=subprocess.Popen(command,stdout=f,stderr=subprocess.STDOUT,cwd=str(ROOT))
  try:
   while proc.poll() is None:
    peak=max(peak,max_rss(proc.pid))
    if time.monotonic()-t0>=limit:
     cause="SESSION_INTERRUPTED" if is_session_cap else "PER_BOX_1200S_TIMEOUT"
     proc.kill();proc.wait(timeout=6);break
    time.sleep(.25)
  finally:
   if proc.poll() is None:proc.kill();proc.wait(timeout=6)
 elapsed=time.monotonic()-t0
 if cause is None and proc.returncode!=0:
  cause=f"PROCESS_EXIT_{proc.returncode}"
 if cause is None:
  try:
   d=json.loads(target.read_text())
   assert d["status"]==STATUS and d["id"]==name
   assert d["input_box"]["R"]==n["R"] and d["input_box"]["tau"]==n["tau"]
   assert d["input_box"]["lambda"]==PLATE and d["route_from_position"]==rt
   l=q(d["H_interval"]["lower"]);h=q(d["H_interval"]["upper"])
   assert l<=h
   return {"node":n,"route":rt,"status":"EVALUATED",
    "elapsed_s":elapsed,"H_interval":d["H_interval"],
    "zero_contains":l<=0<=h,
    "source_json":str(target.relative_to(OUT)),
    "source_log":str(log.relative_to(OUT)),
    "RSS_KiB":d["peak_RSS_KiB"],
    "base_cells":d["base_mesh"]["cells"],
    "hess_cells":d["hessian_mesh"]["cells"]}
  except (ValueError,OSError,KeyError,AssertionError,TypeError) as e:
   cause="INVALID_BOX_RESULT:"+type(e).__name__+":"+str(e)[:150]
 if target.exists():target.unlink()
 if cause=="SESSION_INTERRUPTED":
  return {"node":n,"route":rt,"status":"PENDING_INTERRUPTED",
    "elapsed_s":elapsed,"cause":cause,
    "source_log":str(log.relative_to(OUT)),
    "sampled_peak_KiB":peak}
 raw=log.read_text(errors="replace")
 mesh=re.search(r"MESH\s+\S+\s+route\s+\S+\s+base\s+(\d+)\s+hess\s+(\d+)",raw)
 reason=(cause or "UNKNOWN_ERROR")
 if cause and cause.startswith("PROCESS_EXIT"):
  # Preserve error reason from full traceback for diagnosis.
  reason+="; last_lines="+repr(raw.splitlines()[-5:])[:700]
 err={"status":STATUS,"id":name,"route":rt,
      "input_box":{"R":n["R"],"tau":n["tau"],"lambda":PLATE},
      "H_interval":None,"reason":reason,
      "mesh_cells_observed":({"base":int(mesh.group(1)),
        "hessian":int(mesh.group(2))} if mesh else None),
      "peak_RSS_KiB_sampled_lower":peak,"worker_seconds":elapsed,
      "is_cover":False}
 atomic(err,target)
 return {"node":n,"route":rt,"status":"OPEN",
   "elapsed_s":elapsed,"cause":reason,
   "source_json":str(target.relative_to(OUT)),
   "source_log":str(log.relative_to(OUT)),
   "sampled_peak_KiB":peak}
def settle(st,item):
 n=item["node"];rt=item["route"];status=item["status"]
 if status=="PENDING_INTERRUPTED":
  st["pending"].append(n)
  st.setdefault("interrupted_attempts",[]).append({
   "id":n["id"],"wall_s":item["elapsed_s"],"route":rt})
  return
 st["processed"].append({"id":n["id"],"route":rt,
  "depth":n["depth"],"status":status,"wall_s":item["elapsed_s"],
  "R":n["R"],"tau":n["tau"],"area":str(area(n))})
 if status=="OPEN":
  st["terminal"].append({"node":n,"kind":"TUBE_OPEN_ERROR",
     "reason":item["cause"],"route":rt,"source_json":item["source_json"],
     "source_log":item["source_log"],"worker_wall_s":item["elapsed_s"]})
  return
 if not item["zero_contains"]:
  typ="DECIDED_NONZERO"
 elif q(n["R"][1])-q(n["R"][0])<=MIN and q(n["tau"][1])-q(n["tau"][0])<=MIN:
  typ="TUBE_MIN"
 else:
  kids,axis=split(n)
  st["pending"].extend(kids)
  st["splits"].append({"id":n["id"],"depth":n["depth"],
     "route":rt,"axis":axis,"area":str(area(n)),
     "children":[c["id"] for c in kids],
     "zero_membership_record":True})
  return
 st["terminal"].append({"node":n,"kind":typ,"route":rt,
   "source_json":item["source_json"],"source_log":item["source_log"],
   "H_interval":item["H_interval"],
   "worker_wall_s":item["elapsed_s"],
   "base_cells":item["base_cells"],"hessian_cells":item["hess_cells"],
   "RSS_KiB":item["RSS_KiB"]})
def counts(st):
 decided=[x for x in st["terminal"] if x["kind"]=="DECIDED_NONZERO"]
 tube=[x for x in st["terminal"] if x["kind"]!="DECIDED_NONZERO"]
 todo=st["pending"]+st["inflight"]
 aD=sum((area(x["node"]) for x in decided),F(0))
 aT=sum((area(x["node"]) for x in tube),F(0))
 aP=sum((area(x) for x in todo),F(0))
 assert aD+aT+aP==F(1),("AREA_FAIL",aD,aT,aP)
 assert len({x["node"]["id"] for x in st["terminal"]})==len(st["terminal"])
 assert len({x["id"] for x in todo})==len(todo)
 assert not {x["node"]["id"] for x in st["terminal"]}.intersection(
   {x["id"] for x in todo})
 rdc=collections.Counter((p["route"],p["depth"]) for p in st["processed"])
 rdt=collections.defaultdict(float)
 for p in st["processed"]:rdt[f"{p['route']}|depth{p['depth']}"]+=p["wall_s"]
 bydepth=collections.Counter(str(x["depth"]) for x in st["processed"])
 splits=collections.Counter(str(s["depth"]) for s in st["splits"])
 tubes=sorted(tube,key=lambda x:x["node"]["id"])
 return {"status":STATUS,"plate_lambda":PLATE,
 "full_initial_roots":4096,"initial_root_count":len(st["pending"]) if not st["processed"] else 4096,
 "evaluated_complete_nodes":sum(p["status"]=="EVALUATED" for p in st["processed"]),
 "failed_OPEN_nodes":sum(p["status"]=="OPEN" for p in st["processed"]),
 "attempted_terminal_or_split_nodes":len(st["processed"]),
 "split_parent_count":len(st["splits"]),
 "observed_split_fraction_of_completed_evaluated":
   (len(st["splits"])/sum(p["status"]=="EVALUATED" for p in st["processed"])
    if any(p["status"]=="EVALUATED" for p in st["processed"]) else None),
 "decided_count":len(decided),"tube_evaluated_count":len(tube),
 "tube_by_kind":dict(collections.Counter(x["kind"] for x in tube)),
 "pending_unprocessed_count":len(todo),
 "decided_area_exact":str(aD),"tube_area_exact":str(aT),
 "pending_area_exact":str(aP),"area_total_exact":str(aD+aT+aP),
 "area_partition_valid":True,"full_plate_done":not todo,
 "route_depth_processed":{f"{r}|depth{d}":c for (r,d),c in rdc.items()},
 "route_depth_worker_seconds":dict(rdt),
 "depth_processed":dict(bydepth),"depth_split":dict(splits),
 "elapsed_wall_cumulative_s":st["wall_elapsed_cumulative_s"],
 "H_worker_seconds":sum(p["wall_s"] for p in st["processed"])+
   sum(p["wall_s"] for p in st.get("interrupted_attempts",[])),
 "tubes_coordinates":[{"id":x["node"]["id"],
   "R":x["node"]["R"],"tau":x["node"]["tau"],
   "depth":x["node"]["depth"],"kind":x["kind"],
   "area":str(area(x["node"]))} for x in tubes],
 "unfinished_coordinates":[{"id":x["id"],"R":x["R"],
   "tau":x["tau"],"area":str(area(x))} for x in sorted(todo,key=priority)],
 "global_cost_estimate":"NOT_ESTIMABLE_FROM_PARTIAL_SLAB" if todo
  else "REQUIRES_SEPARATE_LAMBDA_THICKNESS_HYPOTHESES",
 "W_status":"DEFERRED_UNTIL_FULL_PLATE_OR_GENUINE_36H_CAP",
 "never_a_mathematical_certificate":True}
def run_session(session_s=800,max_batches=None):
 assert 0<session_s<=WALL_CAP
 st=readstate()
 t0=time.monotonic()
 batches=0
 while st["pending"] and (max_batches is None or batches<max_batches):
  elapsed=time.monotonic()-t0
  time_left=min(float(session_s)-elapsed,
          WALL_CAP-st["wall_elapsed_cumulative_s"]-elapsed)
  if time_left<20:break
  st["pending"].sort(key=priority)
  batch=st["pending"][:WORKERS]
  st["pending"]=st["pending"][len(batch):]
  st["inflight"]=batch
  atomic(st,STATE)
  with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
   outputs=list(pool.map(lambda n:worker(n,time_left),batch))
  for item in outputs:settle(st,item)
  st["inflight"]=[]
  st["pending"].sort(key=priority)
  st["completed_batches"]+=1;batches+=1
  provisional=counts(st)
  atomic(st,STATE)
  atomic(provisional,OUT/"SUMMARY.json")
  print("BATCH",st["completed_batches"],"processed",provisional["attempted_terminal_or_split_nodes"],
     "decided",provisional["decided_count"],
     "tube",provisional["tube_evaluated_count"],
     "pending",provisional["pending_unprocessed_count"],
     "wall_s",round(time.monotonic()-t0,2),flush=True)
 delta=time.monotonic()-t0
 st["wall_elapsed_cumulative_s"]+=delta
 st["sessions"].append({"session_elapsed_s":delta,"completed_batches":batches,
   "max_batches_requested":max_batches,"session_budget_s":session_s,
   "reason":("FULL_PLATE" if not st["pending"] else
      "ACTUAL_36H_CAP" if st["wall_elapsed_cumulative_s"]>=WALL_CAP else
      "SHORT_SESSION_CHECKPOINT"),
   "pending_count":len(st["pending"])})
 atomic(st,STATE)
 report=counts(st)
 atomic(report,OUT/"SUMMARY.json")
 print("SESSION_SUMMARY",json.dumps({k:report[k] for k in (
  "attempted_terminal_or_split_nodes","decided_count","tube_evaluated_count",
  "pending_unprocessed_count","decided_area_exact","tube_area_exact",
  "pending_area_exact","area_total_exact","full_plate_done",
  "elapsed_wall_cumulative_s")},indent=2),flush=True)
 return report
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--make-registry",action="store_true")
 p.add_argument("--session-seconds",type=float,default=800.)
 p.add_argument("--max-batches",type=int)
 a=p.parse_args()
 if a.make_registry:
  r=make_registry()
  print(STATUS,"FROZEN_ROOTS",len(r["roots"]),"area1",
        sum(area(x) for x in r["roots"])==1,
        "counts",dict(collections.Counter(x["route"] for x in r["roots"])))
  return
 run_session(a.session_seconds,a.max_batches)
if __name__=="__main__":main()
