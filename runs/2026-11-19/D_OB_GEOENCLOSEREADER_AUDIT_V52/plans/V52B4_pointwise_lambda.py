"""Amendment B4 (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
B3 (mean-value in t, lambda over the whole slab) was stopped after its first two pieces failed (-0.0041, -0.0032).
Diagnosis (V52B4_diag.txt): at the point lambda = 21/50, t = 1/16 the node bound is [0.00164, 0.00200] (reference
0.001819); the failure comes from the lambda-interval of width 1/800, because E_z ~ 2e-3 is a cancellation of O(1)
terms and the ball arithmetic loses about 3e-3 per 1/800 of lambda. The producer (C-AXIS C0) avoided this region's
direct sign test by a third-derivative argument (g_ttt < 0 and Phi), which the Reader does not implement.
B4 therefore checks the same 14 pieces at the single value lambda = l0 of each slab (21/50, 43/100), with the B3
mean-value rule in t. The result is a pointwise-lambda confirmation, weaker than a slab confirmation, and is reported so.
"""
import sys, json, time, multiprocessing as mp
from fractions import Fraction as F
import importlib.util
spec = importlib.util.spec_from_file_location("B3", "plans/V52B3_mean_value.py"); B3 = importlib.util.module_from_spec(spec); sys.modules["B3"] = B3; spec.loader.exec_module(B3)

def run(job):
    name, kind, l0, l1, t0, t1, sign = job; r = B3.run((name, kind, l0, l0, t0, t1, sign)); r["lambda_point"] = str(l0); return r

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]; jobs = []
    for ln in open(src):
        r = json.loads(ln)
        if "slab_meta" in r or r["confirmed"]: continue
        l0, l1, t0, t1 = [F(x) for x in r["box"]]; jobs.append((r["leaf"] + "_B4", r["kind"], l0, l1, t0, t1, r["sign"]))
    n = ok = 0
    with open(out, 'w') as f, mp.Pool(2) as pool:
        for r in pool.imap(run, jobs):
            n += 1; ok += r['confirmed']; f.write(json.dumps(r) + "\n"); f.flush(); print(r['leaf'], r['confirmed'], r['evals'], r['extreme'], r['seconds'], flush=True)
    print(f"{ok}/{n} confirmed")
