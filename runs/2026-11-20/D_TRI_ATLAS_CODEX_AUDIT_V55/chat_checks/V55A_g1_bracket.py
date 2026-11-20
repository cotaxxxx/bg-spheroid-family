"""Amendment V55-A (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
V55 (a) was not confirmed: the Reader chord H kernel at lambda = 3 gave intervals of width ~0.04 around values of
about +0.008 (r = 13/16) and -0.014 (r = 27/32). Replacement (same claim): enclose g1(r) = E_x(r e1) directly by the
gradient trace (1), E_x = < xi_1 J - S u_1 K >, J = g P - arccos^2 g, K = g^2 P, at the point q = (r, 0, 0) of the
prolate edge L = diag(1, 1, 3); cells mu = xi_1 (N_MU) x phi in [0, pi/2] (N_PHI, quadrant symmetry), D >= 1 - r > 0.
Ladder (N_MU, N_PHI) = (512, 128), (2048, 256), (4096, 512). Claim: g1(13/16) > 0, g1(27/32) < 0.
"""
import sys, json, time, multiprocessing as mp
from flint import arb, fmpq
from geoenclosereader.interval import clip, sqrtp, sq, U01, PI, acos_safe
from geoenclosereader.series import P_enc
def g1_bound(r, want, NM, NP):
    r = arb(r); tot = arb(0)
    for i in range(NM):
        mu = arb(-1 + fmpq(2*i, NM)).union(arb(-1 + fmpq(2*(i+1), NM))); s = sqrtp(clip(1 - mu*mu, 0, 1))
        for j in range(NP):
            ph = (PI/2)*(arb(j) + U01)/NP; x2 = s*ph.cos(); x3 = s*ph.sin()
            k = 1 - r*mu; D = (sq(mu - r) + sq(x2) + 9*sq(x3)).sqrt(); S = (sq(mu) + sq(x2) + sq(x3)/9).sqrt()
            g = clip(k/(D*S), 0, 1); P = P_enc(g); J = g*P - acos_safe(g)**2; Kk = g*g*P
            v = mu*J - S*clip((mu - r)/D, -1, 1)*Kk
            tot += arb(v.lower() if want == 'lower' else v.upper())
    t = tot*4*(arb(2)/NM)*(PI/2/NP)/(4*PI); return t.lower() if want == 'lower' else t.upper()
def job(item):
    r, sign = item; t0 = time.monotonic()
    for NM, NP in [(512, 128), (2048, 256), (4096, 512)]:
        v = g1_bound(r, 'lower' if sign > 0 else 'upper', NM, NP)
        if (v > 0) if sign > 0 else (v < 0): break
    return {"check": "g1 sign", "r": str(r), "sign": sign, "grid": [NM, NP], "bound": float(v), "confirmed": bool((v > 0) if sign > 0 else (v < 0)), "seconds": round(time.monotonic() - t0, 1)}
if __name__ == '__main__':
    with open(sys.argv[1], 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(job, [(fmpq(13, 16), +1), (fmpq(27, 32), -1)]): f.write(json.dumps(r) + "\n"); f.flush(); print(json.dumps(r), flush=True)
