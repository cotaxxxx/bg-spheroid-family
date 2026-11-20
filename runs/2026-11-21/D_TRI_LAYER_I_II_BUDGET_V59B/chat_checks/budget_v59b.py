"""V59-B extrapolation per PLAN_V59B: keep the 45 COVERED V59 rows, replace the 51 others by their V59-B rows.
Unfinished rows still count as lower bounds (sec + remaining * sec/eval)."""
import json
key = lambda r: (r['layer'], r['stratum'], r['kind'], tuple(r['tile']), tuple(r['cell']))
A = [json.loads(l) for l in open('res_v59.jsonl')]
B = {key(r): r for r in map(json.loads, open('res_v59b.jsonl'))}
R = []; miss = []
for r in A:
    if r['status'] == 'COVERED': R.append(dict(r, src='V59'))
    elif key(r) in B: R.append(dict(B[key(r)], src='V59-B'))
    else: miss.append(key(r)); R.append(dict(r, src='V59(not rerun)'))
st = json.load(open('strata_v59.json'))
cnt = {('I', k): v for k, v in st['counts_I'].items()}; cnt.update({('II', k): v for k, v in st['counts_II'].items()})
cnt[('I', 'rim')] -= 63
YEAR = 3.156e7; tot = {'I': 0.0, 'II': 0.0}
print(f"rows {len(R)}  from V59-B {sum(r['src']=='V59-B' for r in R)}  missing {len(miss)}")
print("layer stratum     n cov  bud unres  mean_sec_lb  cells  CPU-years(lb)")
for k in sorted(set((r['layer'], r['stratum']) for r in R)):
    rs = [r for r in R if (r['layer'], r['stratum']) == k]
    lb = [r['sec'] + (0 if r['status'] == 'COVERED' else r['remaining']*r['sec']/max(r['evals'], 1)) for r in rs]
    mean = sum(lb)/len(lb); yrs = mean*cnt[k]*32/YEAR; tot[k[0]] += yrs
    c = lambda s: sum(r['status'].startswith(s) for r in rs)
    print(f"{k[0]:5} {k[1]:10} {len(rs):3} {c('COVERED'):3} {c('BUDGET'):4} {c('UNRESOLVED'):5} {mean:12.1f} {cnt[k]:6} {yrs:10.2f}")
print({k: round(v, 2) for k, v in tot.items()}, "total", round(sum(tot.values()), 2))
json.dump(R, open('merged_v59b.json', 'w'), default=str)
