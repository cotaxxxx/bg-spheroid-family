"""chat diagnostic (float, not proof): pointwise cancellation in the integrand, co-rotating frame vs lab frame.
For E(p) = (1/4pi) int k acos^2(gamma) dOmega at box-2 centre (R=3/4, tau=1/8, lam=2559/512), compare
L1 norms of pointwise derivatives with the size of the integrated derivative."""
import numpy as np
lam = 2559/512; R = 0.75; tau = 1/8; beta = 2*np.arctan(tau)
n1, n2 = 1200, 2400
psi = (np.arange(n1)+0.5)*np.pi/n1; th = (np.arange(n2)+0.5)*2*np.pi/n2
PS, TH = np.meshgrid(psi, th, indexing="ij"); w = np.sin(PS)*(np.pi/n1)*(2*np.pi/n2)/(4*np.pi)
# eta in contact-centred coordinates (contact direction e_x)
eh, ey, ev = np.cos(PS), np.sin(PS)*np.sin(TH), np.sin(PS)*np.cos(TH)
def f_lab(px, pz, X):   # X = fixed lab-frame unit vectors
    xi0, xi1, xi2 = X; k = 1 - (px*xi0 + (pz/lam)*xi2)
    D = np.sqrt((xi0-px)**2 + xi1**2 + (lam*xi2-pz)**2); B = np.sqrt(xi0**2+xi1**2+xi2**2/lam**2)
    return k*np.arccos(np.clip(k/(D*B), -1, 1))**2
def f_rot(b):
    c, s = np.cos(b), np.sin(b); X = (c*eh - s*ev, ey, s*eh + c*ev)
    return f_lab(R*c, lam*R*s, X)
h = 1e-4
# co-rotating: d/dbeta and d2/dbeta2 at fixed eta
fp, f0, fm = f_rot(beta+h), f_rot(beta), f_rot(beta-h)
d1, d2 = (fp-fm)/(2*h), (fp-2*f0+fm)/h**2
print(f"co-rotating: int f_b = {np.sum(d1*w):+.5f}  L1(f_b) = {np.sum(abs(d1)*w):.4f}  | int f_bb = {np.sum(d2*w):+.5f}  L1(f_bb) = {np.sum(abs(d2)*w):.4f}")
# lab frame: same beta-derivative but surface fixed in the lab: X = O_beta0 eta (fixed), p moves with beta
c0, s0 = np.cos(beta), np.sin(beta); X = (c0*eh - s0*ev, ey, s0*eh + c0*ev)
g = lambda b: f_lab(R*np.cos(b), lam*R*np.sin(b), X)
gp, g0, gm = g(beta+h), g(beta), g(beta-h)
e1, e2 = (gp-gm)/(2*h), (gp-2*g0+gm)/h**2
print(f"lab frame:   int f_b = {np.sum(e1*w):+.5f}  L1(f_b) = {np.sum(abs(e1)*w):.4f}  | int f_bb = {np.sum(e2*w):+.5f}  L1(f_bb) = {np.sum(abs(e2)*w):.4f}")
# --- W-mode integrand (R3 'middle' route): f_b/(R^2 s c); its tau-derivative, L1 vs integral
x = tau; dbdx = 2/(1+x*x); sc = np.sin(beta)*np.cos(beta)
dW_mid = (d2*dbdx/(R*R*sc) - d1*(np.cos(2*beta)/sc)*dbdx/(R*R*sc))
print(f"W-mode d/dtau: int = {np.sum(dW_mid*w):+.5f}  L1 = {np.sum(abs(dW_mid)*w):.3f}  (Codex box-2 cells: signed -0.417, L1 134)")
# --- R4 method C: reflection-averaged F(t), t = sin^2 beta; W = 2/R^2 int dF/dt
def F_t(t):
    b = np.arcsin(np.sqrt(t)); c, s = np.cos(b), np.sin(b)
    Xp = (c*eh - s*ev, ey, s*eh + c*ev); Xm = (c*eh + s*ev, ey, s*eh - c*ev)
    return (f_lab(R*c, lam*R*s, Xp) + f_lab(R*c, lam*R*s, Xm))/2
t0 = np.sin(beta)**2; ht = 1e-4; dtdx = 2*np.sin(beta)*np.cos(beta)*dbdx
Fp, F0, Fm = F_t(t0+ht), F_t(t0), F_t(t0-ht)
k1 = 2/R**2*(Fp-Fm)/(2*ht); k2 = 2/R**2*(Fp-2*F0+Fm)/ht**2*dtdx
print(f"method C:    W = int kernel = {np.sum(k1*w):+.5f}  L1(kernel) = {np.sum(abs(k1)*w):.3f} | d/dtau: int = {np.sum(k2*w):+.5f}  L1 = {np.sum(abs(k2)*w):.3f}")
# --- lab-frame W = lam^2 E_z/z - E_rho/rho (fixed surface points, base point moves); integrand and its tau-derivative
def wlab(b, X):
    rho, z = R*np.cos(b), lam*R*np.sin(b); hh = 1e-5
    fz = (f_lab(rho, z+hh, X) - f_lab(rho, z-hh, X))/(2*hh); fr = (f_lab(rho+hh, z, X) - f_lab(rho-hh, z, X))/(2*hh)
    return lam**2*fz/z - fr/rho
Xl = (c0*eh - s0*ev, ey, s0*eh + c0*ev)     # lab grid = co-rotated grid frozen at beta0 (contact at the grid pole)
hb = 1e-3
wl0 = wlab(beta, Xl); dwl = (wlab(beta+hb, Xl) - wlab(beta-hb, Xl))/(2*hb)*dbdx
print(f"lab lam^2V-H: W = {np.sum(wl0*w):+.5f}  L1(kernel) = {np.sum(abs(wl0)*w):.3f} | d/dtau: int = {np.sum(dwl*w):+.5f}  L1 = {np.sum(abs(dwl)*w):.3f}")
# where is the pointwise L1 mass of the tau-derivative (method C kernel)?  bins in contact angle psi and |xi_z|
X = (c0*eh - s0*ev, ey, s0*eh + c0*ev); xz = np.abs(X[2])
A = abs(k2)*w; tot = A.sum()
for lo, hi in ((0, .25), (.25, .5), (.5, 1), (1, 2), (2, np.pi+1)):
    m = (PS >= lo) & (PS < hi); print(f"  psi in [{lo},{hi}): L1 share {A[m].sum()/tot:5.1%}, area share {w[m].sum():5.1%}, signed {np.sum((k2*w)[m]):+.3f}")
for lo, hi in ((0, .9), (.9, .98), (.98, 1.01)):
    m = (xz >= lo) & (xz < hi); print(f"  |xi_z| in [{lo},{hi}): L1 share {A[m].sum()/tot:5.1%}, area share {w[m].sum():5.1%}, signed {np.sum((k2*w)[m]):+.3f}")
