"""D4 phase A: exact symbolic work only; no numerical integration or scan."""
import sympy as S
from pathlib import Path
import json,hashlib,datetime
x,z,b,mu,lam,q,g=S.symbols('x z b mu lam q gamma', nonzero=True)
R0,R1,R2,R3=S.symbols('R R1 R2 R3')
y=S.symbols('y')
ell=b*x+lam*mu*z
k=b*x+mu*z/lam
v2=x*x+z*z
d1=ell/q-k
d2=-v2/(2*q)+3*ell**2/(2*q**2)-k*ell/q
d3=-3*ell*v2/(2*q**2)+5*ell**3/(2*q**3)+k*v2/(2*q)-3*k*ell**2/(2*q**2)
d4=3*v2**2/(8*q**2)-15*ell**2*v2/(4*q**3)+35*ell**4/(8*q**4)+3*k*ell*v2/(2*q**2)-5*k*ell**3/(2*q**3)
T=[d4-k*d3,d1*d3+d2**2/2-k*d1*d2,d1**2*d2/2-k*d1**3/6,d1**4/24]
def avg(expr):
 p=S.Poly(S.expand(expr),b)
 moments={0:S.Integer(1),1:S.Integer(0),2:(1-y)/2,3:S.Integer(0),4:3*(1-y)**2/8}
 return S.factor(sum(co* moments[n[0]] for n,co in p.terms()).subs(mu**2,y))
out={}
for label,nx,nz,factor in [('K40',4,0,-24),('K22',2,2,-4)]:
 A=[avg(S.Poly(S.expand(t),x,z).coeff_monomial(x**nx*z**nz)) for t in T]
 out[label+'_A']=[str(a) for a in A]
 out[label]=str(S.factor(factor*sum(g**(j+1)*[R0,R1,R2,R3][j]*A[j] for j in range(4))))
# Independent directional derivative route to the quartic density.
t,l0,k0,v0=S.symbols('t ell k v2')
gam=g*(1-k0*t)*(1-2*l0*t/q+v0*t*t/q)**S.Rational(-1,2)
gd=[S.diff(gam,t,j).subs(t,0) for j in range(1,5)]
a1,a2,a3,a4=gd
chain=(-2)*(R3*a1**4+6*R2*a1*a1*a2+3*R1*a2*a2+4*R1*a1*a3+R0*a4) +8*k0*(R2*a1**3+3*R1*a1*a2+R0*a3)
series=-48*sum(g**(j+1)*[R0,R1,R2,R3][j]*T[j] for j in range(4))
delta=S.factor(chain.subs({l0:ell,k0:k,v0:v2})-series)
assert delta==0
out['directional_vs_homogeneous_difference']=str(delta)
C=S.Rational(16*384,35)+S.Rational(128*64,15)+240*2+96*4
out['C4']=str(C)
out['16C4']=str(16*C)
assert 16*C <25600
L=lam*(S.Rational(4,3)-2*(1-lam**2)/3-4*(1-lam**2)**2/35)
out['own_center_L_at_119_200']=str(L.subs(lam,S.Rational(119,200)))
out['own_center_L_minus_509_1000']=str(L.subs(lam,S.Rational(119,200))-S.Rational(509,1000))
out['local_loss_at_delta_1_128']=str(S.Rational(25600,128**2)*S.Rational(13,72))
out['old_margin_minus_local_loss']=str(S.Rational(1547,4860)-S.Rational(25600,128**2)*S.Rational(13,72))
out['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
dest=Path(__file__).with_name('d4_phase_a_result.json');dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
