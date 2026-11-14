"""chat independent checks: QM-1 (dd001338...), QM (e8588c1b...), L2 (0a83e411...). sympy exact + mpmath 40-digit spot checks (spot checks are DIAGNOSTIC)."""
import sympy as sp, mpmath as mm, random
from fractions import Fraction as Fr
ok={}
# --- QM-1 §3: ODE and series ---
g=sp.Symbol('g'); R=sp.acos(g)/sp.sqrt(1-g**2)
ok['QM1_3.1_ODE']=sp.simplify((1-g**2)*sp.diff(R,g,2)-(3*g*sp.diff(R,g)+R))==0
ok['QM1_3.1_bound']=sp.N((sp.Rational(3,2)+sp.pi/2)/sp.Rational(3,4))<5
n=sp.Symbol('n',integer=True,nonnegative=True)
u=sp.Symbol('u',positive=True)
ser=sp.series(sp.asin(sp.sqrt(u))/sp.sqrt(u),u,0,8).removeO()
cn=lambda k: sp.factorial(2*k)/(4**k*sp.factorial(k)**2*(2*k+1))
ok['QM1_3.2_series_coeffs']=all(sp.simplify(ser.coeff(u,k)-cn(k))==0 for k in range(8)) and all(cn(k)<=1 for k in range(60))
ok['QM1_3.2_bounds']=(1/(1-Fr(3,4))**2==16) and (2/(1-Fr(3,4))**3==128) and (4*128+2*16==544)
Psi=sp.Function('Psi'); qq=1-g**2
expr=sp.diff(Psi(qq),g,2)
d1=sp.Symbol('d1'); d2=sp.Symbol('d2')
expr=expr.replace(lambda e: isinstance(e,sp.Subs), lambda e: d2 if e.expr.args[1][1]==2 else d1).replace(lambda e: isinstance(e,sp.Derivative), lambda e: d2 if len(e.variables)==2 else d1)
ok['QM1_3.2_chain']=sp.expand(expr-(4*g**2*d2-2*d1))==0
# --- QM-1 §5-7: random-point checks of derivative formulas and the C3 bound ---
mm.mp.dps=40
random.seed(20261115)
C3=8788+39*mm.pi
worst=0; maxerr=0
def unit(): 
    v=[mm.mpf(random.gauss(0,1)) for _ in range(3)]; nr=mm.sqrt(sum(x*x for x in v)); return [x/nr for x in v]
for trial in range(24):
    lam=mm.mpf(2)/5+mm.mpf(random.random())*(mm.mpf(93)/200-mm.mpf(2)/5)
    mu=mm.mpf(random.uniform(-1,1)); ph=mm.mpf(random.uniform(0,6.28))
    a=mm.sqrt(1-mu*mu); X=[a*mm.cos(ph),a*mm.sin(ph),lam*mu]; N=[lam*a*mm.cos(ph),lam*a*mm.sin(ph),mu]; w=mm.sqrt(sum(x*x for x in N)); nu=[x/w for x in N]
    # base point inside closure: random point r*(unit ellipsoid point)
    r=mm.mpf(random.random())**(mm.mpf(1)/3); m2=mm.mpf(random.uniform(-1,1)); p2=mm.mpf(random.uniform(0,6.28)); a2=mm.sqrt(1-m2*m2)
    P0=[r*a2*mm.cos(p2),r*a2*mm.sin(p2),r*lam*m2]
    U,V,S=unit(),unit(),unit()
    def pt(t1,t2,t3): return [P0[i]+t1*U[i]+t2*V[i]+t3*S[i] for i in range(3)]
    def Dd(t1,t2,t3): p=pt(t1,t2,t3); return mm.sqrt(sum((X[i]-p[i])**2 for i in range(3)))
    def hh(t1,t2,t3): p=pt(t1,t2,t3); return w*sum((X[i]-p[i])*nu[i] for i in range(3))
    def gm(t1,t2,t3): return hh(t1,t2,t3)/(w*Dd(t1,t2,t3))
    def Ff(t1,t2,t3): return hh(t1,t2,t3)*mm.acos(gm(t1,t2,t3))**2
    D0=Dd(0,0,0)
    Fuvs=mm.diff(Ff,(0,0,0),(1,1,1))
    worst=max(worst,abs(Fuvs)*D0**2/C3)
    # closed forms of §5: D_uv=(Pu.Pv)/D
    nvec=[(X[i]-P0[i])/D0 for i in range(3)]
    Pu=[U[i]-nvec[i]*sum(nvec[j]*U[j] for j in range(3)) for i in range(3)]; Pv=[V[i]-nvec[i]*sum(nvec[j]*V[j] for j in range(3)) for i in range(3)]
    Duv=mm.diff(Dd,(0,0,0),(1,1,0)); maxerr=max(maxerr,abs(Duv-sum(Pu[i]*Pv[i] for i in range(3))/D0))
    Duvs=mm.diff(Dd,(0,0,0),(1,1,1)); worst_d=abs(Duvs)*D0**2
    assert worst_d<=3
    gu=mm.diff(gm,(0,0,0),(1,0,0)); guv=mm.diff(gm,(0,0,0),(1,1,0)); guvs=mm.diff(gm,(0,0,0),(1,1,1))
    assert abs(gu)*D0<=2 and abs(guv)*D0**2<=5 and abs(guvs)*D0**3<=24
ok['QM1_5_Duv_closed_form (24 pts)']=maxerr<mm.mpf('1e-25')
ok['QM1_5-6_bounds D_uvs<=3/D^2, gamma_u<=2/D, gamma_uv<=5/D^2, gamma_uvs<=24/D^3 (24 pts)']=True
ok['QM1_7_|F_uvs|D^2<=C3 (24 pts)']=worst<1
print('DIAGNOSTIC max |F_uvs| D^2 / C3 over 24 random configs =',mm.nstr(worst,5))
ok['QM1_7_constant']=(1088*8+2*(3*5*2)==8764) and (3*8+8764==8788) and (3*5+24==39)
# --- QM arithmetic ---
lam=sp.Symbol('lam',positive=True); C2=9*sp.pi+8; C3s=8788+39*sp.pi
ok['QM_3.1']=sp.simplify(1/(4*sp.pi)*sp.Rational(5,2)*sp.Rational(5,2)*C2*8*sp.pi-sp.Rational(25,2)*C2)==0
ok['QM_5.2']=sp.simplify(1/(4*sp.pi)*sp.Rational(5,2)*sp.Rational(5,2)*C2*16*sp.pi-25*C2)==0
eta=sp.Symbol('eta',positive=True); s=sp.Symbol('s',positive=True)
ok['QM_6.1_layer']=sp.simplify(sp.integrate(2*s**-3*4*sp.pi*s**2,(s,eta,2))-8*sp.pi*sp.log(2/eta))==0
d=sp.Symbol('d',positive=True)
ok['QM_7.3']=sp.simplify(1/(4*sp.pi)*sp.Rational(5,2)*sp.Rational(5,2)*4*C3s*d*(4*sp.pi+8*sp.pi*sp.log(2/eta))-25*C3s*d*(1+2*sp.log(2/eta)))==0
om=50*C2*d+25*C3s*d*(1+2*sp.log(1/d))
ok['QM_9.1']=sp.simplify(sp.diff(om,d)-(50*C2+25*C3s*(2*sp.log(1/d)-1)))==0
ok['QM_9.2_log2>1/2']=sp.log(2)>sp.Rational(1,2)
ok['QM_10.1']=sp.N(om.subs(d,sp.Rational(1,2))-25*C2)>0
# --- L2 (3.1): density depends on (rho,b) only via rho*b and rho^2 ---
rho,b,z,mu_,lam_=sp.symbols('rho b z mu lam',real=True)
a2=1-mu_**2
hL=lam_*(1-rho*b)-z*mu_; DL2=a2-2*rho*b+rho**2+(lam_*mu_-z)**2
ok['L2_3.1_h,D invariant under (rho,b)->(-rho,-b)']=sp.expand(hL.subs({rho:-rho,b:-b},simultaneous=True)-hL)==0 and sp.expand(DL2.subs({rho:-rho,b:-b},simultaneous=True)-DL2)==0
Fx=sp.Function('Fx')
ok['L2_3.3_chain']=sp.simplify(sp.diff(Fx(-rho,b),rho)+sp.Subs(sp.Derivative(Fx(sp.Symbol('r'),b),sp.Symbol('r')),sp.Symbol('r'),-rho).doit())==0
for k_,v in ok.items(): print(('PASS ' if v else 'FAIL ')+k_)
print('ALL_PASS',all(bool(v) for v in ok.values()))
