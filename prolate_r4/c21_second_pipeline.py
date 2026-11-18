"""Single-entry resumable C21 second-order staged diagnostic.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Stage B is strictly gated by all 8 boxes.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from . import c21_second_stage_a as stage_a
from . import c21_second_cover as stage_b
from . import c21_second_verify as verifier
from . import c21_second_w as w
from . import c21_second_receipt as receipt
from . import c21_second_pack as pack
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
OUT=Path("runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER")
def main():
 pa=argparse.ArgumentParser()
 pa.add_argument("--session-seconds",type=float,default=86400.0)
 pa.add_argument("--workers",type=int,default=12)
 pa.add_argument("--max-batches",type=int)
 args=pa.parse_args()
 assert 0<args.session_seconds<=86400
 assert 1<=args.workers<=12
 print(STATUS,flush=True)
 try:
  if not (OUT/"STAGE_A_GATE.json").exists():
   stage_a.perform()
  gate=json.loads((OUT/"STAGE_A_GATE.json").read_text())
  if gate["stage_B_gate"]!="STAGE_B_ALLOWED":
   print("STAGE_B_NOT_LAUNCHED_GATE",gate["stage_B_gate"],flush=True)
  else:
   summary=stage_b.run_session(args.session_seconds,args.max_batches,args.workers)
   print("STAGE_B_PARTIAL_OR_COMPLETE",summary["full_subregion_processed"],
     "measured",summary["measured_jobs"],flush=True)
   verifier.verify()
   if summary["full_subregion_processed"] or (
        summary["total_experiment_wall_s_including_calibration"]>=86400):
    subprocess.run([sys.executable,"-m","prolate_r4.c21_second_w"],check=True)
 finally:
  receipt.build()
  pack.run()
if __name__=="__main__":main()
