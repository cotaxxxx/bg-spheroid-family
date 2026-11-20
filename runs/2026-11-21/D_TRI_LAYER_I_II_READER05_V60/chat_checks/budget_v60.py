"""V60 extrapolation (PLAN_V60 §5) and comparison with V59/V59-B. usage: budget_v60.py out_dir
Seconds are converted to this container's seconds: sec / r, r = median(bench_PC) / 45.1."""
import sys, json, statistics, collections
D = sys.argv[1]
R = [json.loads(l) for l in open(f'{D}/res_v60.jsonl')]
r = statistics.median(json.loads(l)['sec'] for l in open(f'{D}/bench.jsonl'))/45.1
M = {(m['layer'], m['stratum'], m['kind'], tuple(m['tile']), tuple(m['cell'])): m for m in json.load(open('../v59/merged_v59b.json'))}
key = lambda x: (x['layer'], x['stratum'], x['kind'], tuple(x['tile']), tuple(x['cell']))
assert len(R) == 96 and len(set(map(key, R))) == 96, (len(R), len(set(map(key, R))))
st = json.load(open('../v59/strata_v59.json'))
cnt = {('I', k): v for k, v in st['counts_I'].items()}; cnt.update({('II', k): v for k, v in st['counts_II'].items()})
cnt[('I', 'rim')] -= 63
YEAR = 3.156e7; tot = {'I': 0.0, 'II': 0.0}
lb = lambda x, sc: (x['sec'] + (0 if x['status'] == 'COVERED' else x['remaining']*x['sec']/max(x['evals'], 1)))/sc
print(f"r = {r:.4f}  (PC budget per combo {R[0]['budget']} s = {R[0]['budget']/r:.0f} container-s)")
print("status counts:", dict(collections.Counter(x['status'].split(':')[0] for x in R)))
print("layer stratum     n cov  bud unres other  mean_sec_lb(cont)  cells  CPU-years(lb)   | V59/V59-B: cov  CPU-years")
old = collections.defaultdict(float)
for k in sorted(set((x['layer'], x['stratum']) for x in R)):
    rs = [x for x in R if (x['layer'], x['stratum']) == k]
    mean = sum(lb(x, r) for x in rs)/len(rs); yrs = mean*cnt[k]*32/YEAR; tot[k[0]] += yrs
    om = [M[key(x)] for x in rs]; omean = sum(lb(x, 1.0) for x in om)/len(om); oyrs = omean*cnt[k]*32/YEAR
    c = lambda s, L=rs: sum(x['status'].startswith(s) for x in L)
    other = len(rs) - c('COVERED') - c('BUDGET') - c('UNRESOLVED')
    print(f"{k[0]:5} {k[1]:10} {len(rs):3} {c('COVERED'):3} {c('BUDGET'):4} {c('UNRESOLVED'):5} {other:5} {mean:15.1f} {cnt[k]:8} {yrs:10.2f}"
          f"   | {c('COVERED', om):3} {oyrs:8.2f}")
    old[k[0]] += oyrs
print("V60 total", {k: round(v, 2) for k, v in tot.items()}, round(sum(tot.values()), 2), "| V59/V59-B total", round(sum(old.values()), 2))
both = [(x, M[key(x)]) for x in R if x['status'] == 'COVERED' and M[key(x)]['status'] == 'COVERED']
if both:
    print(f"combos covered in both ({len(both)}): median evals ratio V60/V59 {statistics.median(a['evals']/b['evals'] for a, b in both):.3f}, "
          f"median leaves ratio {statistics.median(a['leaves']/b['leaves'] for a, b in both):.3f}, "
          f"median container-sec ratio {statistics.median((a['sec']/r)/b['sec'] for a, b in both):.3f}")
U = [x for x in R if M[key(x)]['status'] == 'UNRESOLVED']
print("V59-B UNRESOLVED six:"); [print(' ', x['stratum'], x['kind'], x['tile'], x['cell'], x['status'], x['leaves'], x['evals'], x['remaining'], x['sec']) for x in U]
bad = [x for x in R if x['status'].split(':')[0] in ('NEGATIVE', 'INCONSISTENT', 'KERNEL_LIMIT')]
print("NEGATIVE/INCONSISTENT/KERNEL_LIMIT rows:", len(bad)); [print(' ', x) for x in bad]
