"""chat estimate (float, mesh only): cells needed with R3's GLOBAL B bound (1/lam^2 everywhere)
versus a LOCAL B bound per cell (B = 1 - e xi_z^2, xi_z bounded on the cell). Not an enclosure; a cost estimate."""
import math
def count(R, tau, lam, local, ratio=0.25, bu=32, bv=64):
    beta = 2*math.atan(tau); cb, sb = math.cos(beta), math.sin(beta); e = 1-1/lam**2
    pend = [((i/bu, (i+1)/bu), (j/bv, (j+1)/bv)) for i in range(bu) for j in range(bv)]; n = 0
    while pend:
        (u0, u1), (v0, v1) = pend.pop()
        du, dv = u1-u0, v1-v0
        q = lambda u: 8*u*u/(1+u*u)**2
        spmax = min(1, 4*u1, 4*(1-u0)); a = 4*du; b = 22/7*spmax*dv; diam = a+b
        qlo = q(u0); star = min(R, max(R, 1-qlo)); ds = (1-star)**2+2*star*qlo
        if local:   # max |xi_z| over the cell, from corner/edge samples plus the diameter as margin
            zs = []
            for uu in (u0, (u0+u1)/2, u1):
                for vv in (v0, (v0+v1)/2, v1):
                    psi = 4*math.atan(uu); h = math.cos(psi); vz = math.sin(psi)*math.cos(math.pi*vv)
                    zs.append(abs(sb*h+cb*vz))
            zmax = min(1, max(zs)+diam); Bl = 1-e*zmax**2
        else:
            Bl = 1/lam**2
        if diam**2 <= ratio**2*min(ds/lam**2, Bl): n += 1; continue
        if a >= b: m = (u0+u1)/2; pend += [((u0, m), (v0, v1)), ((m, u1), (v0, v1))]
        else: m = (v0+v1)/2; pend += [((u0, u1), (v0, m)), ((u0, u1), (m, v1))]
    return n
for lam in (2, 3.5, 5):
    g = count(0.5, 0.5, lam, False); l = count(0.5, 0.5, lam, True)
    print(f"lam={lam}: global-B cells {g}, local-B cells {l}, ratio {g/l:.1f}")
