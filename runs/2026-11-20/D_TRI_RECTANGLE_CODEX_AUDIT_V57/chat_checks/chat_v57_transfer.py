"""chat V57 S4/S5: rational re-check of transfer.csv against the V50 ledgers, and of the Krawczyk inclusion (cross.csv numbers)."""
import csv, gzip, hashlib, io, sys, zipfile
from fractions import Fraction as Q
OUT, INP, V50ZIP = sys.argv[1], sys.argv[2], sys.argv[3]
# provenance: bundled V50 ledgers == chat-held V50 zip members
z = zipfile.ZipFile(V50ZIP); names = {n.split('/')[-1]: n for n in z.namelist() if '/N3/E' in n and n.endswith('.tsv.gz')}
same = all(open(f"{INP}/v50/E{k:02d}.tsv.gz", 'rb').read() == z.read(names[f"E{k:02d}.tsv.gz"]) for k in range(12))
print("provenance: 12 bundled V50 ledgers byte-identical to chat-held V50 zip:", same, len(names))
led = {}
for k in range(12):
    for r in csv.DictReader(io.StringIO(gzip.open(f"{INP}/v50/E{k:02d}.tsv.gz", 'rt').read()), delimiter='\t'):
        led[(f"E{k:02d}.tsv.gz", r['path'])] = r
U36 = Q(1, 2**36); eps = Q(1, 2**39); C4 = 40*32*24*32**4
rows = list(csv.DictReader(open(f"{OUT}/transfer.csv"))); bad = []; minrem = {}
leaves = [(k, v) for k, v in led.items() if v['action'] not in ('splitr', 'splitl', 'split')]
for r in rows:
    cand = [v for (src, p), v in leaves if src == r['source'] and r['path'].startswith(p) and int(v['l0']) <= int(r['t0']) and int(r['t1']) <= int(v['l1'])
            and int(v['r0']) <= int(r['r0']) and int(r['r1']) <= int(v['r1'])]
    if len(cand) != 1: bad.append(('nobox', r['source'], r['path'], len(cand))); continue
    v = cand[0]; mode = r['mode']; marg = Q(r['edge_margin']); err = Q(r['error']); rem = Q(r['remaining'])
    alo, ahi, bhi = int(v['alo'])*U36, int(v['ahi'])*U36, int(v['bhi'])*U36
    # chat's reading of the V50 leaf: H_positive -> kappa lower bound a_lo; radial_curvature_negative -> -E_rr upper b_hi;
    # radial_decreasing (T = E_yyyy = 3 kappa'/r) -> -a_hi/3
    act = v['action']; exp_m = {'H_positive': alo, 'radial_curvature_negative': -bhi, 'radial_decreasing': -ahi/3}.get(act)
    want_mode = {'H_positive': ('kappa_positive',), 'radial_curvature_negative': ('Hii_negative',), 'radial_decreasing': ('outer_slope', 'centre_slope')}.get(act, ())
    r0 = Q(int(r['r0']), 2**20)
    exp_e = {'kappa_positive': 50000*eps, 'Hii_negative': 50000*eps, 'outer_slope': (100000*eps/r0**2) if r0 > 0 else None, 'centre_slope': Q(C4, 3)*eps}[mode]
    if mode == 'outer_slope' and r0 < Q(1, 32): bad.append(('outer_slope below 1/32', r['path']))
    if mode == 'centre_slope' and Q(int(r['r1']), 2**20) > Q(1, 32): bad.append(('centre_slope above 1/32', r['path']))
    if mode not in want_mode: bad.append(('mode', r['path'], mode, act))
    if exp_m is None or marg != exp_m: bad.append(('margin', r['source'], r['path'], mode, act, float(marg), None if exp_m is None else float(exp_m)))
    if exp_e is None or err < exp_e: bad.append(('error', r['path'], mode, float(err), exp_e))
    if rem != marg - err or rem <= 0: bad.append(('remaining', r['path']))
    minrem[mode] = min(minrem.get(mode, rem), rem)
print("transfer rows", len(rows), "problems", len(bad)); [print("  ", b) for b in bad[:12]]
print("min remaining by mode:", {k: float(v) for k, v in minrem.items()})
# coverage of [2,5] x [0,1] by the boxes (excluding r<=1/32 centre_slope duplicates if they overlap)
from collections import Counter
print("modes", Counter(r['mode'] for r in rows))
boxes = sorted({(int(r['t0']), int(r['t1']), int(r['r0']), int(r['r1'])) for r in rows})
area = sum((b[1]-b[0])*(b[3]-b[2]) for b in boxes); target = (5-2)*2**20 * 2**20
# overlap test by sweeping a fine grid of the coarsest common resolution
xs = sorted({b[0] for b in boxes} | {b[1] for b in boxes}); ys = sorted({b[2] for b in boxes} | {b[3] for b in boxes})
cov = 0; over = 0; holes = 0
for i in range(len(xs)-1):
    for j in range(len(ys)-1):
        cx, cy = (xs[i]+xs[i+1])/2, (ys[j]+ys[j+1])/2
        n = sum(1 for b in boxes if b[0] < cx < b[1] and b[2] < cy < b[3])
        if n == 0 and 2*2**20 < cx < 5*2**20 and 0 < cy < 2**20: holes += 1
        if n > 1: over += 1
print(f"distinct boxes {len(boxes)}, area/target = {Q(area, target)}, holes {holes}, overlapping cells {over}")
cs = [r for r in rows if r['mode'] == 'centre_slope']; print("centre_slope boxes:", sorted({(r['t0'], r['t1'], r['r0'], r['r1']) for r in cs})[:8])
# S5 Krawczyk (chat's own rational code from the ledger intervals)
c = list(csv.DictReader(open(f"{OUT}/cross.csv")))
iv = lambda r: (Q(float(r['lower'])), Q(float(r['upper'])))
F = {int(r['mode']): iv(r) for r in c if r['derivative'] == '0' and r['N'] == '512'}
Fp = {(int(r['mode']), int(r['derivative'])): iv(r) for r in c if r['N'] == '1024' and r['derivative'] != '0'}
Y = [[Q(-164, 100), Q(189, 100)], [Q(-26, 100), Q(-480, 100)]]; m = [Q(1566969, 10**6), Q(2296586, 10**6)]; rad = Q(1, 1000)
def mul(a, b): p = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]; return (min(p), max(p))
def sc(y, a): return (min(y*a[0], y*a[1]), max(y*a[0], y*a[1]))
def add(*xs): return (sum(x[0] for x in xs), sum(x[1] for x in xs))
for i in range(2):
    YF = add(sc(Y[i][0], F[0]), sc(Y[i][1], F[1]))
    row = []
    for j in range(2):
        e = add(sc(Y[i][0], Fp[(0, j+1)]), sc(Y[i][1], Fp[(1, j+1)])); e = (Q(int(i == j)) - e[1], Q(int(i == j)) - e[0]); row.append(max(abs(e[0]), abs(e[1])))
    norm = sum(row); K = (m[i] - YF[1] - norm*rad, m[i] - YF[0] + norm*rad)
    print(f"Krawczyk row {i+1}: row-sum {float(norm):.6f} (<1: {norm < 1}), image [{float(K[0]):.9f}, {float(K[1]):.9f}] inside ({float(m[i]-rad):.6f}, {float(m[i]+rad):.6f}): {m[i]-rad < K[0] and K[1] < m[i]+rad}")
