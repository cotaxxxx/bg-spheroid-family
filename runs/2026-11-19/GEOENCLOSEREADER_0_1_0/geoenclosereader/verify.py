"""Re-enclose terminal leaves with GeoEncloseReader's own kernels.

A plan (JSON) is fixed before the run. Each test is (mode, action) -> (quantity, sign). For each selected
leaf, the reader tries the plan's grid ladder in the declared order; at each grid it bisects up to the
declared depth (score: d lambda, 4 d rho, 4 d z; boundary leaves bisect lambda only). A leaf is confirmed
iff every surviving child has the declared sign. Children whose lower-left corner (rho0^2 + z0^2 >= 1) is
outside the open ball are dropped, as in the producer's cover.
"""
import json, random, time
from fractions import Fraction
from . import kernels as K
from . import ledger as L

TESTS = {   # (mode, action): (name, kernel call, sign)
    ("V", "positive"): ("E_z", lambda b, g: K.ez_lower(b, g), +1, "ez"),
    ("Z", "positive"): ("E_zz", lambda b, g: K.chord_bound(b, 'z', 'lower', g), +1, "chord"),
    ("E", "H_positive"): ("H=E_yy", lambda b, g: K.chord_bound(b, 'y', 'lower', g), +1, "chord"),
    ("E", "radial_curvature_negative"): ("E_xx", lambda b, g: K.chord_bound(b, 'x', 'upper', g), -1, "chord"),
    ("B", "H_positive"): ("H_b", lambda b, g: K.hb_lower(b, g), +1, "hb"),
}
DEFAULT_LADDER = {"ez": ["v51b", "fine"], "chord": ["v50", "fine"], "hb": ["v50", "fine"]}


def bisect(b, lam_only=False):
    l0, l1, r0, r1, z0, z1 = b
    sc = [l1-l0, 0 if lam_only else 4*(r1-r0), 0 if lam_only else 4*(z1-z0)]; i = sc.index(max(sc))
    lo, hi = 2*i, 2*i+1; mid = (b[lo]+b[hi])//2; c1 = list(b); c2 = list(b); c1[hi] = mid; c2[lo] = mid
    return [tuple(c1), tuple(c2)]


def outside(b):
    return b[2]*b[2] + b[4]*b[4] >= 2**40


def verify_leaf(row, ladder=None, depth=6):
    name, f, sign, fam = TESTS[(row["mode"], row["action"])]
    ladder = ladder or DEFAULT_LADDER; t0 = time.monotonic(); tried = []
    for grid in ladder[fam]:
        todo = [(row["box"], 0)]; vals = []; ok = True; evals = 0
        while todo:
            b, d = todo.pop()
            if outside(b): continue
            v = f(b, grid); evals += 1
            if (v > 0) if sign > 0 else (v < 0): vals.append(float(v))
            elif d < depth: todo += [(c, d+1) for c in bisect(b, fam == "hb")]
            else: ok = False; vals.append(float(v)); break
        ext = (min(vals) if sign > 0 else max(vals)) if vals else None
        tried.append({"grid": grid, "confirmed": ok, "evals": evals, "extreme": ext})
        if ok: break
    return {"leaf": f"{row['file'].split('/')[-1]}:{row['path']}", "quantity": name, "sign": sign, "box": list(row["box"]),
            "producer_A": [None if row["alo"] is None else str(L.value(row["alo"])), None if row["ahi"] is None else str(L.value(row["ahi"]))], "confirmed": tried[-1]["confirmed"],
            "grid_used": tried[-1]["grid"], "attempts": tried, "seconds": round(time.monotonic()-t0, 1)}


def select(rows, plan):
    """plan['select']: {"<mode>:<action>": "all" | {"weakest": n, "random": n}}; seed plan['seed']."""
    rng = random.Random(plan.get("seed", 0)); out = []
    for key, how in plan["select"].items():
        mode, action = key.split(":")
        pool = [r for r in L.terminals(rows) if r["mode"] == mode and r["action"] == action]
        if how == "all": out += pool; continue
        sign = TESTS[(mode, action)][2]
        srt = sorted(pool, key=(lambda r: r["alo"]) if sign > 0 else (lambda r: -r["bhi"]))
        pick = srt[:how.get("weakest", 0)]; rest = [r for r in pool if r not in pick]
        pick += rng.sample(rest, min(how.get("random", 0), len(rest))); out += pick
    return out


def run_item(args):
    row, plan = args
    return verify_leaf(row, plan.get("ladder"), plan.get("depth", 6))
