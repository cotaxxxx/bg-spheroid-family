"""chat checks of the V60 PC result (PLAN_V60 §6, steps 1-4, and the choice of the two reproduction combos for step 5).
usage: verify_v60.py out_dir"""
import sys, json, hashlib, os, random
D = sys.argv[1]; ok = True
def chk(name, c, msg=""):
    global ok; ok &= bool(c); print(("OK   " if c else "FAIL ") + name, msg)
lines = open(f'{D}/manifest_check.txt').read().splitlines()
chk("1 manifest", lines and all(l.endswith(': OK') for l in lines), f"{len(lines)} files")
sums = [l.split() for l in open(f'{D}/SHA256SUMS.txt') if l.strip()]
chk("1 SHA256SUMS", all(hashlib.sha256(open(f'{D}/{fn}', 'rb').read()).hexdigest() == h for h, fn in sums), f"{len(sums)} files")
for t in ("selftest_tri", "selftest_tri2", "selftest_tri3", "selftest_tri4"):
    chk(f"2 {t}", "FAILURES 0" in open(f'{D}/{t}.log').read())
B = [json.loads(l) for l in open(f'{D}/bench.jsonl')]
same = all(b['h33'] == [1.0513999178011142, 1.508953370426753] and b['w3'] == [1.3490595682934676, 1.5693270267803683] for b in B)
print(("OK   " if same else "NOTE ") + "3 bench intervals bit-identical", f"{len(B)} copies, sec {sorted(b['sec'] for b in B)}")
R = [json.loads(l) for l in open(f'{D}/res_v60.jsonl')]
key = lambda x: (x['layer'], x['stratum'], x['kind'], tuple(x['tile']), tuple(x['cell']))
S = json.load(open('samples_v60.json'))
chk("4 rows", len(R) == 96 and sorted(map(key, R)) == sorted(map(key, S)), f"{len(R)} rows")
cand = sorted([x for x in R if x['status'] == 'COVERED' and x['evals'] <= 60], key=lambda x: json.dumps(key(x)))
pick = random.Random(20261121).sample(cand, 2) if len(cand) >= 2 else cand
json.dump([{k: x[k] for k in ('layer', 'stratum', 'kind', 'tile', 'cell', 'box')} for x in pick], open('repro_v60.json', 'w'))
print("5 reproduction combos:", [(key(x), x['leaves'], x['evals'], x['leaf_sha256'][:16]) for x in pick])
print("ALL CHECKS", "PASS" if ok else "FAIL")
