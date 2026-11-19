"""Amendment B3 (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
B2 (t-first splitting to 1/2048) was stopped after about 25 minutes with no piece finished: on a t-interval of width w
the 1-D ez kernel loses roughly 3w to the z-dependency near mu = z, comparable to the margins (2e-3) near lambda_c.
B2 produced no results (log kept as V52B2_run_STOPPED.log).
B3 uses a mean-value (node + derivative) bound instead, for the same 14 pieces and the same claims:
  for t in [t_k, t_k + h]:  E_z(t) >= lower E_z(t_k) + h * min(0, lower E_zz([t_k, t_k + h]))   (claim E_z > 0)
                            E_z(t) <= upper E_z(t_k) + h * max(0, upper E_zz([t_k, t_k + h]))   (claim E_z < 0)
  with lambda over the whole slab in every evaluation. Nodes h = 1/256 (then 1/1024 if a sub-interval fails);
  E_z at nodes by ez_axis_bound (N, refine) = (65536, 64); E_zz by ezz_axis_bound N = 4096.
Valid because E_z(0, t) is C^1 in t inside the ball (P1 Lemma V; V13). Confirmed iff every sub-interval passes.
"""
import sys, json, time, multiprocessing as mp
from fractions import Fraction as F
from flint import fmpq
from geoenclosereader import kernels as K
q = lambda x: fmpq(x.numerator, x.denominator)

def sub_ok(l0, l1, a, b, sign):
    h = b - a
    if sign > 0:
        e = K.ez_axis_bound(q(l0), q(l1), q(a), q(a), 'lower', 65536, 64); d = K.ezz_axis_bound(q(l0), q(l1), q(a), q(b), 'lower', 4096)
        v = float(e) + float(h)*min(0.0, float(d)); return v > 0 and (e + q(h)*(d if d < 0 else 0)) > 0, v
    e = K.ez_axis_bound(q(l0), q(l1), q(a), q(a), 'upper', 65536, 64); d = K.ezz_axis_bound(q(l0), q(l1), q(a), q(b), 'upper', 4096)
    v = float(e) + float(h)*max(0.0, float(d)); return v < 0 and (e + q(h)*(d if d > 0 else 0)) < 0, v

def run(job):
    name, kind, l0, l1, t0, t1, sign = job; t_ = time.monotonic(); worst = None; ok = True; ev = 0
    a = t0
    while a < t1:
        b = min(t1, a + F(1, 256)); good, v = sub_ok(l0, l1, a, b, sign); ev += 1
        if not good:
            c = a
            while c < b:
                e_ = min(b, c + F(1, 1024)); good, v = sub_ok(l0, l1, c, e_, sign); ev += 1
                if not good: ok = False
                worst = v if worst is None else (min(worst, v) if sign > 0 else max(worst, v)); c = e_
        else:
            worst = v if worst is None else (min(worst, v) if sign > 0 else max(worst, v))
        a = b
    return {"leaf": name, "kind": "ez(mean-value)", "box": [str(x) for x in (l0, l1, t0, t1)], "sign": sign, "confirmed": ok,
            "evals": ev, "extreme": worst, "seconds": round(time.monotonic() - t_, 1)}

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]; jobs = []
    for ln in open(src):
        r = json.loads(ln)
        if "slab_meta" in r or r["confirmed"]: continue
        l0, l1, t0, t1 = [F(x) for x in r["box"]]; jobs.append((r["leaf"] + "_B3", r["kind"], l0, l1, t0, t1, r["sign"]))
    n = ok = 0
    with open(out, 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(run, jobs):
            n += 1; ok += r['confirmed']; f.write(json.dumps(r) + "\n"); f.flush(); print(r['leaf'], r['confirmed'], r['evals'], r['extreme'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
