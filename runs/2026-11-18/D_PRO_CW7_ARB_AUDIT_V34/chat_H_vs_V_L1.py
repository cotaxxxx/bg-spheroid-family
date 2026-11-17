"""chat diagnostic (float, not proof): at box-2 centre, split W = lam^2 V - H and compare the pointwise
cancellation of the horizontal part H = E_rho/rho (no z-derivative) with the z part lam^2 V = lam^2 E_z/z."""
import numpy as np
exec(open(__import__('sys').argv[1]).read().split("h = 1e-4")[0])     # grid + f_lab from chat_frame_L1.py
c0, s0 = np.cos(beta), np.sin(beta); X = (c0*eh - s0*ev, ey, s0*eh + c0*ev)
def parts(b):
    rho, z = R*np.cos(b), lam*R*np.sin(b); hh = 1e-5
    fz = (f_lab(rho, z+hh, X) - f_lab(rho, z-hh, X))/(2*hh); fr = (f_lab(rho+hh, z, X) - f_lab(rho-hh, z, X))/(2*hh)
    return fr/rho, lam**2*fz/z
dbdx = 2/(1+tau*tau); hb = 1e-3
H0, V0 = parts(beta); Hp, Vp = parts(beta+hb); Hm, Vm = parts(beta-hb)
for name, k0, kp, km in (("H = E_rho/rho      ", H0, Hp, Hm), ("lam^2 V = lam^2 E_z/z", V0, Vp, Vm), ("W = lam^2 V - H    ", V0-H0, Vp-Hp, Vm-Hm)):
    d = (kp-km)/(2*hb)*dbdx
    print(f"{name}: value {np.sum(k0*w):+9.4f}  L1 {np.sum(abs(k0)*w):8.3f} | d/dtau {np.sum(d*w):+9.4f}  L1 {np.sum(abs(d)*w):9.3f}  ratio {np.sum(abs(d)*w)/max(abs(np.sum(d*w)),1e-12):8.1f}")
