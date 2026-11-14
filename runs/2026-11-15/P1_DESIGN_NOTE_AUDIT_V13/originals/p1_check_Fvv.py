import sympy as S
t,h0,h1,ww=S.symbols('t h0 h1 w',positive=True)
DD=S.Function('D')(t)
hh=h0+h1*t                     # h affine in p  (h_vv = 0)
gam=hh/(ww*DD)
xi=S.symbols('xi')
G=S.acos(xi)**2; R=S.acos(xi)/S.sqrt(1-xi**2); Rg=S.diff(R,xi)
print('G\'=-2R:',S.simplify(S.diff(G,xi)+2*R)==0)
F=hh*G.subs(xi,gam)
gv=S.diff(gam,t); gvv=S.diff(gam,t,2); hv=h1
claim=-4*hv*R.subs(xi,gam)*gv-2*hh*Rg.subs(xi,gam)*gv**2-2*hh*R.subs(xi,gam)*gvv
diff=S.diff(F,t,2)-claim
# numeric spot checks with D(t)=sqrt(c0+c1 t+t^2) (|x-p-tv| form), gamma in (0,1)
import random
D_expr=S.sqrt(4+S.Rational(1,3)*t+t**2)
dd=diff.subs(DD,D_expr).doit()
ok=True
for k in range(6):
    vals={h0:S.Rational(random.randint(1,9),10),h1:S.Rational(random.randint(-9,9),10),ww:S.Rational(random.randint(5,10),10),t:S.Rational(random.randint(0,5),10)}
    r=S.N(dd.subs(vals),30); ok&=abs(r)<1e-25
print('§3.4 F_vv = -4 h_v R g_v - 2 h R_g g_v^2 - 2 h R g_vv (6 random exact-input points, |diff|<1e-25):',ok)
print('§3.4 symbolic:',S.simplify(diff.subs(DD,D_expr).doit())==0)
