"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Reconstruct partition, check exact signs, optionally replay all leaves."""
import argparse
import csv
from fractions import Fraction as Q
import gzip
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic

status="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
scale=4096


def check_one(base,k,worker):
    with gzip.open(base/("cover_"+str(k)+".tsv.gz"),'rt') as f:
        assert f.readline().strip()=="# "+status
        rows=list(csv.DictReader(f,delimiter="\t"))
    records={r['path']:r for r in rows}
    assert len(rows)==len(records)
    counts=dict(negative=0,empty=0,split=0,open=0)
    top=None
    stack=[('r',(k*scale,(k+1)*scale,0,scale,0,scale))]
    volume=Q(0)
    while stack:
        path,b=stack.pop()
        row=records.pop(path)
        assert tuple(int(row[n]) for n in ('l0','l1','r0','r1','z0','z1'))==b
        nm,na=int(row['nm']),int(row['na'])
        kind=row['kind'];counts[kind]+=1
        a,d=int(row['num']),int(row['den'])
        if kind=='split':
            assert a>=0 and d==2*nm*na*(1<<24)
            # Infer the cut from the child records, independently of producer priorities.
            child0=records[path+'0'];child1=records[path+'1']
            names=('l0','l1','r0','r1','z0','z1')
            left=tuple(int(child0[n]) for n in names)
            right=tuple(int(child1[n]) for n in names)
            diffs=[i for i in range(6) if left[i]!=b[i]]
            assert len(diffs)==1 and diffs[0] in (1,3,5)
            j=diffs[0]
            assert left[j]==right[j-1] and 2*left[j]==b[j]+b[j-1]
            assert all(right[h]==b[h] for h in range(6) if h!=j-1)
            assert b[j-1]<left[j]<b[j]
            stack.extend([(path+'0',left),(path+'1',right)])
            continue
        volume+=Q((b[1]-b[0])*(b[3]-b[2])*(b[5]-b[4]),scale**3)
        if kind=='empty':
            assert a==0 and d==1
            assert b[2]**2+b[4]**2>scale**2 or Q(b[4]**2,scale**2)+Q(scale**2,b[1]**2)>1
        elif kind=='negative':
            assert a<0 and d==2*nm*na*(1<<24)
            val=Q(a,d)
            if top is None or val>top[0]:top=(val,path,b)
        else:
            assert kind=='open'
            continue
        if worker:
            worker.stdin.write(" ".join(map(str,b+(nm,na)))+"\n");worker.stdin.flush()
            actual=worker.stdout.readline().split()
            assert actual==["upper" if kind=='negative' else 'empty',str(a),str(d)],(path,actual)
    assert not records and volume==1
    return dict(slab=k,counts=counts,volume=str(volume),
                largest=None if top is None else [str(top[0]),top[1],top[2]])


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path);parser.add_argument('--replay',nargs=2)
    args=parser.parse_args()
    start=monotonic()
    worker=subprocess.Popen(args.replay,stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True) if args.replay else None
    try:
        with open(args.directory/"probe1.stdout.jsonl") as f: rows=[json.loads(s) for s in f]
        tail={r['lam']:list(map(Q,r['upper_exact'])) for r in rows if 'lam' in r}
        assert all(x<0 for x in tail['8'])
        assert all(x<cap for x,cap in zip(tail['5'],(Q(1),Q(1),Q(-3,16))))
        rec=[check_one(args.directory,k,worker) for k in (5,6,7)]
        print(json.dumps(dict(status=status,replayed=bool(worker),slabs=rec,
                             wall_seconds=round(monotonic()-start,4))),flush=True)
    finally:
        if worker:
            worker.stdin.close()
            if worker.wait():raise RuntimeError("replay failed")
    sys.exit(1 if any(r['counts']['open'] for r in rec) else 0)
