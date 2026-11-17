"""chat probe (float-level diagnostic, not proof): W = lam^2 V - H across the sphere, oblate <-> prolate.
Brute-force E (primitive definition, 2D mpmath quad), W = E_beta/(R^2 sin cos) by 5-point stencil in beta."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref, stencil
mp.mp.dps = 20
for R, tau in ((mp.mpf(1)/2, mp.mpf(1)/2), (mp.mpf(3)/4, mp.mpf(1)/3)):
    b0 = 2*mp.atan(tau)
    for lam in ('0.3', '0.5', '0.8', '0.95', '1', '1.05', '1.25', '2', '3.5', '5'):
        l = mp.mpf(lam)
        _, eb, _ = stencil(lambda d: E_ref(l, R*mp.cos(b0+d), l*R*mp.sin(b0+d)), second=False)
        W = eb/(R**2*mp.sin(b0)*mp.cos(b0))
        print(f"R={mp.nstr(R,3)} tau={mp.nstr(tau,3)} lam={lam:>5}  W={mp.nstr(W,8):>12}  W/log(lam)={'—' if lam=='1' else mp.nstr(W/mp.log(l),8)}", flush=True)
