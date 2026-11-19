"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Exact checks for the numerical inequalities quoted in the report."""
import itertools
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

status="DIAGNOSTIC_ONLY / NOT_EVIDENCE"


def lines(folder,name):
    return [json.loads(l) for l in (folder/name).read_text().splitlines()]


def halves(box):
    for corner in itertools.product((0,1),repeat=3):
        out=[]
        for i,j in enumerate(corner):
            a,b=box[2*i:2*i+2]
            assert (a+b)%2==0
            m=(a+b)//2
            out.extend((m,b) if j else (a,m))
        yield tuple(out)


def small_boxes(r):
    us=list(map(Q,r["subbox_upper"]))
    assert len(us)==8
    return list(zip(halves(r["box"]),us))


if __name__=="__main__":
    folder=Path(sys.argv[1])
    rows={v['lam']:list(map(Q,v['upper_exact'])) for v in lines(folder,'probe1.stdout.jsonl') if 'lam' in v}
    assert all(a<b for a,b in zip(rows['8'],(Q(-1,20),Q(-2,5),Q(-3,5))))
    assert all(a<b for a,b in zip(rows['5'],(Q(1),Q(1),Q(-3,16))))
    slabs=lines(folder,'cover3.replay.jsonl')[0]['slabs']
    assert [s['slab'] for s in slabs]==[5,6,7]
    assert all(s['counts']['open']==0 and Q(s['volume'])==1 for s in slabs)
    assert sum(s['counts']['negative'] for s in slabs)==1845
    assert sum(s['counts']['empty'] for s in slabs)==5
    largest=max(Q(s['largest'][0]) for s in slabs)
    assert largest == -Q(71705,34359738368) and largest < -Q(1,2**19)
    assert Q(1,25)-Q(3,16)*Q(24,25)==-Q(7,50)
    assert min(Q(1,20),Q(7,50),4*Q(1,2**19))==Q(1,2**17)
    spot=lines(folder,'spot4.stdout.jsonl')[1:]
    assert [r['box'] for r in spot]==[s['largest'][2] for s in slabs]
    leaves=[child for r in spot for child in small_boxes(r)]
    pending={box for box,u in leaves if u>=0}
    first=len(pending);assert len(leaves)==24 and first==4
    extra=0
    for r in lines(folder,'spot5.stdout.jsonl'):
        if 'subbox_upper' not in r:continue
        assert tuple(r['box']) in pending
        pending.remove(tuple(r['box']))
        children=small_boxes(r);extra+=len(children)
        pending.update(box for box,u in children if u>=0)
    assert not pending and extra==32
    diagnostics=lines(folder,'original4.stdout.jsonl')[1:-1]
    assert len(diagnostics)==8 and all(v['matched'] and v['difference']<2e-6 for v in diagnostics)
    print(json.dumps(dict(status=status,sufficient_lambda=5,tail_cut=8,
          scaled_uniform_upper="-1/131072",finite_largest= str(largest),
          negative_leaves=1845,excluded_leaves=5,unresolved=0,
          separate_arb_initial_unresolved=first,separate_arb_refined_children=extra,
          separate_arb_final_unresolved=len(pending),original_E_points=len(diagnostics),
          original_E_max_fd_difference=max(v['difference'] for v in diagnostics))))
