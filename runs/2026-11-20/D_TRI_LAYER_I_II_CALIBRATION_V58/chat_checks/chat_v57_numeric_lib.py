"""chat non-interval references for the V57 self-tests (numpy Gauss-Legendre)."""
import numpy as np
from chat_v57_numeric import PQ, octant, polegrid
def hi(i, s, t, G):
    X, W = G; Ld = np.array([1, s, s*t]); A = Ld**2; w = X**2
    d = np.einsum('i,i...->...', A, w); B = np.einsum('i,i...->...', 1/A, w); g = 1/np.sqrt(d*B); P, Q = PQ(g); R = A[i-1]/d
    return float((g*(P*R*(1 - R*w[i-1]) - Q*w[i-1]*(1 - R)**2)*W).sum())
def bi(i, s, t, G):
    F, PH, W = G; Ld = np.array([1, s, s*t]); c = np.sqrt(1 - F*F); j, k = [a for a in range(3) if a != i-1]
    w = np.zeros((3,) + F.shape); xi = np.zeros_like(w)
    w[i-1] = -F; w[j] = c*np.cos(PH); w[k] = c*np.sin(PH)
    xi[i-1] = 1 - 2*F*F; xi[j] = 2*F*c*np.cos(PH); xi[k] = 2*F*c*np.sin(PH)
    Lw = Ld[:, None, None]*w; nLw = np.sqrt((Lw**2).sum(0)); u = Lw/nLw
    S = np.sqrt(((xi/Ld[:, None, None])**2).sum(0)); g = F/(nLw*S); P, Q = PQ(g)
    J = g*P - np.arccos(np.clip(g, 0, 1))**2; K = g*g*P
    return float(((xi[i-1]*J - Ld[i-1]*S*u[i-1]*K)*W).sum())
_x, _w = np.polynomial.legendre.leggauss(1200); _xp, _wp = np.polynomial.legendre.leggauss(400)
def _tau_raw(t, r):
    MU, PH = np.meshgrid(_x, (_xp + 1)*np.pi/4, indexing='ij'); W = np.outer(_w, _wp*np.pi/4)/np.pi
    s1 = np.sqrt(1 - MU**2); Y = (s1*np.cos(PH))**2; Z = (s1*np.sin(PH))**2; m = MU - r
    d = m*m + Y + t*t*Z; B = MU**2 + Y + Z/(t*t); k = 1 - r*MU; g = k/np.sqrt(d*B); P, Q = PQ(g)
    return float((k*g*P*((m*m - Y)/d - (MU**2 - Y)/B)*W).sum())
def tau(t, r): return _tau_raw(t, r)
def tau2(t, r, h=1e-3): return (_tau_raw(t, r + h) - 2*_tau_raw(t, r) + _tau_raw(t, r - h))/h**2

# V58 references: general q, full-sphere Gauss-Legendre with the contact point handled by a chart centred at q/|q| when |q|=1
def _sphere(n):
    x, w = np.polynomial.legendre.leggauss(n); xp, wp = np.polynomial.legendre.leggauss(2*n)
    MU, PH = np.meshgrid(x, np.pi*(xp + 1), indexing='ij'); W = np.outer(w, wp)*np.pi/(4*np.pi)
    s = np.sqrt(1 - MU**2); return np.stack([s*np.cos(PH), s*np.sin(PH), MU]), W
def general(kind, s, t, q, n=600):
    X, W = _sphere(n); Ld = np.array([1, s, s*t]); q = np.asarray(q, float)
    v = X - q[:, None, None]; k = 1 - np.einsum('i,i...->...', q, X); Lv = Ld[:, None, None]*v; Dn = np.sqrt((Lv**2).sum(0))
    S = np.sqrt(((X/Ld[:, None, None])**2).sum(0)); g = np.clip(k/(Dn*S), 0, 1); P, Q = PQ(g); F = np.arccos(g)**2; u = Lv/Dn
    if kind == "E3": f = X[2]*(g*P - F) - Ld[2]*S*u[2]*g*g*P
    if kind == "T12": n_ = X/Ld[:, None, None]/S; f = k*g*P*(u[0]*u[1] - n_[0]*n_[1])
    if kind == "H33": b3 = Ld[2]*u[2]; z3 = X[2] - g*S*b3; f = (P*(g*S)**2*(Ld[2]**2 - b3**2) - Q*z3**2)/(Dn*S)
    return float((f*W).sum())
