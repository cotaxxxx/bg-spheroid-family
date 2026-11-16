#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE."""
import hashlib,json
from pathlib import Path
import numpy as np
from research_diagnostic import grid,evaluate,LAM,RAD,TAU

root=Path(__file__).resolve().parent
for name,h in json.loads((root/'IDENTITY_PRE_RUN_SHA256.json').read_text()).items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=h: raise RuntimeError('seal mismatch')
answers={}
def check(lam,rad,tau,quad):
    beta=2*np.arctan(tau)
    v=evaluate(lam,rad,beta,quad)
    rhs=-rad*np.sin(beta)*v[3]+lam*rad*np.cos(beta)*v[4]
    return bool(np.isfinite(v).all() and abs(v[1]-rhs)<2e-5)
for n,m in [(24,192),(48,384),(72,576)]:
    quad=grid(n,m); allok=True; intok=True
    for lam in [2,7/2,5]:
        for rad in [1/8,1/2,15/16,1]:
            for tau in [1/16,1/4,1/2,3/4,15/16]:
                ok=check(lam,rad,tau,quad)
                allok &= ok
                if rad<1: intok &= ok
    answers[f'rule_{n}_{m}_all_60']=allok
    answers[f'rule_{n}_{m}_interior_45']=intok
quad=grid(72,576); ok=True
for lam in LAM:
    for rad in RAD:
        for tau in TAU[1:-1]: ok &= check(lam,rad,tau,quad)
answers['original_Q5_full_sample_rule_72_576']=ok
out={'classification':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','answers':answers}
(root/'IDENTITY_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
