"""chat V31: Phi_s part of the reference check (rerun after the mpc fix in E_ref; same config)."""
import sys, json
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2])
import mpmath as mp
from dataclasses import replace
from flint import fmpq as Q
from prolate_r1 import api, Config
from chat_r1_reference_check_lib import E_ref, stencil, fq, lohi
CFG = replace(Config(), order=6, base_u=32, base_v=64, distance_ratio=Q(1, 2))
allok = True; rows = []
for lam in (Q(2), Q(7, 2), Q(5)):
    lm = fq(lam)
    for s in (Q(1, 1024), Q(1, 4), Q(9, 16)):
        r = mp.sqrt(fq(s)); _, er, err = stencil(lambda d: E_ref(lm, r+d, 0))
        ref = (r*err-er)/(2*r**3); res = api.equatorial_phi_s(s, lam, config=CFG)
        lo, hi = lohi(res.enclosure); sl = mp.mpf('1e-4') if s == Q(1, 1024) else mp.mpf('1e-6')
        ok = lo-sl <= ref <= hi+sl; allok &= ok
        rows.append(dict(case=f"Phi_s lam={lam} s={s} [{res.route}]", ref=mp.nstr(ref, 12), lo=mp.nstr(lo, 10), hi=mp.nstr(hi, 10), ok=bool(ok)))
        print(("PASS " if ok else "FAIL ")+rows[-1]["case"], mp.nstr(ref, 12), f"[{mp.nstr(lo,10)}, {mp.nstr(hi,10)}]", "hw", mp.nstr((hi-lo)/2, 3), flush=True)
json.dump(rows, open(sys.argv[3], "w"), indent=1)
print("SUMMARY", "ALL_PASS" if allok else "FAIL", len(rows))
