"""Amendment B to V52 (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
V52A sampled only C1b's lambda range [9/20, 5/8]. This run samples the other phases of C-AXIS-V1 with the same 1-D axis
kernels and the same piece/bisection rules as V52A (cover()), on slabs of width 1/800 that avoid lambda_c ~ 0.40796,
lambda_x ~ 0.4378 and lambda_partial ~ 0.6435:
  [2/5, 321/800]          lambda < lambda_c : no root; E_zz < 0 on [0, 1/4], E_z < 0 on [1/4, 1] (pole trace included)
  [21/50, 337/800], [43/100, 345/800]  lambda_c < lambda < lambda_x : one root t_c < 1/2 (tube w0 = 1/16, t- >= 1/16)
  [63/100, 505/800], [16/25, 513/800]  lambda < lambda_partial in the band : root near t = 1, t+ clamped at 1
  [13/20, 521/800], [527/800, 33/50]   lambda > lambda_partial : no root; E_zz > 0 on [0, 1/16], E_z > 0 on [1/16, 1]
Rooted slabs: E_zz > 0 on [0, 1/16]; E_z > 0 on [1/16, t-]; E_zz < 0 on [t-, t+]; E_z < 0 on [t+, 1] or the pole trace.
Predictor: root of the 1-D mpmath reference at the slab midpoint (bisection on (0, 1)).
"""
import sys, json, multiprocessing as mp
from fractions import Fraction as F
import importlib.util
spec = importlib.util.spec_from_file_location("A", "plans/V52A_axis_amendment.py"); A = importlib.util.module_from_spec(spec); sys.modules["A"] = A; spec.loader.exec_module(A)  # launcher fix after run 1 (pickling error, nothing computed)
from geoenclosereader import reference as R

def root_any(lam):
    import numpy as np
    ts = [i/200 for i in range(1, 200)] + [0.999]; vals = [R.ez_axis_ref(lam, t) for t in ts]
    for (a, va), (b, vb) in zip(zip(ts, vals), zip(ts[1:], vals[1:])):
        if va > 0 >= vb:
            lo, hi = a, b
            for _ in range(40):
                m = (lo + hi)/2
                if R.ez_axis_ref(lam, m) > 0: lo = m
                else: hi = m
            return (lo + hi)/2
    return None

if __name__ == '__main__':
    out = sys.argv[1]; P = A.pieces; jobs = []; meta = []
    slabs = [("neg", F(2, 5)), ("root", F(21, 50)), ("root", F(43, 100)), ("root", F(63, 100)), ("root", F(16, 25)),
             ("pos", F(13, 20)), ("pos", F(527, 800))]
    for kind, l0 in slabs:
        l1 = l0 + F(1, 800); nm = "L%s" % str(l0).replace('/', '_')
        if kind == "neg":
            jobs += [(nm + ":a%d" % i, 'ezz', l0, l1, a, b, -1) for i, (a, b) in enumerate(P(F(0), F(1, 4), F(1, 64)))]
            jobs += [(nm + ":d%d" % i, 'ez', l0, l1, a, b, -1) for i, (a, b) in enumerate(P(F(1, 4), F(1), F(1, 32)))]
            jobs += [(nm + ":d_pole", 'ez', l0, l1, F(1), F(1), -1)]; meta.append({"slab": nm, "phase": kind})
        elif kind == "pos":
            jobs += [(nm + ":a", 'ezz', l0, l1, F(0), F(1, 16), +1)]
            jobs += [(nm + ":b%d" % i, 'ez', l0, l1, a, b, +1) for i, (a, b) in enumerate(P(F(1, 16), F(1), F(1, 32)))]
            jobs += [(nm + ":b_pole", 'ez', l0, l1, F(1), F(1), +1)]; meta.append({"slab": nm, "phase": kind})
        else:
            tc = root_any(float((l0 + l1)/2)); tcf = F(tc).limit_denominator(4096)
            tm = max(F(1, 16), tcf - F(1, 16)); tp = min(F(1), tcf + F(1, 16))
            meta.append({"slab": nm, "phase": kind, "t_c": tc, "t_minus": str(tm), "t_plus": str(tp)})
            jobs += [(nm + ":a", 'ezz', l0, l1, F(0), F(1, 16), +1)]
            if tm > F(1, 16): jobs += [(nm + ":b%d" % i, 'ez', l0, l1, a, b, +1) for i, (a, b) in enumerate(P(F(1, 16), tm, F(1, 32)))]
            jobs += [(nm + ":c%d" % i, 'ezz', l0, l1, a, b, -1) for i, (a, b) in enumerate(P(tm, tp, F(1, 64)))]
            if tp < 1: jobs += [(nm + ":d%d" % i, 'ez', l0, l1, a, b, -1) for i, (a, b) in enumerate(P(tp, F(1), F(1, 32)))]
            else: jobs += [(nm + ":d_pole", 'ez', l0, l1, F(1), F(1), -1)]
    with open(out, 'w') as f:
        for m in meta: f.write(json.dumps({"slab_meta": m}) + "\n")
        n = ok = 0
        with mp.Pool(2) as pool:
            for r in pool.imap(A.cover, jobs):
                n += 1; ok += r['confirmed']; f.write(json.dumps(r) + "\n"); f.flush(); print(r['leaf'], r['confirmed'], r['ladder'], r['extreme'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
