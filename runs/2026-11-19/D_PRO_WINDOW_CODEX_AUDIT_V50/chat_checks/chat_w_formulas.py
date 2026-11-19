"""chat V50: numeric validation of Codex window formulas (2) E_z and (3)-(4) E_zz against chat's E_ref."""
import sys
sys.path.insert(0, sys.argv[1])
exec(open('chat_win_spot.py').read().split('def H_chord')[0])
from chat_r1_reference_check_lib import E_ref
def Ezz_chord(lam, r, z):
    e2 = mp.mpf(1)/lam**2; dl = max(mp.mpf(0), 1 - r*r - z*z)
    def f(m, psi):
        s = mp.sqrt(max(mp.mpf(0), mp.re(1-m*m))); ex = s*mp.cos(psi)
        v = r*ex + z*m; d = mp.sqrt(dl + v*v); C = 1 + (lam**2-1)*m*m; tot = 0
        for sg in (1, -1):
            l = d - sg*v; xi = (r + sg*l*ex, sg*l*s*mp.sin(psi), z + sg*l*m)
            B = max(e2, 1 - (1-e2)*xi[2]**2); T = 1/mp.sqrt(C*B); g = min(mp.mpf(1), d*T); w = (1 - sg*v/d)/2
            br = z*(1-m*m) - r*ex*m - sg*m*d*(lam**2-1)*(1-m*m)/C
            tot += w*T*(Fp(g)*lam**2*d*d*(1-m*m)/C**2 - Q(g)*br*br)
        return tot
    return mp.quad(f, [0, mp.mpf(1)/lam, mp.mpf(4)/lam, 1], [0, mp.pi/2, mp.pi])/mp.pi
def Ez_2(lam, r, z):
    e2 = mp.mpf(1)/lam**2
    def f(mu, ph):
        s = mp.sqrt(max(mp.mpf(0), 1-mu*mu)); A = (s-r)**2 + 2*r*s*(1-mp.cos(ph)); D = mp.sqrt(A + lam**2*(mu-z)**2)
        B = 1 - (1-e2)*mu*mu; k = 1 - z*mu - r*s*mp.cos(ph); g = min(mp.mpf(1), k/(D*mp.sqrt(B))); uz = lam*(mu-z)/D
        P = Fp(g); J = g*P - mp.acos(g)**2; K = g*g*P
        return mu*J - lam*mp.sqrt(B)*uz*K
    return mp.quad(f, [-1, z-mp.mpf('0.1'), z, z+mp.mpf('0.1'), 1], [0, mp.pi/2, mp.pi])/(2*mp.pi)
for lam, r, z in [(3, mp.mpf('0.5'), mp.mpf('0.3')), (4, mp.mpf('0.7'), mp.mpf('0.45'))]:
    h = mp.mpf('0.002')
    E0 = E_ref(lam, r, lam*z); Ep = E_ref(lam, r, lam*(z+h)); Em = E_ref(lam, r, lam*(z-h))
    print(f"lambda={lam} q=({r},{z}): E_z (2) {mp.nstr(Ez_2(lam,r,z),9)} vs FD {mp.nstr((Ep-Em)/(2*h),9)} | E_zz (3)-(4) {mp.nstr(Ezz_chord(lam,r,z),9)} vs FD {mp.nstr((Ep-2*E0+Em)/h**2,9)}", flush=True)
