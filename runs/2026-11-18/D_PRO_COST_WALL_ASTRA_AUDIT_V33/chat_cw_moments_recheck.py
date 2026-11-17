"""chat V33: (C1)(C2) recheck with the endpoint-regular substitution z = (1+cos phi)/2 (dz/sqrt(z(1-z)) = dphi).
The first run used direct mp.quad on the 1/sqrt endpoint singularity and missed the 1e-25 tolerance by quadrature error (~5e-23)."""
import mpmath as mp
mp.mp.dps = 40
ok = True
for zeta in (mp.mpf(2), mp.mpf(-1), mp.mpc(0.5, 0.3), mp.mpc(-3, 2)):
    lhs = mp.quad(lambda ph: 1/(zeta - (1+mp.cos(ph))/2), [0, mp.pi])/mp.pi
    r = mp.sqrt(zeta*(zeta-1)); r = r if mp.re(r/zeta) > 0 else -r
    e = abs(lhs - 1/r); ok &= e < mp.mpf(10)**-30; print(f"(C2) zeta={mp.nstr(zeta,3)}: err {mp.nstr(e,3)}")
for j in range(8):
    e = abs(mp.quad(lambda ph: ((1+mp.cos(ph))/2)**j, [0, mp.pi])/mp.pi - mp.binomial(2*j, j)/mp.mpf(4)**j); ok &= e < mp.mpf(10)**-30
print("(C1)(C2) recheck:", "PASS" if ok else "FAIL")
