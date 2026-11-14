"""chat independent recomputation of FT_q V2 production (from V2 architecture doc, independent implementation)."""
from fractions import Fraction as F
from math import isqrt, comb
from itertools import product
import json, sys

# ---------- interval arithmetic (independent re-implementation) ----------
def I(a,b=None): return (F(a),F(a if b is None else b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[1],a[1]-b[0])
def mul(a,b):
    z=[x*y for x in a for y in b]; return (min(z),max(z))
def div(a,b):
    assert b[0]>0; return mul(a,(1/b[1],1/b[0]))
def sq(a):
    lo=F(0) if a[0]<=0<=a[1] else min(a[0]*a[0],a[1]*a[1])
    return (lo,max(a[0]*a[0],a[1]*a[1]))
def cut(a,b):
    o=(max(a[0],b[0]),min(a[1],b[1])); assert o[0]<=o[1],("empty",a,b); return o
def root(a):
    assert a[0]>=0
    def ep(x,up):
        n=isqrt((x.numerator<<64)//x.denominator)
        if up and F(n*n,1<<64)!=x: n+=1
        return F(n,1<<32)
    r=(ep(a[0],False),ep(a[1],True))
    assert r[0]**2<=a[0] and r[1]**2>=a[1]
    return r

def enclosure(tau,mu,s,lam,t,eps):
    R=lambda x:(1-x*x)/(1+x*x); Z=lambda x:2*x/(1+x*x)
    rr=(R(tau[1]),R(tau[0])); zz=(Z(tau[0]),Z(tau[1]))
    mu2=sq(mu); a2=sub(I(1),mu2); aa=cut(root(a2),I(0,1))
    se=mul(I(eps),s)
    X=sub(mul(aa,se),rr); x2=sq(X)
    y2=mul(a2,sub(I(1),sq(s)))
    delta=sub(mu,zz); d2=sq(delta); lam2=sq(lam)
    Sdot=mul(I(2),sub(sub(I(1),mul(mul(rr,aa),se)),mul(zz,mu)))
    Ssos=add(add(x2,y2),d2)
    S=cut(cut(Sdot,Ssos),I(0,4))
    transverse=rr[0]**2*(1-s[1]**2)
    negcos=2*(1-zz[1]) if eps==-1 else F(0)
    S=cut(S,(max(S[0],transverse,negcos),F(4)))
    assert S[1]>0
    zlo=d2[0]/S[1]; zhi=min(F(1),d2[1]/S[0]) if S[0]>0 else F(1)
    zeta=cut((zlo,zhi),I(0,1))
    J=(1-(1-lam[0]**2)*zeta[1],1-(1-lam[1]**2)*zeta[0])
    k=cut(root(J),(lam[0],F(1)))
    e2=add(x2,mul(lam2,d2))
    dl=y2[0]+e2[1]; dh=y2[1]+e2[0]
    nlo=y2[0]/dl if dl>0 else F(0)
    nhi=y2[1]/dh if dh>0 else F(1)
    direc=(1-zeta[0])/(1-(1-lam[0]**2)*zeta[0])
    nhat=cut((nlo,min(nhi,direc)),I(0,1))
    w2=(lam[0]**2+(1-lam[0]**2)*mu2[0],lam[1]**2+(1-lam[1]**2)*mu2[1])
    w=cut(root(w2),(lam[0],F(1))); u=cut(root(S),I(0,2))
    graw=div(mul(lam,u),mul(I(2),mul(w,k)))
    rescue=lam[0]*S[0]/4
    gamma=cut((max(graw[0],rescue),graw[1]),I(0,1))
    return (t,gamma,k,nhat)

# ---------- polynomials in 4 vars (y-coords on [0,1]^4) ----------
NV=4
def padd(a,b):
    d=dict(a)
    for e,v in b.items(): d[e]=d.get(e,F(0))+v
    return {e:v for e,v in d.items() if v}
def pneg(a): return {e:-v for e,v in a.items()}
def psub(a,b): return padd(a,pneg(b))
def pmul(a,b):
    d={}
    for e,v in a.items():
        for f,w in b.items():
            g=tuple(i+j for i,j in zip(e,f)); d[g]=d.get(g,F(0))+v*w
    return {e:v for e,v in d.items() if v}
def pconst(c): return {(0,)*NV:F(c)} if c else {}
def pscale(a,c): return {e:v*c for e,v in a.items()} if c else {}
def pvar_affine(i,lo,hi):
    """variable i mapped: x = lo + (hi-lo) y_i"""
    e=tuple(int(j==i) for j in range(NV))
    p={}
    if lo: p[(0,)*NV]=F(lo)
    if hi-lo: p[e]=F(hi-lo)
    return p
def ppow(a,n):
    o=pconst(1)
    for _ in range(n): o=pmul(o,a)
    return o

def bernstein(p,deg):
    """power coeffs (dict) -> full Bernstein array of multidegree deg on [0,1]^4"""
    # per axis transform: b_i = sum_{j<=i} C(i,j)/C(d,j) a_j
    for e in p: assert all(e[ax]<=deg[ax] for ax in range(NV)),("degree overflow",e,deg)
    arr={}
    idxs=list(product(*[range(d+1) for d in deg]))
    # successive axis transforms on dense dict
    cur={e:v for e,v in p.items()}
    for ax in range(NV):
        d=deg[ax]; new={}
        for e,v in cur.items():
            j=e[ax]
            for i in range(j,d+1):
                f=e[:ax]+(i,)+e[ax+1:]
                new[f]=new.get(f,F(0))+v*F(comb(i,j),comb(d,j))
        cur=new
    for ix in idxs: arr[ix]=cur.get(ix,F(0))
    return arr

DEG_B=(2,1,6,1); DEG_W=(4,2,4,0)

def branch(box):
    (t,g,k,n)=box
    T=pvar_affine(0,*t); G=pvar_affine(1,*g); K=pvar_affine(2,*k); N=pvar_affine(3,*n)
    one=pconst(1)
    t2=pmul(T,T); c=psub(one,t2); A=padd(padd(one,t2),pmul(c,G))
    k2=pmul(K,K); q=psub(one,pscale(k2,2)); q2=pmul(q,q)
    Fp=psub(pmul(A,psub(one,N)), pmul(pmul(psub(pscale(A,2),pmul(G,c)),N),q2))
    B=pmul(k2,Fp)
    bB=bernstein(B,DEG_B)
    Bmin=min(bB.values()); Bmax=max(bB.values())
    den=pmul(pmul(pmul(k2,k2),A),A)
    bD=bernstein(den,DEG_W); bN=bernstein(G,DEG_W)
    assert all(v>0 for v in bD.values()),"den coeff not positive"
    ratios=[bN[ix]/bD[ix] for ix in bD]
    Wmin=min(ratios); Wmax=max(ratios)
    if Bmin>=0: row='P'; ell=Wmin*Bmin
    elif Bmax<=0: row='N'; ell=Wmax*Bmin
    else: row='I'; ell=Wmax*Bmin
    return dict(Bmin=Bmin,Bmax=Bmax,Wmin=Wmin,Wmax=Wmax,row=row,ell=ell,nB=len(bB),nW=len(bD))

def main():
    taus=[F(7,8)+F(i,32) for i in range(5)]
    mus=[F(-1)+F(j,2) for j in range(5)]
    ss=[F(h,2) for h in range(3)]
    lams=[F(2,5)+F(13*a,800) for a in range(5)]
    ts=[F(b,4) for b in range(5)]
    Sia={}; cnt={'P':0,'N':0,'I':0}; g0=0; n1=0; nlt=0; ncoef=0
    worst=[]
    for i in range(4):
        for a in range(4):
            tot=F(0)
            for j in range(4):
                for h in range(2):
                    for b in range(4):
                        ellsum=F(0)
                        for eps in (1,-1):
                            box=enclosure((taus[i],taus[i+1]),(mus[j],mus[j+1]),(ss[h],ss[h+1]),(lams[a],lams[a+1]),(ts[b],ts[b+1]),eps)
                            r=branch(box)
                            cnt[r['row']]+=1; ncoef+=2*(r['nB']+r['nW'])
                            if box[1][0]==0: g0+=1
                            if box[3][1]==1: n1+=1
                            else: nlt+=1
                            ellsum+=r['ell']
                            worst.append((r['ell'],(i,j,h,a,b,eps)))
                        tot+=ellsum/(48 if h==0 else 24)
            Sia[(i,a)]=tot
    m0=min(Sia.values()); arg=min(Sia,key=Sia.get)
    print("counts",cnt,"gamma_min=0:",g0,"n_max=1:",n1,"n_max<1:",nlt,"coeffs:",ncoef)
    print("m0 =",m0,"~",float(m0),"argmin",arg)
    print("-24<m0<-23:", F(-24)<m0<F(-23))
    for (i,a),v in sorted(Sia.items()): print("S",i,a,float(v))
    worst.sort(); print("worst branches:",[(float(e),ix) for e,ix in worst[:5]])
    json.dump({'m0':str(m0),'Sia':{f"{i},{a}":str(v) for (i,a),v in Sia.items()},'counts':cnt},open(sys.argv[1] if len(sys.argv)>1 else 'ftq_v2_chat_out.json','w'),indent=1)
main()
