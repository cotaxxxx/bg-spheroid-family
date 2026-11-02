# chat: symbolic (exact) proof of the E3 identity used by the Astra lemma.
# Claim: with the code's definitions,  E_code = H*ox - xi_x*|V|^2 ,  |V|^2 = 1-(1-lam^2)*oz^2.
# The lam-dependent parts agree trivially ((1-lam^2)*xi_x*oz^2 on both sides), so it suffices that
#   D := H*ox - xi_x + s*qx*J^2*sb^2 + s*J*cb*oz = 0 .
# Relations used (all exact from the definitions):
#   cp^2+sp^2=1, sigma^2+g^2=1, cb^2+sb^2=1, qx^2+qz^2=1  (qx^2+qz^2=((1-y)^2A^2+B^2)/N=1, x=y(2-y))
#   s^2=(1-delta)N=1-M  =>  delta_v=M/(1+s)=1-s ;  kappa=2*r*sigma/(1-r^2) with r=sqrt(s)  =>  sp*(1-r^2)=2*r*sigma*cp
import sympy as sp
cp,spp,sg,g,cb,sb,qx,qz,r=sp.symbols('cp sp sigma g cb sb qx qz r',real=True)
L=cp-sg*spp/r; J=g*spp/r; H=cp+r*sg*spp
ox=L*qx-J*cb*qz; oz=L*qz+J*cb*qx
xx=(1-2*sg**2)*qx-2*sg*g*cb*qz
D=sp.expand((H*ox-xx + r**2*qx*J**2*sb**2 + r**2*J*cb*oz)*r**2)
rels=[spp**2+cp**2-1, g**2+sg**2-1, sb**2+cb**2-1, qz**2+qx**2-1, spp*(1-r**2)-2*r*sg*cp]
G=sp.groebner(rels, spp,g,sb,qz,cp,sg,cb,qx,r, order='lex')
rem=G.reduce(D)[1]
print('remainder modulo all relations:', sp.simplify(rem))
print('E3 IDENTITY', 'PROVED (remainder 0)' if sp.simplify(rem)==0 else 'NOT REDUCED TO 0')
# also show the factorization modulo the unit-circle relations only
G0=sp.groebner(rels[:4], spp,g,sb,qz,cp,sg,cb,qx,r, order='lex')
print('modulo unit circles only:', sp.factor(G0.reduce(D)[1]))