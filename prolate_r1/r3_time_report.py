"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Geometry counts and timing extrapolation only."""
import argparse
import json
from pathlib import Path
from flint import fmpq as Q, ctx, arb
from . import Config
from .intervals import STATUS, midpoint
from .quadrature import make_mesh
from .tests.resumable import atomic_json,read_json

def observations(report):
    return [a["detail"] for row in report["tests"] for a in row["attempts"]
            if a.get("detail",{}).get("evaluation_ns") is not None]

def create_report(pilot):
    samples=observations(pilot)
    p=next(x for x in samples if x["name"]=="W_point_(5, 1/2, 1/2)")
    b=next(x for x in samples if x["name"]=="W_box_2")
    root=Path(__file__).resolve().parent
    boxes=json.loads((root/"boxes.json").read_text())["boxes"]
    cfg=Config(); rows=[]; cache={}
    def cells(R,L):
        key=(R,L)
        if key not in cache:
            kap=cfg.kappa if R[1]>=cfg.cap_from else Q(0)
            cache[key]=len(make_mesh(R,kap,cfg,lam=L))
        return cache[key]
    with ctx.workprec(cfg.precision):
        for item in boxes:
            R,T,L=(tuple(Q(v) for v in item[k]) for k in ("R","tau","lam"))
            # Each fixed box lies in one chart and outside the center route.
            nc=cells(R,L); np=cells((midpoint(R),)*2,(midpoint(L),)*2)
            rows.append({"id":item["id"],"box_cells":nc,"point_cells":np,
                         "point_integral_executed":False,"box_integral_executed":False})
    box_rate=Q(b["evaluation_ns"],b["result"]["cells"])
    point_rate=Q(p["evaluation_ns"],p["result"]["cells"])
    box_ns=sum(x["box_cells"] for x in rows)*box_rate
    point_ns=sum(x["point_cells"] for x in rows)*point_rate
    total=box_ns+point_ns
    return {"status":STATUS,"method":"cell-count extrapolation; not a timing bound",
            "config":repr(cfg),"samples":samples,"geometry":rows,
            "box_only_seconds":str(box_ns/1000000000),
            "point_only_seconds":str(point_ns/1000000000),
            "fixed27_box_plus_point_seconds":str(total/1000000000),
            "fixed27_serial_hours_decimal":arb(total/Q(3600000000000)).str(8),
            "ideal_12_workers_hours_decimal":arb(total/Q(43200000000000)).str(8),
            "limitations":["Point sample is middle chart; endpoint point costs differ.",
                "Box sample is equator chart; other charts and lambda vary.",
                "Codex host is not the Ryzen 9 9900X; host speed is not calibrated.",
                "Twelve-worker division is ideal arithmetic, not measured speedup.",
                "No full27 or center remainder integral was executed here."]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pilot")
    ap.add_argument("--out",default="prolate_r1/outputs/R3_TIME_ESTIMATE.json")
    args=ap.parse_args()
    report=create_report(read_json(args.pilot)); atomic_json(args.out,report)
    print(json.dumps({k:v for k,v in report.items() if k not in ("samples","geometry")},indent=2))

if __name__=="__main__": main()
