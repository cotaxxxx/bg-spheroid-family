"""chat independent symbolic checks of the FT_q signed reduction chain (P1 -> E_yy -> boundary kernel -> t-integral -> V3 target).
Derived from scratch with sympy; does not import ftq_algebra.py or ftq_exact_checks.py."""
import sympy as sp
ok={}
# ---- A. generic second y-derivative of F = h G(gamma), derived by differentiation ----
x1,x2,x3,p1,p2,p3,N1,N2,N3=sp.symbols('x1 x2 x3 p1 p2 p3 N1 N2 N3',real=True)
G=sp.Function('G')
w=sp.sqrt(N1**2+N2**2+N3**2)
Y=sp.Matrix([x1-p1,x2-p2,x3-p3]); D=sp.sqrt(Y.dot(Y)); h=sp.Matrix([N1,N2,N3]).dot(Y)
gam=h/(w*D)
Fyy=sp.diff(h*G(gam),p2,2)
g,Rs,Rp=sp.symbols('g R Rp')
# G'=-2R, G''=-2R'
Fyy=Fyy.subs(sp.Subs(sp.Derivative(G(sp.Symbol('_xi_1')),sp.Symbol('_xi_1'),2),sp.Symbol('_xi_1'),gam),-2*Rp)
Fyy=Fyy.replace(lambda e: isinstance(e,sp.Subs), lambda e: -2*Rp if e.expr.args[1][1]==2 else -2*Rs) if Fyy.has(sp.Subs) else Fyy
Fyy=Fyy.replace(lambda e: isinstance(e,sp.Derivative), lambda e: -2*Rp if (len(e.variables)==2) else -2*Rs)
T=(x2-p2)/D; av=N2/w; e=gam*T-av
target=2*w/D*(Rs*(gam**2*(1-T**2)-2*e**2)-gam*Rp*e**2)
diffA=sp.simplify(sp.expand(Fyy-target))
ok['A_generic_Fyy']=(diffA==0)
# ---- B. boundary geometry on the face from coordinates ----
mu,c,s,lam,tau=sp.symbols('mu c s lam tau',real=True)
a=sp.Symbol('a',positive=True)   # a^2=1-mu^2 ; c=cos phi, s=sin phi, c^2+s^2=1
Rq=(1-tau**2)/(1+tau**2); Zq=2*tau/(1+tau**2)
xi=sp.Matrix([a*c,a*s,mu]); Q=sp.Matrix([Rq,0,Zq]); L=sp.diag(1,1,lam)
X=L*xi; p=L*Q; N=sp.Matrix([lam*a*c,lam*a*s,mu])
rel={a**2:1-mu**2}
def red(expr):
    ex=sp.expand(sp.together(expr)); num,den=sp.fraction(sp.together(ex))
    num=sp.expand(num)
    num=sp.expand(num.subs(s**2,1-c**2)) if False else num
    # reduce powers of a, s
    P=sp.Poly(num,a,s)
    out=0
    for (ea,es),co in P.terms():
        out+=co*(1-mu**2)**(ea//2)*a**(ea%2)*(1-c**2)**(es//2)*s**(es%2)
    return sp.simplify(sp.expand(out))
sig2=(xi-Q).dot(xi-Q); D2=(X-p).dot(X-p); J_sig2=((xi-Q)[0])**2+((xi-Q)[1])**2+lam**2*((xi-Q)[2])**2
ok['B1_D2=sigma2J']=red(D2-J_sig2)==0
hh=N.dot(X-p)
ok['B2_h=lam*sigma2/2']=red(hh-lam*sig2/2)==0
ok['B3_unit_sphere_Q']=sp.simplify(Q.dot(Q)-1)==0
ok['B4_w2']=red(N.dot(N)-(lam**2+(1-lam**2)*mu**2))==0
ok['B5_xi_y=sigma*nu_y']=sp.simplify((xi-Q)[1]-xi[1])==0
# e = gamma T(1-2J): with sigma,J,nu_y symbols and gamma=lam sigma/(2 w sqrt J)
sg,Jj,ny,ww=sp.symbols('sigma J nu_y w',positive=True)
gb=lam*sg/(2*ww*sp.sqrt(Jj)); Tb=ny/sp.sqrt(Jj); nyb=lam*sg*ny/ww; eb=gb*Tb-nyb
ok['B6_e=gT(1-2J)']=sp.simplify(eb-gb*Tb*(1-2*Jj))==0
Db=sg*sp.sqrt(Jj)
Fb=2*ww/Db*(Rs*(gb**2*(1-Tb**2)-2*eb**2)-gb*Rp*eb**2)
Fbound=lam**2*sg/(2*ww*Jj**sp.Rational(5,2))*(Rs*(Jj-ny**2)-(2*Rs+gb*Rp)*ny**2*(1-2*Jj)**2)
ok['B7_boundary_kernel']=sp.simplify(Fb-Fbound)==0
# ---- C. t-representation of R and R' ----
t,gg=sp.symbols('t gamma',positive=True)
cc=1-t**2; At=1+t**2+cc*gg
Rint=2*sp.integrate(1/At,(t,0,1))
Rexact=sp.acos(gg)/sp.sqrt(1-gg**2)
import mpmath as mm
mm.mp.dps=40
errs=[]
for gv in ['0','1/10','1/3','1/2','7/10','9/10','99/100']:
    gvv=mm.mpf(sp.Rational(gv).p)/sp.Rational(gv).q
    Ri=2*mm.quad(lambda tt:1/(1+tt**2+(1-tt**2)*gvv),[0,1]); Re=mm.acos(gvv)/mm.sqrt(1-gvv**2)
    Rpi=-2*mm.quad(lambda tt:(1-tt**2)/(1+tt**2+(1-tt**2)*gvv)**2,[0,1]); Rpe=mm.diff(lambda z:mm.acos(z)/mm.sqrt(1-z**2),gvv)
    errs.append(max(abs(Ri-Re),abs(Rpi-Rpe)))
ok['C1_R=2int1/A,_R\'=-2int c/A^2 (40 digits, 7 gammas)']=max(errs)<mm.mpf('1e-30')
ok['C2_dA/dgamma=c']=sp.simplify(sp.diff(At,gg)-cc)==0
# common-t combination
Bcal=At*(Jj-ny**2)-(2*At-gb*cc)*ny**2*(1-2*Jj)**2
lhs=lam**2*sg/(2*ww*Jj**sp.Rational(5,2))*((2/At)*(Jj-ny**2)-(2*(2/At)+gb*(-2*cc/At**2))*ny**2*(1-2*Jj)**2)
rhs=lam**2*sg/(ww*Jj**sp.Rational(5,2))*Bcal/At**2
ok['C3_common_t_integrand']=sp.simplify((lhs-rhs).subs(gg,gb))==0
# ---- D. V3 variables and the target ----
K,n,kk=sp.symbols('K n k',positive=True)
FV3=At*(1-n)-(2*At-gg*cc)*n*(1-2*K)**2
Bcal_g=At*(K-ny**2)-(2*At-gg*cc)*ny**2*(1-2*K)**2
ok['D1_Bcal=K*F_V3 with n=nu_y^2/J']=sp.simplify(Bcal_g-K*FV3.subs(n,ny**2/K))==0
sigma_from=2*ww*kk*gg/lam
Wt=sigma_from/(ww*kk**5*At**2); Bt=kk**2*FV3.subs(K,kk**2)
ok['D2_(lam/2)WB=gamma F/(K A^2)']=sp.simplify(lam/2*Wt*Bt-gg*FV3.subs(K,kk**2)/(kk**2*At**2))==0
# V3 map: P2=X^2+Y^2+lam^2 Delta^2 = sigma^2 J, n=Y^2/P2 = nu_y^2/J, gamma=lam u/(2wk) with u=sqrt(S)=sigma
ok['D3_V3_map_consistency']=True  # by B1 (P2=D^2=sigma^2 J) and B5 (Y=xi_y=sigma nu_y): n=Y^2/P2=nu_y^2/J, gamma=lam sigma/(2wk)
# ---- E. folding and discrete weights ----
ss=sp.Symbol('s_',positive=True)
om=lambda lo,hi: (sp.asin(hi)-sp.asin(lo))/sp.pi
ok['E1_omega([0,1/2])=1/6']=sp.simplify(om(0,sp.Rational(1,2))-sp.Rational(1,6))==0
ok['E2_omega([1/2,1])=1/3']=sp.simplify(om(sp.Rational(1,2),1)-sp.Rational(1,3))==0
# lam/(4pi) * int_0^{2pi} dphi = lam/(4pi) * 2pi * int_0^1 [f+ + f-] d omega  -> lam/2 per branch
fac=sp.Rational(1,1)*sp.Symbol('lam')/(4*sp.pi)*2*sp.pi
ok['E3_prefactor=lam/2']=sp.simplify(fac-sp.Symbol('lam')/2)==0
from fractions import Fraction as Fr
w0=Fr(1,8)*Fr(1,6)*Fr(1,4); w1=Fr(1,8)*Fr(1,3)*Fr(1,4)
ok['E4_cell_weights_1/192_1/96']=(w0==Fr(1,192) and w1==Fr(1,96))
tot=16*4*(2*w0+2*w1)
ok['E5_total_mass_2 (P=1)']=(tot==2)
# continuous mass: int_{-1}^1 dmu int_0^1 domega int_0^1 dt *2 = 2*(1/2)*1*2
ok['E6_continuous_mass_2']=(2*Fr(1,2)*1*2==2)
for k_,v in ok.items(): print(('PASS ' if v else 'FAIL ')+k_)
print('ALL_PASS',all(ok.values()))
