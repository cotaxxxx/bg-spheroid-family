"""V55 plan (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE. chat's own Arb code (not Codex's ring_interval.py).
Checks of Codex's local theorem at the prolate edge t = 3 (s = 1, i.e. lambda = 3):
 (a) circle radius bracket: g1(r) = E_x(r e1) = r H on the equator; H > 0 at r = 13/16, H < 0 at r = 27/32
     (GeoEncloseReader 0.2.1 chord kernel, point boxes, grids v50 -> fine).
 (b) the splitting coefficient (6)  c(r, 3) = 1/2 < k P(g) g [n1^2 - n2^2 - u1^2 + u2^2] >  at q = r e1, L = diag(1,1,3),
     upper bound < 0 for r in [208/256, 216/256] (8 radius intervals), sphere cells mu = xi_1 in [-1,1] (N_MU) x
     phi in [0, pi/2] (N_PHI, quadrant symmetry x4). Ladder (N_MU, N_PHI) = (256, 64), (512, 128), (1024, 256).
"""
import sys, json, time, multiprocessing as mp
from flint import arb, fmpq
from geoenclosereader import kernels as K
from geoenclosereader.interval import clip, sqrtp, sq, U01, PI
from geoenclosereader.series import P_enc
def c_upper(r0, r1, NM, NP):
    r = arb(r0).union(arb(r1)); tot = arb(0)
    for i in range(NM):
        mu = arb(-1 + fmpq(2*i, NM)).union(arb(-1 + fmpq(2*(i+1), NM))); s = sqrtp(clip(1 - mu*mu, 0, 1))
        for j in range(NP):
            ph = (PI/2)*(arb(j) + U01)/NP; x2 = s*ph.cos(); x3 = s*ph.sin()
            k = 1 - r*mu; D2 = sq(mu - r) + sq(x2) + 9*sq(x3); S2 = sq(mu) + sq(x2) + sq(x3)/9
            D = D2.sqrt(); S = S2.sqrt(); g = clip(k/(D*S), 0, 1)
            br = (sq(mu) - sq(x2))/S2 - (sq(mu - r) - sq(x2))/D2
            tot += arb((k*P_enc(g)*g*br/2).upper())
    # mean over the sphere: (1/4pi) * 4 * sum over cells of value * (dmu * dphi); dmu = 2/NM, dphi = (pi/2)/NP
    return (tot*4*(arb(2)/NM)*(PI/2/NP)/(4*PI)).upper()
def job_b(k):
    r0 = fmpq(208 + k, 256); r1 = fmpq(209 + k, 256); t0 = time.monotonic()
    for NM, NP in [(256, 64), (512, 128), (1024, 256)]:
        v = c_upper(r0, r1, NM, NP)
        if v < 0: break
    return {"check": "c(r,3)<0", "r": [str(r0), str(r1)], "grid": [NM, NP], "upper": float(v), "confirmed": bool(v < 0), "seconds": round(time.monotonic() - t0, 1)}
def job_a(item):
    r, sign = item; U = 2**20; L = 3*U; R = int(r*U); box = (L, L, R, R, 0, 0); t0 = time.monotonic()
    for g in ("v50", "fine"):
        v = K.chord_bound(box, 'y', 'lower' if sign > 0 else 'upper', g)
        if (v > 0) if sign > 0 else (v < 0): break
    return {"check": "H sign (g1 = rH)", "r": str(r), "sign": sign, "grid": g, "bound": float(v), "confirmed": bool((v > 0) if sign > 0 else (v < 0)), "seconds": round(time.monotonic() - t0, 1)}
if __name__ == '__main__':
    from fractions import Fraction as F
    with open(sys.argv[1], 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(job_a, [(F(13, 16), +1), (F(27, 32), -1)]): f.write(json.dumps(r) + "\n"); f.flush(); print(json.dumps(r), flush=True)
        for r in pool.imap(job_b, range(8)): f.write(json.dumps(r) + "\n"); f.flush(); print(json.dumps(r), flush=True)
