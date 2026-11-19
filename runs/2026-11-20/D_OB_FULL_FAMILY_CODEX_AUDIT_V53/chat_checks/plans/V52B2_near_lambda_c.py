"""Amendment B2 (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
14 pieces of V52B are unconfirmed, all in the two slabs just above lambda_c ([21/50, 337/800], [43/100, 345/800]),
where E_z itself is only 2e-3 to 9e-3 (1-D mpmath reference, logged in V52B2_reference.txt); no piece has a reference
value of the wrong sign. Cause (tool): V52A's split rule stops splitting t once t-width < 8 x lambda-width (1/100),
and the z-interval dependency of the kernel near mu = z then dominates the width.
Change, only for those 14 pieces: split t first down to width <= 1/2048, then lambda (at most 2 more levels);
ez ladder (N, refine) = (65536, 64), (262144, 128). Same claims and signs as V52B. Confirmed iff all children hold.
"""
import sys, json, time, multiprocessing as mp
from fractions import Fraction as F
import importlib.util
spec = importlib.util.spec_from_file_location("A", "plans/V52A_axis_amendment.py"); A = importlib.util.module_from_spec(spec); sys.modules["A"] = A; spec.loader.exec_module(A)
A.EZ = [(65536, 64), (262144, 128)]

def cover2(job):
    name, kind, l0, l1, t0, t1, sign = job; t_ = time.monotonic()
    for li in range(2):
        todo = [(l0, l1, t0, t1, 0)]; ok = True; ext = None; ev = 0
        while todo:
            a, b, c, d, lam_dep = todo.pop(); good, v = A.sign_ok(kind, a, b, c, d, sign, li); ev += 1
            if good: ext = v if ext is None else (min(ext, v) if sign > 0 else max(ext, v))
            elif d - c > F(1, 2048): m = (c + d)/2; todo += [(a, b, c, m, lam_dep), (a, b, m, d, lam_dep)]
            elif lam_dep < 2: m = (a + b)/2; todo += [(a, m, c, d, lam_dep + 1), (m, b, c, d, lam_dep + 1)]
            else: ok = False; ext = v; break
        if ok: break
    return {"leaf": name, "kind": kind, "box": [str(x) for x in (l0, l1, t0, t1)], "sign": sign, "confirmed": ok,
            "ladder": li, "evals": ev, "extreme": ext, "seconds": round(time.monotonic() - t_, 1)}

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    jobs = []
    for ln in open(src):
        r = json.loads(ln)
        if "slab_meta" in r or r["confirmed"]: continue
        l0, l1, t0, t1 = [F(x) for x in r["box"]]; jobs.append((r["leaf"] + "_B2", r["kind"], l0, l1, t0, t1, r["sign"]))
    n = ok = 0
    with open(out, 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(cover2, jobs):
            n += 1; ok += r['confirmed']; f.write(json.dumps(r) + "\n"); f.flush(); print(r['leaf'], r['confirmed'], r['ladder'], r['evals'], r['extreme'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
