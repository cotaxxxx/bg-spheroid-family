"""chat V57: non-interval independent checks (numpy/mpmath, no Codex code).
(a) near-sphere formula E'(r)/r vs finite difference of E(r e3) on the sphere;
(b) Newton for the crossing Z1 ∩ B2: h1(s,t) = 0 (centre Hessian) and b2(s,t) = E2(e2) = 0 (full gradient trace at the pole e2)."""
import numpy as np
from mpmath import mp, mpf, quad, acos, sqrt, asin
mp.dps = 25
def PQ(g):
    g = np.clip(g, 0, 1); a = np.arccos(g); sa = np.sin(a); small = a < 1e-3
    P = np.where(small, 2 + a*a/3, 2*a/np.where(small, 1, sa))
    dP = np.where(small, -2/3 - 2*a*a/15, -2*(sa - a*np.cos(a))/np.where(small, 1, sa)**3)
    return P, 2*P + g*dP
# (a) sphere: E(r) = 1/2 int_{-1}^{1} k arccos^2(k/D) dmu,  k = 1 - r mu, D = sqrt(1 - 2 r mu + r^2)
def Esph(r): return quad(lambda m: (1 - r*m)*acos((1 - r*m)/sqrt(1 - 2*r*m + r*r))**2, [-1, 1])/2
def Pm(g): a = acos(g); return 2 if a == 0 else 2*a/mp.sin(a)
def form(r): return quad(lambda m: (1 - m*m)*Pm((1 - r*m)/sqrt(1 - 2*r*m + r*r))*(2 - r*m - r*r)/(2*(1 - 2*r*m + r*r)**1.5), [-1, 1])/2
def _main_a():
    print("(a) near-sphere formula E'(r)/r:")
    for r in (mpf('0.2'), mpf('0.5'), mpf('0.9')):
        h = mpf('1e-8'); fd = (Esph(r + h) - Esph(r - h))/(2*h)/r
        print(f"   r={r}: formula {mp.nstr(form(r), 14)}  finite-diff {mp.nstr(fd, 14)}  (>= 1/24 = 0.041667)")
# (b) crossing
def octant(N):
    x, w = np.polynomial.legendre.leggauss(N); th = (x + 1)*np.pi/4; wt = w*np.pi/4
    TH, PH = np.meshgrid(th, th, indexing='ij'); W = np.outer(wt, wt)*np.sin(TH)/(np.pi/2)   # octant mean
    return np.stack([np.sin(TH)*np.cos(PH), np.sin(TH)*np.sin(PH), np.cos(TH)]), W
def h1(s, t, G):
    X, W = G; Ld = np.array([1, s, s*t]); A = Ld**2; w = X**2
    d = np.einsum('i,i...->...', A, w); B = np.einsum('i,i...->...', 1/A, w); g = 1/np.sqrt(d*B); P, Q = PQ(g); R = A[0]/d
    return float((g*(P*R*(1 - R*w[0]) - Q*w[0]*(1 - R)**2)*W).sum())
def polegrid(N, M):
    xf, wf = np.polynomial.legendre.leggauss(N); f = (xf + 1)/2; wf = wf/2
    xp, wp = np.polynomial.legendre.leggauss(M); ph = (xp + 1)*np.pi/4; wp = wp*np.pi/4
    F, PH = np.meshgrid(f, ph, indexing='ij'); W = np.outer(wf, wp)*4*F*4/(4*np.pi)   # 4f df dphi/(4pi), 4 quadrants
    return F, PH, W
def b2(s, t, G):
    F, PH, W = G; Ld = np.array([1, s, s*t]); c = np.sqrt(1 - F*F)
    w = np.stack([c*np.cos(PH), -F, c*np.sin(PH)])          # v = 2 f w
    xi = np.stack([2*F*c*np.cos(PH), 1 - 2*F*F, 2*F*c*np.sin(PH)])
    Lw = Ld[:, None, None]*w; nLw = np.sqrt((Lw**2).sum(0)); u = Lw/nLw
    S = np.sqrt(((xi/Ld[:, None, None])**2).sum(0)); g = F/(nLw*S); P, Q = PQ(g)
    J = g*P - np.arccos(np.clip(g, 0, 1))**2; K = g*g*P
    return float(((xi[1]*J - Ld[1]*S*u[1]*K)*W).sum())
def _main_b():
    for (N, M) in ((192, 192), (384, 384)):
        GO = octant(N); GP = polegrid(N, M)
        x = np.array([1.566969, 2.296586])
        for it in range(8):
            Fv = np.array([h1(*x, GO), b2(*x, GP)]); e = 1e-6
            J = np.array([[(h1(x[0] + e, x[1], GO) - h1(x[0] - e, x[1], GO))/(2*e), (h1(x[0], x[1] + e, GO) - h1(x[0], x[1] - e, GO))/(2*e)],
                          [(b2(x[0] + e, x[1], GP) - b2(x[0] - e, x[1], GP))/(2*e), (b2(x[0], x[1] + e, GP) - b2(x[0], x[1] - e, GP))/(2*e)]])
            dx = np.linalg.solve(J, -Fv); x = x + dx
            if np.abs(dx).max() < 1e-14: break
        det = J[0, 0]*J[1, 1] - J[0, 1]*J[1, 0]
        print(f"(b) N={N}: crossing s={x[0]:.12f} t={x[1]:.12f}  |F|={np.abs(Fv).max():.1e}  J={J.round(5).tolist()}  Delta=h1s*b2t-h1t*b2s={det:.6f}")
    print("    Codex enclosure [1.566967567136, 1.566969483971] x [2.296584862724, 2.296587050977]")
    # sanity: rotational edge values
    GO = octant(384); GP = polegrid(384, 384)
    print("sanity h1(1, 4.724383) ~ 0:", h1(1, 4.724383, GO), "  b2(1, 2.065382) ~ 0:", b2(1, 2.065382, GP), "  b2(1.553891, 1)?", b2(1.553891, 1, GP))
if __name__ == "__main__":
    _main_a(); _main_b()
