"""Amendment V53-B (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Two sampled leaves were not confirmed in V53-A (tool resolution, not a sign seen):
  leaves/28H.tsv:x1101  lambda [0.875, 0.90625], rho [0.5, 0.75], z [0.75, 1]: a large box, most of it outside the ball;
                        v50 depth 6 / graded depth 3 / graded_fine depth 2 were too shallow. -> v50, depth 12.
  mixed/09H.tsv:x10101000110101 (X)  lambda ~ 0.036, rho [0.922, 0.9375], z [0.031, 0.047] (rim, small lambda).
                        -> graded, depth 7 (bisection in rho, z, lambda by the V53 score).
Same claim (H = E_yy > 0 on box ∩ ball, equivalent to E_rho > 0 where rho0 > 0), same drop rule for outside children.
"""
import sys, json, time, importlib.util
spec = importlib.util.spec_from_file_location("V53", "plans/V53_oblate_full_family.py"); P = importlib.util.module_from_spec(spec); sys.modules["V53"] = P; spec.loader.exec_module(P)
from geoenclosereader import kernels as K

def run(name, box, grid, depth):
    t0 = time.monotonic(); todo = [(tuple(box), 0)]; ok = True; ext = None; ev = 0; r = {"mode": "H"}
    while todo:
        b, d = todo.pop()
        if P.outside(b): continue
        v = K.chord_bound(b, 'y', 'lower', grid); ev += 1
        if v > 0: ext = float(v) if ext is None else min(ext, float(v))
        elif d < depth: todo += [(c, d + 1) for c in P.split(r, b)]
        else: ok = False; ext = float(v); break
    return {"leaf": name, "grid": grid, "depth": depth, "confirmed": ok, "evals": ev, "extreme": ext, "seconds": round(time.monotonic() - t0, 1)}

if __name__ == '__main__':
    out = sys.argv[1]
    jobs = [("leaves/28H.tsv:x1101", [917504, 950272, 524288, 786432, 786432, 1048576], "v50", 12),
            ("mixed/09H.tsv:x10101000110101", [37888, 38912, 966656, 983040, 32768, 49152], "graded", 7)]
    with open(out, "w") as f:
        for j in jobs:
            r = run(*j); f.write(json.dumps(r) + "\n"); f.flush(); print(json.dumps(r), flush=True)
