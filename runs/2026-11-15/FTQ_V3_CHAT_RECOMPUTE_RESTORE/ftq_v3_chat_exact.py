"""chat independent EXACT certificate production for FT_q V3 (mu16 / P-only).
Independent implementation: own interval recipe (ftq_v2_chat.py), own polynomial/Bernstein code,
float LP (HiGHS) only to find multipliers; exact rational residual/gain recomputed with flint/Fraction.
Every branch bound ell is a valid exact certificate (feasible point of the LP), not necessarily optimal.
"""
import sys, time, json
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
from math import comb
from itertools import product
import numpy as np
from scipy.optimize import linprog
from flint import fmpq_mat, fmpq

src=open("ftq_v2_chat.py").read().replace("\nmain()\n","\n"); m={}; exec(src,m)
pm,pa,ps,pc,pconst,pva=m['pmul'],m['padd'],m['psub'],m['pscale'],m['pconst'],m['pvar_affine']
NV=4
def pvar(i): return {tuple(int(j==i) for j in range(NV)):F(1)}
def ppow(a,e):
    o=pconst(1)
    for _ in range(e): o=pm(o,a)
    return o
RD=(4,4,6,2); MD=(0,2,2,1)
def P2B(d):
    return [[F(comb(i,j),comb(d,j)) if j<=i else F(0) for j in range(d+1)] for i in range(d+1)]
def kron(A,B):
    return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def tomat(L): return fmpq_mat([[fmpq(x.numerator,x.denominator) for x in r] for r in L])
M_red=tomat(kron(kron(P2B(4),P2B(6)),P2B(2)))        # 105x105 for (gamma,k,n) degrees (4,6,2)
M_full=tomat(kron(kron(kron(P2B(4),P2B(4)),P2B(6)),P2B(2)))  # 525x525
RIDX=list(product(*[range(d+1) for d in RD]))
RIDX_red=list(product(range(5),range(7),range(3)))
POS_full={e:i for i,e in enumerate(RIDX)}; POS_red={e:i for i,e in enumerate(RIDX_red)}
def vec_full(p):
    v=[F(0)]*len(RIDX)
    for e,c in p.items(): v[POS_full[e]]=c
    return v
def vec_red(p):
    v=[F(0)]*len(RIDX_red)
    for e,c in p.items():
        assert e[0]==0; v[POS_red[e[1:]]]=c
    return v
def colmat(vs): return fmpq_mat([[fmpq(v[i].numerator,v[i].denominator) for v in vs] for i in range(len(vs[0]))])
def tofrac(x): return F(int(x.p),int(x.q))
# Bernstein basis polys of degree MD (in y coords), power basis
BB=[]
for al in product(*[range(d+1) for d in MD]):
    p=pconst(1)
    for v in range(NV):
        y=pvar(v); one=pconst(1)
        p=pm(p,pc(pm(ppow(y,al[v]),ppow(ps(one,y),MD[v]-al[v])),comb(MD[v],al[v])))
    BB.append(p)
assert len(BB)==18
def enclosure_trace(tau,mu,s,lam,t,eps):
    I,add,sub,mul,div,sq,cut,root=[m[x] for x in "I add sub mul div sq cut root".split()]
    R=lambda x:(1-x*x)/(1+x*x); Z=lambda x:2*x/(1+x*x)
    rr=(R(tau[1]),R(tau[0])); zz=(Z(tau[0]),Z(tau[1]))
    mu2=sq(mu); a2=sub(I(1),mu2); aa=cut(root(a2),I(0,1)); se=mul(I(eps),s)
    X=sub(mul(aa,se),rr); x2=sq(X); y2=mul(a2,sub(I(1),sq(s)))
    delta=sub(mu,zz); d2=sq(delta)
    Sdot=mul(I(2),sub(sub(I(1),mul(mul(rr,aa),se)),mul(zz,mu))); Ssos=add(add(x2,y2),d2)
    S=cut(cut(Sdot,Ssos),I(0,4)); tr=rr[0]**2*(1-s[1]**2); nc=2*(1-zz[1]) if eps==-1 else F(0)
    S=cut(S,(max(S[0],tr,nc),F(4)))
    w2=(lam[0]**2+(1-lam[0]**2)*mu2[0],lam[1]**2+(1-lam[1]**2)*mu2[1])
    return m['enclosure'](tau,mu,s,lam,t,eps),dict(S=S,delta2=d2,y2=y2,w2=w2)
def constraints(tr,lo,hi):
    Slo,Shi=tr['S']; dzlo,dzhi=tr['delta2']; ylo,yhi=tr['y2']; vlo,vhi=tr['w2']
    assert vlo>0
    return dict(l2=lo*lo,alpha=max(F(1),vlo/(hi*hi)),LT=lo*lo*Slo/(4*vhi),UT=hi*hi*Shi/(4*vlo),
        LZ=lo*lo*(1-lo*lo)*dzlo/(4*vhi),UZ=hi*hi*(1-hi*hi)*dzhi/(4*vlo),LY=lo*lo*ylo/(4*vhi),UY=hi*hi*yhi/(4*vlo))
def branch(box,cst):
    (t,g,k,n)=box
    T_=pva(0,*t);G=pva(1,*g);Kv=pva(2,*k);N=pva(3,*n); one=pconst(1)
    K=pm(Kv,Kv); T=pm(pm(G,G),K); TK1=pm(T,ps(one,K)); TKN=pm(pm(T,K),N)
    qs=[ps(pm(K,ps(one,pc(N,1-cst['l2']))),pconst(cst['l2'])), ps(ps(one,pm(K,N)),pc(T,cst['alpha'])),
        ps(T,pconst(cst['LT'])), ps(pconst(cst['UT']),T), ps(TK1,pconst(cst['LZ'])), ps(pconst(cst['UZ']),TK1),
        ps(TKN,pconst(cst['LY'])), ps(pconst(cst['UY']),TKN)]
    t2=pm(T_,T_); c=ps(one,t2); A=pa(pa(one,t2),pm(c,G)); q=ps(one,pc(K,2)); q2=pm(q,q)
    Fp=ps(pm(A,ps(one,N)), pm(pm(ps(pc(A,2),pm(G,c)),N),q2))
    Np=pm(G,Fp); Dp=pm(K,pm(A,A))
    # exact Bernstein (4,4,6,2)
    ND=M_full*colmat([vec_full(Np),vec_full(Dp)])
    nB=[tofrac(ND[i,0]) for i in range(525)]; dB=[tofrac(ND[i,1]) for i in range(525)]
    assert min(dB)>0
    ell0=min(nB[i]/dB[i] for i in range(525))
    b0=[nB[i]-ell0*dB[i] for i in range(525)]
    assert min(b0)>=0
    # exact H reduced (105 x 144)
    Hred=M_red*colmat([vec_red(pm(bp,qq)) for qq in qs for bp in BB])
    Hred_f=np.array([[float(tofrac(Hred[i,j])) for j in range(144)] for i in range(105)])
    Hf=np.vstack([Hred_f]*5)  # row index (it, red) with it outer, matches RIDX ordering (t outermost)
    df=np.array([float(x) for x in dB]); b0f=np.array([float(x) for x in b0])
    A_ub=np.column_stack([df,Hf])
    res=linprog(c=np.r_[-1.0,np.zeros(144)],A_ub=A_ub,b_ub=b0f,bounds=[(0,None)]*145,method='highs')
    if res.status!=0: a=[F(0)]*144; zf=0.0
    else: a=[F(max(float(x),0.0)) for x in res.x[1:]]; zf=float(res.x[0])
    # exact Ha
    av=fmpq_mat([[fmpq(x.numerator,x.denominator)] for x in a])
    Ha_red=Hred*av; Ha=[tofrac(Ha_red[i,0]) for i in range(105)]*5
    z=min((b0[i]-Ha[i])/dB[i] for i in range(525))
    if z<0: a=[F(0)]*144; Ha=[F(0)]*525; z=F(0)
    b=[b0[i]-z*dB[i]-Ha[i] for i in range(525)]
    assert min(b)>=0 and z>=0 and min(a)>=0
    # exact identity check by reconstruction: N - ell D == sum b_i beta_i + sum sigma_q Q_q  (coefficientwise in degree r)
    ell=ell0+z
    lhs=[nB[i]-ell*dB[i] for i in range(525)]
    rhs=[b[i]+z*0+Ha[i] for i in range(525)]
    assert all(lhs[i]==rhs[i] for i in range(525))
    return dict(ell0=ell0,z=z,ell=ell,zf=zf,status=res.status)
def main(out):
    taus=[F(7,8)+F(i,32) for i in range(5)];mus=[F(-1)+F(j,8) for j in range(17)];ss=[F(h,2) for h in range(3)]
    lams=[F(2,5)+F(13*a,800) for a in range(5)];ts=[F(b,4) for b in range(5)]
    t0=time.time(); Sia={}; cnt={'pos':0,'zero':0,'neg':0,'lpfail':0}; nb=0; records=[]
    for i in range(4):
      for a in range(4):
        tot=F(0)
        for j in range(16):
          for h in range(2):
            for b in range(4):
              pair=F(0)
              for eps in (1,-1):
                box,tr=enclosure_trace((taus[i],taus[i+1]),(mus[j],mus[j+1]),(ss[h],ss[h+1]),(lams[a],lams[a+1]),(ts[b],ts[b+1]),eps)
                r=branch(box,constraints(tr,lams[a],lams[a+1])); nb+=1
                cnt['pos' if r['ell']>0 else 'zero' if r['ell']==0 else 'neg']+=1
                if r['status']!=0: cnt['lpfail']+=1
                pair+=r['ell']; records.append([i,j,h,a,b,eps,str(r['ell0']),str(r['z']),str(r['ell'])])
              tot+=pair/(192 if h==0 else 96)
        Sia[(i,a)]=tot
        print("S",i,a,float(tot),"branches",nb,"elapsed",round(time.time()-t0),flush=True)
    m0=min(Sia.values()); arg=min(Sia,key=Sia.get)
    print("chat exact m0 =",float(m0),"argmin",arg,"counts",cnt)
    print("295346256371/10^12 <= m0_chat:",F(295346256371,10**12)<=m0, " m0_chat < 295346256372/10^12:",m0<F(295346256372,10**12))
    json.dump({'m0':str(m0),'argmin':list(arg),'Sia':{f"{i},{a}":str(v) for (i,a),v in Sia.items()},'counts':cnt,'branches':records},open(out,'w'))
if __name__=="__main__": main(sys.argv[1])
