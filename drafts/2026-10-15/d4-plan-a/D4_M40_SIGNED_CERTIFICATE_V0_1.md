# D4 M40 signed bound — mathematical submission V0.1

2026-10-15. Status: **M40_SIGNED_PASS, conditional on P1 normalization / Lemma V bundle**. Independent chat audit: PASS with the §VI constant correction incorporated below. Judge accepted the corrected constant. This is not D4 CLOSED or CERTIFIED.

The finite-part bridge below also uses the supplied uniform tail premise |T40(64)| < 10^-8. Its incomplete independent audit is not silently promoted. The direct full-kernel bound itself does not use that tail premise.

No repository write, commit, push, branch update, D5 access, numerical sampling, quadrature, parameter scan, or producer/checker run was used. The computational assistance is finite exact polynomial algebra in Python's standard-library rational/integer arithmetic.

## I. Executive verdict

On the entire fixed swept region

\[
119/200\le\lambda\le33/50,\qquad \rho^2+(z/\lambda)^2\le1/64,
\]

we obtain

\[
-E_{\rho^4}\le C:=\frac{193787991018310321}{1991390625000000}<100.
\]

With e0 = 1/100000000, an admissible finite-part upper bound and contractual constant are

\[
B_{40}=C+e_0=\frac{775151964152896909}{7965562500000000},
\]
\[
M_{40}^-=\max(0,B_{40}+e_0)
=\frac{387575982116276267}{3982781250000000}<100.
\]

The exact gap is

\[
100-M_{40}^-=\frac{10702142883723733}{3982781250000000}>0.
\]

The method certifies a signed composite kernel before bounding its positive geometric weight. It does not replace individual R derivatives by absolute bounds. It supplies the requested finite-part bound by an exact full/finite/tail bridge, instead of expanding the 64-term finite kernel.

## II. Sources and premises

The P1 definitions were checked against the existing local source text of `analysis/D_OB_P1_DESIGN_NOTE.md`, previously pinned to bg-oblate-spheroid commit `111c3169d950939bf375012673b43495e4480ee1`, blob `f81e120e44a866d206117d4fab5fac627f26ccd1`. No new Git pin verification is claimed in this submission. The note itself is marked analytic derivation pass / external audit pending / not binding. All analytic conclusions retain the specified P1 / Lemma V condition.

The normalization used is

\[
X=(\sqrt{1-\mu^2}\cos\phi,\sqrt{1-\mu^2}\sin\phi,\lambda\mu),
\quad w^2=\lambda^2(1-\mu^2)+\mu^2,
\]
\[
n=(\lambda\sqrt{1-\mu^2}\cos\phi,\lambda\sqrt{1-\mu^2}\sin\phi,\mu)/w,
\quad Y=X-p,\ D=|Y|,\ \gamma=n\cdot Y/D,
\]
\[
h=w\,n\cdot Y,\quad F=hG(\gamma),\quad G(\gamma)=\arccos^2\gamma,
\quad E=\frac1{4\pi\lambda}\int_{-1}^1\int_0^{2\pi}F\,d\phi\,d\mu.
\]

The uniform finite/tail identity and bound are inherited from the supplied accepted Plan A reduction. The new proof does not assume center constants 23,18 hold off centre. Neither mixed M22 nor a stronger central lower bound is used.

## III. Equivalent signed target kernel

Fix the unit physical differentiation direction v=e_rho. Write

\[
T=(Y/D)\cdot v,\quad a=n\cdot v,\quad e=\gamma T-a,\quad s=1-T^2.
\]

Let P_k be the Legendre polynomial, with P_0=1, P_1=T and the usual three-term recurrence. Differentiating at fixed X and n gives

\[
\partial_v^k\gamma=k!D^{-k}(\gamma P_k(T)-aP_{k-1}(T)),\qquad k\ge1.
\]

Define the following composite polynomials, retaining cancellation:

\[
V_0=\frac{\gamma^2s(3-7T^2)}8-2\gamma eTs+\frac{e^2(3T^2-1)}2,
\]
\[
V_1=\frac{\gamma^3s^2}4-2\gamma^2eTs+\gamma e^2(3T^2-2)+2e^3T,
\]
\[
V_2=-\frac32\gamma^2e^2s+2\gamma e^3T+e^4.
\]

For the common auxiliary variable t, put

\[
c=1-t^2,\quad A_t=1+\gamma+(1-\gamma)t^2,
\quad \eta=c/A_t.
\]

The full signed kernel is

\[
\mathcal K=4[1+\eta(1-\gamma)]
\left(12V_0-6\eta V_1+4\eta^2V_2-3\eta^3\gamma e^4\right),
\]

and the exact identity is

\[
-F_{vvvv}=wD^{-3}\int_0^1\mathcal K\,dt.
\]

For transparency, before substituting the common R integral, product and chain rules give

\[
-F_{vvvv}=2wD^{-3}
\left(24RV_0+12R'V_1+4R''V_2+R'''\gamma e^4\right).
\]

Thus all R derivatives are combined at the same t and gamma; no separate derivative majorants occur. The factor 4[1+eta(1-gamma)] equals 8/A_t.

### Relation to the requested finite J40

Write E40 = E40_finite + T40(64). By the accepted reduction,

\[
\int_{-1}^1\int_0^1\mathcal J_{40}\,dt\,d\mu=-E40_{\rm finite}.
\]

Therefore a bound -E40 <= C implies the requested integral bound <= C+e0. This is the exact target certified here. The complete-kernel route does not require truncating or estimating the individual P_(2k,j) terms.

## IV. Coverage: uniform gamma and regularity

At p=0,

\[
\gamma_0=\frac\lambda{w|X|}\ge\frac{2\lambda}{1+\lambda^2}\ge7/8.
\]

On the swept ellipsoid, |p| <= 1/8 and |X| >= 119/200. If delta is the angle between X and X-p, tangent geometry gives

\[
\sin\delta\le25/119,\qquad \cos\delta\ge391/400.
\]

If theta is the angle between n and X, then cos(theta)>=7/8 and sin(theta)<=sqrt(15)/8<=31/64. Angle addition consequently gives

\[
\gamma\ge\frac78\frac{391}{400}-\frac{31}{64}\frac{25}{119}
=\frac{286953}{380800}
>\frac{55}{73}.
\]

All these angles are acute and their sum is acute (the displayed lower cosine is positive). Also gamma <= 1.

Gram positivity for the three unit vectors n,Y/D,v gives

\[
e^2\le(1-\gamma^2)(1-T^2).
\]

The existing D>=833/1600 follows directly from X=Lx, p=Lq, |x|=1, |q|<=1/8, L=diag(1,1,lambda). Thus all differentiations are internal and regular. A sharper weighted lower bound used only after the signed certificate appears below.

## V. Exact rational Bernstein certificate K <= 24

The composite bracket S=12V0-6eta V1+4eta^2 V2-3eta^3 gamma e^4 expands to

\[
\begin{aligned}
S={}&\tfrac32\gamma^2s(3-7T^2)-\tfrac32\eta\gamma^3s^2
-12\gamma(2-\eta\gamma)eTs\\
&+6[(3T^2-1)-\eta\gamma(3T^2-2)-\eta^2\gamma^2s]e^2\\
&-4\eta(3-2\eta\gamma)Te^3
+\eta^2(4-3\eta\gamma)e^4.
\end{aligned}
\]

The expression is invariant under (T,e)->(-T,-e), so take T>=0. Since 0<=eta gamma<=1/2, both odd-e coefficients are nonpositive. Replacing e by -|e| can only increase K. This is a one-sided sign argument, not a triangle inequality or an absolute bound on the derivative.

Use rational stereographic variables

\[
T=\frac{1-u^2}{1+u^2},\quad
\gamma=\frac{1-v^2}{1+v^2},\quad
 e=-\frac{4uvp}{(1+u^2)(1+v^2)},\quad
\eta=\frac{q(1+v^2)}2,
\]

where u,p,q belong to [0,1], v belongs to [0,3/8]. This covers the complete relaxed Gram domain. The case gamma=1 has e=0 and is included without a singular division.

Put U=1+u^2, V=1+v^2, Tn=1-u^2, Gn=1-v^2, En=-4uvp. Define

\[
N_0=\tfrac12G_n^2u^2(3U^2-7T_n^2)-8G_nE_nT_nu^2
+\tfrac12E_n^2(3T_n^2-U^2),
\]
\[
N_1=4G_n^3u^4-8G_n^2E_nT_nu^2
+G_nE_n^2(3T_n^2-2U^2)+2E_n^3T_n,
\]
\[
N_2=-6G_n^2E_n^2u^2+2G_nE_n^3T_n+E_n^4,
\]
\[
N_S=12N_0-3qN_1+q^2N_2-\tfrac38q^3G_nE_n^4.
\]

Then

\[
\mathcal K=\frac{4(1+qv^2)N_S}{U^4V^2}.
\]

The positive-denominator polynomial certificate is

\[
\mathcal P=6U^4V^2-(1+qv^2)N_S\ge0.
\]

After setting v=3vhat/8, P has 77 nonzero power terms and multidegree (8,8,4,4) in (u,vhat,p,q). Every variable was subdivided into the four intervals [0,1/4], [1/4,1/2], [1/2,3/4], [3/4,1] **before evaluation**. These are 256 auxiliary boxes, not changes to physical scope or lambda. No adaptive subdivision was used.

Exact tensor Bernstein conversion followed by two midpoint subdivisions per variable gave:

- 256 boxes evaluated;
- 2025 Bernstein coefficients per box;
- 0 boxes with a negative coefficient;
- minimum coefficient over every box:

\[
\boxed{\frac{26392159755}{7516192768}>0.}
\]

Consequently P>0 and K<24 throughout the relaxed domain, hence K<=24 throughout the actual swept region and all surface/auxiliary variables.

The enclosed exact calculation is a reproducible finite algebraic verification. It is not an independent audit. No floating point arithmetic participates.

## VI. Surface integration without early dependency destruction

Only after K<=24 is certified do we bound its positive factor w D^-3.

Write y=mu^2, Q0=|X|^2=1-(1-lambda^2)y. From the swept constraint,

\[
|X\cdot p|\le\frac18\sqrt{1-y+\lambda^4y}.
\]

The elementary identity

\[
(1+\lambda^2)^2Q_0^2-4\lambda^2(1-y+\lambda^4y)
=(1-\lambda^2)^2[1-(1+\lambda^2)y]^2\ge0
\]

implies

\[
\frac{\sqrt{1-y+\lambda^4y}}{Q_0}
\le\frac{1+\lambda^2}{2\lambda}\le\frac87.
\]

Thus D^2>=Q0-2|X dot p|>=(5/7)Q0 and

\[
D^{-3}\le(7/5)^{3/2}Q_0^{-3/2}<\frac53 Q_0^{-3/2}.
\]

Let

\[
l=\frac{119}{200},\qquad c_{\min}=1-\left(\frac{33}{50}\right)^2=\frac{1411}{2500},
\qquad c_\lambda=1-\lambda^2.
\]

Throughout the band, \(c_\lambda\ge c_{\min}\). Concavity gives

\[
w\le1-\frac{c_{\min}}2(1-\mu^2).
\]

Therefore

\[
I:=\frac1{4\pi\lambda}\int_{-1}^1\int_0^{2\pi}wD^{-3}\,d\phi\,d\mu
\le\frac5{6l}\left[\frac2l-\frac{c_{\min}}2J_{\rm low}(c_{\min})\right].
\]

Here the positive-coefficient binomial expansion, together with \(c_\lambda\ge c_{\min}\), gives the uniform rigorous lower bound

\[
\int_{-1}^1\frac{1-\mu^2}{(1-c_\lambda\mu^2)^{3/2}}\,d\mu
\ge J_{\rm low}(c_{\min})
=\frac43+\frac{2c_{\min}}5+
\frac{3c_{\min}^2}{14}+\frac{5c_{\min}^3}{36}.
\]

The companion integral is exact for each \(\lambda\):

\[
\int_{-1}^1(1-c_\lambda\mu^2)^{-3/2}\,d\mu=\frac2\lambda\le\frac2l.
\]

No quadrature or remainder estimate is needed for the lower bound because all omitted binomial-series terms are nonnegative.

Exact arithmetic yields

\[
I\le\frac{193787991018310321}{47793375000000000}.
\]

Since the auxiliary t interval has length one, -E40 <= 24I = C, proving the full bound stated in I.

## VII. Phi averaging, consistency, and tail

This proof keeps the entire common-t signed numerator through differentiation and rationalization. It certifies that numerator pointwise before surface integration. It never estimates |F40| or individual R derivatives. The final majorant is independent of phi, so its phi average is exact (the zeroth moment equals one). No phi-series cancellation is assumed and no positive and negative monomials are separately absolutized. This is a direct signed integrated majorant alternative to a Bernstein hull of the large truncated phi numerator.

At p=0 the Legendre derivative identity is exactly the directional Taylor expansion of h G(gamma); hence it specializes to the same P1 center kernel without assuming the center bound globally. Formal product-rule composite identities were checked by exact polynomial arithmetic.

For the sphere at p=0, gamma=1, e=0, D=w=1. Integrating the common t factor gives

\[
\int_0^1K\,dt=6(1-T^2)(3-7T^2)-2(1-T^2)^2.
\]

The spherical moments <T^2>=1/3, <T^4>=1/5 give -E40=16/3, matching the required sphere control. Isotropy then gives E22=E40/3=-16/9. Parity follows from reflection invariance of the original surface integral; the proof also covers signed swept points.

For the requested finite quantity, using E40=E40_finite+T and |T|<e0,

\[
-E40_{\rm finite}=-E40+T\le C+e_0=B40.
\]

Adding the symmetric tail again supplies the requested contractual form M40^-=max(0,B40+e0). The extra e0 is deliberate and conservative. If the direct full-kernel proof is adopted independently, C itself suffices and the tail is unnecessary for this component.

## VIII. Failure localization and ruling

The target 100 is attained; no true derivative growth is inferred. Losses that remain are the Gram-domain relaxation, the pointwise signed upper hull, and the final positive-weight majorization. Their exact combined cost is already small enough. The proof does not depend on the unknown M22 or an improved center lower bound.

Post-audit Judge ruling (2026-10-15): Plan A is METHOD_SELECTED; this M40 component is PASS.

M40_SIGNED_PASS — conditional on P1 normalization / Lemma V bundle; finite bridge additionally conditional on the supplied tail premise. Independent chat audit: PASS with the §VI correction incorporated in V0.1.

SIXTH_ORDER=HOLD / NOT SELECTED.

**D4 overall: not CLOSED / not CERTIFIED by this component.**

## Appendix A. Exact polynomial computation

The following standard-library script constructs the entire cancelled polynomial, changes from power to tensor Bernstein coefficients, and visits the a-priori fixed auxiliary partition. Integer midpoint subdivision uses one common positive denominator. The minimum reported is over all 518400 terminal Bernstein coefficients.

### Polynomial certificate

```python
from fractions import Fraction as Q
from itertools import product
from math import comb,lcm
import json
class P(dict):
 def __add__(a,b):
  if not isinstance(b,P): b=P({(0,0,0,0):Q(b)})
  c=P(a)
  for i,x in b.items(): c[i]=c.get(i,0)+x
  return P({i:x for i,x in c.items() if x})
 __radd__=__add__
 def __neg__(a): return P({i:-x for i,x in a.items()})
 def __sub__(a,b): return a+-b
 def __rsub__(a,b): return -a+b
 def __mul__(a,b):
  if not isinstance(b,P): return P({i:x*b for i,x in a.items() if x*b})
  c=P()
  for i,x in a.items():
   for j,y in b.items():
    k=tuple(i[h]+j[h] for h in range(4));c[k]=c.get(k,0)+x*y
  return P({i:x for i,x in c.items() if x})
 __rmul__=__mul__
 def __pow__(a,n):
  b=P({(0,0,0,0):Q(1)})
  for _ in range(n):b=b*a
  return b
X=[P({tuple(int(i==j) for i in range(4)):Q(1)}) for j in range(4)]
u,v,p,q=X;v=Q(3,8)*v
U=1+u*u;V=1+v*v;T=1-u*u;G=1-v*v;E=-4*u*v*p
N0=Q(1,2)*G**2*u**2*(3*U**2-7*T**2)-8*G*E*T*u**2+Q(1,2)*E**2*(3*T**2-U**2)
N1=4*G**3*u**4-8*G**2*E*T*u**2+G*E**2*(3*T**2-2*U**2)+2*E**3*T
N2=-6*G**2*E**2*u**2+2*G*E**3*T+E**4
S=12*N0-3*q*N1+q**2*N2-Q(3,8)*q**3*G*E**4
F=6*U**4*V**2-(1+q*v**2)*S
ns=tuple(max(i[j] for i in F) for j in range(4)); inds=list(product(*[range(n+1) for n in ns])); positions={i:k for k,i in enumerate(inds)}
a=[F.get(i,Q(0)) for i in inds]
for axis,n in enumerate(ns):
 b=[]
 for idx in inds:
  val=Q(0)
  for h in range(idx[axis]+1):
   j=list(idx);j[axis]=h
   val+=a[positions[tuple(j)]]*Q(comb(idx[axis],h),comb(n,h))
  b.append(val)
 a=b
D=lcm(*(x.denominator for x in a));a=[int(x*D) for x in a]
lines=[]
for axis,n in enumerate(ns):
 ls=[]
 for idx in inds:
  if idx[axis]:continue
  line=[]
  for j in range(n+1):
   ii=list(idx);ii[axis]=j;line.append(positions[tuple(ii)])
  ls.append(line)
 lines.append(ls)
def split(a,axis):
 n=ns[axis];L=[0]*len(a);R=L.copy()
 for line in lines[axis]:
  vals=[a[i] for i in line]
  for j in range(n+1):
   L[line[j]]=sum(comb(j,k)*vals[k] for k in range(j+1))*2**(n-j)
   R[line[j]]=sum(comb(n-j,k)*vals[j+k] for k in range(n-j+1))*2**j
 return L,R
# Fixed a priori: four equal intervals in every auxiliary variable.
seq=[j for j in range(4) for _ in range(2)]
minimum=None;failed=0;cells=0;minpath=None
def visit(a,depth,path):
 global minimum,failed,cells,minpath
 if depth==len(seq):
  cells+=1;m=min(a)
  if m<0:failed+=1
  if minimum is None or m<minimum:minimum=m;minpath=path
  return
 L,R=split(a,seq[depth]);visit(L,depth+1,path+'0');visit(R,depth+1,path+'1')
visit(a,0,'')
res={'degrees':ns,'terms':len(F),'cells':cells,'failed_cells':failed,'min_bernstein':str(Q(minimum,D*2**sum(ns[j] for j in seq))),'minpath':minpath,'claim':'K <= 24','status':'PASS' if failed==0 else 'INCONCLUSIVE'}
print(json.dumps(res,indent=2))
with open('/workspace/scratch/330c7d76ef73/d4_signed_poly_result.json','w') as f:json.dump(res,f,indent=2)

```

### Polynomial output

```json
{
  "degrees": [
    8,
    8,
    4,
    4
  ],
  "terms": 77,
  "cells": 256,
  "failed_cells": 0,
  "min_bernstein": "26392159755/7516192768",
  "minpath": "10111111",
  "claim": "K <= 24",
  "status": "PASS"
}
```

### Identity and rational checks

```python
from d4_signed_poly import P,X,Q
from math import factorial
# Independent Legendre recurrence and product/chain rule composites.
g,T,e,r=X;a=g*T-e
leg=[P({(0,0,0,0):Q(1)}),T]
for n in range(1,4):leg.append(Q(2*n+1,n+1)*T*leg[n]-Q(n,n+1)*leg[n-1])
ej=[None]+[g*leg[k]-a*leg[k-1] for k in range(1,5)]
s=1-T*T
v0=g*ej[4]-a*ej[3]
v1=g*ej[2]**2+2*g*ej[1]*ej[3]-2*a*ej[1]*ej[2]
v2=3*g*ej[1]**2*ej[2]-a*ej[1]**3
assert not(v0-(Q(1,8)*g*g*s*(3-7*T*T)-2*g*e*T*s+Q(1,2)*e*e*(3*T*T-1)))
assert not(v1-(Q(1,4)*g**3*s*s-2*g*g*e*T*s+g*e*e*(3*T*T-2)+2*e**3*T))
assert not(v2-(-Q(3,2)*g*g*e*e*s+2*g*e**3*T+e**4))
S=12*v0-6*r*v1+4*r*r*v2-3*r**3*g*e**4
Sexp=Q(3,2)*g*g*s*(3-7*T*T)-Q(3,2)*r*g**3*s*s-12*g*(2-r*g)*e*T*s+6*((3*T*T-1)-r*g*(3*T*T-2)-r*r*g*g*s)*e*e-4*r*(3-2*r*g)*T*e**3+r*r*(4-3*r*g)*e**4
assert not(S-Sexp)
# Sphere integration: integrate auxiliary t first, then uniform spherical T.
sphere=6*s*(3-7*T*T)-2*s*s
avg=sum(coef*Q(1,k[1]+1) for k,coef in sphere.items() if k[1]%2==0)
assert avg==Q(16,3)
l=Q(119,200);cn=1-Q(33,50)**2
J=Q(4,3)+Q(2,5)*cn+Q(3,14)*cn**2+Q(5,36)*cn**3
I=Q(5,6)/l*(2/l-cn*J/2)
C=24*I;eps=Q(1,10**8);B=C+eps;M=C+2*eps
assert M<100
assert (Q(7,5)**3)<Q(5,3)**2
assert Q(391,400)**2<=1-Q(25,119)**2
assert Q(31,64)**2>=Q(15,64)
gmin=Q(7,8)*Q(391,400)-Q(31,64)*Q(25,119)
assert gmin>Q(55,73)
print('LEGENDRE_COMPOSITES: PASS; ODD_SIGN_EXPANSION: PASS; SPHERE: -16/3')
for name,x in [('gamma_min',gmin),('I',I),('C',C),('B_finite',B),('M_with_tail',M),('100_minus_M',100-M)]:print(name,str(x))

```
