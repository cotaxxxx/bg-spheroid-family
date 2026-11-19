import sys, json, time, multiprocessing as mp
sys.path.insert(0,'.')
from chat_vz_check_B import *
from flint import arb, fmpq
NT, NP = 2048, 256
def hb(l0, l1):
    lam=arb(fmpq(l0,2**20)).union(arb(fmpq(l1,2**20))); e2=1/(lam*lam); L2=lam*lam; tot=arb(0)
    for i in range(NT):
        t=(arb(i)+U01)/NT
        for k in range(NP):
            ph=PI*(arb(k)+U01)/NP; co=ph.cos(); si=ph.sin(); m2=(1-t*t)*sq(co); j=(1-t*t)*sq(si); C=1+(L2-1)*m2; c=1/C
            B=clip(1-4*(1-e2)*t*t*m2,e2.lower(),1); T=(c/B).sqrt(); g=clip(t*T,0,1)
            tot+=arb((T*t*t*(P_enc(g)*c*(1-j*c)-Q_enc(g)*j*sq(2-c))).lower())
    return float((tot/(NT*NP)).lower()), (tot/(NT*NP)).lower() > 0
def run(item):
    nm,l0,l1=item; t0=time.monotonic(); todo=[(l0,l1,0)]; vals=[]; ok=True
    while todo:
        a,b,d=todo.pop(); v,good=hb(a,b)
        if good: vals.append(v)
        elif d<3: m=(a+b)//2; todo+=[(a,m,d+1),(m,b,d+1)]
        else: ok=False; vals.append(v)
    return {'name':nm,'confirmed':ok,'children':len(vals),'min':min(vals),'seconds':round(time.monotonic()-t0,1)}
if __name__=='__main__':
    items=[(r['name'],r['box'][0],r['box'][1]) for r in map(json.loads,open('nb_check.jsonl')) if r['kind']=='Hb' and not r['confirmed']]
    with mp.Pool(int(sys.argv[1])) as p:
        for o in p.imap(run,items): print(json.dumps(o),flush=True)
