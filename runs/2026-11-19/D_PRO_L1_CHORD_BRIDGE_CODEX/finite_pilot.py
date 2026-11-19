"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed finite-window pilot; no fit parameters."""
import json
import subprocess
import sys
from time import perf_counter

points=[(5,0,0),(5,1/4,0),(5,0,1/4),(5,1/4,1/4),(5,1/2,1/2),
        (5,3/4,0),(5,1,0),(5,3/4,5/8),(5,0,15/16),
        (6,1/4,0),(6,1/2,1/2),(7,1/4,1/2)]
# All fractions above are dyadic, exactly representable.
status="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
with subprocess.Popen(sys.argv[1:3],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True) as worker:
    print(json.dumps({"status":status,"mesh":"128 x 16"}))
    for lam,r,z in points:
        for growing in (False,True):
            x,y=int(4096*r),int(4096*z)
            b=[4096*lam,4096*lam+(512 if growing else 0),
               x,min(4096,x+(64 if growing else 0)),y,min(4096,y+(64 if growing else 0)),128,16]
            start=perf_counter()
            worker.stdin.write(" ".join(map(str,b))+"\n")
            worker.stdin.flush()
            fields=worker.stdout.readline().split()
            if len(fields)!=3: raise RuntimeError("worker missing complete result")
            kind,n,d=fields
            print(json.dumps(dict(box=b,kind=kind,upper=[int(n),int(d)],decimal=int(n)/int(d),
                                  wall_seconds=round(perf_counter()-start,6))),flush=True)
    worker.stdin.close()
    if worker.wait(): raise RuntimeError("worker error")
