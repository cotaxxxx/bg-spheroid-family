"""chat: non-interval checks of Codex identities (4) and (6) and the gradient trace (1), numpy Gauss-Legendre."""
import numpy as np
from chat_tri_centre import PQ
def grid(n):
    xm, wm = np.polynomial.legendre.leggauss(n); xp, wp = np.polynomial.legendre.leggauss(2*n)
    MU, PH = np.meshgrid(xm, np.pi*(xp + 1)); W = np.outer(wp, wm)*np.pi/(4*np.pi)
    S_ = np.sqrt(1 - MU**2); return np.stack([S_*np.cos(PH), S_*np.sin(PH), MU]), W
def parts(Ld, q, X):
    v = X - q[:, None, None]; k = 1 - np.einsum('i,i...->...', q, X)
    Dv = Ld[:, None, None]*v; D = np.sqrt((Dv**2).sum(0)); S = np.sqrt(((X/Ld[:, None, None])**2).sum(0))
    g = np.clip(k/(D*S), 0, 1); return v, k, D, S, g
def E(Ld, q, X, W):
    v, k, D, S, g = parts(Ld, q, X); return float((k*np.arccos(g)**2*W).sum())
def grad(Ld, q, X, W):
    v, k, D, S, g = parts(Ld, q, X); P, Q = PQ(g); J = g*P - np.arccos(g)**2; K = g*g*P; u = Ld[:, None, None]*v/D
    return np.array([float(((X[i]*J - Ld[i]*S*u[i]*K)*W).sum()) for i in range(3)])
X, W = grid(400)
Ld = np.array([1.0, 1.5, 3.0]); q = np.array([0.3, 0.2, 0.1])
gr = grad(Ld, q, X, W); h = 1e-5
fd = np.array([(E(Ld, q + h*e, X, W) - E(Ld, q - h*e, X, W))/(2*h) for e in np.eye(3)])
print("(1) gradient trace vs central difference of E:", gr, fd, "max diff", np.abs(gr - fd).max())
G = gr/q; A = Ld**2
v, k, D, S, g = parts(Ld, q, X); P, Q = PQ(g); B = S**2
for i, j in [(0, 1), (0, 2), (1, 2)]:
    lhs = q[i]*q[j]*(G[j] - G[i]); rhs = (A[j] - A[i])*float((k*P*g*(v[i]*v[j]/D**2 - X[i]*X[j]/(A[i]*A[j]*B))*W).sum())
    print(f"(4) pair {i+1}{j+1}: lhs {lhs:.12f}  rhs {rhs:.12f}")
# (6) and its derivation: d/d eps E along L = diag(1, e^eps, 3 e^eps) at q = r e1 vs finite difference in eps of E on the circle
for r in (208/256, 0.82393827, 216/256):
    Ld0 = np.array([1.0, 1.0, 3.0]); q = np.array([r, 0, 0]); v, k, D, S, g = parts(Ld0, q, X); P, Q = PQ(g)
    n = (X/Ld0[:, None, None])/S; u = Ld0[:, None, None]*v/D
    c = 0.5*float((k*P*g*(n[0]**2 - n[1]**2 - u[0]**2 + u[1]**2)*W).sum())
    eps = 1e-5
    def Eeps(e, phi):
        L = np.array([1.0, np.exp(e), 3*np.exp(e)]); qq = np.array([r*np.cos(phi), r*np.sin(phi), 0]); return E(L, qq, X, W)
    d0 = (Eeps(eps, 0) - Eeps(-eps, 0))/(2*eps); d90 = (Eeps(eps, np.pi/2) - Eeps(-eps, np.pi/2))/(2*eps)
    print(f"(6) r={r:.8f}: c = {c:.8f};  (dE/deps(phi=0) - dE/deps(phi=pi/2))/2 = {(d0 - d90)/2:.8f}")
