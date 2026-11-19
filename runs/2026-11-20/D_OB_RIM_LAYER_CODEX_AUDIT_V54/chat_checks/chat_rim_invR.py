import mpmath as mp
mp.mp.dps = 20
# <1/|xi_h - p|> over the sphere with breakpoints at the two singular points mu = +-sqrt(1 - rho^2), phi = 0,
# and in a polar chart around p on the projected disc (independent second method).
for rho in ('0.5', '0.9', '0.99'):
    rho = mp.mpf(rho); m0 = mp.sqrt(1 - rho*rho)
    f = lambda mu, ph: 1/mp.sqrt((mp.sqrt(1 - mu*mu)*mp.cos(ph) - rho)**2 + (1 - mu*mu)*mp.sin(ph)**2)
    bp = sorted(set([-1, -m0, 0, m0, 1]))
    v1 = mp.quad(f, bp, [0, mp.mpf('1e-3'), mp.mpf('1e-2'), mp.mpf('0.1'), mp.pi], maxdegree=10)/(2*mp.pi)
    # polar chart around p: x = rho + R cos t, y = R sin t; m = sqrt(1 - x^2 - y^2); two faces, weight 1/m; (1/4pi)*2*int (1/R)(1/m) R dR dt
    def g(t):
        c = mp.cos(t); Rmax = -rho*c + mp.sqrt(1 - rho*rho*mp.sin(t)**2)
        return mp.quad(lambda R: 1/mp.sqrt(max(1 - (rho + R*c)**2 - (R*mp.sin(t))**2, mp.mpf('1e-60'))), [0, Rmax])
    v2 = mp.quad(g, [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])/(2*mp.pi)
    print(mp.nstr(rho, 3), 'sphere-quad', mp.nstr(v1, 12), ' polar-chart', mp.nstr(v2, 12), ' pi/2', mp.nstr(mp.pi/2, 12), flush=True)
