"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed finite-window cover; output includes all branch decisions."""
import gzip
import io
import json
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
from time import monotonic

SCALE=4096
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"


def rule(box):
    l0,l1,r0,r1,z0,z1=box
    scores=[8*(r1-r0),8*(z1-z0),l1-l0]
    span=max(scores)
    if span>=8192: grid=(32,4)
    elif span>=4096: grid=(64,8)
    elif span>=2048: grid=(128,16)
    elif span>=1024: grid=(256,16)
    elif span>=512: grid=(256,32)
    elif span>=256: grid=(512,32)
    elif span>=128: grid=(512,64)
    else: grid=(1024,64)
    return grid, (2,4,0)[scores.index(span)], span


def slab(args):
    k,binpath,tabpath,outdir=args
    out=Path(outdir)/("cover_"+str(k)+".tsv.gz")
    if out.exists(): raise FileExistsError(out)
    start=monotonic()
    stack=[("r",(k*SCALE,(k+1)*SCALE,0,SCALE,0,SCALE))]
    counts=dict(split=0,negative=0,empty=0,open=0)
    largest=None
    with open(out,'xb') as raw, gzip.GzipFile(filename="",mode='wb',fileobj=raw,mtime=0) as compressed:
        with io.TextIOWrapper(compressed,encoding="utf-8",newline="\n") as log:
            log.write("# "+STATUS+"\npath\tl0\tl1\tr0\tr1\tz0\tz1\tnm\tna\tkind\tnum\tden\n")
            with subprocess.Popen([binpath,tabpath],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True) as worker:
                while stack:
                    path,box=stack.pop()
                    grid,cut,span=rule(box)
                    if sum(counts.values())>=100000 or monotonic()-start>=880:
                        kind,num,den='open',0,1
                    else:
                        worker.stdin.write(" ".join(map(str,box+grid))+"\n")
                        worker.stdin.flush()
                        words=worker.stdout.readline().split()
                        if len(words)!=3: raise RuntimeError("incomplete result "+str(box))
                        typ,num,den=words[0],int(words[1]),int(words[2])
                        if typ=='empty': kind='empty'
                        elif typ!='upper' or den<=0: raise RuntimeError("invalid result")
                        elif num<0: kind='negative'
                        elif span<=64: kind='open'
                        else: kind='split'
                    if kind=='split':
                        a,b=list(box),list(box)
                        assert (box[cut]+box[cut+1])%2==0
                        m=(box[cut]+box[cut+1])//2
                        a[cut+1]=b[cut]=m
                        stack.extend([(path+"1",tuple(b)),(path+"0",tuple(a))])
                    elif kind=='negative':
                        v=Fraction(num,den)
                        if largest is None or v>largest[0]: largest=(v,path,box)
                    log.write("\t".join(map(str,(path,)+box+grid+(kind,num,den)))+"\n")
                    counts[kind]+=1
                worker.stdin.close()
                if worker.wait(): raise RuntimeError("bad worker exit")
    return dict(status=STATUS,lambda_slab=[k,k+1],counts=counts,
                largest=None if largest is None else [str(largest[0]),largest[1],largest[2]],
                wall_seconds=round(monotonic()-start,4))


if __name__=="__main__":
    binary,tables,out=sys.argv[1:4]
    with ProcessPoolExecutor(max_workers=3) as pool:
        for record in pool.map(slab,[(i,binary,tables,out) for i in (5,6,7)]):
            print(json.dumps(record),flush=True)
