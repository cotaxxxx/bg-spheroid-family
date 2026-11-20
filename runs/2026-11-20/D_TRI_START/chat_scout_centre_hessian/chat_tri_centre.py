"""chat: independent scout of the centre Hessian of the triaxial family (DIAGNOSTIC_ONLY, non-interval).
Chord form (3) at q = 0: v = 0, d = 1, l = 1 on both sides, T = (C B)^(-1/2) with C = |L e|^2, B = |L^-T e|^2:
  E_ii(0) = < T [ P(T) L_ii^2/C (1 - L_ii^2 e_i^2/C) - Q(T) e_i^2 (1 - L_ii^2/C)^2 ] >_e.
L = diag(1, s, s t)."""
import numpy as np
def PQ(g):
    g = np.clip(g, 0, 1); a = np.arccos(g); sa = np.sin(a); small = a < 1e-3
    P = np.where(small, 2 + a*a/3, 2*a/np.where(small, 1, sa))
    dP = np.where(small, -2/3 - 2*a*a/15, -2*(sa - a*np.cos(a))/np.where(small, 1, sa)**3)  # dP/dg
    return P, 2*P + g*dP
xm, wm = np.polynomial.legendre.leggauss(96); xp, wp = np.polynomial.legendre.leggauss(192)
MU, PH = np.meshgrid(xm, np.pi*(xp + 1)); W = np.outer(wp, wm)*np.pi/(4*np.pi)   # dmu dphi / (4 pi)
S_ = np.sqrt(1 - MU**2); E = np.stack([S_*np.cos(PH), S_*np.sin(PH), MU])
def hess_centre(s, t):
    Ld = np.array([1.0, s, s*t]); C = np.einsum('i,i...->...', Ld**2, E**2); B = np.einsum('i,i...->...', Ld**-2, E**2)
    T = 1/np.sqrt(C*B); P, Q = PQ(T); out = []
    for i in range(3):
        Li2 = Ld[i]**2; ei2 = E[i]**2
        f = T*(P*Li2/C*(1 - Li2*ei2/C) - Q*ei2*(1 - Li2/C)**2); out.append(float((f*W).sum()))
    return out
if __name__ == '__main__':
    print("checks against the rotational family (reference-ball normalization):")
    print("  sphere", hess_centre(1, 1), "expect 4/3 each")
    print("  oblate lambda=0.5 -> L=diag(1,2,2) ~ diag(0.5,1,1): axial (x) expect 0.236973*scale, transverse 1.58874*scale")
    print("   ", hess_centre(2, 1))
    print("  prolate lambda=4.724383 (s=1, t=lambda): transverse h1=h2 expect ~0", hess_centre(1, 4.724383))
