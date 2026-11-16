"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed width/time records; no sign decision."""
import argparse
import json
from pathlib import Path
from time import perf_counter_ns
from dataclasses import replace
from flint import fmpq as Q,ctx
from . import Config,angular_quotient
from .intervals import STATUS,bounds,midpoint

def measure(item,cfg):
    boxes=tuple(tuple(Q(v) for v in item[k]) for k in ("R","tau","lam"))
    start=perf_counter_ns()
    result=angular_quotient(*boxes,angle_kind="tau",config=cfg)
    box_ns=perf_counter_ns()-start
    start=perf_counter_ns()
    point=angular_quotient(*(midpoint(x) for x in boxes),angle_kind="tau",config=cfg)
    point_ns=perf_counter_ns()-start
    with ctx.workprec(cfg.precision):
        bl,bh=bounds(result.enclosure); pl,ph=bounds(point.enclosure)
    bw,pw=bh-bl,ph-pl
    return {"status":STATUS,"box_id":item["id"],"width":str(bw),
            "point_width":str(pw),"inflation_ratio":str(bw/pw) if pw else None,
            "box_time_ns":box_ns,"point_time_ns":point_ns,
            "box_cells":result.cells,"point_cells":point.cells,
            "route":result.route,"point_route":point.route}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pilot",action="store_true")
    ap.add_argument("--fixed27",action="store_true")
    ap.add_argument("--output-dir",default="prolate_r1/outputs")
    args=ap.parse_args()
    if not (args.pilot or args.fixed27): ap.error("select --pilot and/or --fixed27")
    root=Path(__file__).resolve().parent
    items=json.loads((root/"boxes.json").read_text())["boxes"]
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    if args.pilot:
        cfg=replace(Config(),order=2,base_u=2,base_v=4,distance_ratio=Q(2))
        row=measure(items[13],cfg)
        (out/"dig_pilot.json").write_text(json.dumps(row,indent=2)+"\n")
        print(json.dumps(row),flush=True)
    if args.fixed27:
        # Fixed order and coverage: NEVER skip or prioritize according to sign.
        target=out/"dig_fixed27.jsonl"
        with target.open("w") as fp:
            for item in items:
                row=measure(item,Config())
                fp.write(json.dumps(row)+"\n"); fp.flush()
                print(json.dumps(row),flush=True)

if __name__=="__main__": main()
