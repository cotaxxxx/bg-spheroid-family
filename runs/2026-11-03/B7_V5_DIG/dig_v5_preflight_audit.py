#!/usr/bin/env python3
"""Dig V5 PREFLIGHT auditor adapted from the earlier chat B7 checker.

This is NOT an independent auditor: it is bundled with the V5 production
package and optionally imports the production kernel for sampled leaves.
Usage:
  python3 chat_b7_pass_audit.py [RESULT_JSON] [--work DIR] [--no-float] [--gauss N] [--chunk K]
Default RESULT_JSON: ~/B7_work/b7_v3/full_probe_v3/L0_T0_D0_full.json
Sections
 [1] SHA-256 of the 9 sources vs the V3 manifest, and recomputed fingerprint == cfg fingerprint
 [2] result file / leaf file consistency (status, leaf_file_sha256, cfg constants, outer box)
 [3] per-leaf bookkeeping (exact): K floor recomputed from the formula, midpoint.lo = main.lo + sum rem.lo,
     selected = max(midpoint.lo, K floor, zeroth.lo) [V4], bound_source (tie order K_FLOOR, MIDPOINT, ZEROTH), delta boxes tile the outer delta, depth, parts
 [4] exact partition proof: leaves tile y[0,1] x p[P0,1] x t[0,1] x u[0,1] with no gap/overlap (guillotine check)
 [5] aggregate + final lower recomputed with independently typed constants (KQ, P0, 7/11, 2/3)
 [6] statistics
 [7] FLOAT cross-check (numpy; NOT evidence): per-leaf 4D Gauss integral at several outer points must be
     >= the certified per-leaf lower bound; also prints the float estimate of J.
Report is printed and saved next to the result file as chat_pass_audit_<key>.txt
"""
import sys, os, json, hashlib, time, argparse
from fractions import Fraction as Q
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('result', nargs='?', default=os.path.expanduser('~/B7_work/b7_v3/full_probe_v3/L0_T0_D0_full.json'))
ap.add_argument('--work', default=None, help='folder with the source files (default: parent of the result folder)')
ap.add_argument('--no-float', action='store_true')
ap.add_argument('--gauss', type=int, default=3)
ap.add_argument('--chunk', type=int, default=1500)
ap.add_argument('--version', choices=('auto','v4','v41','v5'), default='auto', help='producer version (auto: detect from the work folder)')
ap.add_argument('--recompute', type=int, default=40, help='[8] number of sampled leaves recomputed exactly with the production kernel (0 = skip)')
args = ap.parse_args()
RES = Path(args.result).resolve()
WORK = Path(args.work).resolve() if args.work else RES.parent.parent

out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.append(s)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
bad = []
def check(cond, msg):
    if not cond: bad.append(msg); say('  FAIL:', msg)
    return cond

MANIFEST = {
 'b7_constants_v3.py': 'd96b1ef70c3c67bbf8e0acc37b7e66f174ecbbe0f1c42eb940d2d77f760590ef',
 'v3_fixed_128.py': 'ed724a764c7e3c9b01792e43ab37a68b8f62b8915a64ec663f69ce94b515bcf1',
 'v6_b7_adaptive_128.py': 'b2389bf8a908373a1d39ac25bb4be55b1581bf04584d2f8083feb2ded9324d35',
 'v6_b7_delta_local_128.py': '7f5ee03f03d256aa71628c085c4a44e8cf98ff2b0d19ff5afd094145996aece9',
 'v6_b7_hybrid_128.py': '506f1beedc753bda86b872c71b604f226fd90f8e501d572ab7f5503651e5f755',
 'v6_b7_priority_128.py': '10877b81df9bb97d5cebc9a886847d5cb5b228638efc0de1ed322d01ce4082ec',
 'v6_b7_safe_128.py': 'ff0e93dc75d8114bdfc329c3356fbe1f00f2dc91ebe2120338e1c6bd3b10d4e9',
 'v6_b_ad2_128.py': '9621a4e967f88b8e93883963e1663f101e1eb1691673fbc10ebab0ad1e02062c',
}
PRODUCERS = {'v4': ('v6_b7_unified_outerrem_v4.py', '085296d892e111f2dc6c3253edacfc3653eea8b2d0ad3203e0e0d07212f0a16f'),
             'v41': ('v6_b7_unified_outerrem_v41.py', '017cf2726efaddbb1716af7e451708a4248ad195ad6581520e48fdc817247dfe'),
             'v5': ('v6_b7_unified_outerrem_v5.py', '3e7752ef6258246aefbbefb85c0e04b8a25ec02196a585692f85d301fb7e9f8f')}
VER = args.version
if VER == 'auto':
    have = [v for v, (f, _) in PRODUCERS.items() if (WORK / f).exists()]
    if len(have) != 1: sys.exit('cannot auto-detect producer version in %s (found %s); pass --version' % (WORK, have))
    VER = have[0]
PROD_FILE, PROD_SHA = PRODUCERS[VER]
MANIFEST[PROD_FILE] = PROD_SHA
if VER == 'v5':MANIFEST['b7_constants_v5.py']='3d766084caabc5738ea3de70068d688635e6b565a0a8fbe29d14c18ccec3c9c0'
SOURCES = ('v3_fixed_128.py','v6_b_ad2_128.py','v6_b7_safe_128.py','v6_b7_adaptive_128.py','v6_b7_priority_128.py',
           'v6_b7_hybrid_128.py',PROD_FILE,'v6_b7_delta_local_128.py','b7_constants_v3.py')
if VER == 'v5':SOURCES+=('b7_constants_v5.py',)
# Independently typed constants (chat), compared with the run's cfg
S = 1 << 128
KQ = Q(275,4) if VER == 'v5' else 2*Q(11,10)*4 / Q(2,5)**8          # = 859375/64, from Qhat >= -4, W <= 2*(11/10), |V|^4 B^2 >= (2/5)^8
P0 = Q(5, 10**7)
SIG0 = 2*P0/(1+P0*P0)
DELTAS = [(Q(3,10**8),Q(1,10**4)),(Q(1,10**4),Q(1,10**2)),(Q(1,10**2),Q(1,25)),(Q(1,25),Q(4,25)),(Q(4,25),Q(15,64))]
LAMS = [(Q(2,5),Q(173,400)),(Q(173,400),Q(93,200))]
TAUS = [(Q(7,8)+Q(n,32), Q(7,8)+Q(n+1,32)) for n in range(4)]

say('=== Dig B7 V5 preflight audit (producer %s) ===' % VER, time.strftime('%Y-%m-%d %H:%M:%S'), '| python', sys.version.split()[0])
say('result', RES); say('work', WORK)

# ---------- [1]
say('\n[1] source SHA-256 vs manifest')
for n in SOURCES:
    p = WORK / n
    if not check(p.exists(), 'missing source ' + n): continue
    h = sha(p); say(f'  {n:30s} {h[:16]}…', 'MATCH' if h == MANIFEST[n] else 'DIFFERENT')
    check(h == MANIFEST[n], 'source differs from %s manifest: %s' % (VER, n))
fp = hashlib.sha256()
for n in SOURCES:
    fp.update(n.encode()); fp.update((WORK/n).read_bytes() if (WORK/n).exists() else b'')
fp = fp.hexdigest()

# ---------- [2]
say('\n[2] result / leaf file')
R = json.loads(RES.read_text())
cfg = R['config']
LF = RES.with_name(R['leaf_file'])
say('  status', R['status'], '| leaves', R['leaves'], '| final_lower', R['final_lower'], '| seconds', round(R.get('seconds_this_invocation', 0)))
check(R['status'] == 'PASS', 'status is not PASS')
lf_sha = sha(LF)
check(lf_sha == R['leaf_file_sha256'], 'leaf file SHA mismatch')
say('  leaf file', LF.name, lf_sha[:16] + '…', 'SHA MATCH' if lf_sha == R['leaf_file_sha256'] else 'SHA MISMATCH')
check(cfg['fingerprint'] == fp, 'cfg fingerprint != recomputed fingerprint of sources')
say('  fingerprint recomputed', fp[:16] + '…', 'MATCH cfg' if cfg['fingerprint'] == fp else 'DIFFERS from cfg')
check(cfg['mode'] == 'full', 'mode is not full')
check(Q(cfg['KQ']) == KQ, 'cfg KQ differs from version-specific constant')
check(Q(cfg['p_cut']) == P0 and Q(cfg['sigma_cut']) == SIG0, 'cfg p_cut/sigma_cut differ')
key = cfg['key']
i, j, k = int(key[1]), int(key[4]), int(key[7])
OUTER = (LAMS[i], TAUS[j], DELTAS[k])
outer_cfg = tuple(tuple(Q(x) for x in pr) for pr in cfg['outer'])
check(outer_cfg == OUTER, 'outer box in cfg differs from expected ' + key)
say('  key', key, '| outer', [[str(a), str(b)] for a, b in OUTER], '| bound_policy', cfg['bound_policy'])
L = json.loads(LF.read_text())
check(L['config'] == cfg, 'leaf file cfg != result cfg')
check(int(L['scale_denominator']) == S, 'scale is not 2^128')
check(L.get('schema') == 'V6-B7-LEAVES-v2', 'leaf schema is not V6-B7-LEAVES-v2')
check(cfg['bound_policy'] == ('max_midpoint_K_floor_zeroth_outerrem_v5_Astra_F_ge_minus_275_over_4' if VER == 'v5' else 'max_midpoint_K_floor_zeroth_outerrem_v4_Qhat_ge_minus4'), 'unexpected bound_policy')
leaves = L['leaves']
check(len(leaves) == R['leaves'], 'leaf count mismatch')

# ---------- [3]
say('\n[3] per-leaf exact bookkeeping (%d leaves)' % len(leaves))
def kfloor(cell):
    (ya, yb), (pa, pb), (ta, tb), (ua, ub) = cell
    sg = lambda p: 2*p/(1+p*p)
    q = -2*KQ*(sg(pb)-sg(pa))*(2*(tb-ta)/(1+ta*ta))*(yb-ya)*(ub-ua)
    return (q*S).__floor__()
tot_sel = 0; tot_main = 0; tot_rem = [0]*4
nbad = 0; uids = set(); cells = []
src_count = {}; neg = 0; pos = 0; kf_sum = 0; z_sum = 0; tot_z = 0; min_sel = None; maxdepth = 0
maxparts = tuple(cfg['max_parts'])
for lf in leaves:
    c = tuple(tuple(Q(x) for x in pr) for pr in lf['cell'])
    cells.append(c)
    ok = True
    ok &= lf['uid'] not in uids; uids.add(lf['uid'])
    ok &= all(a < b for a, b in c) and c[1][0] >= 0 and c[1][1] <= 1 and c[2][0] >= 0 and c[2][1] <= 1
    ml, mh = int(lf['main']['lo']), int(lf['main']['hi'])
    rl = [int(lf['remainder'][a]['lo']) for a in 'yptu']; rh = [int(lf['remainder'][a]['hi']) for a in 'yptu']
    tl, th = int(lf['total']['lo']), int(lf['total']['hi'])
    ok &= ml <= mh and all(a <= b for a, b in zip(rl, rh))
    ok &= tl == ml + sum(rl) and th == mh + sum(rh)
    kf = kfloor(c)
    ok &= kf == int(lf['k_floor_raw'])
    zl, zh = int(lf['zeroth']['lo']), int(lf['zeroth']['hi'])
    ok &= zl <= zh
    src, sel = max((('K_FLOOR', kf), ('MIDPOINT', tl), ('ZEROTH', zl)), key=lambda e: e[1])
    ok &= sel == int(lf['selected_lower_raw'])
    ok &= lf['bound_source'] == src
    ok &= lf['depth'] <= cfg['depth']; maxdepth = max(maxdepth, lf['depth'])
    ok &= len(lf['outer_parts']) == 3 and all(1 <= a <= b for a, b in zip(lf['outer_parts'], maxparts))
    ok &= lf['rem_parts'] in (1, 2, 4) and lf['rem_parts'] <= cfg['max_rem_parts']
    db = sorted(tuple(tuple(Q(x) for x in pr) for pr in b) for b in lf['delta_boxes'])
    ok &= len(db) <= cfg['max_delta'] and len(db)*lf['rem_parts']**2 <= cfg['max_rem_kernel_boxes']
    ok &= all(b[0] == OUTER[0] and b[1] == OUTER[1] for b in db)
    ok &= db[0][2][0] == OUTER[2][0] and db[-1][2][1] == OUTER[2][1]
    ok &= all(db[n][2][1] == db[n+1][2][0] for n in range(len(db)-1)) and all(b[2][0] < b[2][1] for b in db)
    if not ok:
        nbad += 1
        if nbad <= 5: say('  bad leaf uid', lf['uid'])
    tot_sel += sel; tot_main += ml
    for a in range(4): tot_rem[a] += rl[a]
    src_count[lf['bound_source']] = src_count.get(lf['bound_source'], 0) + 1
    if sel < 0: neg += sel
    else: pos += sel
    if lf['bound_source'] == 'K_FLOOR': kf_sum += sel
    if lf['bound_source'] == 'ZEROTH': z_sum += sel
    tot_z += zl
    min_sel = sel if min_sel is None else min(min_sel, sel)
check(nbad == 0, '%d leaves fail bookkeeping' % nbad)
say('  leaves failing bookkeeping:', nbad, '| max depth', maxdepth)

# ---------- [4]
say('\n[4] exact partition proof of the inner domain')
t0 = time.time()
DOM = ((Q(0), Q(1)), (P0, Q(1)), (Q(0), Q(1)), (Q(0), Q(1)))
n = len(cells)
rank = []
for a in range(4):
    vals = sorted({c[a][0] for c in cells} | {c[a][1] for c in cells} | {DOM[a][0], DOM[a][1]})
    m = {v: r for r, v in enumerate(vals)}
    rank.append(m)
    check(vals[0] == DOM[a][0] and vals[-1] == DOM[a][1], 'leaves leave the domain on axis %d' % a)
lo = [[rank[a][c[a][0]] for a in range(4)] for c in cells]
hi = [[rank[a][c[a][1]] for a in range(4)] for c in cells]
top = (tuple(rank[a][DOM[a][0]] for a in range(4)), tuple(rank[a][DOM[a][1]] for a in range(4)))
stack = [(list(range(n)), top)]
part_ok = True; nodes = 0
while stack and part_ok:
    idx, (blo, bhi) = stack.pop(); nodes += 1
    if len(idx) == 1:
        q = idx[0]
        if tuple(lo[q]) != blo or tuple(hi[q]) != bhi: part_ok = False; say('  leaf does not fill its region (gap), uid', leaves[q]['uid'])
        continue
    best = None
    for a in range(4):
        srt = sorted(idx, key=lambda q: lo[q][a])
        pm = -1; half = len(srt)/2
        for kk in range(1, len(srt)):
            pm = max(pm, hi[srt[kk-1]][a])
            if pm <= lo[srt[kk]][a]:
                cut = lo[srt[kk]][a]
                if pm < cut or not (blo[a] < cut < bhi[a]): continue   # gap or degenerate; keep searching
                score = abs(kk - half)
                if best is None or score < best[0]: best = (score, a, kk, srt, cut)
    if best is None: part_ok = False; say('  no separating cut for a group of', len(idx), 'leaves (overlap or gap)'); break
    _, a, kk, srt, cut = best
    l_hi = list(bhi); l_hi[a] = cut; r_lo = list(blo); r_lo[a] = cut
    stack.append((srt[:kk], (blo, tuple(l_hi)))); stack.append((srt[kk:], (tuple(r_lo), bhi)))
check(part_ok, 'leaves do not partition the inner domain')
say('  PARTITION', 'PASS' if part_ok else 'FAIL', '| tree nodes', nodes, '| %.1fs' % (time.time()-t0))

# ---------- [5]
say('\n[5] aggregate and final lower (independent constants)')
check(tot_sel == int(L['aggregate_raw']['total_lower']), 'sum of selected != aggregate_raw.total_lower')
check(Q(tot_sel, S) == Q(R['total_lower']), 'sum of selected != result total_lower')
check(tot_main == int(L['aggregate_raw']['main_lower']), 'sum of main.lo mismatch')
check(tot_z == int(L['aggregate_raw']['zeroth_lower']), 'sum of zeroth.lo mismatch')
J = Q(tot_sel, S)
lam_lo, lam_hi = OUTER[0]
pref = J*lam_lo*Q(7,11) if J >= 0 else J*lam_hi*Q(2,3)       # 7/11 < 2/pi < 2/3
loss = 2*lam_hi*KQ*SIG0                                      # contact strip p in [0,P0]: F >= -KQ, beta range pi
final = pref - loss
check(loss == Q(R['contact_loss_upper']), 'contact loss mismatch')
check(final == Q(R['final_lower']) == Q(L['final_lower']), 'final lower mismatch')
check(Q(7,11) < 2/Q(314159266,10**8) and Q(3) < Q(314159265,10**8), '2/pi bracket: 7/11 < 2/pi < 2/3 (3.14159265 < pi < 3.14159266)')
say('  J lower (sum selected) =', float(J), '| exact matches result:', Q(tot_sel, S) == Q(R['total_lower']))
say('  prefactor part        =', float(pref))
say('  contact loss          =', float(loss))
say('  FINAL LOWER           =', float(final), '(exact rational recomputed, matches result:', final == Q(R['final_lower']), ')')
say('  FINAL LOWER > 0       :', final > 0)
check(final > 0, 'final lower not positive')

# ---------- [6]
say('\n[6] statistics')
say('  bound source counts', src_count)
say('  sum positive selected %.6g | sum negative selected %.6g | sum over K-floor leaves %.6g | sum over ZEROTH leaves %.6g' % (pos/S, neg/S, kf_sum/S, z_sum/S))
say('  minimum selected per leaf %.4g' % (min_sel/S))
say('  margin: final lower / contact loss = %.3g' % float(final/loss))

# ---------- [7]
if not args.no_float:
    say('\n[7] FLOAT cross-check (numpy, NOT evidence): Gauss-%d^4 per leaf, kappa form' % args.gauss)
    try:
        import numpy as np
        def F(y, p, t, u, eps, lam, tau, dl):
            A = (1-tau**2)/(1+tau**2); Bt = 2*tau/(1+tau**2)
            x = y*(2-y); N = 1-A*A*x; M = dl+(1-dl)*A*A*x
            s = np.sqrt((1-dl)*N); qx = (1-y)*A/np.sqrt(N); qz = Bt/np.sqrt(N)
            sg = 2*p/(1+p*p); g = (1-p*p)/(1+p*p)
            cb = eps*(1-t*t)/(1+t*t); sb = 2*t/(1+t*t)
            dv = M/(1+s); kap = 2*np.sqrt(s)*sg/dv; c = 1/np.sqrt(1+kap**2); sn = kap*c
            W = 4*sg/np.sqrt(dv**2+4*s*sg**2)
            Lc = c-sg*sn/np.sqrt(s); Jc = g*sn/np.sqrt(s)
            ox = Lc*qx-Jc*cb*qz; oy = Jc*sb; oz = Lc*qz+Jc*cb*qx
            xx = (1-2*sg**2)*qx-2*sg*g*cb*qz; xy = 2*sg*g*sb; xz = (1-2*sg**2)*qz+2*sg*g*cb*qx
            H = c+np.sqrt(s)*sg*sn
            V2 = ox**2+oy**2+lam**2*oz**2; U2 = V2-ox**2
            w = np.sqrt(lam**2*(xx**2+xy**2)+xz**2); T = w*np.sqrt(V2); G = lam*H
            E = -s*qx*Jc**2*sb**2-s*Jc*cb*oz+(1-lam**2)*xx*oz**2
            P = H*H*U2; Rr = E*E; uu = u*u
            Bh = (1+uu)*T+(1-uu)*G
            num = (1+uu)*T*(P-2*Rr)+(1-uu)*G*(P-Rr)
            jac = 2*(1-p*p)/(1+p*p)**2*2/(1+t*t)
            return W*jac*num/(V2**2*Bh**2)
        xg, wg = np.polynomial.legendre.leggauss(args.gauss)
        G4 = np.array(np.meshgrid(*([xg]*4), indexing='ij')).reshape(4, -1)
        W4 = np.prod(np.array(np.meshgrid(*([wg]*4), indexing='ij')).reshape(4, -1), axis=0)
        lo_f = np.array([[float(a) for a, b in c] for c in cells]); hi_f = np.array([[float(b) for a, b in c] for c in cells])
        sel_f = np.array([int(lf['selected_lower_raw'])/S for lf in leaves])
        zlo_f = np.array([int(lf['zeroth']['lo'])/S for lf in leaves])
        dmid = (float(OUTER[2][0])*float(OUTER[2][1]))**0.5
        pts = [('lam_lo,tau_lo,delta_lo', float(OUTER[0][0]), float(OUTER[1][0]), float(OUTER[2][0])),
               ('lam_hi,tau_hi,delta_hi', float(OUTER[0][1]), float(OUTER[1][1]), float(OUTER[2][1])),
               ('center (delta geometric mid)', float(sum(OUTER[0])/2), float(sum(OUTER[1])/2), dmid)]
        for name, lam, tau, dl in pts:
            t0 = time.time(); est = np.empty(n); fmin = np.empty(n)
            for s0 in range(0, n, args.chunk):
                a = lo_f[s0:s0+args.chunk]; b = hi_f[s0:s0+args.chunk]
                h = (b-a)/2; m = (a+b)/2
                X = m[:, :, None] + h[:, :, None]*G4[None, :, :]
                f = F(X[:, 0], X[:, 1], X[:, 2], X[:, 3], 1.0, lam, tau, dl) + F(X[:, 0], X[:, 1], X[:, 2], X[:, 3], -1.0, lam, tau, dl)
                est[s0:s0+args.chunk] = (f*W4).sum(axis=1)*np.prod(h, axis=1)
                fmin[s0:s0+args.chunk] = f.min(axis=1)*np.prod(b-a, axis=1)
            fin = np.isfinite(est)
            viol = sel_f - est
            tol = 1e-12 + 1e-6*np.abs(est)
            nv = int(np.sum(fin & (viol > tol)))
            say(f'  [{name}] J_float = {np.sum(est[fin]):.6f} | nonfinite {int((~fin).sum())} | leaves with certified lower > float integral: {nv}'
                + (f' (max excess {viol[fin].max():.3g}, sum excess {viol[fin & (viol > tol)].sum():.3g})' if nv else '') + f' | {time.time()-t0:.0f}s')
            zv = zlo_f - fmin; zt = 1e-12 + 1e-6*np.abs(fmin); nz = int(np.sum(np.isfinite(fmin) & (zv > zt)))
            say(f'      ZEROTH pointwise check: leaves with zeroth.lo > |K|*min_nodes(sum_eps F): {nz}' + (f' (max excess {zv[np.isfinite(fmin)].max():.3g})' if nz else ''))
            say(f'      float 𝓘 estimate without contact strip ≈ (2λ/π)·J_float = {2*lam/np.pi*np.sum(est[fin]):.6f}')
    except ImportError:
        say('  numpy not available; skipped (rerun after: pip install numpy --break-system-packages)')

# ---------- [8]
if args.recompute > 0:
    say('\n[8] exact recomputation of sampled leaves with the PRODUCTION kernel (consistency of recorded values; uses production code)')
    try:
        import random
        sys.path.insert(0, str(WORK))
        import importlib; P = importlib.import_module(PROD_FILE[:-3])
        from v6_b7_hybrid_128 import main_interval
        from v6_b7_safe_128 import kernel
        from v3_fixed_128 import I as PI, iv as piv, mulq_interval as pmul, S as PS
        check(PS == S, 'production scale differs')
        rng = random.Random(20261102)
        def pick(cond, k):
            c = [q for q in range(n) if cond(leaves[q])]; rng.shuffle(c); return c[:k]
        q4 = max(1, args.recompute // 4)
        chosen = []
        for cond in (lambda l: l['rem_parts'] == 4, lambda l: len(l['delta_boxes']) > 1,
                     lambda l: l['bound_source'] == 'ZEROTH', lambda l: l['bound_source'] == 'K_FLOOR',
                     lambda l: tuple(l['outer_parts']) != (1, 1, 1)):
            for q in pick(cond, q4):
                if q not in chosen: chosen.append(q)
        for q in pick(lambda l: True, args.recompute):
            if len(chosen) >= args.recompute + 4*q4: break
            if q not in chosen: chosen.append(q)
        t0 = time.time(); nfail = 0
        for q in chosen:
            lf = leaves[q]; c = cells[q]
            vol = Q(1)
            for a_, b_ in c: vol *= b_ - a_
            db = [tuple(tuple(Q(x) for x in pr) for pr in b) for b in lf['delta_boxes']]
            main = pmul(main_interval(OUTER, c, tuple(lf['outer_parts'])), vol)
            rows = []
            for sub in P.lambda_tau_boxes(db, lf['rem_parts']):
                row = []; z = piv(0)
                for i_ in range(4):
                    h = piv(0)
                    for e in (1, -1):
                        k_ = kernel(sub, c, e, ('inner', i_)); h = h + k_.d2
                        if i_ == 0: z = z + k_.v
                    row.append(h)
                rows.append(row + [z])
            rem = [pmul(PI.raw(min(r[i_].lo for r in rows), max(r[i_].hi for r in rows)), vol*(c[i_][1]-c[i_][0])**2/Q(24)) for i_ in range(4)]
            zz = pmul(PI.raw(min(r[4].lo for r in rows), max(r[4].hi for r in rows)), vol)
            got = [(main.lo, main.hi)] + [(r.lo, r.hi) for r in rem] + [(zz.lo, zz.hi)]
            rec = [(int(lf['main']['lo']), int(lf['main']['hi']))] + [(int(lf['remainder'][a_]['lo']), int(lf['remainder'][a_]['hi'])) for a_ in 'yptu'] + [(int(lf['zeroth']['lo']), int(lf['zeroth']['hi']))]
            if got != rec:
                nfail += 1; say('  MISMATCH uid', lf['uid'], 'rem_parts', lf['rem_parts'], 'delta boxes', len(db), 'outer_parts', lf['outer_parts'])
        from collections import Counter
        say('  recomputed', len(chosen), 'leaves | rem_parts', dict(Counter(leaves[q]['rem_parts'] for q in chosen)),
            '| multi-delta', sum(len(leaves[q]['delta_boxes']) > 1 for q in chosen), '| sources', dict(Counter(leaves[q]['bound_source'] for q in chosen)),
            '| mismatches', nfail, '| %.0fs' % (time.time()-t0))
        check(nfail == 0, '%d sampled leaves differ from exact production recomputation' % nfail)
    except Exception as e:
        check(False, 'section 8 could not run: ' + repr(e))

say('\n=== VERDICT (sections 1-5 and 8, exact):', 'ALL CHECKS PASS' if not bad else 'FAIL: ' + '; '.join(bad), '===')
rep = RES.with_name('dig_v5_preflight_audit_%s_%s.txt' % (VER, key))
rep.write_text('\n'.join(out) + '\n'); print('saved:', rep)
