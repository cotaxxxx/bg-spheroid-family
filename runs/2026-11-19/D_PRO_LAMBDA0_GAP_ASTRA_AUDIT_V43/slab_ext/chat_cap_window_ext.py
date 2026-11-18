"""chat V43 DIAGNOSTIC_ONLY / NOT_EVIDENCE: binary question - does Astra's unchanged (G9) range bound stay > 0
on the whole window lambda in [2, 5] (eps in [1/5, 1/2], 24 eps slabs), pole layer chi <= lambda^-2?  Uses cap_interval.py unchanged."""
import sys, json, time, multiprocessing as mp
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q, arb
from cap_interval import geometry, bound
G = None
def init():
    global G; G = geometry(96, 48)
def work(idx):
    i, j, k = idx
    e = (Q(1,5)+Q(3,10)*Q(i,24), Q(1,5)+Q(3,10)*Q(i+1,24))
    box = [e, (Q(j,8), Q(j+1,8)), (Q(k,8), Q(k+1,8))]
    r = bound(box, G)[0]
    return idx, r.lower().fmpq(), bool(r > 0), bool(r > arb(Q(1,4)))
if __name__ == '__main__':
    t = time.monotonic(); ids = [(i,j,k) for i in range(24) for j in range(8) for k in range(8)]
    with mp.Pool(4, initializer=init) as p: rows = p.map(work, ids)
    for i in range(24):
        sub=[r for r in rows if r[0][0]==i]; print(json.dumps({'eps_slab':i,'eps':[str(Q(1,5)+Q(3,10)*Q(i,24)),str(Q(1,5)+Q(3,10)*Q(i+1,24))],'all_positive':all(r[2] for r in sub),'all_gt_quarter':all(r[3] for r in sub)}))
    mn = min(rows, key=lambda r: r[1])
    print(json.dumps({'boxes': len(rows), 'all_positive': all(r[2] for r in rows), 'all_gt_quarter': all(r[3] for r in rows),
                      'min_lower': int(mn[1].p)/int(mn[1].q), 'min_lower_exact': str(mn[1]), 'min_index': mn[0], 'seconds': round(time.monotonic()-t, 1)}))
