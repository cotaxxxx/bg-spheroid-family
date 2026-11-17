"""chat V31: sampled check of phi cap constants |f_x|<=9, sigma|f_xx|<=37 (lambda in [2,5]); sampling only, not proof."""
import numpy as np
rng = np.random.default_rng(5)
def f(lam, px, pz, xi):
    k = lam*(1-px*xi[0])-pz*xi[2]            # h = lam*k
    w = np.sqrt(lam**2*(1-xi[2]**2)+xi[2]**2)
    D = np.sqrt((xi[0]-px)**2+xi[1]**2+(lam*xi[2]-pz)**2)
    g = np.clip(k/(w*D), -1, 1)
    return (k/lam)*np.arccos(g)**2
m1 = m2 = 0
for _ in range(200000):
    lam = rng.uniform(2, 5); v = rng.normal(size=3); xi = v/np.linalg.norm(v)
    R = rng.uniform(0, 0.999) ** 0.3; px = R  # equator point p=(R,0,0)
    sig = np.sqrt((xi[0]-R)**2+xi[1]**2+xi[2]**2)
    h = 1e-4*min(1, sig)
    a, b, c = f(lam, px+h, 0, xi), f(lam, px, 0, xi), f(lam, px-h, 0, xi)
    m1 = max(m1, abs((a-c)/(2*h))); m2 = max(m2, sig*abs((a-2*b+c)/h**2))
print("max|f_x| =", m1, "(claim 9)  max sigma|f_xx| =", m2, "(claim 37)")
