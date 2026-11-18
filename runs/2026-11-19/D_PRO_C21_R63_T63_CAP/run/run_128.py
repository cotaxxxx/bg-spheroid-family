"""C21 R63_T63 external epsilon cap diagnostic.
Only imports byte-identical Astra cap_interval.py. DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import json,time,multiprocessing as mp
from pathlib import Path
from flint import fmpq as F,ctx
from cap_interval import geometry,record
ctx.prec=128
ROOT=Path(__file__).resolve().parent
G=None
def init():
 global G
 G=geometry(96,48)
def compute(indices):
 i,j,k=indices
 e0=F(1,5); step=(F(16,79)-e0)/2
 eb=(e0+step*i,e0+step*(i+1))
 wb=(F(j,8),F(j+1,8));ub=(F(k,8),F(k+1,8))
 v=record((eb,wb,ub),G);v['index']=[i,j,k]
 return v
def main():
 ids=[(i,j,k) for i in range(2) for j in range(8) for k in range(8)]
 started=time.monotonic();rows=[]
 out=ROOT/'CAP_R63_T63_128.jsonl'
 assert not out.exists(),"Existing results — do not overwrite"
 with out.open("x") as f,mp.Pool(2,initializer=init) as pool:
  for row in pool.imap(compute,ids,chunksize=1):
   rows.append(row);f.write(json.dumps(row,sort_keys=True)+"\n");f.flush()
   if len(rows)%32==0:print("PROGRESS",len(rows),"min",min(float(r['lower_exact'].split('/')[0])/float(r['lower_exact'].split('/')[1]) if '/' in r['lower_exact'] else float(r['lower_exact']) for r in rows),flush=True)
 elapsed=time.monotonic()-started
 from fractions import Fraction as Q
 mini=min(rows,key=lambda x:Q(x['lower_exact']))
 summary={"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","purpose":"R63_T63 polar E_z stationarity exclusion candidate","lambda_plate":["79/16","5"],"epsilon":["1/5","16/79"],"precision_bits":128,"geometry_cells":[96,48],"outer_grid":[2,8,8],"planned_count":128,"count":len(rows),"workers":2,"all_lower_gt_zero":all(Q(r["lower_exact"])>0 for r in rows),"all_lower_gt_one_quarter":all(Q(r["lower_exact"])>Q(1,4) for r in rows),"minimum_lower_exact":mini["lower_exact"],"minimum_index":mini["index"],"minimum_lower_float":float(Q(mini["lower_exact"])),"wall_seconds":elapsed,"frozen_cap_interval_source_unchanged":True,"heavy_slab_state_untouched":True}
 (ROOT/'CAP_R63_T63_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
 print("SUMMARY",json.dumps(summary,sort_keys=True),flush=True)
if __name__=="__main__":main()
