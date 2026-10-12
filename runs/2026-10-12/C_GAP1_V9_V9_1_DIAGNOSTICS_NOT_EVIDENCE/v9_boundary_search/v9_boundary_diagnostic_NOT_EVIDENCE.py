#!/usr/bin/env python3
"""v9 §2: unmodified v0.4.1 kernel; right-first depth<=3; diagnostic only."""
import json,sys,time
from fractions import Fraction
from pathlib import Path
from gap1_producer import global_axial_c1b_kernel as k
k.ctx.prec=k.BITS;k.base.ctx.prec=k.BITS
out=Path('/home/daybreak/gap1-run-v0-4-out/v9_boundary_diagnostic_NOT_EVIDENCE')
out.mkdir(parents=True,exist_ok=True)
ledger=out/'diagnostic.jsonl'
q,ok=k.gap1_coarse_slabs();assert ok and len(q)==160

def run_tree(s,region):
    fn=k.attempt_x if region=='X' else k.attempt_l
    passed,rec,*tail=fn(s)
    reason=tail[-1]; work=tail[-2]
    item={'region':region,'coarse':s.coarse,'depth':s.depth,'lo':str(s.ll),'hi':str(s.lr),'pass':bool(passed),'attempt_reason':reason,'work':work,'utc_epoch':time.time()}
    with ledger.open('a') as f:f.write(json.dumps(item,sort_keys=True,default=str)+'\n')
    print('LEAF',region,s.coarse,s.depth,str(s.ll),str(s.lr),'PASS' if passed else 'FAIL',reason,flush=True)
    if passed:return True
    if s.depth>=3:return False
    left,right=s.children()
    if not run_tree(right,region):return False
    return run_tree(left,region)

print('V9_DIAGNOSTIC_NOT_EVIDENCE',flush=True)
for m in range(117,108,-1):
    x=q[m]; l=q[m-1]
    print('M',m,'X',x,'L',l,flush=True)
    if not run_tree(x,'X'):
        print('STOP X_DIAGNOSTIC_FAIL m',m,flush=True);sys.exit(3)
    if run_tree(l,'L'):
        b=Fraction(2,5)+Fraction(m,3200)
        print('BOUNDARY_PASS',m,str(b),flush=True)
        (out/'boundary.json').write_text(json.dumps({'m':m,'lambda_b':str(b),'status':'PASS','evidence':'NOT_EVIDENCE'},indent=2)+'\n')
        sys.exit(0)
print('STOP L_DIAGNOSTIC_EXHAUSTED m=109',flush=True)
sys.exit(4)
