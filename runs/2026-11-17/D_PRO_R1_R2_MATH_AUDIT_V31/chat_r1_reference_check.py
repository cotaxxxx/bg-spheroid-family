"""chat V31: R1 R2 kernels vs chat's brute-force reference E (primitive definition, 2D mpmath quad,
finite differences). Runs Codex code from argv[1]; tight config fixed BEFORE running:
order 6, base 32x64, distance_ratio 1/2 (the rest default)."""
import sys, time, json
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from dataclasses import replace
from flint import fmpq as Q, arb
from prolate_r1 import api, Config
mp.mp.dps = 25
CFG = replace(Config(), order=6, base_u=32, base_v=64, distance_ratio=Q(1, 2))

def E_ref(lam, px, pz):
    lam = mp.mpf(lam)
    def f(mu, phi):
        s = mp.sqrt(1-mu*mu); xi = s*mp.cos(phi); eta = s*mp.sin(phi)
        w = mp.sqrt(lam**2*(1-mu*mu)+mu*mu); h = lam*(1-px*xi)-pz*mu
        D = mp.sqrt((xi-px)**2+eta**2+(lam*mu-pz)**2)
        return h*mp.acos(h/(w*D))**2
    return mp.re(2*mp.quad(f, [-1, -0.5, 0, 0.5, 1], [0, mp.pi/4, mp.pi/2, mp.pi])/(4*mp.pi*lam))
H = mp.mpf('0.004')
def stencil(F):
    e = {k: F(k*H) for k in (-2, -1, 0, 1, 2)}
    d1 = (8*(e[1]-e[-1]) - (e[2]-e[-2]))/(12*H)
    d2 = (16*(e[1]+e[-1]) - (e[2]+e[-2]) - 30*e[0])/(12*H*H)
    return e[0], d1, d2
def fq(x): return mp.mpf(int(x.p))/int(x.q)
def lohi(b): return mp.mpf(b.lower().str(30, radius=False)), mp.mpf(b.upper().str(30, radius=False))
rows = []; allok = True
def rec(name, ball, ref, slack=mp.mpf('1e-7')):
    global allok
    lo, hi = lohi(ball); ok = lo-slack <= ref <= hi+slack
    allok &= ok
    rows.append(dict(case=name, ref=mp.nstr(ref, 12), lo=mp.nstr(lo, 10), hi=mp.nstr(hi, 10), halfwidth=mp.nstr((hi-lo)/2, 3), ok=bool(ok)))
    print(("PASS " if ok else "FAIL ")+name, mp.nstr(ref, 12), "in", f"[{mp.nstr(lo,10)}, {mp.nstr(hi,10)}]", "hw", mp.nstr((hi-lo)/2, 3), flush=True)

# 1) angular_raw and angular_quotient at interior points (tau chart)
for lam in (Q(2), Q(7, 2), Q(5)):
    for R, tau in ((Q(1, 2), Q(1, 2)), (Q(3, 4), Q(1, 3)), (Q(15, 16), Q(1, 2))):
        if R == Q(15, 16) and lam != Q(7, 2): continue
        b0 = 2*mp.atan(fq(tau)); Rm, lm = fq(R), fq(lam)
        e, eb, ebb = stencil(lambda d: E_ref(lm, Rm*mp.cos(b0+d), lm*Rm*mp.sin(b0+d)))
        t = time.time()
        raw = api.angular_raw(R, tau, lam, angle_kind="tau", config=CFG)
        W = api.angular_quotient(R, tau, lam, angle_kind="tau", config=CFG)
        tag = f"lam={lam} R={R} tau={tau}"
        rec("E   "+tag, raw.balls[0], e); rec("Eb  "+tag, raw.balls[1], eb); rec("Ebb "+tag, raw.balls[2], ebb, mp.mpf('1e-5'))
        rec("W   "+tag+" ["+W.route+"]", W.enclosure, eb/(Rm**2*mp.sin(b0)*mp.cos(b0)), mp.mpf('1e-6'))
        print("   time", round(time.time()-t, 1), "cells", raw.cells, flush=True)
# 2) endpoint charts (tau = 0: equator, tau = 1: pole) — W as limit lam^2 V - H
for lam in (Q(2), Q(5)):
    lm = fq(lam); R = Q(1, 2); Rm = fq(R)
    # equator: W = lam^2 E_zz(R,0) - E_x(R,0)/R
    _, _, ezz = stencil(lambda d: E_ref(lm, Rm, d))
    _, ex, _ = stencil(lambda d: E_ref(lm, Rm+d, 0))
    rec(f"W equator lam={lam} R=1/2", api.angular_quotient(R, Q(0), lam, angle_kind="tau", config=CFG).enclosure, lm**2*ezz - ex/Rm, mp.mpf('1e-6'))
    # pole: W = lam^2 E_z/z - E_xx at (0, lam R)
    _, ez, _ = stencil(lambda d: E_ref(lm, 0, lm*Rm+d))
    _, _, exx = stencil(lambda d: E_ref(lm, d, lm*Rm))
    rec(f"W pole lam={lam} R=1/2", api.angular_quotient(R, Q(1), lam, angle_kind="tau", config=CFG).enclosure, lm**2*ez/(lm*Rm) - exx, mp.mpf('1e-6'))
# 3) centre W (R <= 1/16): W(R=1/32, tau=1/2) vs reference
for lam in (Q(2), Q(5)):
    lm = fq(lam); R = Q(1, 32); Rm = fq(R); b0 = 2*mp.atan(mp.mpf(1)/2)
    _, eb, _ = stencil(lambda d: E_ref(lm, Rm*mp.cos(b0+d), lm*Rm*mp.sin(b0+d)))
    Wc = api.angular_quotient(R, Q(1, 2), lam, angle_kind="tau", config=CFG)
    rec(f"W centre lam={lam} R=1/32 [{Wc.route}]", Wc.enclosure, eb/(Rm**2*mp.sin(b0)*mp.cos(b0)), mp.mpf('1e-4'))
# 4) axis g = d/dt E(0,0,lam t)
for lam in (Q(2), Q(7, 2), Q(5)):
    lm = fq(lam)
    for t in (Q(1, 32), Q(1, 2), Q(7, 8)):
        tm = fq(t)
        _, g, _ = stencil(lambda d: E_ref(lm, 0, lm*(tm+d)))
        rec(f"g lam={lam} t={t}", api.axis_g(t, lam, config=CFG).enclosure, g)
# 5) equatorial Phi_s = (r E_rr - E_r)/(2 r^3)
for lam in (Q(2), Q(7, 2), Q(5)):
    lm = fq(lam)
    for s in (Q(1, 1024), Q(1, 4), Q(9, 16)):
        r = mp.sqrt(fq(s))
        _, er, err = stencil(lambda d: E_ref(lm, r+d, 0))
        rec(f"Phi_s lam={lam} s={s}", api.equatorial_phi_s(s, lam, config=CFG).enclosure, (r*err-er)/(2*r**3), mp.mpf('1e-4') if s == Q(1, 1024) else mp.mpf('1e-6'))
json.dump(rows, open(sys.argv[2], "w"), indent=1)
print("SUMMARY", "ALL_PASS" if allok else "FAIL", len(rows))
