import json,sys,time,os
from pathlib import Path
from gap1_producer import global_axial_c1b_kernel as k
k.ctx.prec=k.BITS;k.base.ctx.prec=k.BITS
region=sys.argv[1]; idx=int(sys.argv[2]); root=Path('/home/daybreak/gap1-run-v0-4-out/v91_parallel_NOT_EVIDENCE');root.mkdir(exist_ok=True)
q,ok=k.gap1_coarse_slabs();assert ok
s=q[idx]; fn=k.attempt_x if region=='X' else k.attempt_l
records=[]
def check(s):
    passed,rec,*tail=fn(s); reason=tail[-1];work=tail[-2]
    records.append(dict(region=region,coarse=idx,depth=s.depth,lo=str(s.ll),hi=str(s.lr),pass_=bool(passed),attempt_reason=reason,work=work))
    if passed:return True
    if s.depth==3:return False
    left,right=s.children()
    return check(right) and check(left)
try:
    result=check(s)
    obj={'region':region,'slab':idx,'PASS':result,'leaves':records,'NOT_EVIDENCE':True}
    tmp=root/f'{region}_{idx:03}.tmp';tmp.write_text(json.dumps(obj,default=str,ensure_ascii=False)+'\n');tmp.rename(root/f'{region}_{idx:03}.json')
    print(region,idx,'PASS' if result else 'FAIL',len(records),flush=True)
    sys.exit(0 if result else 3)
except Exception as e:
    (root/f'{region}_{idx:03}.error').write_text(repr(e)+'\n')
    raise
