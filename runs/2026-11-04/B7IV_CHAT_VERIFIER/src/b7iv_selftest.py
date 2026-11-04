"""Self-tests for the chat independent B7 verifier.  python3 -I b7iv_selftest.py
1. rigor of the interval primitives against exact rationals (random)
2. 2/pi rational bracket (Machin formula, exact rationals)
3. kernel point value vs plain float transcription
4. representation: lam*(2/pi)*Int K  ==  H from P1 directly (float quadrature, 2 points)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fractions import Fraction as Fr
from b7iv_ia import IA
import b7iv_vk as VK
import b7iv_vleaf as VL

ok = True
def rep(name, cond, extra=''):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name + ((' | ' + extra) if extra else ''), flush=True)
    ok = ok and bool(cond)

# 1 ------------------------------------------------------------------
rng = np.random.default_rng(20261104); bad = 0; n = 3000
for trial in range(3):
    e = rng.integers(-50, 50, n).astype(float)
    al = rng.uniform(-1, 1, n) * 2.0**e; ah = al + np.abs(al) * rng.choice([0, 1e-16, 1e-6, 1.0], n)
    e = rng.integers(-50, 50, n).astype(float)
    bl = rng.uniform(-1, 1, n) * 2.0**e; bh = bl + np.abs(bl) * rng.choice([0, 1e-16, 1e-6, 1.0], n)
    X, Y = IA(al, ah), IA(bl, bh)
    P = IA(np.abs(al) + 1e-200, np.abs(ah) + np.abs(al) + 1e-200)
    res = {'+': X + Y, '-': X - Y, '*': X * Y, 'sq': X.sq(), 'inv': P.inv(), 'sqrt': P.sqrt()}
    for i in range(0, n, 5):
        xs = (Fr(al[i]), Fr(ah[i])); ys = (Fr(bl[i]), Fr(bh[i])); ps = (Fr(P.lo[i]), Fr(P.hi[i]))
        chk = {'+': [x + y for x in xs for y in ys], '-': [x - y for x in xs for y in ys],
               '*': [x * y for x in xs for y in ys],
               'sq': [x * x for x in xs] + ([Fr(0)] if xs[0] <= 0 <= xs[1] else []),
               'inv': [1 / ps[0], 1 / ps[1]]}
        for k, vals in chk.items():
            if not (Fr(res[k].lo[i]) <= min(vals) and Fr(res[k].hi[i]) >= max(vals)):
                bad += 1
        r = res['sqrt']
        if not (Fr(r.lo[i]) ** 2 <= ps[0] and Fr(r.hi[i]) ** 2 >= ps[1]):
            bad += 1
rep('interval primitives enclose exact results (random, 6 ops)', bad == 0, 'violations=%d' % bad)
rep('clamp constant CL < 4/25', Fr(VK.CL) < Fr(4, 25))

# 2 ------------------------------------------------------------------
def atan_bounds(x, n):
    """alternating series: partial sums S_n (odd n -> upper? ) return (lo, hi) for atan(x), 0<x<1."""
    terms = [(-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(n + 1)]
    a = sum(terms[:-1]); b = sum(terms)
    return (min(a, b), max(a, b))
a5 = atan_bounds(Fr(1, 5), 30); a239 = atan_bounds(Fr(1, 239), 10)
pi_lo = 16 * a5[0] - 4 * a239[1]; pi_hi = 16 * a5[1] - 4 * a239[0]   # Machin
lo, hi = VL.TWO_OVER_PI
rep('2/pi bracket (Machin, exact rationals)', lo < 2 / pi_hi and 2 / pi_lo < hi, '%.15f' % float(2 / pi_lo))

# 3 ------------------------------------------------------------------
def kern_float(lam, tau, delta, y, p, t, u, eps):
    A = (1 - tau * tau) / (1 + tau * tau); B = 2 * tau / (1 + tau * tau)
    x = y * (2 - y); N = 1 - A * A * x; M = delta + (1 - delta) * A * A * x
    s = math.sqrt((1 - delta) * N); qx = (1 - y) * A / math.sqrt(N); qz = B / math.sqrt(N)
    sig = 2 * p / (1 + p * p); g = (1 - p * p) / (1 + p * p)
    cb = eps * (1 - t * t) / (1 + t * t); sb = 2 * t / (1 + t * t); dv = M / (1 + s)
    kap = 2 * math.sqrt(s) * sig / dv; root = math.sqrt(1 + kap * kap); cp = 1 / root; sp = kap / root
    W = 4 * sig / math.sqrt(dv * dv + 4 * s * sig * sig)
    L = cp - sig * sp / math.sqrt(s); J = g * sp / math.sqrt(s)
    ox = L * qx - J * cb * qz; oz = L * qz + J * cb * qx
    xx = (1 - 2 * sig * sig) * qx - 2 * sig * g * cb * qz; xy = 2 * sig * g * sb
    xz = (1 - 2 * sig * sig) * qz + 2 * sig * g * cb * qx
    H = cp + math.sqrt(s) * sig * sp
    V2 = 1 - (1 - lam * lam) * oz * oz; U2 = V2 - ox * ox
    w = math.sqrt(lam * lam * (xx * xx + xy * xy) + xz * xz); T = w * math.sqrt(V2); G = lam * H
    E = -s * qx * J * J * sb * sb - s * J * cb * oz + (1 - lam * lam) * xx * oz * oz
    P = H * H * U2; R = E * E; Bh = (1 + u * u) * T + (1 - u * u) * G
    num = (1 + u * u) * T * (P - 2 * R) + (1 - u * u) * G * (P - R)
    jac = 2 * (1 - p * p) / (1 + p * p) ** 2 * 2 / (1 + t * t)
    return W * jac * num / (V2 * V2 * Bh * Bh)
pts = [(Fr(2, 5), Fr(15, 16), Fr(1, 20), Fr(3, 10), Fr(1, 100), Fr(1, 3), Fr(1, 2)),
       (Fr(93, 200), Fr(7, 8), Fr(3, 10**8), Fr(9, 10), Fr(7, 10), Fr(9, 10), Fr(1, 9))]
for pt in pts:
    V = [IA.from_pairs([(q, q)]) for q in pt]
    for eps in (1, -1):
        k = VK.F_K(V, eps)[1].v
        f = kern_float(*[float(q) for q in pt], eps)
        rep('kernel point enclosure eps=%d' % eps, k.lo[0] - 1e-9 * abs(f) <= f <= k.hi[0] + 1e-9 * abs(f),
            '%.15g in [%.15g, %.15g]' % (f, k.lo[0], k.hi[0]))

# 4 ------------------------------------------------------------------
def R_Rg(g):
    g = np.clip(g, 0, 1); al = np.arccos(g); s = np.sin(al); small = al < 0.02; u = 1 - g * g
    R = np.where(small, 1 + u / 6 + 3 * u * u / 40, al / np.where(small, 1, s))
    Rg = np.where(small, -2 * g * (1 / 6 + 3 * u / 20), (al * np.cos(al) - s) / np.where(small, 1, s) ** 3)
    return R, Rg
def Err(lam, rho, z, n=300):
    tg, tw = np.polynomial.legendre.leggauss(n); th = (tg + 1) * np.pi / 2; thw = tw * np.pi / 2
    ph = np.arange(2 * n) * np.pi / n
    MU, PH = np.meshgrid(np.cos(th), ph, indexing='ij'); Wt = np.outer(thw * np.sin(th), np.full(2 * n, np.pi / n))
    a = np.sqrt(1 - MU * MU); X = np.stack([a * np.cos(PH), a * np.sin(PH), lam * MU])
    w = np.sqrt(lam * lam * (1 - MU * MU) + MU * MU); nn = np.stack([lam * a * np.cos(PH), lam * a * np.sin(PH), MU]) / w
    Y = X - np.array([rho, 0, z])[:, None, None]; D = np.sqrt((Y * Y).sum(0)); h = w * (Y * nn).sum(0); g = h / (w * D)
    R, Rg = R_Rg(g); hv = -w * nn[0]; Dv = -Y[0] / D; gv = hv / (w * D) - g * Dv / D; Dvv = (1 - Dv * Dv) / D
    gvv = -hv * Dv / (w * D * D) - gv * Dv / D - g * Dvv / D + g * Dv * Dv / (D * D)
    F = -4 * hv * R * gv - 2 * h * Rg * gv * gv - 2 * h * R * gvv
    return (Wt * F).sum() / (4 * np.pi * lam)
def gl(n, a=0.0, b=1.0):
    x, w = np.polynomial.legendre.leggauss(n); return a + (b - a) * (x + 1) / 2, (b - a) * w / 2
kv = np.vectorize(kern_float)
for lam, tau, delta in [(0.42, 0.9, 0.2), (0.45, 0.95, 0.05)]:
    A = (1 - tau * tau) / (1 + tau * tau); B = 2 * tau / (1 + tau * tau); r = math.sqrt(1 - delta)
    vv, vw = gl(10)
    Hd = sum(w_ * Err(lam, v * r * A, lam * r * B) for v, w_ in zip(vv, vw))
    tot = 0.0
    ys, yw = gl(12); ts, tw_ = gl(12); us, uw = gl(6)
    for a, b in zip([0, 1e-3, 1e-2, 0.05, 0.2, 0.5], [1e-3, 1e-2, 0.05, 0.2, 0.5, 1]):
        ps, pw = gl(12, a, b)
        Y, P, T, U = np.meshgrid(ys, ps, ts, us, indexing='ij')
        Wt = np.einsum('i,j,k,l->ijkl', yw, pw, tw_, uw)
        tot += (Wt * (kv(lam, tau, delta, Y, P, T, U, 1) + kv(lam, tau, delta, Y, P, T, U, -1))).sum()
    Hr = lam * (2 / math.pi) * tot
    rep('representation lam=%g tau=%g delta=%g' % (lam, tau, delta), abs(Hr / Hd - 1) < 1e-4, 'P1 %.7f  B7 %.7f' % (Hd, Hr))
print('ALL SELFTESTS PASS' if ok else 'SELFTEST FAILURE')
sys.exit(0 if ok else 1)
