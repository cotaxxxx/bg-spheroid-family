"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Prespecified refinements of inconclusive separate F1 checks."""
import itertools
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path
from time import perf_counter
sys.path.insert(0,str(Path(__file__).resolve().parent))
import spot_arb

STATUS=spot_arb.STATUS


def children(box):
    for corner in itertools.product((0,1),repeat=3):
        out=[]
        for j,c in enumerate(corner):
            a,b=box[2*j:2*j+2]
            assert (a+b)%2==0
            m=(a+b)//2
            out.extend((a,m) if c==0 else (m,b))
        yield tuple(out)


def run(job):
    spot_arb.NM,spot_arb.NA=512,64
    return spot_arb.run(job)


if __name__=="__main__":
    start=perf_counter()
    lines=[json.loads(s) for s in Path(sys.argv[1]).read_text().splitlines()][1:]
    tasks=[(f"{r['case']}.{j}",b) for r in lines
           for j,(b,u) in enumerate(zip(children(r['box']),r['subbox_upper'])) if Fraction(u)>=0]
    print(json.dumps(dict(status=STATUS,parents=tasks,grid=[512,64])),flush=True)
    with ProcessPoolExecutor(max_workers=4) as pool:
        for level in (1,2):
            if not tasks:break
            next_tasks=[]
            for r in pool.map(run,tasks):
                print(json.dumps(dict(level=level,**r)),flush=True)
                for j,(b,u) in enumerate(zip(children(r['box']),r['subbox_upper'])):
                    if Fraction(u)>=0: next_tasks.append((f"{r['case']}.{j}",b))
            tasks=next_tasks
    print(json.dumps(dict(status=STATUS,remaining=len(tasks),wall_seconds=round(perf_counter()-start,3))))
    sys.exit(1 if tasks else 0)
