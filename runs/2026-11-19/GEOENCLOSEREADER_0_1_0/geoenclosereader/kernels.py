"""Independent Arb kernels for the volume-preserving prolate spheroid family (lambda >= 1).

Reference ball |q| <= 1, q = (rho, 0, z) by rotational symmetry, L = diag(1, 1, lambda), eps = 1/lambda.
E(q) = <k alpha^2>,  k = 1 - q.xi,  alpha = arccos(gamma),  gamma = k/(D sqrt B),
D = |L(xi - q)|,  B = |L^-T xi|^2 = eps^2 + (1 - eps^2)(1 - mu^2).
Spherical averages <.> are probability averages; by symmetry phi in [0, pi].

Formulas (audited in V48-V51):
 (2)  gradient trace  E_i = < xi_i J - L_ii sqrt(B) u_i K >,  J = gamma P - arccos^2 gamma,  K = gamma^2 P,
      u = L(xi - q)/D.  Here only i = z (axial) is used:  E_z = < mu J - lambda sqrt(B) u_z K >.
 (3)  chord representation of E_ii (directions e, m = e_z, v = q.e, delta = 1 - |q|^2, d = sqrt(delta + v^2),
      l_s = d - s v, w_s = (1 - s v/d)/2, C = |L e|^2, T_s = (C B_s)^(-1/2)):
      E_ii = < sum_s w_s T_s [ P(d T_s) L_ii^2 d^2/C (1 - L_ii^2 e_i^2/C) - Q(d T_s) {q_i + s e_i (l_s - L_ii^2 d/C)}^2 ] >
 (4)  i = z bracket written as  z(1 - m^2) - rho e_x m - s m d (lambda^2 - 1)(1 - m^2)/C.
 (9)  boundary trace on the equator |q| = 1:
      H_b = < T t^2 [ P(tT) c (1 - j c) - Q(tT) j (2 - c)^2 ] >  over t in [0,1], phi in [0, pi],
      m^2 = (1 - t^2) cos^2 phi, j = (1 - t^2) sin^2 phi, B = 1 - 4(1 - lambda^-2) t^2 m^2, c = 1/C, T = sqrt(c/B).
 Equator relations (6): H = E_rho/rho = E_yy,  E_xx = H + rho H_rho = d(rho H)/d rho.

All clips below are valid for every q in the closed ball, so a bound holds on box ∩ ball.
"""
from flint import arb, fmpq
from .interval import clip, sqrtp, sq, acos_safe, U01, PI, box_arbs
from .series import P_enc, Q_enc

# ---------------------------------------------------------------- grids
GRID_EZ = {   # (2): mu cells NM, phi cells NP; band |mu - z| < BAND refined: mu x SUBM, phi k < KR x SUBR, k = 0 x SUB0
    "v50": dict(NM=256, NP=48, SUBM=16, KR=1, SUBR=1, SUB0=1, BAND=fmpq(1, 8)),
    "v51b": dict(NM=256, NP=48, SUBM=16, KR=1, SUBR=1, SUB0=32, BAND=fmpq(1, 8)),
    "fine": dict(NM=1024, NP=192, SUBM=4, KR=16, SUBR=4, SUB0=16, BAND=fmpq(1, 4)),
}
GRID_CHORD = {"v50": dict(NM=512, NPSI=64), "fine": dict(NM=1024, NPSI=128)}
GRID_HB = {"v50": dict(NT=512, NPHI=64), "fine": dict(NT=2048, NPHI=256)}
_cache = {}


def _cells_ez(z0, z1, NM, NP, SUBM, KR, SUBR, SUB0, BAND):
    out = []
    for i in range(NM):
        m0 = -1 + fmpq(2*i, NM); m1 = -1 + fmpq(2*(i+1), NM)
        band = (m1 > z0 - BAND and m0 < z1 + BAND); sub = SUBM if band else 1
        for j in range(sub):
            mu = arb(m0 + (m1-m0)*fmpq(j, sub)).union(arb(m0 + (m1-m0)*fmpq(j+1, sub))); w = (m1-m0)/sub
            for k in range(NP):
                ns = (SUB0 if k == 0 else SUBR if k < KR else 1) if band else 1
                for r in range(ns):
                    out.append((mu, PI*(arb(k*ns + r)+U01)/(NP*ns), w/ns))
    return out


def ez_lower(box, grid="fine"):
    """Lower bound of E_z over box ∩ ball by (2)."""
    g_ = GRID_EZ[grid] if isinstance(grid, str) else grid
    (l0, l1, r0, r1, z0, z1), lam, rho, z = box_arbs(box); e2 = 1/(lam*lam); tot = arb(0)
    for mu, ph, wm in _cells_ez(z0, z1, **g_):
        s = sqrtp(clip(1-mu*mu, 0, 1)); c = ph.cos()
        A = sq(s-rho) + 2*rho*s*clip(1-c, 0, 2); D2 = A + lam*lam*sq(mu-z)
        B = clip(clip(1-(1-e2)*mu*mu, 0, 1), e2.lower(), 1); rB = B.sqrt()
        if D2.lower() > 0:
            D = D2.sqrt(); k = 1 - z*mu - rho*s*c
            g = clip(k/(D*rB), 0, 1); uz = clip(lam*(mu-z)/D, -1, 1)
        else:                       # contact cell: a-priori ranges, valid on the closed ball
            g = U01; uz = 2*U01 - 1
        P = P_enc(g); J = g*P - acos_safe(g)**2; K = g*g*P
        tot += arb((mu*J - lam*rB*uz*K).lower())*arb(wm)
    return (tot*(PI/g_["NP"])/(2*PI)).lower()


def _chord_cells(NM, NPSI):
    key = ("chord", NM, NPSI)
    if key not in _cache:
        _cache[key] = [((arb(i)+U01)/NM, PI*(arb(k)+U01)/NPSI) for i in range(NM) for k in range(NPSI)]
    return _cache[key]


def chord_bound(box, comp, want, grid="v50"):
    """Lower ('lower') or upper ('upper') bound of E_ii, i in {'x','y','z'}, over box ∩ ball by (3)/(4).
    Sides s = +-1 are combined with w_+ + w_- = 1:  lower = L_max - sup(w_smaller)(L_max - L_min)."""
    g_ = GRID_CHORD[grid] if isinstance(grid, str) else grid
    _, lam, rho, z = box_arbs(box); e2 = 1/(lam*lam); L2 = lam*lam
    dl = clip(1 - sq(rho) - sq(z), 0, 1); tot = arb(0); cells = _chord_cells(g_["NM"], g_["NPSI"])
    for m, psi in cells:
        s = sqrtp(clip(1-m*m, 0, 1)); ex = s*psi.cos(); ey = s*psi.sin()
        v = rho*ex + z*m; d = sqrtp(clip(dl + sq(v), 0, 4)); C = 1 + (L2-1)*m*m
        bs = []; ws = []
        for sg in (1, -1):
            l = d - sg*v; xz = z + sg*l*m; xr2 = sq(rho + sg*l*ex) + sq(l*ey)
            B1 = e2 + (1-e2)*clip(1-sq(xz), 0, 1); B2 = e2 + (1-e2)*clip(xr2, 0, 1)
            B = clip(B1, B2.lower(), B2.upper()) if B1.overlaps(B2) else B1
            T = 1/(C*B).sqrt(); g = clip(d*T, 0, 1)
            w = clip((1 - sg*v/d)/2, 0, 1) if d.lower() > 0 else U01
            if comp == 'z':
                br = z*(1-m*m) - rho*ex*m - sg*m*d*(L2-1)*(1-m*m)/C
                val = T*(P_enc(g)*L2*d*d*(1-m*m)/(C*C) - Q_enc(g)*sq(br))
            else:
                ei = ey if comp == 'y' else ex; qi = 0 if comp == 'y' else rho
                br = qi + sg*ei*(l - d/C)
                val = T*(P_enc(g)*d*d/C*(1 - sq(ei)/C) - Q_enc(g)*sq(br))
            bs.append(val); ws.append(w)
        if want == 'lower':
            a_, b_ = bs[0].lower(), bs[1].lower()
            val = (arb(b_) - arb(ws[0].upper())*(arb(b_) - arb(a_))) if a_ <= b_ else (arb(a_) - arb(ws[1].upper())*(arb(a_) - arb(b_)))
            tot += arb(val.lower())
        else:
            a_, b_ = bs[0].upper(), bs[1].upper()
            val = (arb(b_) + arb(ws[0].upper())*(arb(a_) - arb(b_))) if a_ >= b_ else (arb(a_) + arb(ws[1].upper())*(arb(b_) - arb(a_)))
            tot += arb(val.upper())
    r = tot/len(cells)
    return r.lower() if want == 'lower' else r.upper()


def hb_lower(box, grid="v50"):
    """Lower bound of the boundary-equator trace H_b over the lambda-interval of box by (9)."""
    g_ = GRID_HB[grid] if isinstance(grid, str) else grid
    NT, NPHI = g_["NT"], g_["NPHI"]
    _, lam, _, _ = box_arbs(box); e2 = 1/(lam*lam); L2 = lam*lam; tot = arb(0)
    for i in range(NT):
        t = (arb(i)+U01)/NT
        for k in range(NPHI):
            ph = PI*(arb(k)+U01)/NPHI; co = ph.cos(); si = ph.sin()
            m2 = (1 - t*t)*sq(co); j = (1 - t*t)*sq(si); C = 1 + (L2-1)*m2; c = 1/C
            B = clip(1 - 4*(1-e2)*t*t*m2, e2.lower(), 1); T = (c/B).sqrt(); g = clip(t*T, 0, 1)
            tot += arb((T*t*t*(P_enc(g)*c*(1 - j*c) - Q_enc(g)*j*sq(2 - c))).lower())
    return (tot/(NT*NPHI)).lower()
