"""chat V50 pre-check (non-interval, chat's own code): binary sign questions at Codex's window brackets."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref
mp.mp.dps = 20
def Fp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return 2*(1+mp.mpf(2)/3*h+mp.mpf(8)/15*h*h)
    return 2*mp.acos(g)/mp.sqrt(1-g*g)
def Q(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return mp.mpf(10)/3 - mp.mpf(14)/15*h*0
    return 2*Fp(g) + g*(g*Fp(g)-2)/(1-g*g)
def H_chord(lam, r, z):
    e2 = mp.mpf(1)/lam**2; dl = max(mp.mpf(0), 1 - r*r - z*z)
    def f(m, psi):
        s = mp.sqrt(max(mp.mpf(0), mp.re(1-m*m))); ex = s*mp.cos(psi); ey = s*mp.sin(psi); j = ey*ey
        v = r*ex + z*m; d = mp.sqrt(max(mp.mpf(0), dl + v*v)); C = 1 + (lam**2-1)*m*m; U = 1 - 1/C
        if d == 0: return mp.mpf(0)
        tot = 0
        for sg in (1, -1):
            l = d - sg*v
            if l <= 0: continue
            xz = z + sg*l*m; B = max(e2, 1 - (1-e2)*xz*xz); g = min(mp.mpf(1), d/mp.sqrt(C*B)); w = (1 - sg*v/d)/2
            tot += w*(d*d*(1-j/C)/C**1.5*Fp(g)/mp.sqrt(B) - j*(d*U - sg*v)**2/mp.sqrt(C)*Q(g)/mp.sqrt(B))
        return tot
    return mp.quad(f, [0, mp.mpf(1)/lam, mp.mpf(4)/lam, 1], [0, mp.pi/2, mp.pi])/mp.pi
def show(name, a, b):
    print(f"{name}: left {mp.nstr(a,8)}  right {mp.nstr(b,8)}  sign change: {a > 0 > b}", flush=True)
#done: show("lambda_c: H(0,0) at 4.72438311 / 4.72438366", H_chord(mp.mpf('4.72438311'), 0, 0), H_chord(mp.mpf('4.72438366'), 0, 0))
show("circle lambda=3: H(rho,0) at rho 0.823933 / 0.823943", H_chord(mp.mpf(3), mp.mpf('0.823933'), 0), H_chord(mp.mpf(3), mp.mpf('0.823943'), 0))
show("circle lambda=4: H(rho,0) at rho 0.536318 / 0.536328", H_chord(mp.mpf(4), mp.mpf('0.536318'), 0), H_chord(mp.mpf(4), mp.mpf('0.536328'), 0))
show("lambda_b: H(rho=1-1e-7, 0) at 2.06538200 / 2.06538255", H_chord(mp.mpf('2.06538200'), 1-mp.mpf(10)**-7, 0), H_chord(mp.mpf('2.06538255'), 1-mp.mpf(10)**-7, 0))
# off-plane: E_z/z > 0 at sample points (E_ref central difference in reference z)
for lam, r, z in [(3, '0.8', '0.3'), (3, '0.5', '0.85'), (2, '0.95', '0.2'), (4.5, '0.2', '0.1'), (4.9, '0.6', '0.7')]:
    r = mp.mpf(r); z = mp.mpf(z); hz = mp.mpf('0.0005')
    Ez = (E_ref(lam, r, lam*(z+hz)) - E_ref(lam, r, lam*(z-hz)))/(2*hz)
    print(f"off-plane E_z/z at lambda={lam} q=({r},{z}): {mp.nstr(Ez/z,6)}  positive: {Ez > 0}", flush=True)
# on the circle at lambda=3: E_zz > 0 and E_xx < 0 (meridian saddle) by E_ref differences
lam = 3; r0 = mp.mpf('0.823938'); h = mp.mpf('0.002')
E0 = E_ref(lam, r0, 0)
Ezz = (E_ref(lam, r0, lam*h) - 2*E0 + E_ref(lam, r0, -lam*h))/h**2
Exx = (E_ref(lam, r0+h, 0) - 2*E0 + E_ref(lam, r0-h, 0))/h**2
print(f"circle lambda=3 rho*~0.823938: E_zz {mp.nstr(Ezz,6)} (>0: {Ezz>0}), E_rhorho {mp.nstr(Exx,6)} (<0: {Exx<0})", flush=True)
