"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed 5x5x5 Stage1 feasibility preflight."""
from itertools import product
import argparse, json
from pathlib import Path
from flint import ctx, fmpq as Q
from majorant import majorant

def run(path):
    ctx.prec=128
    grid=[(Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)),
          (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)),
          (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1))]
    items=[]
    for h,v,w in product(*grid):
        a=majorant(((h,h),(v,v),(w,w)))
        items.append({'point':[str(h),str(v),str(w)],'A':str(a['A']),
            'violates_1_8':a['A']>Q(1,8)})
    bad=[x for x in items if x['violates_1_8']]
    result={'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
      'scope':'pointwise feasibility only, not a full box2 run',
      'points_tested':len(items),'violating':len(bad),
      'maximum_A':str(max(Q(x['A']) for x in items)),
      'fixed_threshold':'1/8','stage1_executed':False,
      'violators':bad}
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(f"{len(bad)}/{len(items)} exceed 1/8")
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    run(ap.parse_args().output)
