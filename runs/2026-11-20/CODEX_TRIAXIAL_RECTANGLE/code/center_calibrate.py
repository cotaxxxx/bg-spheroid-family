"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed 32-box center calibration."""
from pathlib import Path
import csv,json,time,sys
from center_interval import center
ROOT=Path(__file__).resolve().parents[1]

def run():
    scale=1280
    cases=[]
    for j in range(8):
        for i in range(4):
            slo=1280+704*i;shi=slo+704;tlo=1280+800*j;thi=tlo+800
            cases.append((i+4*j,slo,shi,tlo,thi))
    out=ROOT/'out/center_calibration.csv'
    with out.open('w') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow('case mode slo_i shi_i tlo_i thi_i scale nmu nw component lower upper elapsed_seconds result'.split())
        for case,slo,shi,tlo,thi in cases:
            for mode in ['full_shape_box','shape_midpoint']:
                bounds=(slo,shi,tlo,thi) if mode=='full_shape_box' else ((slo+shi)//2,)*2+((tlo+thi)//2,)*2
                for n in [64,128,256]:
                    start=time.perf_counter();v=center(*bounds,scale=scale,nmu=n,components=(2,))[2]
                    elapsed=time.perf_counter()-start
                    w.writerow([case,mode,*bounds,scale,n,n//2,3,*v,elapsed,'positive' if v[0]>0 else 'unresolved'])
                    f.flush()
            print('center calibration',case,flush=True)
    print(out,flush=True)
if __name__=='__main__':run()
