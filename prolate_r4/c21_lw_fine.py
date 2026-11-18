"""LW wide lambda fine calibration, fixed before run.
DIAGNOSTIC_ONLY / NOT_EVIDENCE, not part of earlier four-case calibration.
"""
import argparse,json
from pathlib import Path
from flint import fmpq as Q
from . import c21_regular as H
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 a=p.parse_args()
 H.BU=16;H.BV=32;H.RATIO=Q(1,2)
 obj=H.run("LW")
 obj["calibration_plan"]="FIXED_LW_CALIBRATION.md"
 Path(a.output).write_text(json.dumps(obj,indent=2)+"\n")
 print("LW_FINE",obj["H_interval"],"seconds",obj["wall_s"],flush=True)
if __name__=="__main__":main()
