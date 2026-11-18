"""chat V39: independent primitive-E H values at points inside second-order stage-B boxes; containment in the box H interval.
Physical p = (rho, lambda*z), rho = R cos beta, z = R sin beta, beta = 2 atan tau (chat V31 lib)."""
import sys, json, os
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from fractions import Fraction as F
from chat_r1_reference_check_lib import E_ref, stencil
mp.mp.dps = 25
q = lambda s: mp.mpf(F(s).numerator)/F(s).denominator
ok = True
for name in sys.argv[3:]:
    d = json.load(open(os.path.join(sys.argv[2], name + '.json'))); b = d['input_box']; iv = d['H_interval']
    lo, hi = q(iv['lower']), q(iv['upper'])
    (r0, r1), (t0, t1), (l0, l1) = [(q(x), q(y)) for x, y in (b['R'], b['tau'], b['lambda'])]
    pts = [((r0+r1)/2, (t0+t1)/2, (l0+l1)/2), (r0, t0, l1), (r1, t1, l0)]
    for R, tau, lam in pts:
        be = 2*mp.atan(tau); rho, pz = R*mp.cos(be), lam*R*mp.sin(be)
        _, er, _ = stencil(lambda dd: E_ref(lam, rho+dd, pz), second=False)
        H = er/rho if rho > mp.mpf('1e-12') else None
        inside = H is not None and lo <= H <= hi; ok &= inside
        print(f"{name} R={mp.nstr(R,6)} tau={mp.nstr(tau,6)} lam={mp.nstr(lam,8)}  H={mp.nstr(H,10)}  box=[{mp.nstr(lo,8)}, {mp.nstr(hi,8)}]  {'IN' if inside else 'OUT/NA'}", flush=True)
print("SUMMARY", "PASS" if ok else "CHECK")
