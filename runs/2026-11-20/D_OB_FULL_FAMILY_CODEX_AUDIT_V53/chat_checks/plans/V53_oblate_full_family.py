"""V53 plan (fixed before run): GeoEncloseReader 0.2.0 on Codex D_OB_FULL_FAMILY (zip sha256 4ef5785b...).
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Ledger rows: path mode l0 l1 r0 r1 z0 z1 n k lo hi blo bhi action (box units 2^-20, values 2^-36).
Groups of terminal 'sign' rows (seed 53): for each group the 5 weakest (smallest lo for positive claims, largest hi
for negative claims) and 10 random; small-lambda groups (thin, mixed, recovered, rim; lambda <= 1/8) 3 weakest + 5 random.
Reader 0.2.1 (fixed before this run): oblate boxes use the corner hull for B in the chord kernels (0.2.0 gave NaN for
lambda <= 1/8: e2 + (1 - e2) X with a wide e2 ball), and graded m-cells (m = 1 - (1 - t)^p) resolve small C near m = 1.
  H groups (claim H = E_yy > 0, chord (3) i = y, ladder v50 (depth 6) -> graded (depth 3) -> graded_fine (depth 2)):
    low/16H-31H, finer/*H, window/*H, leaves/21H-31H, thin/*H, mixed/*H, recovered/*H, salvage/*H (all 8)
  X groups (claim E_rho > 0 with rho0 > 0; checked as H > 0, equivalent there): mixed/*H X rows, recovered/*H X rows,
    rim.tsv X rows
  V groups (axis E_z sign = sign of the producer interval; 1-D ez_axis_bound, (N, refine) = (16384, 32) -> (65536, 64)):
    leaves/*V, finer/*V, low/*V
  Z groups (axis E_zz sign; 1-D ezz_axis_bound N = 2048 -> 8192): leaves/*Z, finer/*Z, low/*Z
Bisection depth <= 6 (H: score d lambda, 4 d rho, 4 d z; axis: t first while t-width >= 8 x lambda-width).
Sub-boxes whose lower-left corner is outside the open ball are dropped. Confirmed iff every child has the sign.
"""
import sys, glob, json, random, time, multiprocessing as mp
from flint import fmpq
from geoenclosereader import kernels as K
U = 2**20

def rows(pattern, modes):
    out = []
    for fn in sorted(glob.glob(pattern)):
        for ln in open(fn):
            p = ln.split()
            if len(p) == 16: p = [p[0] + ":" + p[1]] + p[2:]   # rim.tsv carries the tree name in front
            if len(p) < 15 or p[1] not in modes or p[-1] != 'sign': continue
            out.append({"file": fn, "path": p[0], "mode": p[1], "box": tuple(int(x) for x in p[2:8]), "lo": int(p[10]), "hi": int(p[11])})
    return out

def pick(rs, rng, nw=5, nr=10):
    pos = [r for r in rs if r["lo"] > 0]; neg = [r for r in rs if r["hi"] < 0]
    out = sorted(pos, key=lambda r: r["lo"])[:nw] + sorted(neg, key=lambda r: -r["hi"])[:nw][:max(0, nw - len(pos))]
    rest = [r for r in rs if r not in out]; return out + rng.sample(rest, min(nr, len(rest)))

def outside(b): return b[2]*b[2] + b[4]*b[4] >= 2**40

def test(r, b, li):
    sign = 1 if r["lo"] > 0 else -1; q = lambda x: fmpq(x, U)
    if r["mode"] in ("H", "X"):
        v = K.chord_bound(b, 'y', 'lower', ["v50", "graded", "graded_fine"][li]); return v > 0, float(v), 1
    if r["mode"] == "V":
        N, rf = [(16384, 32), (65536, 64)][li]
        v = K.ez_axis_bound(q(b[0]), q(b[1]), q(b[4]), q(b[5]), 'lower' if sign > 0 else 'upper', N, rf)
    else:
        v = K.ezz_axis_bound(q(b[0]), q(b[1]), q(b[4]), q(b[5]), 'lower' if sign > 0 else 'upper', [2048, 8192][li])
    return ((v > 0) if sign > 0 else (v < 0)), float(v), sign

def split(r, b):
    l0, l1, r0, r1, z0, z1 = b
    if r["mode"] in ("H", "X"):
        sc = [l1 - l0, 4*(r1 - r0), 4*(z1 - z0)]; i = sc.index(max(sc))
    else:
        i = 2 if (z1 - z0) >= 8*(l1 - l0) else 0
    lo, hi = 2*i, 2*i + 1; m = (b[lo] + b[hi])//2; c = list(b); e = list(b); c[hi] = m; e[lo] = m
    return [tuple(c), tuple(e)]

def run(item):
    g, r = item; t0 = time.monotonic(); res = None
    levels = [(0, 6), (1, 3), (2, 2)] if r["mode"] in ("H", "X") else [(0, 6), (1, 6)]
    for li, maxd in levels:
        todo = [(r["box"], 0)]; ok = True; ext = None; ev = 0
        while todo:
            b, d = todo.pop()
            if outside(b): continue
            good, v, s = test(r, b, li); ev += 1
            if good: ext = v if ext is None else (min(ext, v) if s > 0 else max(ext, v))
            elif d < maxd and (b[1] > b[0] or b[3] > b[2] or b[5] > b[4]): todo += [(c, d + 1) for c in split(r, b)]
            else: ok = False; ext = v; break
        res = {"group": g, "leaf": r["file"].split('/')[-2] + "/" + r["file"].split('/')[-1] + ":" + r["path"], "mode": r["mode"],
               "box": list(r["box"]), "producer": [r["lo"], r["hi"]], "confirmed": ok, "ladder": li, "evals": ev, "extreme": ext,
               "seconds": round(time.monotonic() - t0, 1)}
        if ok: break
    return res

if __name__ == '__main__':
    root, out = sys.argv[1], sys.argv[2]; rng = random.Random(53); items = []
    G = [("low_H", "low/[123][0-9]H.tsv", "H"), ("finer_H", "finer/*H.tsv", "H"), ("window_H", "window/*H.tsv", "H"),
         ("leaves_H_21_31", "leaves/[23][0-9]H.tsv", "H"), ("thin_H", "thin/*H.tsv", "H"), ("mixed_H", "mixed/*H.tsv", "H"),
         ("recovered_H", "recovered/*H.tsv", "H"), ("mixed_X", "mixed/*H.tsv", "X"), ("recovered_X", "recovered/*H.tsv", "X"),
         ("rim_X", "rim.tsv", "X"), ("leaves_V", "leaves/*V.tsv", "V"), ("finer_V", "finer/*V.tsv", "V"), ("low_V", "low/*V.tsv", "V"),
         ("leaves_Z", "leaves/*Z.tsv", "Z"), ("finer_Z", "finer/*Z.tsv", "Z"), ("low_Z", "low/*Z.tsv", "Z")]
    for g, pat, mode in G:
        rs = rows(f"{root}/{pat}", {mode})
        if g == "leaves_H_21_31": rs = [r for r in rs if 21 <= int(r["file"].split('/')[-1][:2]) <= 31]
        small = g.split("_")[0] in ("thin", "mixed", "recovered", "rim")
        items += [(g, r) for r in (pick(rs, rng, 3, 5) if small else pick(rs, rng))]
    items += [("salvage_H", r) for r in rows(f"{root}/salvage/*H.tsv", {"H"})]
    n = ok = 0
    with open(out, "w") as f, mp.Pool(2) as pool:
        for r in pool.imap(run, items):
            n += 1; ok += r["confirmed"]; f.write(json.dumps(r) + "\n"); f.flush()
            print(r["group"], r["leaf"], r["confirmed"], r["ladder"], r["extreme"], r["seconds"], flush=True)
    print(f"{ok}/{n} confirmed")
