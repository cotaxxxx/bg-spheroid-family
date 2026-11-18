"""Independent secondary pilot, pre-registered FIXED_CALIBRATION_V2.md.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No retroactive reinterpretation of coarse results.
"""
import argparse,json
from pathlib import Path
from flint import fmpq as Q
from . import c21_regular as H
CASES=("G2","G35","EQ","STRIP_08")
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--name",choices=CASES,required=True)
 p.add_argument("--output",required=True)
 a=p.parse_args()
 H.BU=16;H.BV=32;H.RATIO=Q(1,2)
 obj=H.run(a.name)
 obj["calibration_plan"]="FIXED_CALIBRATION_V2.md"
 obj["diagnostic_level"]="independent second mesh policy; no global assertion"
 Path(a.output).write_text(json.dumps(obj,indent=2)+"\n")
 print("CALIBRATION",a.name,obj["H_interval"]["halfwidth"],obj["wall_s"],flush=True)
if __name__=="__main__":main()
