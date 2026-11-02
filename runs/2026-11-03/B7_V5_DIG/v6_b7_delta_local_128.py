"""Adaptive geometric delta hull for V6-B7 local diagnostics. Not a certificate."""
from fractions import Fraction as Q
from time import perf_counter
from v3_fixed_128 import I,iv,mulq_interval
from v6_b7_safe_128 import kernel

def rem_hull(outer,cell,subboxes):
    vol=Q(1)
    for a,b in cell:vol*=b-a
    result=[]
    for i in range(4):
        lo=hi=None
        for sub in subboxes:
            h=sum((kernel(sub,cell,e,('inner',i)).d2 for e in (1,-1)),iv(0))
            lo=h.lo if lo is None else min(lo,h.lo)
            hi=h.hi if hi is None else max(hi,h.hi)
        result.append(mulq_interval(I.raw(lo,hi),vol*(cell[i][1]-cell[i][0])**2/Q(24)))
    return result

def split_geometric(outer):
    a,b=outer[2]
    mid=min(b,2*a) if b>2*a else (a+b)/2
    if mid==b or mid==a:return None
    return (outer[:2]+((a,mid),),outer[:2]+((mid,b),))

def adaptive(outer,cell,threshold=Q(1,10**10),max_boxes=64):
    """Split delta only if the p remainder is below -threshold; deterministic worst-first."""
    start=perf_counter()
    boxes=[outer]
    evaluations=0
    while True:
        rem=rem_hull(outer,cell,boxes)
        evaluations+=4*len(boxes)*2
        if sum(min(0,r.lo) for r in rem)>=-threshold*2**128 or len(boxes)>=max_boxes:break
        candidates=[(float(b[2][1]/b[2][0]),j) for j,b in enumerate(boxes)]
        ratio,j=max(candidates)
        pair=split_geometric(boxes[j])
        if pair is None:break
        boxes[j:j+1]=pair
    return {'boxes':boxes,'rem':rem,'seconds':perf_counter()-start,'kernel_calls':evaluations,
            'threshold_reached':sum(min(0,r.lo) for r in rem)>=-threshold*2**128}
