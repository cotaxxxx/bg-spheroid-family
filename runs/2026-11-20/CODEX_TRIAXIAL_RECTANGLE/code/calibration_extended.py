"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Width and boundary stress calibration C2.

Imports the immutable C1A arithmetic. Only the geometric enclosures differ:
bounded direction components replace ratios in cells intersecting contact.
"""
from pathlib import Path
import itertools,csv,argparse,time,multiprocessing as mp
import numpy as np
from calibration import Box,box,lo,hi,pi_box,angle_ranges,outward_sum,case,UNIT,MODES,ROOT

LADDER=[128,256,512,1024,2048]
SHAPES=[0,7,24,31]
BOUNDARY={
    'G3_123':(43691,21845,43691),
    'G3_13':(39322,0,52429),
    'G3_23':(0,39322,52429),
    'D12':(39322,52429,0),
}

def make_cases():
    ans=[]
    for ident in SHAPES:
        for half in [256,1024,4096]:
            for mode in MODES:
                sp=case(ident,mode)
                sc=(sp['slo']+sp['shi'])//2;tc=(sp['tlo']+sp['thi'])//2
                sp.update(slo=max(UNIT,sc-half),shi=min(209716,sc+half),
                          tlo=max(UNIT,tc-half),thi=min(6*UNIT,tc+half),
                          experiment='shape_width',half=half,domain='ball_interior')
                ans.append(sp)
        for mode in MODES:
            sp=case(ident,mode)
            for i,c in enumerate(BOUNDARY[mode],1):
                sp[f'q{i}lo']=c-8 if c else 0
                sp[f'q{i}hi']=c+8 if c else 0
            sp.update(experiment='boundary_box',half=16,domain='intersection_closed_ball')
            ans.append(sp)
    return ans

def enclosure(spec,M):
    W=M//2
    s=Box(spec['slo']/UNIT,spec['shi']/UNIT)
    t=Box(spec['tlo']/UNIT,spec['thi']/UNIT)
    q=[Box(spec[f'q{i}lo']/UNIT,spec[f'q{i}hi']/UNIT) for i in range(1,4)]
    aa3=s*t
    A=[Box(1),s.sq(),aa3.sq()]
    normq=(q[0].sq()+q[1].sq()+q[2].sq()).sqrt()
    if not normq.a < 1: raise ValueError('empty closed-ball intersection')
    if spec['domain']=='ball_interior' and not normq.b < 1: raise ValueError('not interior')
    minD=0 if normq.b>=1 else (1-normq).sq().a
    minB=(Box(1)/A[2]).a
    ratio_bound=float((Box(1)/(2*s)).b)
    b_bound=float(aa3.b)
    w=Box(np.arange(W)/W,np.arange(1,W+1)/W)
    den=1+w.sq();cp=(1-w.sq())/den;sp=2*w/den
    weight=Box(4)/pi_box()/den
    sums=[];contact=0
    for start in range(0,M,16):
        j=np.arange(start,start+16)[:,None]
        mu=Box(-1+2*j/M,-1+2*(j+1)/M)
        radial=(1-mu.sq()).cut(0,1).sqrt()
        xa=[radial*cp,radial*sp,mu]
        total=Box(0)
        for sg1,sg2 in itertools.product([-1,1],repeat=2):
            xi=[sg1*xa[0],sg2*xa[1],mu]
            v=[xi[i]-q[i] for i in range(3)]
            D2=(v[0].sq()+A[1]*v[1].sq()+A[2]*v[2].sq()).cut(minD,np.inf)
            B=(xi[0].sq()+xi[1].sq()/A[1]+xi[2].sq()/A[2]).cut(minB,1)
            regular=D2.a>0
            contact+=int(np.count_nonzero(~regular))
            safeD2=Box(np.where(regular,D2.a,1),np.where(regular,D2.b,1))
            D,S=safeD2.sqrt(),B.sqrt()
            k=(1-q[0]*xi[0]-q[1]*xi[1]-q[2]*xi[2]).cut(0,2)
            rawgamma=k/(D*S)
            gamma=Box(np.where(regular,rawgamma.a,0),np.where(regular,rawgamma.b,1)).cut(0,1)
            ang=angle_ranges(gamma)
            if spec['mode']=='D12':
                raw=v[0]*v[1]/safeD2
                first=Box(np.where(regular,raw.a,-ratio_bound),np.where(regular,raw.b,ratio_bound)).cut(-ratio_bound,ratio_bound)
                second=(xi[0]*xi[1]/(A[1]*B)).cut(-ratio_bound,ratio_bound)
                val=k*ang['R']*(first-second)/(q[0]*q[1])
            else:
                rawb=A[2]*v[2]/D
                b=Box(np.where(regular,rawb.a,-b_bound),np.where(regular,rawb.b,b_bound)).cut(-b_bound,b_bound)
                val=(xi[2]*ang['J']-b*S*ang['K'])/q[2]
            total=total+val
        weighted=weight*total/4
        sums.append((outward_sum(weighted.a,False),outward_sum(weighted.b,True)))
    a=np.asarray(sums)
    value=Box(outward_sum(a[:,0],False),outward_sum(a[:,1],True))/(M*W)
    return value,contact

def evaluate(spec):
    rows=[]
    for M in LADDER:
        tick=time.perf_counter()
        value,contact=enclosure(spec,M)
        seconds=time.perf_counter()-tick
        lower,upper=float(value.a),float(value.b)
        state='positive' if lower>0 else ('negative' if upper<0 else 'unresolved')
        rows.append({**spec,'unit':UNIT,'nmu':M,'nw':M//2,'sphere_cells':4*M*(M//2),
                     'contact_cells':contact,'lower':lower,'upper':upper,'width':upper-lower,
                     'seconds':seconds,'result':state})
        if state=='positive':break
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=2)
    ar=ap.parse_args()
    if not 1<=ar.workers<=2: raise ValueError('worker limit')
    cs=make_cases()
    keys=list(cs[0])+['unit','nmu','nw','sphere_cells','contact_cells','lower','upper','width','seconds','result']
    with (ROOT/'out/calibration_extended.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader()
        with mp.Pool(ar.workers) as pool:
            for rows in pool.imap(evaluate,cs):
                w.writerows(rows);f.flush()
                x=rows[-1]
                print(x['shape'],x['experiment'],x['half'],x['mode'],x['nmu'],x['lower'],x['upper'],x['result'],flush=True)

if __name__=='__main__':main()
