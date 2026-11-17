"""chat reference: H = E_rho/rho at box-2 centre and at 4 interior points, brute-force E (2D mpmath quad), 5-point stencil."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref, stencil
mp.mp.dps = 25
pts = [(mp.mpf(3)/4, mp.mpf(1)/8, mp.mpf(2559)/512), (mp.mpf(95)/128+mp.mpf(1)/512, mp.mpf(15)/128+mp.mpf(1)/256, mp.mpf(1280)/256),
       (mp.mpf(97)/128-mp.mpf(1)/512, mp.mpf(17)/128-mp.mpf(1)/256, mp.mpf(5)-mp.mpf(1)/1024), (mp.mpf(95)/128+mp.mpf(1)/256, mp.mpf(17)/128-mp.mpf(1)/512, mp.mpf(5)-mp.mpf(1)/512),
       (mp.mpf(97)/128-mp.mpf(1)/256, mp.mpf(15)/128+mp.mpf(1)/512, mp.mpf(1279)/256+mp.mpf(1)/1024)]
for R, tau, lam in pts:
    b = 2*mp.atan(tau); rho, z = R*mp.cos(b), lam*R*mp.sin(b)
    _, er, _ = stencil(lambda d: E_ref(lam, rho+d, z), second=False)
    print(f"R={mp.nstr(R,12)} tau={mp.nstr(tau,12)} lam={mp.nstr(lam,12)}  H = E_rho/rho = {mp.nstr(er/rho, 12)}", flush=True)
