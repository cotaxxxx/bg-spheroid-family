"""Amendment V55-A2 (fixed before run): g1(13/16) > 0 was not reached at (4096, 512) (lower -0.00059; value ~0.007).
Same kernel as V55-A, finer cells only for r = 13/16: (N_MU, N_PHI) = (4096, 2048), then (8192, 2048)."""
import sys, json, time, importlib.util
spec = importlib.util.spec_from_file_location("A", "plans/V55A_g1_bracket.py"); A = importlib.util.module_from_spec(spec); sys.modules["A"] = A; spec.loader.exec_module(A)
from flint import fmpq
t0 = time.monotonic()
for NM, NP in [(4096, 2048), (8192, 2048)]:
    v = A.g1_bound(fmpq(13, 16), 'lower', NM, NP); r = {"check": "g1 sign", "r": "13/16", "grid": [NM, NP], "lower": float(v), "confirmed": bool(v > 0), "seconds": round(time.monotonic() - t0, 1)}
    print(json.dumps(r), flush=True); open(sys.argv[1], 'a').write(json.dumps(r) + "\n")
    if v > 0: break
