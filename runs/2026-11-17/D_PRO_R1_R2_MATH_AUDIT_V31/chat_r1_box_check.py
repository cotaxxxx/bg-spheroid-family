"""chat V31: box soundness of R1 R2 against chat's brute-force reference at sampled interior points."""
import sys, random, json
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from dataclasses import replace
from flint import fmpq as Q
from prolate_r1 import api, Config
sys.path.insert(0, sys.argv[2])
from chat_r1_reference_check_lib import E_ref, stencil, fq, lohi
CFG = replace(Config(), order=6, base_u=32, base_v=64, distance_ratio=Q(1, 2))
random.seed(31); allok = True; rows = []
def chk(name, ball, refs):
    global allok
    lo, hi = lohi(ball); ok = all(lo-mp.mpf('1e-7') <= r <= hi+mp.mpf('1e-7') for r in refs)
    allok &= ok; rows.append(dict(case=name, lo=mp.nstr(lo, 10), hi=mp.nstr(hi, 10), refs=[mp.nstr(r, 10) for r in refs], ok=ok))
    print(("PASS " if ok else "FAIL ")+name, f"[{mp.nstr(lo,8)}, {mp.nstr(hi,8)}]", [mp.nstr(r, 8) for r in refs], flush=True)
# W box: R,tau width 1/64, lambda width 1/256 (V25/R1 box size); middle chart and equator chart
for (R0, T0, L0) in ((Q(1, 2), Q(1, 2), Q(7, 2)), (Q(3, 4), Q(1, 8), Q(5)), (Q(5, 8), Q(3, 4), Q(2))):
    B = ((R0-Q(1, 128), R0+Q(1, 128)), (T0-Q(1, 128), T0+Q(1, 128)), (L0-Q(1, 512), L0+Q(1, 512)) if L0 not in (Q(2), Q(5)) else ((L0, L0+Q(1, 256)) if L0 == 2 else (L0-Q(1, 256), L0)))
    Wb = api.angular_quotient(*B, angle_kind="tau", config=CFG)
    raw = api.angular_raw(*B, angle_kind="tau", config=CFG)
    refsW, refsE = [], []
    for _ in range(4):
        r = fq(B[0][0]) + (fq(B[0][1])-fq(B[0][0]))*mp.mpf(random.random())
        t = fq(B[1][0]) + (fq(B[1][1])-fq(B[1][0]))*mp.mpf(random.random())
        l = fq(B[2][0]) + (fq(B[2][1])-fq(B[2][0]))*mp.mpf(random.random())
        b0 = 2*mp.atan(t)
        e, eb, _ = stencil(lambda d: E_ref(l, r*mp.cos(b0+d), l*r*mp.sin(b0+d)), second=False)
        refsW.append(eb/(r**2*mp.sin(b0)*mp.cos(b0))); refsE.append(eb)
    chk(f"W box {B} [{Wb.route}]", Wb.enclosure, refsW)
    chk(f"Ebeta box {B}", raw.balls[1], refsE)
# g box and Phi_s box
for (T, L) in (((Q(15, 32), Q(17, 32)), (Q(895, 256), Q(897, 256))), ((Q(1, 64), Q(3, 64)), (Q(2), Q(2)+Q(1, 256)))):
    gb = api.axis_g(T, L, config=CFG); refs = []
    for _ in range(4):
        t = fq(T[0]) + (fq(T[1])-fq(T[0]))*mp.mpf(random.random()); l = fq(L[0]) + (fq(L[1])-fq(L[0]))*mp.mpf(random.random())
        _, g, _ = stencil(lambda d: E_ref(l, 0, l*(t+d)), second=False); refs.append(g)
    chk(f"g box {T} {L}", gb.enclosure, refs)
for (S, L) in (((Q(15, 64), Q(17, 64)), (Q(1279, 256), Q(5))), ((Q(1, 512), Q(3, 512)), (Q(895, 256), Q(897, 256)))):
    pb = api.equatorial_phi_s(S, L, config=CFG); refs = []
    for _ in range(4):
        s = fq(S[0]) + (fq(S[1])-fq(S[0]))*mp.mpf(random.random()); l = fq(L[0]) + (fq(L[1])-fq(L[0]))*mp.mpf(random.random())
        r = mp.sqrt(s); _, er, err = stencil(lambda d: E_ref(l, r+d, 0)); refs.append((r*err-er)/(2*r**3))
    chk(f"Phi_s box {S} {L} [{pb.route}]", pb.enclosure, refs)
json.dump(rows, open(sys.argv[3], "w"), indent=1, default=str)
print("SUMMARY", "ALL_PASS" if allok else "FAIL", len(rows))
