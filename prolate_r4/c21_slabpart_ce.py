"""One CE MVT calibration, pre-frozen prior to the main 1024 boxes.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from __future__ import annotations
import argparse,json,resource,time
from pathlib import Path
from flint import fmpq as Q
from .c21_slabpart_mvt import calculate,STATUS
CE_R=(Q(0),Q(1,64))
CE_T=(Q(63,128),Q(65,128))
def main():
 a=argparse.ArgumentParser();a.add_argument("--output",required=True)
 opt=a.parse_args()
 print("DIAGNOSTIC_ONLY / NOT_EVIDENCE",flush=True)
 obj=calculate("CE",CE_R,CE_T)
 obj["purpose"]="pre-run MVT extended-box CE calibration ONLY"
 Path(opt.output).write_text(json.dumps(obj,indent=2)+"\n")
 print("CE_RESULT",obj["H_interval"],"wall_s",obj["wall_s"],flush=True)
if __name__=="__main__":main()
