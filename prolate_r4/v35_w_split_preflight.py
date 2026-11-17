"""V35 option-(a) W stage-1 four-child pointwise PRE-FLIGHT ONLY.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Never treats samples as rigorous B4 integration.
"""
import itertools,sys,json,resource,time
from pathlib import Path
from flint import fmpq as Q,ctx
sys.path.insert(0,str(Path(__file__).parent))
import stage0 as S
import majorant as M
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
TF=lambda x:4*x*x/(1+x*x)**2
RBOUNDS=((Q(95,128),Q(3,4)),(Q(3,4),Q(97,128)))
TBOUNDS=((Q(15,128),Q(1,8)),(Q(1,8),Q(17,128)))
LBOUNDS=(Q(1279,256),Q(5))
Q_CENTER=Q(512,2559)**2
Q_RADIUS=max(Q_CENTER-Q(1,25),Q(256,1279)**2-Q_CENTER)
GRID=(
  (Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)),
  (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)),
  (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)),
)
def configure(r,tau):
  rc=(r[0]+r[1])/2
  midtau=(tau[0]+tau[1])/2
  tc=TF(midtau)
  rad=(r[1]-r[0])/2
  trad=max(tc-TF(tau[0]),TF(tau[1])-tc)
  S.RC=M.RC=rc
  S.TC=M.TC=tc
  S.QC=M.QC=Q_CENTER
  S.CENTRE=(rc,tc,Q_CENTER)
  S.RAD=M.RAD=(rad,trad,Q_RADIUS)
  return dict(outer_R=list(map(str,r)),outer_tau=list(map(str,tau)),
              outer_lambda=list(map(str,LBOUNDS)),
              center=list(map(str,S.CENTRE)),radii=list(map(str,S.RAD)))
def run(out):
  ctx.prec=128
  t0=time.monotonic()
  trials=[]
  for i,r in enumerate(RBOUNDS):
    for j,tau in enumerate(TBOUNDS):
      params=configure(r,tau)
      bad=[];mxa=Q(0);mxtail=Q(0);notconv=0
      for h,v,w in itertools.product(*GRID):
        vals=M.majorant(((h,h),(v,v),(w,w)))
        a=vals["A"]
        if a>mxa: mxa=a
        if vals["tail_upper"] is None: notconv+=1
        else: mxtail=max(mxtail,vals["tail_upper"])
        if a>Q(1,4):
          bad.append({"point":[str(h),str(v),str(w)],"A":str(a)})
      trials.append({"child":[i,j],**params,
                     "samples":125,
                     "max_A_point_sample":str(mxa),
                     "violating_1_4_point_samples":len(bad),
                     "nonconvergent_point_samples":notconv,
                     "max_pointwise_tail_density":str(mxtail),
                     "violations":bad})
  obj={"status":STATUS,"scope":"four-child point samples only",
       "v35_correct_commit":"e5f1b2450c31481f1e32bf58ad96245e92df9d4f",
       "fixed_stage1_option":"a","fixed_A_threshold":"1/4",
       "fixed_tail_integral_budget_per_child":"3/100",
       "spatial_coverage_checked":False,"rigorous_tail_integral_calculated":False,
       "stage1_W_executed":False,"child_results":trials,
       "wall_seconds":time.monotonic()-t0,
       "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       "warning":"Point samples alone cannot justify admission of any spatial patch."}
  Path(out).write_text(json.dumps(obj,indent=2)+"\n")
  print(json.dumps({"children":[{"id":x["child"],
                  "max_A_point_sample":x["max_A_point_sample"],
                  "A_sample_violations":x["violating_1_4_point_samples"],
                  "max_tail_density":x["max_pointwise_tail_density"]}
                  for x in trials],
                  "wall_seconds":obj["wall_seconds"]},indent=2))
if __name__=="__main__":
  import argparse
  p=argparse.ArgumentParser()
  p.add_argument("--output",required=True)
  a=p.parse_args()
  run(a.output)
