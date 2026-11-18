"""Fixed 3-box AX / CE / BD pre-slab calibration.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Run this BEFORE adaptive slab coverage.
"""
import argparse,concurrent.futures,json,os,resource,subprocess,sys,time
from pathlib import Path
from flint import fmpq as Q
OUT=Path("runs/2026-11-18/D_PRO_C21_SLAB_ADAPTIVE")
CASE_LIMIT={"AX":600,"CE":600,"BD":300}
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def one(name):
 from . import c21_special as sp, c21_regular as re
 if name in ("AX","CE"):
  sp.BU=16;sp.BV=32;sp.RATIO=Q(1,2)
  result=sp.run(name)
 else:
  re.BU=16;re.BV=32;re.RATIO=Q(1,2)
  result=re.run("BD")
 result["scope"]="AX_CE_BD_precibration_only"
 result["calibration_plan"]="CALIBRATION_RULE_FREEZE.md"
 assert result["status"]==STATUS
 return result
def launch(name):
 started=time.monotonic();path=OUT/f"cal_{name}.json"
 log=OUT/f"cal_{name}.log"
 cmd=[sys.executable,"-u","-m","prolate_r4.slab_calibrate",
      "--one",name,"--output",str(path)]
 try:
  with log.open("wb") as f:
   p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,
                    timeout=CASE_LIMIT[name],check=False)
  if p.returncode:raise RuntimeError(f"exit={p.returncode}")
  doc=json.loads(path.read_text())
  result={"name":name,"status":"COMPLETED","wall_s":doc["wall_s"],
    "parent_wall_s":time.monotonic()-started,
    "H_interval":doc["H_interval"],"peak_RSS_KiB":doc["peak_RSS_KiB"],
    "mesh_cells":doc["mesh_cells"]}
 except (subprocess.TimeoutExpired,RuntimeError,ValueError,OSError) as ex:
  result={"name":name,"status":"OPEN",
    "stop_reason":type(ex).__name__+":"+str(ex)[:180],
    "parent_wall_s":time.monotonic()-started}
  if path.exists():path.unlink()
  path.write_text(json.dumps({"status":STATUS,"name":name,
     "calibration_status":"OPEN","H_interval":None,
     "reason":result["stop_reason"],
     "wall_s":result["parent_wall_s"]},indent=2)+"\n")
 return result
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--one",choices=CASE_LIMIT)
 parser.add_argument("--output")
 args=parser.parse_args()
 if args.one:
  if not args.output:parser.error("output needed")
  doc=one(args.one)
  Path(args.output).write_text(json.dumps(doc,indent=2)+"\n")
  print("CALIBRATED",args.one,doc["H_interval"],flush=True)
  return
 OUT.mkdir(parents=True,exist_ok=True)
 t0=time.monotonic()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  futs={pool.submit(launch,name):name for name in CASE_LIMIT}
  result=[f.result() for f in concurrent.futures.as_completed(futs)]
 result.sort(key=lambda x:list(CASE_LIMIT).index(x["name"]))
 record={"status":STATUS,"scope":"fixed preregistered AX CE BD before slab",
  "rule":"CALIBRATION_RULE_FREEZE.md","results":result,
  "total_parent_wall_s":time.monotonic()-t0,
  "no_slab_boxes_processed":True}
 (OUT/"calibration_status.json").write_text(json.dumps(record,indent=2)+"\n")
 print(json.dumps(record,indent=2))
if __name__=="__main__":main()
