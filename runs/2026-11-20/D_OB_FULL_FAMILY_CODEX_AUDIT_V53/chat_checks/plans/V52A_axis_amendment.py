"""Amendment A to V52 (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Reason: the 2-D ez grid is too wide for the lambda_x landmarks (|E_z(0,1/2)| ~ 1e-3 there; width ~ 2e-2).
On the axis the integrand is azimuth-free, so GeoEncloseReader 0.2.0 adds 1-D axis kernels (ez_axis_bound,
ezz_axis_bound). Consistency: lambda = 1/2, z = 3/4: E_z in [0.01074, 0.01745] (N 4096) vs reference 0.0140937;
E_zz(0,0) in [0.23512, 0.23882] vs D-OB 0.236973.
Checks:
 L1. lambda_x landmarks: E_z(0,1/2) < 0 at 699/1600 and > 0 at 281/640. Ladder (N, refine) = (65536, 64), (262144, 128).
 L2. Independent re-derivation of the C1b / C1c axial structure on sampled slabs of width 1/800 in [9/20, 5/8]:
     slabs k = 0, 139 and 6 random (seed 52) of 1..138. Predictor t_c = root of the 1-D mpmath reference at the slab
     midpoint; t- = max(1/2, t_c - 1/16), t+ = min(1, t_c + 1/16) (the C1 contract's w0 = 1/16).
     (a) E_zz(0,t) > 0 on [0, 1/16]; (b) E_z(0,t) > 0 on [1/16, t-] (includes the wall t-);
     (c) E_zz(0,t) < 0 on [t-, t+] (tube); (d) E_z(0,t) < 0 on [t+, 1] (t+ = 1: the pole trace E_z(0,1) < 0).
     Intervals are split into equal pieces of width 1/32 (tube: 1/64) and bisected in t and lambda up to depth 5.
     ez ladder (N, refine) = (16384, 32), (65536, 64); ezz N = 2048, 8192.
     Together: for every lambda in the slab, E_z(0, .) > 0 on (0, t-], one zero in (t-, t+), < 0 on [t+, 1).
"""
import sys, json, random, time, multiprocessing as mp
from fractions import Fraction as F
from flint import fmpq
from geoenclosereader import kernels as K, reference as R
q = lambda x: fmpq(x.numerator, x.denominator)
EZ = [(16384, 32), (65536, 64)]; EZZ = [2048, 8192]

def sign_ok(kind, l0, l1, t0, t1, sign, ladder_idx):
    if kind == 'ez':
        N, rf = EZ[ladder_idx]; v = K.ez_axis_bound(q(l0), q(l1), q(t0), q(t1), 'lower' if sign > 0 else 'upper', N, rf)
    else:
        v = K.ezz_axis_bound(q(l0), q(l1), q(t0), q(t1), 'lower' if sign > 0 else 'upper', EZZ[ladder_idx])
    return ((v > 0) if sign > 0 else (v < 0)), float(v)

def cover(job):
    """job = (name, kind, l0, l1, t0, t1, sign): confirm the sign on the rectangle by ladder + bisection (depth <= 5)."""
    name, kind, l0, l1, t0, t1, sign = job; t_ = time.monotonic()
    for li in range(2):
        todo = [(l0, l1, t0, t1, 0)]; ok = True; ext = None; ev = 0
        while todo:
            a, b, c, d, dep = todo.pop(); good, v = sign_ok(kind, a, b, c, d, sign, li); ev += 1
            if good: ext = v if ext is None else (min(ext, v) if sign > 0 else max(ext, v))
            elif dep < 5:
                if (d - c) >= 8*(b - a): m = (c + d)/2; todo += [(a, b, c, m, dep+1), (a, b, m, d, dep+1)]
                else: m = (a + b)/2; todo += [(a, m, c, d, dep+1), (m, b, c, d, dep+1)]
            else: ok = False; ext = v; break
        if ok: break
    return {"leaf": name, "kind": kind, "box": [str(x) for x in (l0, l1, t0, t1)], "sign": sign, "confirmed": ok,
            "ladder": li, "evals": ev, "extreme": ext, "seconds": round(time.monotonic() - t_, 1)}

def root(lam):
    lo, hi = 0.5, 1.0
    if R.ez_axis_ref(lam, 0.999) > 0: return None
    for _ in range(40):
        m = (lo + hi)/2
        if R.ez_axis_ref(lam, m) > 0: lo = m
        else: hi = m
    return (lo + hi)/2

def pieces(t0, t1, w):
    out = []; a = t0
    while a < t1: b = min(t1, (a // w + 1)*w); out.append((a, b)); a = b
    return out

if __name__ == '__main__':
    out = sys.argv[1]; jobs = []
    jobs += [("lx_lo", 'ez', F(699, 1600), F(699, 1600), F(1, 2), F(1, 2), -1), ("lx_hi", 'ez', F(281, 640), F(281, 640), F(1, 2), F(1, 2), +1)]
    rng = random.Random(52); ks = [0, 139] + sorted(rng.sample(range(1, 139), 6)); meta = []
    for k in ks:
        l0 = F(9, 20) + F(k, 800); l1 = l0 + F(1, 800); tc = root(float((l0 + l1)/2))
        tcf = F(tc).limit_denominator(4096); tm = max(F(1, 2), tcf - F(1, 16)); tp = min(F(1), tcf + F(1, 16))
        meta.append({"slab": k, "lambda": [str(l0), str(l1)], "t_c": tc, "t_minus": str(tm), "t_plus": str(tp)})
        jobs += [("k%03d:a" % k, 'ezz', l0, l1, F(0), F(1, 16), +1)]
        jobs += [("k%03d:b%d" % (k, i), 'ez', l0, l1, a, b, +1) for i, (a, b) in enumerate(pieces(F(1, 16), tm, F(1, 32)))]
        jobs += [("k%03d:c%d" % (k, i), 'ezz', l0, l1, a, b, -1) for i, (a, b) in enumerate(pieces(tm, tp, F(1, 64)))]
        if tp < 1: jobs += [("k%03d:d%d" % (k, i), 'ez', l0, l1, a, b, -1) for i, (a, b) in enumerate(pieces(tp, F(1), F(1, 32)))]
        else: jobs += [("k%03d:d_pole" % k, 'ez', l0, l1, F(1), F(1), -1)]
    with open(out, 'w') as f:
        for m in meta: f.write(json.dumps({"slab_meta": m}) + "\n")
        n = ok = 0
        with mp.Pool(2) as pool:
            for r in pool.imap(cover, jobs):
                n += 1; ok += r['confirmed']; f.write(json.dumps(r) + "\n"); f.flush(); print(r['leaf'], r['confirmed'], r['ladder'], r['extreme'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
