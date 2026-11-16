"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Deterministic pre-run box generator."""
import json
from pathlib import Path
from flint import fmpq as Q


def around(c,width,lo,hi):
    # Full width. At domain endpoints translate inward, never go out of scope.
    a = max(lo,min(c-width/2,hi-width))
    return [str(a),str(a+width)]


def specification():
    boxes = []
    for lam in (Q(2),Q(7,2),Q(5)):
        for r in (Q(1,8),Q(1,2),Q(7,8)):
            for t in (Q(0),Q(1,2),Q(1)):
                boxes.append({'id':len(boxes), 'anchor':[str(r),str(t),str(lam)],
                              'R':around(r,Q(1,64),Q(0),Q(15,16)),
                              'tau':around(t,Q(1,64),Q(0),Q(1)),
                              'lam':around(lam,Q(1,256),Q(2),Q(5))})
    return {'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','precisions':[128,192],
            'cells':[32,64],'series_N':96,
            'width_convention':'total width; endpoint anchors use inward translation',
            'rule':'No result-dependent changes to boxes, cells, or series order.',
            'boxes':boxes}


if __name__ == '__main__':
    p = Path(__file__).with_name('boxes.json')
    with p.open('x') as f:
        f.write(json.dumps(specification(),indent=2)+'\n')
