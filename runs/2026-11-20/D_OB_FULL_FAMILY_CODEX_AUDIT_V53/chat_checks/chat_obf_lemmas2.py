import sys; sys.path.insert(0, 'GER2')
import mpmath as mp
from geoenclosereader import kernels as K
mp.mp.dps = 20
U = 2**20
def pb(l): return (int(l*U), int(l*U), 0, 0, 0, 0)
print("Reader chord H(0,0) (v50) vs Codex §3 formula 1.588741807 (0.5), 1.431361649 (0.3), 0.333158453 (1/32)")
for l in (0.5, 0.3, 1/32):
    print(' ', l, float(K.chord_bound(pb(l), 'y', 'lower', 'v50')), float(K.chord_bound(pb(l), 'y', 'upper', 'v50')), flush=True)
print("Reader hb_lower (9) vs Codex §7 formula 0.41032294 (0.5), 0.1723500785 (0.1)")
for l in (0.5, 0.1):
    b = (int(l*U), int(l*U), 0, 0, 0, 0); print(' ', l, float(K.hb_lower(b, 'v50')), flush=True)
print("§4 h(rho) = -A'(rho)/rho, A = <(1 - rho cos)^2 / sqrt(1 - 2 rho cos + rho^2)>_phi; claims h(0)=1/2, h>0, h >= (5/16)(1-rho^2)")
A = lambda r: mp.quad(lambda p: (1 - r*mp.cos(p))**2/mp.sqrt(1 - 2*r*mp.cos(p) + r*r), [0, mp.pi])/mp.pi
for r in ('0.01', '0.3', '0.6', '0.9', '0.99'):
    r = mp.mpf(r); h = -mp.diff(A, r)/r; print(' ', mp.nstr(r, 3), mp.nstr(h, 8), '>= (5/16)(1-r^2)', h >= mp.mpf(5)/16*(1 - r*r))
