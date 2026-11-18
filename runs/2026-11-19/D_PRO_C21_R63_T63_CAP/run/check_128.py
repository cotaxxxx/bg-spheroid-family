"""Exact fraction ledger check, not independent reintegration or analytic theorem."""
import json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
R=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (R/"CAP_R63_T63_128.jsonl").read_text().splitlines()]
expected={(i,j,k) for i in range(2) for j in range(8) for k in range(8)}
ids=[tuple(r['index']) for r in rows]
eps0=F(1,5);step=(F(16,79)-eps0)/2
checks={"count_128":len(rows)==128,"no_duplicates":len(ids)==len(set(ids)),"full_indices":set(ids)==expected,"endpoints_exact":True,"all_lower_gt_zero":True,"all_lower_gt_quarter":True,"upper_gte_lower":True}
for x in rows:
 i,j,k=x['index']
 target=[(eps0+step*i,eps0+step*(i+1)),(F(j,8),F(j+1,8)),(F(k,8),F(k+1,8))]
 checks['endpoints_exact']&=tuple(tuple(F(t) for t in p) for p in x["box"])==tuple(target)
 lo=F(x['lower_exact']);hi=F(x['upper_exact'])
 checks['all_lower_gt_zero']&=lo>0
 checks['all_lower_gt_quarter']&=lo>F(1,4)
 checks['upper_gte_lower']&=hi>=lo
 mini=min(rows,key=lambda x:F(x['lower_exact']))
out={"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","scope":"Verify cover and exact scalar bounds (NOT independent interval reintegration)","checks":checks,"verdict":"LEDGER_PASS_NOT_CERTIFICATION" if all(checks.values()) else "FAIL","minimum_lower_exact":mini["lower_exact"],"minimum_index":mini["index"],"minimum_lower_float":float(F(mini["lower_exact"]))}
(R/"CAP_R63_T63_CHECK.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,sort_keys=True))
assert all(checks.values())
