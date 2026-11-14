"""chat independent symbolic checks for the P1 design note (commit 6c6282a8, SHA 2c304ee6...)."""
import sympy as S
mu,phi,lam,rho,z,a_=S.symbols('mu phi lambda rho z a',real=True)
a=S.sqrt(1-mu**2)
X=S.Matrix([a*S.cos(phi),a*S.sin(phi),lam*mu])
# §1 normal, w, dA
grad=S.Matrix([X[0],X[1],X[2]/lam**2])
w=S.sqrt(lam**2*(1-mu**2)+mu**2)
nu=S.Matrix([lam*a*S.cos(phi),lam*a*S.sin(phi),mu])/w
print('§1 nu parallel to grad:',S.simplify(nu.cross(grad))==S.zeros(3,1),' |nu|=1:',S.simplify(nu.dot(nu)-1)==0)
cr=X.diff(mu).cross(X.diff(phi))
print('§1 |x_mu x x_phi|^2 = w^2:',S.simplify(cr.dot(cr)-w**2)==0)
# meridional h
p=S.Matrix([rho,0,z]); h=w*(X-p).dot(nu)
print('§1 h = lam(1-rho a cos phi) - z mu:',S.simplify(h-(lam*(1-rho*a*S.cos(phi))-z*mu))==0)
# Lemma 3.2 bounds on R and R_gamma via alpha
al=S.symbols('alpha',positive=True)
Rg=-(S.sin(al)-al*S.cos(al))/S.sin(al)**3          # dR/dgamma with gamma=cos(alpha)
f=S.sin(al)**3-S.sin(al)+al*S.cos(al)             # f>=0  <=>  R_gamma>=-1
print('§3.2 f(0)=',S.limit(f,al,0),' f(pi/2)=',f.subs(al,S.pi/2),' f\'=sin*(3 sin cos - alpha):',S.simplify(S.diff(f,al)-S.sin(al)*(3*S.sin(al)*S.cos(al)-al))==0)
import math
print('§3.2 numeric min of f on (0,pi/2]:',min(float(f.subs(al,k*math.pi/2000)) for k in range(1,1001)))
print('§3.2 Rgamma at alpha->0:',S.limit(Rg,al,0),' at pi/2:',Rg.subs(al,S.pi/2))
# Lemma 3.3 / 3.4: symbolic derivatives along a unit direction v, generic functions
t=S.symbols('t',real=True)
hh=S.Function('h')(t); DD=S.Function('D')(t); ww=S.symbols('w',positive=True)
gam=hh/(ww*DD); G=S.Function('G')
F=hh*G(gam)
Fvv=S.diff(F,t,2).subs(S.Derivative(hh,(t,2)),0)
g_v=S.diff(gam,t); g_vv=S.diff(gam,t,2).subs(S.Derivative(hh,(t,2)),0)
hv=S.diff(hh,t); Dv=S.diff(DD,t); Dvv=S.diff(DD,t,2)
claim_gv=hv/(ww*DD)-gam*Dv/DD
claim_gvv=-hv*Dv/(ww*DD**2)-claim_gv*Dv/DD-gam*Dvv/DD+gam*Dv**2/DD**2
print('§3.3 gamma_v formula:',S.simplify(g_v-claim_gv)==0,' gamma_vv formula:',S.simplify(g_vv-claim_gvv)==0)
# F_vv formula of Lemma 3.4: see p1_check_Fvv.py (concrete-function check)
print('§3.4 C2 term sum 4pi+8+5pi = 9pi+8:',S.simplify(4*S.pi+8+5*S.pi-(9*S.pi+8))==0)
# D_vv for D=|x-p|, p moving along v
v=S.Matrix(S.symbols('v1 v2 v3',real=True)); xs=S.Matrix(S.symbols('x1 x2 x3',real=True)); ps=S.Matrix(S.symbols('p1 p2 p3',real=True))
Dp=S.sqrt((xs-ps-t*v).dot(xs-ps-t*v))
Dv_=S.diff(Dp,t).subs(t,0); Dvv_=S.diff(Dp,t,2).subs(t,0); D0=Dp.subs(t,0)
print('§3.3 D_vv=(|v|^2-D_v^2)/D:',S.simplify(Dvv_-(v.dot(v)-Dv_**2)/D0)==0)
# Lemma 4.2 arithmetic
M,s0=S.symbols('M s0',positive=True)
val=(4*S.pi*s0+M/s0).subs(s0,S.sqrt(M/(4*S.pi)))
print('§4.2 4pi s0+M/s0 at s0=sqrt(M/4pi) = 2 sqrt(4piM):',S.simplify(val-2*S.sqrt(4*S.pi*M))==0, ' optimal:',S.solve(S.diff(4*S.pi*s0+M/s0,s0),s0))
print('§4.2 at M=4pi -> 8pi:',S.simplify(2*S.sqrt(4*S.pi*4*S.pi)-8*S.pi)==0)
# axis: E(0,lam t) = (1/2) int A alpha^2 dmu
print('§1 axis h = lam(1-t mu) at rho=0,z=lam t:',S.simplify(h.subs({rho:0,z:lam*t})-lam*(1-t*mu))==0)
