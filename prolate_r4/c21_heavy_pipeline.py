"""Run one bounded diagnostic session, then exact check and archive.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Does NOT run 36h in background.
"""
from __future__ import annotations
import argparse,json
from . import c21_heavy_cover as cover
from . import c21_heavy_verify as verify
from . import c21_heavy_plot as plot
from . import c21_heavy_receipt as receipt
from . import c21_heavy_pack as pack
from . import c21_heavy_w as W
STATUS=cover.STATUS
def main():
 a=argparse.ArgumentParser()
 a.add_argument("--session-seconds",type=float,default=129600.)
 a.add_argument("--max-batches",type=int)
 options=a.parse_args()
 cover.run_session(options.session_seconds,options.max_batches)
 verify.check()
 plot.build()
 sel=W.frozen_selection()
 if sel is None:
  cover.atomic({"status":STATUS,"W_interval":None,"W_selection":"DEFERRED",
    "reason":"PENDING_UNEVALUATED, or fewer than three evaluated tubes",
    "full_tube_W":False},cover.OUT/"W_DEFERRED.json")
 else:
  print("W_SELECTION_READY: run separate 3-box W sampler only within global wall budget")
 cover.atomic({"status":STATUS,"ref_E_full_grid":"NOT_PERFORMED",
   "reason":"Direct E finite differences and quadrature are numerical only; "
    "terminal samples and valid nonaxis points require post-measurement selection"},
    cover.OUT/"E_REFERENCE_STATUS.json")
 receipt.build()
 pack.pack()
 print("PIPELINE_DONE",STATUS)
if __name__=="__main__":main()
