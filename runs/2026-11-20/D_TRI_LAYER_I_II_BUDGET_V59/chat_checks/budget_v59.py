"""V59 extrapolation per PLAN_V59 (lower bounds for BUDGET/UNRESOLVED rows)."""
import json, collections
R = [json.loads(l) for l in open('res_v59.jsonl')]; st = json.load(open('strata_v59.json'))
cnt = {('I', k): v for k, v in st['counts_I'].items()}; cnt.update({('II', k): v for k, v in st['counts_II'].items()})
cnt[('I', 'rim')] -= 63      # equatorial rim cells: kernel limit (H33 at contact), reported separately
YEAR = 3.156e7; tot = {'I': 0.0, 'II': 0.0}
print("layer stratum   n  covered  budget/unres  mean_sec_lowerbound  cells  x32 tiles -> CPU-years (lower bound)")
for key in sorted(set((r['layer'], r['stratum']) for r in R)):
    rs = [r for r in R if (r['layer'], r['stratum']) == key]
    lb = []
    for r in rs:
        s = r['sec']
        if r['status'] != 'COVERED':
            per = s/max(r['evals'], 1); s += r['remaining']*per
        lb.append(s)
    mean = sum(lb)/len(lb); cov = sum(r['status'] == 'COVERED' for r in rs)
    yrs = mean*cnt[key]*32/YEAR; tot[key[0]] += yrs
    print(f"{key[0]:5} {key[1]:10} {len(rs):3} {cov:7} {len(rs)-cov:12} {mean:18.1f} {cnt[key]:7} {yrs:12.2f}")
print({k: round(v, 2) for k, v in tot.items()}, "CPU-years (python/numpy, lower bounds; equatorial rim 63 cells and layer II axis strips excluded)")
