"""D-PRO R4 V35 option-a rigorous B4 cover gate for four outer child boxes.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No signed 35-coefficient integration here.
Uses CW7 positive-denominator bounds and Neumann B4 only for nonnegative tail.
Resource-limited to prespecified 60s, 32768 leaves / child, depth 16.
"""
from __future__ import annotations
import argparse,heapq,itertools,json,resource,time
from pathlib import Path
from flint import fmpq as Q,ctx
from . import v35_w_split_preflight as V
import stage0 as S
import majorant as M

STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
H=(-Q(1),Q(0),Q(1,2),Q(3,4),Q(7,8),Q(15,16),Q(31,32),Q(63,64),Q(127,128),Q(1))
VV=(Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1))
WW=(Q(0),Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1))
LIMIT_LEAVES=32768
LIMIT_DEPTH=16
LIMIT_SECONDS_PER_CHILD=60.0
A_LIMIT=Q(1,4)
TAIL_LIMIT=Q(3,100)
def spatial_init():
    return [(tuple((arr[i],arr[i+1]) for arr,i in zip((H,VV,WW),idx)),0)
            for idx in itertools.product(range(len(H)-1),range(len(VV)-1),range(len(WW)-1))]
def measure(cell):
    m=Q(1,2)
    for a,b in cell:m*=b-a
    return m
def split(cell):
    lengths=[(b-a)/(Q(2) if i==0 else Q(1)) for i,(a,b) in enumerate(cell)]
    axis=max(range(3),key=lambda i:lengths[i])
    a,b=cell[axis]; mid=(a+b)/2
    out=[]
    for ends in ((a,mid),(mid,b)):
        cp=list(cell);cp[axis]=ends;out.append(tuple(cp))
    return out,axis
def run_child(i,j):
    outer=V.configure(V.RBOUNDS[i],V.TBOUNDS[j])
    before=time.perf_counter()
    pending=spatial_init()
    accept=[]
    accepted_tail=Q(0)
    splits_A=0;splits_tail=0
    processed=0;reject_reason=None
    A_max_accepted=Q(0)
    # All initial 180 patches cover entire [-1,1]x[0,1]x[0,1].
    while True:
        if time.perf_counter()-before >= LIMIT_SECONDS_PER_CHILD:
            reject_reason="TIME_LIMIT";break
        if len(accept)+len(pending)>LIMIT_LEAVES:
            reject_reason="LEAF_LIMIT";break
        if pending:
            cell,depth=pending.pop()
            processed+=1
            ma=M.majorant(cell)
            A=ma["A"]
            if not ma["convergent"] or A>A_LIMIT:
                if depth>=LIMIT_DEPTH:
                    reject_reason="DEPTH_LIMIT_A";break
                ch,axis=split(cell)
                pending.extend([(c,depth+1) for c in ch])
                splits_A+=1
                continue
            upper=ma["tail_upper"]
            if upper is None:
                raise ArithmeticError("missing B4 upper on accepted cell")
            val=measure(cell)*upper
            accept.append((val,cell,depth,A))
            accepted_tail+=val
            A_max_accepted=max(A,A_max_accepted)
        else:
            if accepted_tail<=TAIL_LIMIT:
                break
            # Refine the largest rigorous tail contribution, even if A already
            # passed. This is a deterministic pre-registered refinement rule.
            idx=max(range(len(accept)),key=lambda k:accept[k][0])
            val,cell,depth,A=accept.pop(idx)
            accepted_tail-=val
            if depth>=LIMIT_DEPTH:
                reject_reason="DEPTH_LIMIT_TAIL";break
            children,axis=split(cell)
            pending.extend([(c,depth+1) for c in children])
            splits_tail+=1
    complete=not pending and reject_reason is None
    # With an exhausted budget path, the accept list is an incomplete spatial
    # cover and no global bound is asserted.
    if complete:
        assert sum((measure(c) for _,c,_,_ in accept),Q(0))==1
        assert all(A<=A_LIMIT for _,_,_,A in accept)
        assert accepted_tail<=TAIL_LIMIT
    return {"outer_child":[i,j],**outer,
      "status":STATUS,"scope":"B4-tail-cover-preflight-only",
      "rigorous_complete_B4_cover":complete,
      "rigorous_B4_upper":str(accepted_tail) if complete else None,
      "A_max_accepted":str(A_max_accepted) if complete else None,
      "integrated_tail_of_current_accepted_patches_NOT_COMPLETE":str(accepted_tail),
      "accepted_patches":len(accept),"unprocessed_pending":len(pending),
      "evaluations":processed,
      "A_triggered_splits":splits_A,"tail_budget_triggered_splits":splits_tail,
      "stop_reason":reject_reason,
      "wall_s":time.perf_counter()-before,
      "all_35_signed_coefficients_integrated":False,
      "W_child_enclosure":None}
def main(output):
    ctx.prec=128
    beg=time.perf_counter()
    result=[]
    for i in range(2):
        for j in range(2):
            print("START",i,j,flush=True)
            item=run_child(i,j)
            result.append(item)
            print("FINISH",i,j,{k:item[k] for k in ("rigorous_complete_B4_cover","rigorous_B4_upper","accepted_patches","stop_reason","wall_s")},flush=True)
    report={"status":STATUS,
            "scope":"four child rigorous nonnegative B4 preflight; NO W coefficient integral",
            "fixed_option":"a","V35_source":"e5f1b2450c31481f1e32bf58ad96245e92df9d4f",
            "initial_spatial_patches":(len(H)-1)*(len(VV)-1)*(len(WW)-1),
            "max_depth":LIMIT_DEPTH,"max_leaves":LIMIT_LEAVES,
            "wall_cap_per_child_seconds":LIMIT_SECONDS_PER_CHILD,
            "A_accept_limit":"1/4","B4_integral_budget_per_child":"3/100",
            "children":result,"all_four_B4_complete":all(x["rigorous_complete_B4_cover"] for x in result),
            "W_box2_complete":False,
            "total_elapsed_s":time.perf_counter()-beg,
            "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "note":"No numeric result is a full-box W enclosure. If incomplete, even the tail upper is not for the whole spatial domain."}
    Path(output).write_text(json.dumps(report,indent=2)+"\n")
    print("FINAL all_four",report["all_four_B4_complete"],"elapsed",report["total_elapsed_s"],flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",required=True)
    main(p.parse_args().output)
