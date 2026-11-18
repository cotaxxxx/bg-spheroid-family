"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Rigorous range integral for a polar cap lemma."""
from flint import arb,fmpq as Q,ctx
from pathlib import Path
import json,time
ctx.prec=128
def iv(a,b):
    a,b=Q(a),Q(b)
    return arb((a+b)/2,(b-a)/2)
def sq(x):
    a,b=x.lower().fmpq(),x.upper().fmpq()
    return iv(0 if a<=0<=b else min(a*a,b*b),max(a*a,b*b))
def positive(x):
    a,b=x.lower().fmpq(),x.upper().fmpq()
    return iv(max(Q(0),a),max(Q(0),b))
def geometry(nt=96,np=48):
    pi=arb.pi();lo=arb(Q(3,4)).acos();hi=pi-arb(Q(1,64));dt=(hi-lo)/nt;dp=pi/np
    rows=[]
    ph=[(dp*iv(j,j+1)).cos() for j in range(np)]
    for i in range(nt):
        th=lo+dt*iv(i,i+1);mu=th.cos();ss=th.sin()
        rows.append((mu,ss,sq(ss),sq(mu)))
    return rows,ph,dt*dp/(2*pi)
def bound(box,grid):
    e,w,u=[iv(*a) for a in box];e2=sq(e);ew=e*w;z=(1-sq(ew)).sqrt();r=ew*u;r2=sq(r);pi=arb.pi()
    rows,ph,vol=grid;total=arb(0)
    for mu,ss,s2,mu2 in rows:
        a=z-mu;aa=sq(a);B=s2+e2*mu2;rootB=B.sqrt();T=ss/rootB
        for co in ph:
            k=1-z*mu-r*ss*co
            # Exact nonnegative sum keeps the squared transverse distance valid.
            A=sq(ss-r)+2*ss*r*(1-co)
            d2=aa+e2*A;d=d2.sqrt()
            gamma=e*k/(d*rootB)
            # The actual geometric gamma lies in [0,1].
            gamma=iv(max(Q(0),gamma.lower().fmpq()),min(Q(1),gamma.upper().fmpq()))
            f1=mu*k;f2=mu*k+sq(k)*a/d2
            low=T/d*(pi*(f1+f2)-gamma*(positive(f1)+2*positive(f2)))
            if not low.is_finite():raise ArithmeticError('nonfinite lower envelope')
            total+=low
    far=total*vol
    south=pi/(64*z)
    north=e*sq(w)*(1+sq(w)).sqrt()/(1+z)
    result=far-south-north
    return result,far,south,north
def record(box,grid):
    st=time.monotonic();res,far,south,north=bound(box,grid)
    return {'box':[[str(x) for x in a] for a in box],'interval':str(res),'lower_exact':str(res.lower().fmpq()),'upper_exact':str(res.upper().fmpq()),'gt_one_quarter':bool(res>arb(Q(1,4))),'seconds':time.monotonic()-st,'far':str(far),'south':str(south),'north':str(north)}
if __name__=='__main__':
    boxes=[[(Q(7,40),Q(1,5)),(Q(3,4),Q(1)),(Q(3,4),Q(1))],[(Q(0),Q(1,40)),(Q(3,4),Q(1)),(Q(3,4),Q(1))],[(Q(7,40),Q(1,5)),(Q(0),Q(1,4)),(Q(3,4),Q(1))],[(Q(7,40),Q(1,5)),(Q(3,4),Q(1)),(Q(0),Q(1,4))]]
    grid=geometry();rows=[]
    for b in boxes:
        row=record(b,grid);rows.append(row);print(json.dumps(row),flush=True)
        Path(__file__).with_name('CAP_INTERVAL_PILOT_R1.json').write_text(json.dumps({'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','precision_bits':ctx.prec,'grid':[96,48],'rows':rows},indent=2)+'\n')
