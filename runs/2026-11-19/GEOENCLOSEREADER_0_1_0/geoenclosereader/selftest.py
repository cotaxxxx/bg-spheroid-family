"""Quick regression against values audited in V51 (about 1-2 minutes on one core)."""
import time
import mpmath as mp
from . import kernels as K, reference as R, verify as V, ledger as L

U = 2**20


def _box(l, r, z):
    return tuple(int(round(x*U)) for x in (l, l, r, r, z, z))


def run():
    ok = True; t0 = time.monotonic()
    def report(name, cond, info):
        nonlocal ok; ok &= bool(cond); print(("ok  " if cond else "FAIL"), name, info, flush=True)
    # 1. normalization: exact sphere axis vs 2-D reference; Taylor coefficients 4/3 and 8/9
    a = R.ez_axis_sphere(0.25); b = R.ez_ref(1, 0, 0.25)
    report("sphere axis 1-D vs 2-D quadrature", abs(a - b) < 1e-9, mp.nstr(a, 12))
    r = mp.mpf("0.02"); c2 = (mp.mpf(4)/3 - R.ez_axis_sphere(r)/r)/r**2
    report("sphere axis Taylor coefficient 8/9", abs(c2 - mp.mpf(8)/9) < 1e-3, mp.nstr(c2, 8))
    # 2. interval kernel encloses the reference near the boundary (V51 amendment C point)
    lo = K.ez_lower(_box(1.0039, 0.95459, 0.25494), "fine"); ref = R.ez_ref(1.0039, 0.95459, 0.25494)
    report("ez_lower(fine) <= E_z reference and > 0", 0 < float(lo) <= float(ref), f"{float(lo):.6f} <= {mp.nstr(ref, 8)}")
    # 3. boundary trace on the B00 leaf (V51: 0.1274012451978957)
    hb = float(K.hb_lower((1048576, 1310720, 0, 0, 0, 0), "v50"))
    report("hb_lower B00 regression", abs(hb - 0.1274012451978957) < 1e-12, hb)
    # 4. chord H leaf E00:x0 (V51: confirmed, 2 children, min 0.107956)
    row = {"mode": "E", "action": "H_positive", "box": (1048576, 1310720, 0, 524288, 0, 0), "file": "E00", "path": "x0", "alo": 0, "ahi": 0}
    res = V.verify_leaf(row, {"chord": ["v50"]}, depth=4)
    report("chord H E00:x0 regression", res["confirmed"] and abs(res["attempts"][0]["extreme"] - 0.107956) < 1e-6, res["attempts"][0])
    # 5. tree structure checker on a synthetic tree
    rows = [{"path": "x", "box": (0, 4, 0, 4, 0, 0), "action": "splitl"},
            {"path": "x0", "box": (0, 2, 0, 4, 0, 0), "action": "positive"},
            {"path": "x1", "box": (2, 4, 0, 4, 0, 0), "action": "splitr"},
            {"path": "x10", "box": (2, 4, 0, 2, 0, 0), "action": "positive"},
            {"path": "x11", "box": (2, 4, 2, 4, 0, 0), "action": "empty"}]
    t = L.check_tree(rows); bad = L.check_tree(rows[:-1])
    report("tree checker accepts a valid tree and rejects a missing leaf", t["ok"] and not bad["ok"], t["relative_volume"])
    print("selftest", "passed" if ok else "FAILED", f"{time.monotonic()-t0:.0f}s"); return 0 if ok else 1
