"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed center box-width pilot B."""
from pathlib import Path
import csv,time
from center_interval import center
ROOT=Path(__file__).resolve().parents[1]

def run():
    scale=163840
    with (ROOT/'out/center_pilot_b.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow('case shrink slo_i shi_i tlo_i thi_i scale nmu nw component lower upper elapsed_seconds result'.split())
        for case in [0,7,20,27,31,32]:
            for shrink in [8,16,32,64,128]:
                if case==32:
                    shi=524288;thi=983040;slo=shi-90112//shrink;tlo=thi-102400//shrink
                else:
                    j,i=divmod(case,4)
                    sm=(1280+704*i+352)*128;tm=(1280+800*j+400)*128
                    ds=45056//shrink;dt=51200//shrink
                    slo,shi,tlo,thi=sm-ds,sm+ds,tm-dt,tm+dt
                for n in [512,1024]:
                    start=time.perf_counter()
                    v=center(slo,shi,tlo,thi,scale=scale,nmu=n,components=(2,))[2]
                    elapsed=time.perf_counter()-start
                    w.writerow([case,shrink,slo,shi,tlo,thi,scale,n,n//2,3,*v,elapsed,'positive' if v[0]>0 else 'unresolved']);f.flush()
            print('pilot center case',case,flush=True)
if __name__=='__main__':run()
