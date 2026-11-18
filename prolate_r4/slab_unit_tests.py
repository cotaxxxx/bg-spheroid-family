"""Pure exact-rational contract tests for frozen slab controller.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No interval sign evidence.
"""
from fractions import Fraction as F
from . import slab_adaptive as S
from .slab_box_eval import route
def test():
 roots=S.initial()
 assert len(roots)==256
 assert len({x["id"] for x in roots})==256
 assert sum((S.area(x) for x in roots),F(0))==1
 assert roots[0]["id"]=="R00_T00"
 assert roots[1]["id"]=="R00_T08"
 assert roots[2]["id"]=="R08_T00"
 # Route precedence and no spurious z derivative route.
 assert route((F(0),F(1,16)),(F(15,16),F(1)))=="AXIS"
 assert route((F(0),F(1,16)),(F(0),F(1,16)))=="CENTER"
 assert route((F(15,16),F(1)),(F(0),F(1,16)))=="BOUNDARY"
 assert route((F(1,2),F(9,16)),(F(1,2),F(9,16)))=="REGULAR"
 # Parent rectangle is exactly tiled by children; tie must split R.
 root=roots[0]
 children,axis=S.split(root)
 assert axis=="R"
 assert sum((S.area(x) for x in children),F(0))==S.area(root)
 current=children
 for level in range(1,8):
  nxt=[]
  for x in current:
   y,_=S.split(x);nxt.extend(y)
  assert sum((S.area(x) for x in nxt),F(0))==S.area(root)
  current=nxt
 assert all(S.q(x["R"][1])-S.q(x["R"][0])<=F(1,256) and
            S.q(x["tau"][1])-S.q(x["tau"][0])<=F(1,256) for x in current)
 # Synthetic accounting does not classify pending as evaluated tube.
 st={"terminal":[],"pending":roots,"inflight":[],"processed_jobs":[],
     "split_events":[],"wall_elapsed_cumulative_s":600,
     "calibration_wall_s":600,"H_adaptive_wall_s":0,
     "W_sample_wall_s":0}
 sm=S.counts(st)
 assert sm["area_decided_exact"]=="0"
 assert sm["area_tube_evaluated_exact"]=="0"
 assert sm["area_pending_exact"]=="1"
 assert sm["area_partition_sum_exact"]=="1"
 print("DIAGNOSTIC_ONLY / NOT_EVIDENCE")
 print("PASS: 256 initial exact area, deterministic Morton, route precedence")
 print("PASS: exact dyadic tiling/tie R, min width, pending three-way ledger")
if __name__=="__main__":test()
