"""V54 plan (fixed before run): GeoEncloseReader 0.2.1 interval spot checks of the rim-layer claims at lambda = 1/32
(point lambda, point (rho, z)). DIAGNOSTIC_ONLY / NOT_EVIDENCE. These are pointwise sign confirmations, independent of
Codex's code; the claims themselves are proved analytically in the report.
  H = E_yy > 0 on the equator: rho in {1/2, 15/16, 63/64}            (claim H >= lambda/24 = 0.0013)
  E_zz < 0 off the equator:    (rho, z) in {(1/2, 1/4), (7/8, 1/4), (31/32, 1/16)}   (claim E_zz <= -6 lambda/55)
Ladder graded -> graded_fine. Confirmed iff the declared sign holds.
"""
import sys, json, time, multiprocessing as mp
from flint import fmpq
from geoenclosereader import kernels as K
L = fmpq(1, 32)
def job(it):
    name, comp, rho, z, sign = it; t0 = time.monotonic(); box = (L, L, rho, rho, z, z)
    for g in ("graded", "graded_fine"):
        v = K.chord_bound(box, comp, 'lower' if sign > 0 else 'upper', g)
        ok = (v > 0) if sign > 0 else (v < 0)
        if ok: break
    return {"leaf": name, "comp": comp, "rho": str(rho), "z": str(z), "sign": sign, "confirmed": bool(ok), "grid": g, "bound": float(v), "seconds": round(time.monotonic()-t0, 1)}
if __name__ == '__main__':
    items = [("H_rho_1/2", 'y', fmpq(1, 2), fmpq(0), 1), ("H_rho_15/16", 'y', fmpq(15, 16), fmpq(0), 1), ("H_rho_63/64", 'y', fmpq(63, 64), fmpq(0), 1),
             ("Ezz_1/2_1/4", 'z', fmpq(1, 2), fmpq(1, 4), -1), ("Ezz_7/8_1/4", 'z', fmpq(7, 8), fmpq(1, 4), -1), ("Ezz_31/32_1/16", 'z', fmpq(31, 32), fmpq(1, 16), -1)]
    with open(sys.argv[1], 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(job, items): f.write(json.dumps(r) + "\n"); f.flush(); print(json.dumps(r), flush=True)
