"""Run exactly four PRE-REGISTERED second-mesh calibrations.
DIAGNOSTIC_ONLY / NOT_EVIDENCE; per-process 240 second hard cap.
"""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
CASES=("G2","G35","EQ","STRIP_08")
def run():
 out=[]
 for case in CASES:
  path=ROOT/(case+"_cal_v2.json")
  log=ROOT/(case+"_cal_v2.log")
  cmd=[sys.executable,"-u","-m","prolate_r4.c21_calibration_v2",
       "--name",case,"--output",str(path)]
  print("START",case,flush=True)
  t=time.monotonic()
  try:
   with log.open("wb") as f:
    v=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=240)
   if v.returncode!=0:raise RuntimeError("exit="+str(v.returncode))
   j=json.loads(path.read_text())
   r={"name":case,"state":"COMPLETED",
      "halfwidth":j["H_interval"]["halfwidth"],"wall_s":j["wall_s"],
      "mesh_cells":j["mesh_cells"],"max_RSS":j["peak_RSS_KiB"]}
  except (subprocess.TimeoutExpired,RuntimeError,ValueError) as e:
   r={"name":case,"state":"OPEN","cause":str(e),
      "wall_outer_s":time.monotonic()-t}
   if path.exists():path.unlink()
   path.write_text(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
    "name":case,"calibration":"v2","state":"OPEN","error":r["cause"],
    "H_interval":None})+"\n")
  out.append(r);print("END",case,json.dumps(r),flush=True)
 (ROOT/"calibration_v2_status.json").write_text(json.dumps(
   {"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
    "fixed_plan":"FIXED_CALIBRATION_V2.md","results":out},indent=2)+"\n")
if __name__=="__main__":run()
