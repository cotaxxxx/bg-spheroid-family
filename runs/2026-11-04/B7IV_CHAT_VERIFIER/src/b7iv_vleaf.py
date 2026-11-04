"""Chat independent B7 verifier -- vectorised leaf bounds, tiling check, box verdict.

Mathematical inputs (and nothing from the producer):
  * representation H = lam*(2/pi)*Int_{[0,1]^4} sum_eps K   (v0_repr_check.py)
  * Astra lemma 1: F >= -275/4 ;  Astra lemma 2: F >= -b3[1-3rho/2]_+
  * iterated 1-D midpoint rule with exact remainder (diagonal second derivatives)
Leaf hints taken from the producer file only choose subdivisions.
"""
import numpy as np
from fractions import Fraction as Fr
from b7iv_ia import IA, JT, dn, up
import b7iv_vk as VK

KQ = Fr(275, 4)
P0 = Fr(1, 2000000)
TWO_OVER_PI = (Fr(636619772, 10**9), Fr(636619773, 10**9))   # checked with arb in selftest

def fr(x):
    return Fr(x)

def parts(pair, n):
    a, b = pair
    return [(a + (b - a) * Fr(i, n), a + (b - a) * Fr(i + 1, n)) for i in range(n)]

def sigma(p):
    return 2 * p / (1 + p * p)

def dsigma(pa, pb):
    return sigma(pb) - sigma(pa)

def dbeta_hi(ta, tb):
    # beta=2 atan t ; atan(tb)-atan(ta)=atan((tb-ta)/(1+ta tb)) <= (tb-ta)/(1+ta tb)
    return 2 * (tb - ta) / (1 + ta * tb)

def vol(cell):
    v = Fr(1)
    for a, b in cell:
        v *= b - a
    return v

def float_exact(x):
    if not np.isfinite(x):
        raise ArithmeticError('non-finite bound')
    return Fr(float(x))

# ---------------------------------------------------------------- tiling
def check_tiling(cells, domain):
    """Exact check that the boxes tile `domain` (guillotine recursion)."""
    stack = [(list(range(len(cells))), domain)]
    nodes = 0
    while stack:
        idx, reg = stack.pop(); nodes += 1
        if not idx:
            return False, 'empty region %r' % (reg,)
        if len(idx) == 1:
            if tuple(cells[idx[0]]) != tuple(reg):
                return False, 'box %d != region' % idx[0]
            continue
        found = None
        for ax in range(4):
            order = sorted(idx, key=lambda i: cells[i][ax][0])
            maxhi = None
            for k in range(len(order) - 1):
                h = cells[order[k]][ax][1]
                maxhi = h if maxhi is None or h > maxhi else maxhi
                c = cells[order[k + 1]][ax][0]
                if maxhi <= c and c > reg[ax][0]:
                    if maxhi != c:
                        return False, 'gap on axis %d' % ax
                    found = (ax, c, order[:k + 1], order[k + 1:]); break
            if found:
                break
        if not found:
            return False, 'no guillotine cut (overlap or non-guillotine)'
        ax, c, L, R = found
        rl = list(reg); rr = list(reg)
        rl[ax] = (reg[ax][0], c); rr[ax] = (c, reg[ax][1])
        for i in L:
            if not (reg[ax][0] <= cells[i][ax][0] and cells[i][ax][1] <= c):
                return False, 'box outside left region'
        stack.append((L, tuple(rl))); stack.append((R, tuple(rr)))
    return True, nodes

# ---------------------------------------------------------------- batches
def ia_cols(rows):
    """rows: list of 7-tuples of (lo,hi) Fractions -> list of 7 IA arrays."""
    cols = []
    for k in range(7):
        cols.append(IA.from_pairs([r[k] for r in rows]))
    return cols

def main_lower(outer, leaves):
    """Per leaf: lower endpoint of sum_eps K(mid) valid on all of outer."""
    rows = []; own = []; radii = []
    for li, lf in enumerate(leaves):
        mid = tuple(((a + b) / 2, (a + b) / 2) for a, b in lf['cell'])
        n = lf['outer_parts']
        for la in parts(outer[0], n[0]):
            for ta in parts(outer[1], n[1]):
                for da in parts(outer[2], n[2]):
                    sub = (la, ta, da)
                    rows.append((sub, mid)); own.append(li)
    own = np.array(own)
    V_sub = ia_cols([r[0] + r[1] for r in rows])
    V_cen = ia_cols([tuple(((a + b) / 2, (a + b) / 2) for a, b in r[0]) + r[1] for r in rows])
    point = VK.K2(V_cen).v
    direct = VK.K2(V_sub).v
    acc = point
    for i in range(3):
        d1 = VK.K2(V_sub, var=i).a
        r = IA.from_pairs([(-(s[i][1] - s[i][0]) / 2, (s[i][1] - s[i][0]) / 2) for s, _ in rows])
        acc = acc + d1 * r
    m = acc.meet(direct)
    lo = np.full(len(leaves), np.inf)
    np.minimum.at(lo, own, m.lo)
    bad = ~np.isfinite(m.lo)
    if bad.any():
        lo[np.unique(own[bad])] = -np.inf
    return lo

def rem_zeroth(outer, leaves):
    rows = []; own = []
    for li, lf in enumerate(leaves):
        for d in lf['delta_boxes']:
            for la in parts(outer[0], lf['rem_parts']):
                for ta in parts(outer[1], lf['rem_parts']):
                    rows.append(((la, ta, d),) + (lf['cell'],)); own.append(li)
    own = np.array(own)
    V = ia_cols([r[0] + tuple(r[1]) for r in rows])
    d2 = np.full((len(leaves), 4), np.inf); z = np.full(len(leaves), np.inf)
    for i in range(4):
        k = VK.K2(V, var=3 + i)
        col = np.full(len(leaves), np.inf)
        vals = np.where(np.isfinite(k.b.lo), k.b.lo, -np.inf)
        np.minimum.at(col, own, vals)
        d2[:, i] = col
        if i == 0:
            zv = np.where(np.isfinite(k.v.lo), k.v.lo, -np.inf)
            np.minimum.at(z, own, zv)
    return d2, z

def slabs(lo, hi):
    ratio = hi / lo
    n = 8 if ratio > 16 else 4 if ratio >= 3 else 2
    e = [lo]
    for k in range(1, n):
        q = Fr(float(lo) * (float(hi) / float(lo)) ** (k / n)).limit_denominator(10**15)
        assert e[-1] < q < hi
        e.append(q)
    e.append(hi)
    return list(zip(e[:-1], e[1:]))

def astra3_density_hi(V, eps):
    lam, tau, delta, y, p, t, u = V
    tt = tau.sq(); Ac = (1 - tt) / (1 + tt); Bs = 2 * tau / (1 + tt)
    x = y * (2 - y); A2 = Ac.sq(); N = 1 - A2 * x
    M = delta + (1 - delta) * A2 * x
    s = ((1 - delta) * N).sqrt(); rs = s.sqrt(); dv = M / (1 + s)
    qx = (1 - y) * Ac / N.sqrt(); qz = Bs / N.sqrt()
    pp = p.sq(); sig = 2 * p / (1 + pp); g = (1 - pp) / (1 + pp)
    tq = t.sq(); cb = eps * ((1 - tq) / (1 + tq)); sb = 2 * t / (1 + tq)
    kap = 2 * rs * sig / dv
    cp = 1 / (1 + kap.sq()).sqrt(); sp = kap * cp
    L = cp - sig * sp / rs; Jt = g * sp / rs
    ox = L * qx - Jt * cb * qz; oy = Jt * sb; oz = L * qz + Jt * cb * qx
    s2 = sig.sq()
    xx = (1 - 2 * s2) * qx - 2 * sig * g * cb * qz
    xy = 2 * sig * g * sb
    xz = (1 - 2 * s2) * qz + 2 * sig * g * cb * qx
    Hh = cp + rs * sig * sp
    l2 = lam.sq()
    V2 = (1 - (1 - l2) * oz.sq()).clamp(VK.CL, 1.0)
    U2 = (oy.sq() + l2 * oz.sq()).clamp(0.0, 1.0)
    w2 = (l2 * (xx.sq() + xy.sq()) + xz.sq()).clamp(VK.CL, 1.0)
    T2 = w2 * V2
    r_a = (l2 * Hh.sq() / T2).lo
    r_b = (l2 * cp.sq()).lo
    r0, r1, r2 = lam * xx, lam * xy, xz
    v0, v1, v2 = ox, oy, lam * oz
    c0 = r1 * v2 - r2 * v1; c1 = r2 * v0 - r0 * v2; c2 = r0 * v1 - r1 * v0
    r_c = (1 - (c0.sq() + c1.sq() + c2.sq()) / T2).lo
    rho = np.fmax(np.fmax(np.fmax(r_a, r_b), r_c), 0.0)
    rho = np.where(np.isfinite(rho), rho, 0.0)
    fac = np.maximum(0.0, up(1.0 - dn(1.5 * rho)))
    W = 4 * sig / (dv.sq() + 4 * s * s2).sqrt()
    b3 = (2 * W * w2.sqrt() * U2 / (l2 * V2 * V2.sqrt())).hi
    env = (2 * W / (l2 * lam)).hi
    b3 = np.fmin(np.fmin(b3, env), 275 / 4)          # 275/4 exact in binary
    b3 = np.where(np.isfinite(b3), np.maximum(b3, 0.0), 275 / 4)
    return np.where(fac > 0, up(b3 * fac), 0.0)

def astra3_lower(outer, leaves):
    rows = []; own = []
    sl = slabs(*outer[2])
    for li, lf in enumerate(leaves):
        for d in sl:
            rows.append(((outer[0], outer[1], d), lf['cell'])); own.append(li)
    own = np.array(own)
    V = ia_cols([r[0] + tuple(r[1]) for r in rows])
    dens = up(astra3_density_hi(V, 1) + astra3_density_hi(V, -1))
    worst = np.zeros(len(leaves))
    np.maximum.at(worst, own, dens)
    out = []
    for li, lf in enumerate(leaves):
        (ya, yb), (pa, pb), (ta, tb), (ua, ub) = lf['cell']
        area = dsigma(pa, pb) * dbeta_hi(ta, tb) * (yb - ya) * (ub - ua)
        out.append(-float_exact(worst[li]) * area)
    return out

def leaf_bounds(outer, leaves):
    """Returns list of (lower Fraction, source, dict of candidates)."""
    ml = main_lower(outer, leaves)
    d2, z = rem_zeroth(outer, leaves)
    a3 = astra3_lower(outer, leaves)
    res = []
    for li, lf in enumerate(leaves):
        cell = lf['cell']; v = vol(cell)
        cand = {}
        if np.isfinite(ml[li]) and np.all(np.isfinite(d2[li])):
            cand['MIDPOINT'] = float_exact(ml[li]) * v + sum(
                float_exact(d2[li, i]) * v * (cell[i][1] - cell[i][0]) ** 2 / 24 for i in range(4))
        if np.isfinite(z[li]):
            cand['ZEROTH'] = float_exact(z[li]) * v
        (ya, yb), (pa, pb), (ta, tb), (ua, ub) = cell
        cand['K_FLOOR'] = -2 * KQ * dsigma(pa, pb) * dbeta_hi(ta, tb) * (yb - ya) * (ub - ua)
        cand['ASTRA3'] = a3[li]
        src = max(cand, key=lambda k: cand[k])
        res.append((cand[src], src, cand))
    return res

def parse_leaf(lf, outer):
    cell = tuple((fr(a), fr(b)) for a, b in lf['cell'])
    db = lf.get('delta_boxes') or [outer]
    db = [tuple((fr(a), fr(b)) for a, b in d) for d in db]
    for d in db:
        if d[0] != outer[0] or d[1] != outer[1]:
            raise ValueError('delta box lambda/tau differ from outer')
    ds = sorted(d[2] for d in db)
    if ds[0][0] != outer[2][0] or ds[-1][1] != outer[2][1] or any(ds[i][1] != ds[i + 1][0] for i in range(len(ds) - 1)):
        raise ValueError('delta boxes do not tile outer delta')
    return {'cell': cell, 'outer_parts': tuple(int(n) for n in lf.get('outer_parts', (1, 1, 1))),
            'delta_boxes': [d[2] for d in db], 'rem_parts': int(lf.get('rem_parts', 1)),
            'uid': lf.get('uid'), 'depth': lf.get('depth', 0)}

def final_lower(outer, total):
    lam_lo, lam_hi = outer[0]
    pre = total * lam_lo * TWO_OVER_PI[0] if total >= 0 else total * lam_hi * TWO_OVER_PI[1]
    return pre - 2 * lam_hi * KQ * sigma(P0)
