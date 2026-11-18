"""Run FIXED representative-box matrix sequentially, 120 sec / box.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Individual subprocess measurements, no parallelism.
"""
import json,subprocess,sys,time
from pathlib import Path
from .c21_regular import BOXES as NORMAL
from .c21_special import SPECIAL
OUT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
NAMES=["G35","EQ","BD","LW"]+[f"STRIP_{k:02}" for k in range(1,16)]+["AX","STRIP_00"]
assert len(NAMES)==21
def run():
 OUT.mkdir(exist_ok=True,parents=True)
 seq=[]
 for name in NAMES:
  module="prolate_r4.c21_special" if name in SPECIAL else "prolate_r4.c21_regular"
  path=OUT/(name+".json");log=OUT/(name+".log")
  argv=[sys.executable,"-u","-m",module,"--name",name,"--output",str(path)]
  print("START",name,flush=True)
  started=time.monotonic()
  try:
   with log.open("wb") as f:
    p=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,timeout=120,check=False)
   if p.returncode!=0:
    raise RuntimeError("SUBPROCESS_EXIT_"+str(p.returncode))
   j=json.loads(path.read_text())
   row={"name":name,"state":"COMPLETED","halfwidth":j["H_interval"]["halfwidth"],
        "wall_s":j["wall_s"],"peak_RSS_KiB":j["peak_RSS_KiB"],
        "contains_zero_RECORD_ONLY":j["zero_included_RECORD_ONLY"]}
  except (subprocess.TimeoutExpired,RuntimeError,ValueError) as e:
   row={"name":name,"state":"OPEN","error":type(e).__name__+": "+str(e),
        "elapsed_outer_s":time.monotonic()-started}
   if path.exists():path.unlink()
   path.write_text(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
      "name":name,"state":"OPEN","error":row["error"],
      "uncomputed_H_interval":None})+"\n")
  seq.append(row)
  print("END",name,json.dumps(row),flush=True)
 (OUT/"batch_status.json").write_text(json.dumps(
    {"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","plan":"FIXED_PLAN.md",
     "results":seq},indent=2)+"\n")
if __name__=="__main__":run()
