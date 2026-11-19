"""chat V49 (1): chord formula (3) with exact F', Q vs chat's earlier NP7/E_ref values."""
import mpmath as mp
mp.mp.dps = 20
def Fp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return 2*(1+mp.mpf(2)/3*h+mp.mpf(8)/15*h*h)
    return 2*mp.acos(g)/mp.sqrt(1-g*g)
def Q(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return mp.mpf(10)/3 + mp.mpf(4)*h*0  # Q(1)=10/3 (leading); only on null sets
    return 2*Fp(g) + g*(g*Fp(g)-2)/(1-g*g)
def H_chord(lam, r, z):
    e2 = mp.mpf(1)/lam**2; dl = 1 - r*r - z*z
    def f(m, psi):
        s = mp.sqrt(1-m*m); ex = s*mp.cos(psi); ey = s*mp.sin(psi); j = ey*ey
        v = r*ex + z*m; d = mp.sqrt(dl + v*v); C = 1 + (lam**2-1)*m*m; U = 1 - 1/C
        tot = 0
        for sg in (1, -1):
            l = d - sg*v; xz = z + sg*l*m; B = 1 - (1-e2)*xz*xz; g = min(mp.mpf(1), d/mp.sqrt(C*B)); w = (1 - sg*v/d)/2
            tot += w*(d*d*(1-j/C)/C**1.5*Fp(g)/mp.sqrt(B) - j*(d*U - sg*v)**2/mp.sqrt(C)*Q(g)/mp.sqrt(B))
        return tot
    return mp.quad(f, [0, mp.mpf(1)/lam, mp.mpf(4)/lam, 1], [0, mp.pi/2, mp.pi])/mp.pi   # average over m in [0,1], psi in [0,pi]
ref = [(5, 0, 0, '-0.0243031238'), (5, mp.mpf('0.3'), mp.mpf('0.4'), '-0.08283274943'), (5, mp.mpf('0.5'), 0, '-0.0820759960'), (10, mp.mpf('0.2'), mp.mpf('0.6'), '-0.207568431')]
ok = True
for lam, r, z, h in ref:
    v = H_chord(lam, r, z); ok &= abs(v - mp.mpf(h)) < 1e-8
    print(f"lambda={lam} q=({r},{z}): chord {mp.nstr(v,12)}  ref {h}")
print("PASS" if ok else "FAIL", "chord formula (3) reproduces NP7 / E_ref values at 4 points")
