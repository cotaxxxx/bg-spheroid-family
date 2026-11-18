"""chat V37: independent primitive-E H references at the C21 pilot box centres (chat's V31 lib, physical p_z = lambda*z),
compared with Dig's corrected references and with the producer intervals (coarse first pass and fine calibration)."""
import sys, json, os
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref, stencil
from fractions import Fraction as F
mp.mp.dps = 25
R = sys.argv[2]
ref = json.load(open(os.path.join(R, 'primitive_E_hires_CORRECTED.json')))['results']
def interval(name):
    out = {}
    for tag, fn in (('coarse', f'{name}.json'), ('fine', f'{name}_cal_v2.json'), ('fine', f'{name}_cal_fine.json')):
        p = os.path.join(R, fn)
        if os.path.exists(p):
            d = json.load(open(p)); e = d.get('H_interval')
            if isinstance(e, dict) and 'lower' in e: out[tag] = (mp.mpf(F(e['lower']).numerator)/F(e['lower']).denominator, mp.mpf(F(e['upper']).numerator)/F(e['upper']).denominator)
    return out
allok = True
for r in ref:
    c = r['n160']; lam = mp.mpf(c['lambda']); rho = mp.mpf(c['rho']); pz = mp.mpf(c['original_E_pz'])
    assert abs(pz - lam*mp.mpf(c['normalized_z'])) < mp.mpf(10)**-20
    _, er, _ = stencil(lambda d: E_ref(lam, rho+d, pz), second=False)
    H = er/rho; dig = mp.mpf(c['H_center_num']); iv = interval(r['box'])
    cont = {k: (lo <= H <= hi) for k, (lo, hi) in iv.items()}
    agree = abs(H-dig) < mp.mpf('1e-6')
    allok &= agree and all(cont.values())
    print(f"{r['box']:9s} chat H={mp.nstr(H,12):>16}  Dig={mp.nstr(dig,12):>16}  |diff|={mp.nstr(abs(H-dig),2):>8}  contained={cont}", flush=True)
print("SUMMARY", "PASS" if allok else "CHECK")
