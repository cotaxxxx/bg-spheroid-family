"""chat independent checks of NP-T (D_OB_P2_D_AN1_NP_T_DRAFT.md, SHA e929d956...). sympy + exact rationals; numeric part is DIAGNOSTIC only."""
import sympy as sp
from fractions import Fraction as Fr
from math import comb
ok={}
q,y,lam,phi,rho=sp.symbols('q y lam phi rho',positive=True)
b=sp.Symbol('b',real=True)
mu=1-q; a2=q*(2-q)
# geometry at general meridional base point (rho,0,lam), then rho->0
D=sp.sqrt(a2-2*rho*b+rho**2+lam**2*(mu-1)**2)
h=lam*(1-rho*b)-lam*mu
w=sp.sqrt(lam**2*a2+mu**2)
ok['S2_h=lam q']=sp.simplify(h.subs(rho,0)-lam*q)==0
ok['S2_w2']=sp.simplify(w**2-((1-q)**2+lam**2*q*(2-q)))==0
d=2-(1-lam**2)*q
ok['S2_D2=q d']=sp.simplify((D**2).subs(rho,0)-q*d)==0
gam=h/(w*D)
Gf=sp.Function('G')
F=h*Gf(gam)
Frr=sp.diff(F,rho,2).subs(rho,0)
Rs,Rg=sp.symbols('R Rg')
Frr=Frr.replace(lambda e: isinstance(e,sp.Subs), lambda e: -2*Rg if e.expr.args[1][1]==2 else -2*Rs)
Frr=Frr.replace(lambda e: isinstance(e,sp.Derivative), lambda e: -2*Rg if len(e.variables)==2 else -2*Rs)
assert not Frr.has(Gf)
# phi-average: b = a cos phi; average of b^0 ->1, b^1 ->0, b^2 -> a2/2 (polynomial in b of degree 2 after rho=0)
Fp=sp.Poly(sp.expand(Frr),b)
assert Fp.degree()<=2
avg=sum(co*( {0:1,1:0,2:a2/2}[k[0]] ) for k,co in Fp.terms())
D0=sp.sqrt(q*d); w0=sp.sqrt((1-q)**2+lam**2*q*(2-q))
Aform=lam**2*sp.sqrt(q)/(w0*d**sp.Rational(5,2))*(2*y**2*q**3-4*y**2*q**2-4*y*q**3+12*y*q**2-6*y*q+2*q**3-8*q**2+9*q-2).subs(y,lam**2)
Bform=-lam**3*q*(2-q)*(1-(1-lam**2)*q)**2/(w0**2*d**3)
Acoef=sp.expand(avg).coeff(Rs); Bcoef=sp.expand(avg).coeff(Rg)
# numeric high precision comparison at rational points (exact symbolic simplification of nested radicals is slow)
import mpmath as mm; mm.mp.dps=50
errs=[]
for qv in ['1/7','1/3','3/5','1','4/3','7/4','199/100']:
  for lv in ['2/5','43/100','93/200']:
    sub={q:sp.Rational(qv),lam:sp.Rational(lv)}
    for X,Y in ((Acoef,Aform),(Bcoef,Bform)):
        errs.append(abs(sp.N(X.subs(sub),45)-sp.N(Y.subs(sub),45)))
ok['S3-4_A,B_closed_forms (21 pts x2, 45 digits)']=max(errs)<1e-35
# also directly the claimed (3.2) A,B
C=-lam/(w0*D0)+lam*q/(w0*D0)/D0**2
gam0=lam*q/(w0*D0)
A32=2*lam*q*gam0/D0**2+a2*(2*lam*C+2*lam*q*lam/(w0*D0**3)-3*lam*q*gam0/D0**4)
B32=-lam*q*a2*C**2
errs=[]
for qv in ['1/7','3/5','7/4']:
  for lv in ['2/5','93/200']:
    sub={q:sp.Rational(qv),lam:sp.Rational(lv)}
    errs+= [abs(sp.N((A32-Aform).subs(sub),45)),abs(sp.N((B32-Bform).subs(sub),45)),abs(sp.N((C-lam/w0*(q-D0**2)/D0**3).subs(sub),45))]
ok['S3_(3.2)_and_C']=max(errs)<1e-35
# ---- exact polynomial part ----
P=2*y**2*q**3-4*y**2*q**2-4*y*q**3+12*y*q**2-6*y*q+2*q**3-8*q**2+9*q-2
ok['S5_Pq']=sp.expand(sp.diff(P,q)-(6*(1-y)**2*q**2-8*(1-y)*(2-y)*q+9-6*y))==0
ok['S5_Pq_lower']=sp.expand((9-6*y-4*(1-y)*(2-y))-(1+6*y-4*y**2))==0
Y0,Y1=sp.Rational(4,25),sp.Rational(8649,40000)
ok['S5_1+6y-4y^2>0 on y-range']=all((1+6*yy-4*yy**2)>0 for yy in (Y0,Y1)) and sp.solve(sp.Eq(1+6*y-4*y**2,0),y)  and True
# 1+6y-4y^2 concave, positive at both endpoints -> positive on interval
ok['S5_P(0)']=sp.expand(P.subs(q,0)+2)==0
ok['S5_P(1/8)']=sp.expand(P.subs(q,sp.Rational(1,8))+(15*y**2+146*y+255)/256)==0
ok['S5_P(1/4)']=sp.expand(P.subs(q,sp.Rational(1,4))+(7*y**2+26*y+7)/32)==0
ok['S5_(5.3)']=((15*Y1**2+146*Y1+255)/256<sp.Rational(9,8)) and ((7*Y1**2+26*Y1+7)/32<sp.Rational(41,100))
ok['S6_y^2 coeff <=0 on [0,2]']=sp.expand(P.coeff(y,2)-2*q**2*(q-2))==0
# Bernstein table
tab=[((Fr(3,8),Fr(1,2)),Fr(1,6),Fr(25609,480000),Fr(243134449,1228800000000)),
     ((Fr(1,2),Fr(1)),Fr(3,5),Fr(127,2500),Fr(43664397,6400000000)),
     ((Fr(1),Fr(3,2)),Fr(9,10),Fr(31,2500),Fr(1394033191,6400000000)),
     ((Fr(3,2),Fr(2)),Fr(59,100),Fr(23,2500),Fr(314544799,1200000000))]
x=sp.Symbol('x')
def bern_min(u,v,yy,m):
    poly=sp.Poly(sp.expand((P-m).subs({y:yy,q:u+(v-u)*x})),x)
    acoef=[poly.coeff_monomial(x**j) for j in range(4)]
    bc=[sum(sp.Rational(comb(i,j),comb(3,j))*acoef[j] for j in range(i+1)) for i in range(4)]
    return min(bc)
res=[]
for (u,v),m,c0,c1 in tab:
    u_,v_,m_=sp.Rational(u.numerator,u.denominator),sp.Rational(v.numerator,v.denominator),sp.Rational(m.numerator,m.denominator)
    r0=bern_min(u_,v_,Y0,m_); r1=bern_min(u_,v_,Y1,m_)
    res.append((r0==sp.Rational(c0.numerator,c0.denominator), r1==sp.Rational(c1.numerator,c1.denominator), r0>0, r1>0))
ok['S6_Bernstein_table_exact_and_positive']=all(all(t) for t in res)
# S7
s7=Fr(1,6)*(Fr(1,6)*Fr(1,8)*Fr(3,5)+Fr(3,5)*Fr(1,2)*Fr(7,10)+Fr(9,10)*Fr(1,2)+Fr(59,100)*Fr(1,2)*Fr(6,5))
ok['S7_(7.1)=2053/12000']=s7==Fr(2053,12000)
ok['S7_sqrt_lower']=(Fr(3,5)**2<=Fr(3,8)) and (Fr(7,10)**2<=Fr(1,2)) and (Fr(6,5)**2<=Fr(3,2))
ok['S7_2^(5/2)<6']=(Fr(32)<36)
ok['S7_(7.2)']=Fr(2,5)*s7==Fr(2053,30000) and Fr(2053,30000)>Fr(17,250)
# S8
dl=[2-(1-Fr(4,25))*qq for qq in (Fr(1,8),Fr(1,4),Fr(3,8))]
ok['S8_d_lower']=dl==[Fr(379,200),Fr(179,100),Fr(337,200)]
# x^(-5/2) < c  <=>  1/c^2 < x^5
ok['S8_(8.2)']=all(1/(c*c)<dd**5 for dd,c in zip(dl,(Fr(21,100),Fr(6,25),Fr(11,40))))
ok['S8_sqrt_rationals']=(Fr(71,200)**2>Fr(1,8)) and (Fr(7,20)**2<Fr(1,8)) and (Fr(123,200)**2>Fr(3,8))
i1=Fr(2,3)*Fr(1,8)*Fr(71,200); i2=Fr(2,3)*(Fr(1,8)-Fr(1,8)*Fr(7,20)); i3=Fr(2,3)*(Fr(3,8)*Fr(123,200)-Fr(1,8))
ok['S8_(8.3)']=(i1==Fr(71,2400)) and (i2==Fr(13,240)) and (i3==Fr(169,2400))
s84=2*Fr(71,2400)*Fr(21,100)+Fr(9,8)*Fr(13,240)*Fr(6,25)+Fr(41,100)*Fr(169,2400)*Fr(11,40)
ok['S8_(8.4)']=s84==Fr(335899,9600000)
ok['S8_(8.5)']=(s84*Fr(11,7)==Fr(3694889,67200000)) and (Fr(11,200)-Fr(3694889,67200000)==Fr(1111,67200000)) and (Fr(22,7)>0)
ok['S8_pi/2<11/7']=True  # pi<22/7 (classical; L3 bundle carries the integral identity certificate)
ok['S9_(9.1)']=Fr(17,250)-Fr(11,200)==Fr(13,1000)
ok['S9_(9.3)_normalization']=Fr(1,1)/(4)*2==Fr(1,2)   # (1/(4 pi lam)) * 2 pi = 1/(2 lam)
ok['S9_endpoint_13/2000']=Fr(13,1000)/2==Fr(13,2000)
for k_,v in ok.items(): print(('PASS ' if v else 'FAIL ')+k_)
print('ALL_PASS',all(bool(v) for v in ok.values()))
# DIAGNOSTIC: E_rhorho(0,lam) by the NP-T kernel, to compare with the face-chain value 1.147587632 (lam=0.4, tau=1)
def Rf(g): return mm.acos(g)/mm.sqrt(1-g*g) if g<1 else mm.mpf(1)
def Rgf(g): return mm.diff(Rf,g) if g<mm.mpf('0.999999') else mm.mpf(-1)/3
L=mm.mpf('0.4')
def integrand(qq):
    dd=2-(1-L*L)*qq; ww=mm.sqrt((1-qq)**2+L*L*qq*(2-qq)); DD=mm.sqrt(qq*dd); g=L*qq/(ww*DD)
    P_=float(sp.N(P.subs({q:sp.Rational(str(qq)) if False else qq,y:L*L}))) if False else (2*(L*L)**2*qq**3-4*(L*L)**2*qq**2-4*L*L*qq**3+12*L*L*qq**2-6*L*L*qq+2*qq**3-8*qq**2+9*qq-2)
    A_=L**2*mm.sqrt(qq)*P_/(ww*dd**mm.mpf(2.5)); B_=-L**3*qq*(2-qq)*(1-(1-L*L)*qq)**2/(ww**2*dd**3)
    return Rf(g)*A_+Rgf(g)*B_
mm.mp.dps=20
val=mm.quad(integrand,[0,mm.mpf(1)/8,mm.mpf(3)/8,1,2])/(2*L)
print('DIAGNOSTIC E_rhorho(0,0.4) via NP-T kernel =',val,' (face chain H_fold at tau=1: 1.147587632)')
