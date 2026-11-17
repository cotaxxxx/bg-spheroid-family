"""Fixed Method B direct-W diagnostic, WITHOUT changing R3 original modules.

Route only: R3 density.evaluate(mode='W') over box tau>0, tau<1.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import argparse
import json
import os
import platform
import sys
import time
import flint
from pathlib import Path

from flint import arb, fmpq as Q, ctx
from prolate_r1 import Config
from prolate_r1.api import cb_for, deriv_integral, domain_for, W_cap
from prolate_r1.intervals import (ball, bounds, midpoint, radius,
                                  sym, serial, Result, STATUS)
from prolate_r1.quadrature import make_mesh, integrate

RANGE_BOX = ((Q(95,128), Q(97,128)),
             (Q(15,128), Q(17,128)),
             (Q(1279,256), Q(5)))
POINT = tuple((lo+hi)/2 for lo,hi in RANGE_BOX)
LIMIT = {"point": Q(1,20), "box": Q(3,10)}

def rational_mid(tup):
    return tuple((a+b)/2 for a,b in tup)

def run(case, outdir):
    started=time.monotonic_ns()
    cfg=Config()
    assert cfg.precision==128 and cfg.order==6
    assert cfg.base_u==32 and cfg.base_v==64
    assert cfg.distance_ratio==Q(1,4)
    boxes=tuple((x,x) for x in POINT) if case=="point" else RANGE_BOX
    R,T,L=boxes
    assert R[0]>0 and T[0]>0 and T[1]<1 and L[0]>=2
    # Proven fmpq geometric lower bound on R^2 sin(beta) cos(beta).
    denominator_lower=R[0]**2 * (2*T[0]*(1-T[1]**2)/(1+T[1]**2)**2)
    assert denominator_lower>0
    print("CASE",case,"START",flush=True)
    print("DENOMINATOR_LOWER",str(denominator_lower),flush=True)
    detail={"status":STATUS,"route":"R3_existing_middle_direct_W_no_endpoint_Taylor",
       "base_commit":"fdfb498f2117cc0c5d72e88cc3be05eac9727bd8",
       "case":case,"input_boxes":repr(boxes),
       "physical_midpoint":repr(POINT),
       "denominator_lower":str(denominator_lower),
       "config":repr(cfg),"python":sys.version,
       "flint_version":flint.__version__,"platform":platform.platform(),
       "environment":{k:os.environ.get(k) for k in
          ("PYTHONHASHSEED","OMP_NUM_THREADS","OPENBLAS_NUM_THREADS")}}
    with ctx.workprec(cfg.precision):
        dom=domain_for(R,L,cfg)
        assert dom.kappa==0, "box2 expected kappa=0"
        t=time.monotonic_ns()
        mesh=make_mesh(R,dom.kappa,cfg,lam=L)
        detail["mesh_ns"]=time.monotonic_ns()-t
        detail["mesh_cells"]=len(mesh)
        print("MESH_CELLS",len(mesh),"TIME_SEC",round(detail["mesh_ns"]/1e9,4),flush=True)
        t=time.monotonic_ns()
        p0=tuple(arb(midpoint(x)) for x in boxes)
        point_result=integrate(cb_for(p0,dom,"W"),mesh,cfg.order)[0]
        detail["point_evaluation_ns"]=time.monotonic_ns()-t
        detail["point_interval"]=serial(point_result)
        print("POINT_RESULT",point_result, "TIME_SEC",
              round(detail["point_evaluation_ns"]/1e9,4),flush=True)
        accum=arb(0)
        derivative_details={}
        for idx,name in enumerate(("R","x","lam")):
            h=radius(boxes[idx])
            if not h: continue
            t=time.monotonic_ns()
            params=tuple(ball(x) for x in boxes)
            derivative=deriv_integral(params,dom,mesh,"W",(name,),(1,))[0]
            component=derivative*sym(h)
            accum+=component
            derivative_details[name]={"derivative_integral":serial(derivative),
                                     "parameter_half_width":str(h),
                                     "correction":serial(component),
                                     "elapsed_ns":time.monotonic_ns()-t}
            print("CORRECTION",name,"HALF",str(h),
                   "TERM",component,
                   "TIME_SEC",round(derivative_details[name]["elapsed_ns"]/1e9,4),
                   flush=True)
        cap=W_cap(R,dom.kappa)
        result=Result((point_result+accum+cap,),(point_result,),
                    (accum,),(cap,),len(mesh),
                    "method_B_directW_same_R3_kernel",{"source":"R3"})
        low,hi=bounds(result.enclosure)
        half=(hi-low)/2
        detail["result"]=result.to_json()
        detail["derivative_components"]=derivative_details
        detail["total_ns"]=time.monotonic_ns()-started
        detail["half_width"]=str(half)
        detail["half_width_decimal"]=str(arb(half))
        detail["threshold"]=str(LIMIT[case])
        detail["width_result"]="PASS" if half<=LIMIT[case] else "FAIL"
        detail["mathematical_certification"]=False
    output=outdir/(case+".json")
    tmp=output.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(detail,indent=2,ensure_ascii=False)+"\n")
    os.replace(tmp,output)
    print("FINISHED",case, "WIDTH",str(half),"THRESHOLD",str(LIMIT[case]),
          "RESULT",detail["width_result"],
          "TOTAL_SECONDS",round(detail["total_ns"]/1e9,3),
          "EVIDENCE",output,flush=True)
    return 0 if detail["width_result"]=="PASS" else 1

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--case",choices=["point","box"],required=True)
    p.add_argument("--output-dir",required=True)
    args=p.parse_args()
    outdir=Path(args.output_dir)
    outdir.mkdir(parents=True,exist_ok=True)
    raise SystemExit(run(args.case,outdir))

if __name__=="__main__":
    main()
