#!/usr/bin/env python3
"""TAILAX_V1 ledger checker. Rerun from saved JSON, no numerical integration."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
ROOT=Path(__file__).resolve().parent
PS="0fb1fbf4e1cfbd77bfb860cb5825217fcc1b7b0975011e978908e1f628cbea86"
MS="9373ac07c721c99b1ffa2b683d9f560e4fb1cea0dad124054b8eb14ef8cfa7f8"
assert hashlib.sha256((ROOT/"PLAN_TAIL_AXIS_BEFORE_RUN.md").read_bytes()).hexdigest()==PS
assert hashlib.sha256((ROOT/"MATH_DERIVATION_BEFORE_PROBE.md").read_bytes()).hexdigest()==MS
d=json.loads((ROOT/"PILOT_RESULT.json").read_text())
assert d["plan_sha256"]==PS and d["arb_bits"]==192 and d["phi_cells"]==256
assert d["t_nodes"]==[8,16,32,64] and d["N"]==20
assert d["type"]=="EPSILON_ZERO_INNER_KERNEL_ONLY_NOT_A_GLOBAL_H_BOUND"
assert len(d["axis_symmetry"])==2
for rec in d["axis_symmetry"]:
    assert all(rec["checks"].values())
rows=[]
for t,x in zip([8,16,32,64],d["measurements"]):
    assert x["t"]==t and x["status"]=="COMPLETE"
    saved=json.loads((ROOT/("PILOT_T%03d.json"%t)).read_text())
    assert saved==x
    def iv(key):
        r=x[key];lo=F(r["lower"]);hi=F(r["upper"])
        assert lo<=hi
        return lo,hi
    kl,kh=iv("Kbar_interval")
    rl,rh=iv("rbar_factored_interval")
    il,ih=iv("rbar_indirect_interval")
    sl,sh=iv("mean_subtractor_interval")
    tl,th=iv("t_times_Kbar")
    ql,qh=iv("t_squared_times_rbar")
    assert il<=rh and ih>=rl, "factored vs indirect intervals disjoint"
    assert il<=kh+sh and ih>=kl+sl, "indirect interval excludes sum"
    assert tl<=t*kl and th>=t*kh
    assert ql<=t*t*rl and qh>=t*t*rh
    minraw=F(0) if kl<=0<=kh else min(abs(kl),abs(kh))
    maxres=max(abs(rl),abs(rh))
    assert bool(rl<=0<=rh)==x["rbar_contains_zero"]
    assert bool(maxres<minraw)==x["residual_abs_max_below_raw_abs_min"]
    assert str(minraw)==x["raw_abs_min_exact"]
    assert str(maxres)==x["residual_abs_max_exact"]
    assert x["wall_seconds"]>=0
    rows.append({"t":t,"Kbar":[float(kl),float(kh)],"rbar":[float(rl),float(rh)],
        "t_squared_rbar":[float(t*t*rl),float(t*t*rh)],
        "rbar_contains_zero":x["rbar_contains_zero"],
        "abs_residual_below_abs_raw":x["residual_abs_max_below_raw_abs_min"],
        "residual_over_raw_worst_case":float(maxres/minraw) if minraw>0 else None,
        "wall_s":x["wall_seconds"]})
out={"classification":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","plan_sha256":PS,
    "math_pre_run_sha256":MS,"status":"RECORD_FORMAT_CHECKS_ONLY",
    "scope":"epsilon_zero_inner_kernel_at_rho=1/2,z=0",
    "all_four_records_internally_consistent":True,
    "axis_rational_symmetry_checks":d["axis_symmetry"],
    "measurements":rows}
(ROOT/"CHECK_RESULT.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(out,indent=2))
