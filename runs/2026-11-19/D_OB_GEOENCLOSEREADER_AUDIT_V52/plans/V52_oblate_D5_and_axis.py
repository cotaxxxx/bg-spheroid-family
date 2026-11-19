"""V52 plan (fixed before run): GeoEncloseReader 0.2.0 on the oblate D-OB evidence. DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Inputs: V4 run1 output (v4_run_out.jsonl.gz, ZIP V4_RUN1_EVIDENCE_20261111.zip), V4_LOWEST20 TSV,
Plan B run1 output (planb_run_out.jsonl, sha256 ec1fd135...).
Selection (seed 52): V4 lowest 20 + random 40; Plan B lowest 20 + random 40; centre column r <= 1/8 all 26 lambda strips;
thin collar r in [59999/60000, 1] random 40 of the tau 32 x lambda 26 grid; axial landmarks (point boxes).
Claims: D5 boxes H = E_yy > 0 (chord ladder v50 -> fine, depth 6, polar bisection).
Landmarks: E_zz(0,0) < 0 at 2/5, > 0 at 83/200 (lambda_c); E_z(0,1/2) < 0 at 699/1600, > 0 at 281/640 (lambda_x);
E_z(0,1) (pole trace) < 0 at 5/8, > 0 at 33/50 (lambda_partial). Confirmed iff the declared sign holds.
"""
import sys, json, random, multiprocessing as mp
from fractions import Fraction as F
from flint import fmpq
from geoenclosereader import oblate_d5 as O, kernels as K

def landmark(item):
    name, kind, lam, z, sign = item; q = lambda x: fmpq(x.numerator, x.denominator); L = q(F(lam)); Z = q(F(z))
    box = (L, L, fmpq(0), fmpq(0), Z, Z)
    if kind == 'Ezz':
        v = K.chord_bound(box, 'z', 'lower' if sign > 0 else 'upper', 'fine')
    else:
        v = K.ez_bound(box, 'lower' if sign > 0 else 'upper', 'fine')
    ok = (v > 0) if sign > 0 else (v < 0)
    return {"leaf": name, "quantity": kind, "lambda": lam, "z": z, "sign": sign, "confirmed": bool(ok), "bound": float(v)}

def d5(item):
    name, pb = item; return O.verify_polar(name, pb)

if __name__ == '__main__':
    v4p, low20, pbp, out = sys.argv[1:5]; rng = random.Random(52); items = []
    v4 = O.final_leaves(v4p); byname = {r['box']['name']: r for r in v4}
    lows = [ln.split('\t')[0] for ln in open(low20).read().splitlines()[1:]]
    items += [("V4low:" + n, O.polar_from_record(byname[n]['box'])) for n in lows]
    rest = [r for r in v4 if r['box']['name'] not in set(lows)]
    items += [("V4rand:" + r['box']['name'], O.polar_from_record(r['box'])) for r in rng.sample(rest, 40)]
    pb = O.final_leaves(pbp); pbs = sorted(pb, key=lambda r: F(r['H_lower']))
    items += [("PBlow:" + r['box']['name'], O.polar_from_record(r['box'])) for r in pbs[:20]]
    items += [("PBrand:" + r['box']['name'], O.polar_from_record(r['box'])) for r in rng.sample(pbs[20:], 40)]
    LAM = [F(2, 5) + F(k, 100) for k in range(27)]; TAU = [F(i, 32) for i in range(33)]
    items += [("centre:l%02d" % m, (F(0), F(1, 8), F(0), F(1), LAM[m], LAM[m + 1])) for m in range(26)]
    grid = [(i, m) for i in range(32) for m in range(26)]
    items += [("collar:t%02d_l%02d" % (i, m), (F(59999, 60000), F(1), TAU[i], TAU[i + 1], LAM[m], LAM[m + 1])) for i, m in rng.sample(grid, 40)]
    marks = [("lc_lo", 'Ezz', '2/5', '0', -1), ("lc_hi", 'Ezz', '83/200', '0', +1), ("lx_lo", 'Ez', '699/1600', '1/2', -1),
             ("lx_hi", 'Ez', '281/640', '1/2', +1), ("ld_lo", 'Ez', '5/8', '1', -1), ("ld_hi", 'Ez', '33/50', '1', +1)]
    n = 0; ok = 0
    with open(out, 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(landmark, marks):
            n += 1; ok += r['confirmed']; f.write(json.dumps(r) + '\n'); f.flush(); print(r['leaf'], r['confirmed'], r['bound'], flush=True)
        for r in pool.imap(d5, items):
            n += 1; ok += r['confirmed']; f.write(json.dumps(r) + '\n'); f.flush(); print(r['leaf'], r['confirmed'], r['grid_used'], r['attempts'][-1]['min'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
