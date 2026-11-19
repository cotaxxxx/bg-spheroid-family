"""Non-interval reference values (mpmath quadrature). For cross-checks only, never as proof input."""
import mpmath as mp


def ez_ref(lam, rho, z, dps=20):
    """E_z by (2) at a point, in the same normalization as kernels.ez_lower."""
    mp.mp.dps = dps; lam = mp.mpf(lam); rho = mp.mpf(rho); z = mp.mpf(z); e2 = 1/lam**2
    def f(mu, ph):
        s = mp.sqrt(max(1-mu*mu, 0)); c = mp.cos(ph)
        D = mp.sqrt((s-rho)**2 + 2*rho*s*(1-c) + lam**2*(mu-z)**2)
        B = e2 + (1-e2)*(1-mu*mu); rB = mp.sqrt(B); k = 1 - z*mu - rho*s*c
        g = min(max(k/(D*rB), 0), 1); a = mp.acos(g); P = 2*a/mp.sin(a) if a > 0 else mp.mpf(2)
        return mu*(g*P - a*a) - lam*rB*(lam*(mu-z)/D)*(g*g*P)
    bp = [-1, z-0.05, z-0.005, z, z+0.005, z+0.05, 1]
    return mp.quad(f, bp, [0, 0.005, 0.05, 0.5, mp.pi])/(2*mp.pi)


def ez_axis_sphere(r, dps=25):
    """lambda = 1, rho = 0: E_z(0, r) by a one-dimensional quadrature of (2) (accurate to ~1e-15)."""
    mp.mp.dps = dps; r = mp.mpf(r)
    def f(mu):
        D = mp.sqrt(1 - 2*r*mu + r*r); g = min((1 - r*mu)/D, 1); a = mp.acos(g)
        P = 2*a/mp.sin(a) if a > 0 else mp.mpf(2)
        return mu*(g*P - a*a) - ((mu - r)/D)*g*g*P
    return mp.quad(f, [-1, r, 1], maxdegree=10)/2


def sphere_axis_taylor2(r):
    """Two-term Taylor expansion of E_z(0, r)/r on the sphere: 4/3 - 8 r^2/9.
    NOT exact: the remainder is about -0.084 r^4 near r = 0 and -0.13 r^4 near r = 1
    (sphere_axis_check.log; V51 erratum E2). Use it to check normalization, not as a bound."""
    return mp.mpf(4)/3 - 8*mp.mpf(r)**2/9
