"""chat V31: Phi_s box soundness (rerun after mpc fix) of R1 R2 against chat's brute-force reference at sampled interior points."""
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
for (S, L) in (((Q(15, 64), Q(17, 64)), (Q(1279, 256), Q(5))), ((Q(1, 512), Q(3, 512)), (Q(895, 256), Q(897, 256)))):
    pb = api.equatorial_phi_s(S, L, config=CFG); refs = []
    for _ in range(4):
        s = fq(S[0]) + (fq(S[1])-fq(S[0]))*mp.mpf(random.random()); l = fq(L[0]) + (fq(L[1])-fq(L[0]))*mp.mpf(random.random())
        r = mp.sqrt(s); _, er, err = stencil(lambda d: E_ref(l, r+d, 0)); refs.append((r*err-er)/(2*r**3))
    chk(f"Phi_s box {S} {L} [{pb.route}]", pb.enclosure, refs)
json.dump(rows, open(sys.argv[3], "w"), indent=1, default=str)
print("SUMMARY", "ALL_PASS" if allok else "FAIL", len(rows))
