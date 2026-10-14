# D4 Plan A — axis mixed one-sided certificate V0

2026-10-15 JST. Judge's revised instruction dated 2026-10-15.

**M22_SIGNED_PASS — mathematical submission, conditional on P1 normalization / Lemma V bundle; independent chat audit requested.**

No D4 CLOSED / CERTIFIED declaration is made. No repository write, commit, push, branch modification, D5 access, parameter scan, quadrature, adaptive subdivision, or producer run was performed. Exact polynomial calculations used Python standard-library rational/integer arithmetic. No M40 calculation was rerun; its corrected Judge constant is a fixed input.

## I. Executive verdict

For the entire fixed axis interval, including its endpoints,

\[
\lambda\in[119/200,33/50],\quad \rho=0,\quad 0\le z\le\lambda/8,
\]

we prove (in fact also for signed z with |z|<=lambda/8)

\[
-E_{\rho\rho zz}(0,z;\lambda)
\le B_{22}:=\frac{193787991018310321}{995695312500000}<200.
\]

There is no phi truncation and no phi tail:

\[
\varepsilon_{22}=0,\qquad
\boxed{M_{22}^-=\max(0,B_{22})=B_{22}.}
\]

The exact comparison is

\[
200-B_{22}=\frac{5351071481689679}{995695312500000}>0.
\]

The route keeps the common auxiliary integral, computes the phi-averaged mixed coefficient exactly, certifies the complete signed polynomial, and only then bounds the positive geometric weight. It proves an integrated bound; it does not claim the sufficient pointwise inequality N22<=100 lambda Omega^4.

## II. Original kernel and its exact common-integral identities

Use the instruction's a^2=1-mu^2, u=lambda mu-z, d^2=a^2+u^2, h=lambda-z mu, w^2=lambda^2 a^2+mu^2, g=h/(wd), c=1-t^2, Omega=(2-c)wd+ch.

For P,Q as supplied,

\[
K_{20}=\frac1\lambda\int_0^1(P/\Omega+Q/\Omega^2)\,dt,
\]

with

\[
P=2h^2d^{-2}-3a^2h^2d^{-4}+4a^2\lambda h d^{-2}-2a^2\lambda^2,
\quad Q=a^2ch(h-\lambda d^2)^2d^{-4}.
\]

Direct substitution of R=2wd/Omega and R'=-2c(wd)^2/Omega^2 at the common-integrand level gives exactly this expression. The sparse Laurent-polynomial difference is zero.

Independent differentiation of P/Omega+Q/Omega^2 gives

\[
\begin{aligned}
\mathcal N_{22}={}&-P''\Omega^3+2P'\Omega^2\Omega'+P\Omega^2\Omega''-2P\Omega(\Omega')^2\\
&-Q''\Omega^2+4Q'\Omega\Omega'+2Q\Omega\Omega''-6Q(\Omega')^2.
\end{aligned}
\]

The exact Laurent-polynomial difference against the negative second derivative is zero. We separately checked the supplied Y'', Q'', and Omega'' formulas (for Omega'', using d^2=a^2+u^2). In particular, the negative contribution -6Q(Omega')^2 is retained; no sign is discarded before cancellation.

### An equivalent phi-averaged signed integrand

Let X be the surface point, n its unit normal, Y=X-p, and n_Y=Y/d. On the axis write

\[
n_Y=(b\cos\phi,b\sin\phi,\zeta),\quad b=\sqrt{1-\zeta^2},\quad \gamma=n\cdot n_Y.
\]

Both n and n_Y are in the same meridional plane. For a signed scalar chi,

\[
\gamma n_Y-n=\chi(\zeta\cos\phi,\zeta\sin\phi,-b),\qquad
\chi^2=1-\gamma^2.
\]

Introduce formal physical direction variables X_1,X_3 and define

\[
T=b\cos\phi X_1+\zeta X_3,\quad
 e=\chi(\zeta\cos\phi X_1-bX_3),\quad
 L=X_1^2+X_3^2,\quad s=L-T^2.
\]

The following homogeneous polynomials come directly from the fourth directional product and chain rule:

\[
V_0=\tfrac18\gamma^2s(3L-7T^2)-2\gamma eTs+\tfrac12e^2(3T^2-L),
\]
\[
V_1=\tfrac14\gamma^3s^2-2\gamma^2eTs+\gamma e^2(3T^2-2L)+2e^3T,
\]
\[
V_2=-\tfrac32\gamma^2e^2s+2\gamma e^3T+e^4.
\]

For eta=c/[1+gamma+(1-gamma)t^2], define the finite linear functional

\[
\mathscr A(f)=\langle[X_1^2X_3^2]f\rangle_\phi.
\]

It uses exact moments <cos^(2k)phi>=binom(2k,k)/4^k and odd moments zero; in this mixed coefficient only powers 0 and 2 occur. The complete signed mixed kernel is

\[
\boxed{
\mathcal K_{22}=\frac{4}{6}[1+\eta(1-\gamma)]
\mathscr A(12V_0-6\eta V_1+4\eta^2V_2-3\eta^3\gamma e^4).
}
\]

The factor 1/6 converts a directional fourth-derivative coefficient into the mixed derivative. Including energy normalization gives the pointwise common-t identity

\[
\boxed{
\frac{\mathcal N_{22}}{\Omega^4}
=\frac{w}{2d^3}\mathcal K_{22}.
}
\]

Thus

\[
-E_{\rho\rho zz}
=\frac1{2\lambda}\int_{-1}^1\frac w{d^3}
\int_0^1\mathcal K_{22}\,dt\,d\mu.
\]

The connection was verified independently at each of R,R',R'',R''' before substituting their common integral, and again at the common-t rational-integrand level. Every difference is exactly zero. No absolute bound on an R derivative is inserted.

## III. Center / V0 specialization

The current Library source `D4_CENTER_FOURTH_COEFFICIENT_BOUNDS_V0.md` was read. Its definition is

\[
P_{22,j}(c_0,y)=\lambda^2q_0^4\langle[X_1^2X_3^2]T_j\rangle_\phi,
\quad c_0=1-\lambda^2,\quad y=\mu^2,\quad q_0=1-c_0y.
\]

The existing companion coefficient data were used as exact input, without recomputing the centre bounds. Differentiate the supplied K20 twice, keeping coefficients of R^(j) separate. Setting h=lambda, u=lambda mu, d^2=q0 gives

\[
\boxed{
\partial_z^2K_{20}(0,\lambda,\mu)
=-\frac4{\lambda^2q_0^4}
\sum_{j=0}^3\gamma_0^{j+1}R^{(j)}(\gamma_0)P_{22,j}(c_0,y).
}
\]

For each j=0,1,2,3, clearing q0^4 and substituting q0=1-(1-lambda^2)mu^2 yields the zero polynomial, coefficient by coefficient over the rationals. Merely treating q0 as an independent variable would not be the defining V0 identity; the explicit substitution is included in the check.

Results: j=0 difference=0; j=1 difference=0; j=2 difference=0; j=3 difference=0.

This is the main consistency control. The centre bound |E22|<18 is NOT applied off centre. As a separate auxiliary check, the same V0 polynomials at lambda=1 integrate exactly to -16/9.

## IV. Fixed-domain coverage and rational certificate

### Geometric coverage

The fixed swept ellipsoid implies |p|<=1/8, |X|>=119/200, d>=833/1600. At p=0,

\[
\gamma_0\ge2\lambda/(1+\lambda^2)\ge7/8.
\]

Let delta be the angle between X and X-p. Then sin(delta)<=25/119 and cos(delta)>=391/400. The angle between n and X has sine <=sqrt(15)/8<=31/64. Angle addition proves throughout the swept region

\[
\gamma\ge\frac78\frac{391}{400}-\frac{31}{64}\frac{25}{119}
=\frac{286953}{380800}>\frac{55}{73}.
\]

These are geometric lemmas, not a reuse of a centre fourth-derivative bound or a recomputation of M40.

Reflection of the axial coordinate changes (zeta,chi) to (-zeta,-chi) and leaves the mixed even coefficient invariant. Thus take zeta>=0 without losing either half of the axis. Rationalize exactly by

\[
\zeta=\frac{1-r^2}{1+r^2},\quad b=\frac{2r}{1+r^2},\quad
\gamma=\frac{1-v^2}{1+v^2},\quad \chi=\frac{2v}{1+v^2},\quad
\eta=\frac{q(1+v^2)}2,
\]

where r,q belong to [0,1] and v belongs to [-3/8,3/8]. This covers the full axis geometry and permits both signs of chi. Degenerate endpoints are included continuously. No physical domain is shrunk.

### Polynomial to certify

Let U=1+r^2, V=1+v^2, G=1-v^2, and B denote cos(phi). Define homogeneous polynomials

\[
T_n=2rBX_1+(1-r^2)X_3,\qquad
E_n=2v[(1-r^2)BX_1-2rX_3],
\]
\[
L=X_1^2+X_3^2,\qquad S_n=LU^2-T_n^2.
\]

Set

\[
N_0=\tfrac18G^2S_n(3LU^2-7T_n^2)-2GE_nT_nS_n
+\tfrac12E_n^2(3T_n^2-LU^2),
\]
\[
N_1=\tfrac14G^3S_n^2-2G^2E_nT_nS_n
+GE_n^2(3T_n^2-2LU^2)+2E_n^3T_n,
\]
\[
N_2=-\tfrac32G^2E_n^2S_n+2GE_n^3T_n+E_n^4,
\]
\[
N=\mathscr A(12N_0-3qN_1+q^2N_2-\tfrac38q^3GE_n^4).
\]

All phi averaging is completed here. N is a polynomial with 74 nonzero coefficients, retained in full in the result appendix. The exact mixed kernel is

\[
\mathcal K_{22}=\frac{2(1+qv^2)N}{3U^4V^2}.
\]

Since U^4V^2>0, the chosen fixed target K22<=48 is equivalent to

\[
\boxed{\mathscr P=72U^4V^2-(1+qv^2)N\ge0.}
\]

There is no termwise absolute-value step. Dependence among gamma,chi,zeta,b,eta remains encoded in the same rational variables until this signed numerator is formed.

### Exact Bernstein record

Set v=-3/8+(3/4)s. The polynomial in (r,s,q) has multidegree (8,8,4), with 259 nonzero power coefficients. Before evaluation, each auxiliary variable was assigned the four equal intervals with rational endpoints 0,1/4,1/2,3/4,1. No result-driven refinement occurred.

There are 64 auxiliary boxes and 405 Bernstein coefficients in each box, for 25,920 coefficients total. All are strictly positive.

\[
\boxed{\min b=\frac{139515}{1792}>0,\qquad
\max b=\frac{744477}{512}.}
\]

The appendix records each box's exact min/max numerators, a common positive denominator, and positive/zero/negative coefficient counts. Every box has (405,0,0). The script also completely defines and reproduces the coefficient arrays.

Therefore K22<=48 holds throughout the relaxed domain and hence on the required physical axis.

## V. Integrated exact bound

Only after the signed composite certificate is proved do we majorize the positive weight. Put l=119/200, cmin=1411/2500 and Q0=1-(1-lambda^2)mu^2.

The swept-ellipsoid condition gives

\[
|X\cdot p|\le\tfrac18\sqrt{1-\mu^2+\lambda^4\mu^2},
\quad
\frac{\sqrt{1-\mu^2+\lambda^4\mu^2}}{Q_0}
\le\frac{1+\lambda^2}{2\lambda}\le8/7.
\]

The middle inequality follows by squaring positive quantities; its numerator difference is (1-lambda^2)^2[1-(1+lambda^2)mu^2]^2. Consequently

\[
d^2\ge(5/7)Q_0,\qquad d^{-3}\le(5/3)Q_0^{-3/2},
\quad w\le1-\tfrac12c_{\min}(1-\mu^2).
\]

Using the positive binomial series, uniformly for c_lambda=1-lambda^2>=cmin,

\[
\int_{-1}^1\frac{1-\mu^2}{(1-c_\lambda\mu^2)^{3/2}}\,d\mu
\ge J_{\rm low}(c_{\min})
=\frac43+\frac{2c_{\min}}5+
\frac{3c_{\min}^2}{14}+\frac{5c_{\min}^3}{36}.
\]

This explicitly uses cmin, as directed. Omitted series terms are nonnegative. The companion integral of Q0^(-3/2) is exactly 2/lambda <=2/l.

Thus the positive axis weight satisfies

\[
I:=\frac1{2\lambda}\int_{-1}^1wd^{-3}\,d\mu
\le\frac5{6l}\left[\frac2l-\frac{c_{\min}}2J_{\rm low}(c_{\min})\right]
=\frac{193787991018310321}{47793375000000000}.
\]

The t interval has length one. Therefore

\[
\boxed{-E_{\rho\rho zz}\le48I
=\frac{193787991018310321}{995695312500000}<200.}
\]

This calculation bounds the mixed integral. The prior M40 certificate and its numerical constant are not rerun or modified.

## VI. Independent checks within this submission

These are separate algebraic derivations/checks in this calculation, NOT a claim of an independent external chat audit.

1. K20 -> P,Q,Omega: exact difference zero.
2. Negative second derivative -> N22: exact difference zero.
3. Supplied Q'' and Omega'' formulas: exact difference zero, with defining distance identity where needed.
4. Directional phi-averaged mixed expression -> differentiated K20: four exact zero differences for the four R derivative coefficients.
5. Common-t rational-integrand connection: exact difference zero after positive denominator clearing and the defining Omega and d identities.
6. z=0 -> V0 P22,j: four coefficient-level exact zero polynomials.
7. Sphere, auxiliary only: exact -16/9.
8. Signed Bernstein: 25,920 positive coefficients; none zero or negative.
9. Rational comparison to 200: positive exact difference shown above.

No independent worst-case replacement of P,Q,Omega, no early triangle inequality, and no phi tail were used.

## VII. Exact D4 Taylor margin

The fixed Judge input is

\[
M_{40}^-=\frac{193787991018310321}{1991390625000000}+\frac2{10^8}
=\frac{387575982116276267}{3982781250000000}.
\]

With the new M22^- above and the unchanged m*=1547/4860,

\[
\boxed{
\frac{1547}{4860}-\frac{M_{40}^-}{384}
-\frac{M_{22}^-}{2}\left(\frac{33}{1625}\right)^2
=\frac{900009544615558979777197}{36346861687500000000000000}>0.
}
\]

This is about 0.0247616851, for display only. Replacing the stronger new M22 bound by the contractual 200 gives exactly

\[
\frac{55022792357943797893}{2326199148000000000000}>0,
\]

matching the Judge's specified margin. The center lower bound was not strengthened.

## VIII. Recommended D4 ruling

**Recommended D4 ruling: Plan A METHOD_SELECTED candidate → positivity inequality PASS, conditional on P1 normalization / Lemma V bundle.**

The whole closed D4 box uses the predeclared FTC paths, all contained in the fixed swept region. At r=0 the regular extension of H is included; positivity of that extension does not remove the symmetry-forced central stationary point. The theorem-to-D-P2 handoff and final Judge discharge remain separate requirements. No D4 CLOSED / CERTIFIED declaration follows from this submission alone.

Sixth-order: HOLD. Independent chat audit requested for the new M22 certificate and its connection to the existing contracts.

---

# Reproducibility appendices

Extract each fenced block under its filename into one scratch directory. Execute `python d4_m22_checks.py` and `python d4_m22_certificate.py`. No third-party package is required. The scripts do not read or write a repository or run a D-P2 producer. The input V0 file contains the existing E22 coefficient records; the comparison uses only those coefficients, not their numerical bound.

## d4_m22_algebra.py

SHA-256: e24ff38dae62d7457aedc65ab46e528c8a737c5887e3ff037b098c4fdb6ed30b

```python
"""Exact polynomial algebra and analytic beta-series bounds; no parameter sampling."""
from fractions import Fraction as F
from math import comb,ceil
import json
from pathlib import Path
NVAR=12 # x,z,b,mu,lambda,q; Laurent exponents allowed
class P(dict):
 def __add__(a,b):
  if not isinstance(b,P): b=P({(0,)*NVAR:F(b)})
  d=P(a)
  for k,v in b.items(): d[k]=d.get(k,F(0))+v
  return P({k:v for k,v in d.items() if v})
 __radd__=__add__
 def __neg__(a):return P({k:-v for k,v in a.items()})
 def __sub__(a,b):return a+-b
 def __rsub__(a,b):return -a+b
 def __mul__(a,b):
  if not isinstance(b,P):return P({k:v*F(b) for k,v in a.items() if v*F(b)})
  d=P()
  for k,v in a.items():
   for l,w in b.items():
    h=tuple(i+j for i,j in zip(k,l));d[h]=d.get(h,F(0))+v*w
  return P({k:v for k,v in d.items() if v})
 __rmul__=__mul__
 def __truediv__(a,b):return a*F(1,b)
 def __pow__(a,n):
  if n<0:
   assert len(a)==1
   k,v=next(iter(a.items()));return P({tuple(i*n for i in k):v**n})
  out=P({(0,)*NVAR:F(1)})
  for _ in range(n):out=out*a
  return out
def var(i):return P({tuple(int(j==i) for j in range(NVAR)):F(1)})

```

## d4_m22_v0_input.json

SHA-256: a5907dc8d8146d5c0e9eea8e50ad2f6d30301db19caf2ed6e7a1aeec9dff8324

```json
{
  "bounds": {
    "E22": {
      "terms": [
        {
          "j": 0,
          "numerator": {
            "0,0": "1/8",
            "0,1": "2",
            "0,2": "-21/8",
            "1,0": "-1/8",
            "1,1": "-25/4",
            "1,2": "111/8",
            "1,3": "-6",
            "2,1": "9/2",
            "2,2": "-81/4",
            "2,3": "75/4",
            "2,4": "-9/2",
            "3,2": "33/4",
            "3,3": "-25/2",
            "3,4": "19/4",
            "4,3": "1/2",
            "4,4": "-1/2"
          },
          "degree_y": 4,
          "bernstein_abs_c_envelope": [
            "1089/20000",
            "1547039/50000000",
            "5902237341/125000000000",
            "62724453923241/312500000000000",
            "1291467969/31250000000"
          ],
          "integral_upper": "4071239836401658181020681448494946783346704450841763288697865512351825766108960085093971403096019/3278940982406894379337796119253832134229858788546199513427087132313813678245456489746093750000000"
        },
        {
          "j": 1,
          "numerator": {
            "0,0": "1/8",
            "0,1": "1/4",
            "0,2": "-3/8",
            "1,0": "-1/8",
            "1,1": "-7/4",
            "1,2": "39/8",
            "1,3": "-3",
            "2,1": "5/4",
            "2,2": "-41/4",
            "2,3": "27/2",
            "2,4": "-9/2",
            "3,2": "8",
            "3,3": "-35/2",
            "3,4": "25/2",
            "3,5": "-3",
            "4,3": "7/4",
            "4,4": "-13/4",
            "4,5": "3/2"
          },
          "degree_y": 5,
          "bernstein_abs_c_envelope": [
            "1089/20000",
            "176110079/6400000000",
            "2715730761531/80000000000000",
            "4786550311505520313/102400000000000000000",
            "50651778143241/781250000000000",
            "0"
          ],
          "integral_upper": "1135908853160963240187111912514847542170484924313009611598360310227830032850170494534545629583241358684883/2541896662174460341370805060569769897662321565619594161316015045307719392860417574276796800000000000000000"
        },
        {
          "j": 2,
          "numerator": {
            "2,1": "-1/8",
            "2,2": "-1/2",
            "2,3": "11/8",
            "2,4": "-3/4",
            "3,2": "11/8",
            "3,3": "-15/4",
            "3,4": "27/8",
            "3,5": "-1",
            "4,3": "1",
            "4,4": "-5/2",
            "4,5": "2",
            "4,6": "-1/2"
          },
          "degree_y": 6,
          "bernstein_abs_c_envelope": [
            "0",
            "222551307/25600000000",
            "13894637659/1875000000000",
            "442320927649/48828125000000",
            "302041310210585253/25600000000000000000",
            "0",
            "0"
          ],
          "integral_upper": "14473150092420926437979011994648950990527921128649636577820792408697163963510452082398153176204443563461/296950544646549105300327693991795548792327285703223616976169981928471891689301118490280000000000000000000"
        },
        {
          "j": 3,
          "numerator": {
            "4,3": "1/8",
            "4,4": "-3/8",
            "4,5": "3/8",
            "4,6": "-1/8"
          },
          "degree_y": 6,
          "bernstein_abs_c_envelope": [
            "0",
            "0",
            "0",
            "445761758226674241/409600000000000000000",
            "0",
            "0",
            "0"
          ],
          "integral_upper": "593873397744724708833199652761350998598607203281322815612395276324295729211007921930457812441/420701882928909264191610271699804540316251774526934592032054143567918254127280000000000000000000"
        }
      ]
    }
  }
}
```

## d4_m22_checks.py

SHA-256: 0c14f2064e25a8262e8fce4c491a31004c12a63d7c542a1e291623fd467f00af

```python
from fractions import Fraction as F
from math import comb,factorial
import json
# Load polynomial class only, not prior certificates or numerical evaluations.
from d4_m22_algebra import P,var
h,u,d,w,lam,mu,c,O,g,x,z,b=map(var,range(12))
a2=1-mu*mu
Op=-(2-c)*w*u*d**-1-c*mu
Opp=(2-c)*w*(d*d-u*u)*d**-3
rates={0:-mu,1:-1,2:-u*d**-1,7:Op,8:g*(-mu*h**-1+u*d**-2)}
def derivative(p):
 out=P()
 for idx,val in p.items():
  for j,rate in rates.items():
   if idx[j]:
    ii=list(idx);ii[j]-=1
    out+=P({tuple(ii):val*idx[j]})*rate
 return out
def subst(p,mapping):
 out=P()
 for idx,val in p.items():
  term=P({(0,)*12:val})
  for j,n in enumerate(idx):
   if n:term*=mapping.get(j,var(j))**n
  out+=term
 return out
U=d**-2-lam*h**-1
CC=F(3,2)*d**-4-2*lam*h**-1*d**-2+lam**2*h**-2
PP=2*h*h*d**-2-3*a2*h*h*d**-4+4*a2*lam*h*d**-2-2*a2*lam*lam
QQ=a2*c*h*(h-lam*d*d)**2*d**-4
common=2*h*h*lam**-1*O**-1*(d**-2-a2*CC)+a2*c*h**3*lam**-1*O**-2*U**2
assert not(common-lam**-1*(PP*O**-1+QQ*O**-2))
NN=-derivative(derivative(PP))*O**3+2*derivative(PP)*O**2*Op+PP*O**2*Opp-2*PP*O*Op**2-derivative(derivative(QQ))*O**2+4*derivative(QQ)*O*Op+2*QQ*O*Opp-6*QQ*Op**2
assert not(-derivative(derivative(PP*O**-1+QQ*O**-2))-NN*O**-4)
# K20 coefficients of R,R',...; independent differentiation.
K=[h*lam**-1*g*(d**-2-a2*CC),-F(1,2)*h*lam**-1*a2*g*g*U*U]
def DR(coeffs):
 out=[P() for _ in range(len(coeffs)+1)]
 for j,k in enumerate(coeffs):out[j]+=derivative(k);out[j+1]+=k*rates[8]
 return out
Kzz=DR(DR(K))
# Compare to stored V0 P22,j, polynomial by polynomial, no centre bound reuse.
old=json.load(open('d4_m22_v0_input.json'))['bounds']['E22']['terms']
for j,k in enumerate(Kzz):
 kc=subst(k,{0:lam,1:lam*mu})
 # d^(2m) -> q^m. Use variable O as q in this comparison.
 kd=P()
 for idx,val in kc.items():
  assert idx[2]%2==0
  ii=list(idx);ii[7]+=ii[2]//2;ii[2]=0;kd+=P({tuple(ii):val})
 po=P()
 for key,val in old[j]['numerator'].items():
  ic,iy=map(int,key.split(','));po+=F(val)*(1-lam*lam)**ic*mu**(2*iy)
 expected=-4*g**(j+1)*po*lam**-2*O**-4
 assert not(subst((kd-expected)*O**4,{7:1-(1-lam*lam)*mu*mu})),('centre mismatch',j)
# Fourth directional derivative, followed by exact phi average, independent of K20 differentiation.
T=(b*x+u*z)*d**-1
av=(lam*b*x+mu*z)*w**-1
e=g*T-av;norm=x*x+z*z;ss=norm-T*T
V0=F(1,8)*g*g*ss*(3*norm-7*T*T)-2*g*e*T*ss+F(1,2)*e*e*(3*T*T-norm)
V1=F(1,4)*g**3*ss*ss-2*g*g*e*T*ss+g*e*e*(3*T*T-2*norm)+2*e**3*T
V2=-F(3,2)*g*g*e*e*ss+2*g*e**3*T+e**4
Vs=[24*V0,12*V1,4*V2,g*e**4]
def phi_mixed(p):
 out=P()
 for idx,val in p.items():
  if idx[9:11]!=(2,2) or idx[11]%2:continue
  power=idx[11];ii=list(idx);ii[9]=ii[10]=ii[11]=0
  out+=P({tuple(ii):val})*a2**(power//2)*F(comb(power,power//2),2**power)
 return out
# Polynomial reduction modulo d^2=a2+u^2 after clearing monomial denominators.
def canonical(p):
 p=subst(p,{8:h*w**-1*d**-1})
 if not p:return p
 shifts=[max(0,-min(i[j] for i in p)) for j in range(12)]
 pp=P({tuple(i[j]+shifts[j] for j in range(12)):v for i,v in p.items()})
 out=P()
 for idx,val in pp.items():
  ii=list(idx);n=ii[2];ii[2]=n%2
  out+=P({tuple(ii):val})*(a2+u*u)**(n//2)
 return out
for j,vv in enumerate(Vs):
 target=w*lam**-1*d**-3*phi_mixed(vv)/6
 assert not(canonical(target+Kzz[j])),('mixed mismatch',j)
# Common-t integrand connection (not only equality after integration).
rr=P()
for j,k in enumerate(Kzz):rr+=-k*2*(-1)**j*factorial(j)*c**j*(w*d)**(j+1)*O**(-j-1)
diff=subst(rr-lam**-1*NN*O**-4,{8:h*w**-1*d**-1})
if diff:
 shifts=[max(0,-min(i[j] for i in diff)) for j in range(12)]
 diff=P({tuple(i[j]+shifts[j] for j in range(12)):val for i,val in diff.items()})
 diff=subst(diff,{7:(2-c)*w*d+c*h})
 assert not(canonical(diff))
# Verify supplied derivatives, reducing only the defining d^2 identity.
assert not(canonical(Opp-(2-c)*w*a2*d**-3))
VV=h-lam*d*d;YY=h*VV*VV
Y1=-mu*VV*VV+2*h*VV*(-mu+2*lam*u)
Y2=-4*mu*VV*(-mu+2*lam*u)+2*h*(-mu+2*lam*u)**2-4*lam*h*VV
assert not(derivative(YY)-Y1)
assert not(derivative(derivative(YY))-Y2)
assert not(derivative(derivative(QQ))-a2*c*(Y2*d**-4+8*u*Y1*d**-6-4*YY*d**-6+24*u*u*YY*d**-8))
sphere=F(0)
for j,term in enumerate(old):
 integ=sum(F(val)*F(2,2*int(key.split(',')[1])+1) for key,val in term['numerator'].items() if key.split(',')[0]=='0')
 sphere-=4*[F(1),F(-1,3),F(4,15),F(-12,35)][j]*integ
assert sphere==F(-16,9)
# Supplied corrected geometric integral lemma, evaluated for M22 (M40 not recomputed).
l=F(119,200);cmin=F(1411,2500)
J=F(4,3)+F(2,5)*cmin+F(3,14)*cmin**2+F(5,36)*cmin**3
I=F(5,6)/l*(2/l-cmin*J/2)
B22=48*I
assert B22<=200
M40=F(193787991018310321,1991390625000000)+F(2,10**8)
margin=F(1547,4860)-M40/384-B22/2*F(33,1625)**2
margin200=F(1547,4860)-M40/384-100*F(33,1625)**2
assert margin>0
assert margin200==F(55022792357943797893,2326199148000000000000)
result={'common_t_integrand_connection':'difference=0','K20_common_integral':'difference=0','N22_second_derivative':'difference=0','centre_V0_coefficients':['difference=0']*4,'mixed_directional_connection':['difference=0']*4,'I_upper':str(I),'B22':str(B22),'200_minus_B22':str(200-B22),'M40_fixed':str(M40),'Taylor_margin':str(margin),'Taylor_margin_using_200':str(margin200),'epsilon22':0,'Q_second_derivative':'difference=0','Omega_second_derivative':'difference=0 modulo d^2=a^2+u^2','sphere_control':str(sphere)}
print(json.dumps(result,indent=2))
open('d4_m22_checks_result.json','w').write(json.dumps(result,indent=2))

```

## d4_m22_checks_result.json

SHA-256: 91f63c1cf34ae9f92278bfdb9e27dbaf16456ef8d316b3aa352739ab4fc05fc1

```json
{
  "common_t_integrand_connection": "difference=0",
  "K20_common_integral": "difference=0",
  "N22_second_derivative": "difference=0",
  "centre_V0_coefficients": [
    "difference=0",
    "difference=0",
    "difference=0",
    "difference=0"
  ],
  "mixed_directional_connection": [
    "difference=0",
    "difference=0",
    "difference=0",
    "difference=0"
  ],
  "I_upper": "193787991018310321/47793375000000000",
  "B22": "193787991018310321/995695312500000",
  "200_minus_B22": "5351071481689679/995695312500000",
  "M40_fixed": "387575982116276267/3982781250000000",
  "Taylor_margin": "900009544615558979777197/36346861687500000000000000",
  "Taylor_margin_using_200": "55022792357943797893/2326199148000000000000",
  "epsilon22": 0,
  "Q_second_derivative": "difference=0",
  "Omega_second_derivative": "difference=0 modulo d^2=a^2+u^2",
  "sphere_control": "-16/9"
}
```

## d4_m22_certificate.py

SHA-256: c9839d1c0a88fc92e3b4adef0419efc7494a74191943805820293df67de0ee65

```python
from fractions import Fraction as F
from math import comb,lcm
from itertools import product
import json
NV=6
class P(dict):
 def __add__(a,b):
  if not isinstance(b,P):b=P({(0,)*NV:F(b)})
  c=P(a)
  for i,x in b.items():c[i]=c.get(i,0)+x
  return P({i:x for i,x in c.items() if x})
 __radd__=__add__
 def __neg__(a):return P({i:-x for i,x in a.items()})
 def __sub__(a,b):return a+-b
 def __rsub__(a,b):return -a+b
 def __mul__(a,b):
  if not isinstance(b,P):return P({i:x*b for i,x in a.items() if x*b})
  c=P()
  for i,x in a.items():
   for j,y in b.items():
    k=tuple(i[h]+j[h] for h in range(NV));c[k]=c.get(k,0)+x*y
  return P({i:x for i,x in c.items() if x})
 __rmul__=__mul__
 def __pow__(a,n):
  b=P({(0,)*NV:F(1)})
  for _ in range(n):b=b*a
  return b
X=[P({tuple(int(i==j) for i in range(NV)):F(1)}) for j in range(NV)]
u,v,q,x,z,b=X
U=1+u*u;V=1+v*v;G=1-v*v;norm=x*x+z*z
T=2*u*b*x+(1-u*u)*z
E=2*v*((1-u*u)*b*x-2*u*z)
S=norm*U*U-T*T
N0=F(1,8)*G**2*S*(3*norm*U**2-7*T**2)-2*G*E*T*S+F(1,2)*E**2*(3*T**2-norm*U**2)
N1=F(1,4)*G**3*S*S-2*G*G*E*T*S+G*E*E*(3*T*T-2*norm*U*U)+2*E**3*T
N2=-F(3,2)*G*G*E*E*S+2*G*E**3*T+E**4
NS=12*N0-3*q*N1+q*q*N2-F(3,8)*q**3*G*E**4
mixed=P()
for idx,val in NS.items():
 if idx[3:5]!=(2,2):continue
 if idx[5]%2:continue
 moment=F(comb(idx[5],idx[5]//2),2**idx[5])
 key=idx[:3]+(0,0,0);mixed[key]=mixed.get(key,0)+val*moment
poly=72*U**4*V**2-(1+q*v*v)*mixed # K22 <= 48
# v=-3/8+3/4*vv, fixed a priori entire signed interval.
pp={}
for idx,val in poly.items():
 for j in range(idx[1]+1):
  key=(idx[0],j,idx[2])
  pp[key]=pp.get(key,0)+val*comb(idx[1],j)*F(-3,8)**(idx[1]-j)*F(3,4)**j
pp={i:x for i,x in pp.items() if x}
ns=tuple(max(i[j] for i in pp) for j in range(3));inds=list(product(*[range(n+1) for n in ns]));pos={i:k for k,i in enumerate(inds)}
a=[pp.get(i,F(0)) for i in inds]
for ax,n in enumerate(ns):
 out=[]
 for idx in inds:
  val=0
  for j in range(idx[ax]+1):
   ii=list(idx);ii[ax]=j;val+=a[pos[tuple(ii)]]*F(comb(idx[ax],j),comb(n,j))
  out.append(val)
 a=out
D=lcm(*(v.denominator for v in a));a=[int(v*D) for v in a]
lines=[]
for ax,n in enumerate(ns):
 ls=[]
 for idx in inds:
  if idx[ax]:continue
  line=[]
  for j in range(n+1):ii=list(idx);ii[ax]=j;line.append(pos[tuple(ii)])
  ls.append(line)
 lines.append(ls)
def split(a,ax):
 n=ns[ax];L=[0]*len(a);R=L.copy()
 for line in lines[ax]:
  vals=[a[i] for i in line]
  for j in range(n+1):
   L[line[j]]=sum(comb(j,k)*vals[k] for k in range(j+1))*2**(n-j)
   R[line[j]]=sum(comb(n-j,k)*vals[j+k] for k in range(n-j+1))*2**j
 return L,R
# Fixed 4-way subdivision on each of three auxiliary coordinates; no adaptation.
seq=[0,0,1,1,2,2];mins=[];maxs=[];signs=[]
def visit(a,dep,path):
 if dep==len(seq):
  mins.append(min(a));maxs.append(max(a));signs.append({'path':path,'nonnegative':min(a)>=0,'positive_count':sum(v>0 for v in a),'zero_count':sum(v==0 for v in a),'negative_count':sum(v<0 for v in a),'min_numerator':str(min(a)),'max_numerator':str(max(a))});return
 L,R=split(a,seq[dep]);visit(L,dep+1,path+'0');visit(R,dep+1,path+'1')
visit(a,0,'');den=D*2**sum(ns[j] for j in seq)
res={'target':'K22 <= 48','degrees':ns,'terms':len(pp),'boxes':len(mins),'coefficients_per_box':len(inds),'min':str(F(min(mins),den)),'max':str(F(max(maxs),den)),'negative_boxes':sum(x<0 for x in mins),'common_denominator':str(den),'box_records':signs,'mixed_numerator':{','.join(map(str,i[:3])):str(x) for i,x in mixed.items()}}
print({k:v for k,v in res.items() if k not in ('box_records','mixed_numerator')})
with open('d4_m22_certificate_result.json','w') as f:json.dump(res,f,indent=2)

```

## d4_m22_certificate_result.json

SHA-256: 1e36f65bc1badba9aa25897d185ab9078e0fd0f77b56671034baaa6d83444398

```json
{
  "target": "K22 <= 48",
  "degrees": [
    8,
    8,
    4
  ],
  "terms": 259,
  "boxes": 64,
  "coefficients_per_box": 405,
  "min": "139515/1792",
  "max": "744477/512",
  "negative_boxes": 0,
  "common_denominator": "90389045961176802918400",
  "box_records": [
    {
      "path": "000000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7402255452479637631795200",
      "max_numerator": "11943590350677548099174400"
    },
    {
      "path": "000001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7410661951822180122624000",
      "max_numerator": "11910720062163072004915200"
    },
    {
      "path": "000010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7419149293554300773990400",
      "max_numerator": "11873104566971963277312000"
    },
    {
      "path": "000011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7427717477675999585894400",
      "max_numerator": "11831397214807701376204800"
    },
    {
      "path": "000100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7050345584971790627635200",
      "max_numerator": "9389478156231804085862400"
    },
    {
      "path": "000101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7050345584971790627635200",
      "max_numerator": "9363305405597393751244800"
    },
    {
      "path": "000110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7050345584971790627635200",
      "max_numerator": "9337779944403654043238400"
    },
    {
      "path": "000111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7050345584971790627635200",
      "max_numerator": "9312973375710007699046400"
    },
    {
      "path": "001000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7037180662541061193728000",
      "max_numerator": "8305665793131147037900800"
    },
    {
      "path": "001001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7038429060357768295219200",
      "max_numerator": "8334126205749484742246400"
    },
    {
      "path": "001010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7039223495332036450713600",
      "max_numerator": "8365440923985381467750400"
    },
    {
      "path": "001011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7040017930306304606208000",
      "max_numerator": "8399709767357486333952000"
    },
    {
      "path": "001100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7242077168300504540774400",
      "max_numerator": "9967123026023687808614400"
    },
    {
      "path": "001101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7262627285343045628723200",
      "max_numerator": "9926042224046642508595200"
    },
    {
      "path": "001110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7283842463120283716812800",
      "max_numerator": "9892133260287245549568000"
    },
    {
      "path": "001111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "7301951368907770036224000",
      "max_numerator": "9866813662504086719692800"
    },
    {
      "path": "010000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "9363305405597393751244800",
      "max_numerator": "20853374486545620900249600"
    },
    {
      "path": "010001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "9337779944403654043238400",
      "max_numerator": "20684406465724132884480000"
    },
    {
      "path": "010010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "9312973375710007699046400",
      "max_numerator": "20521550256865379824435200"
    },
    {
      "path": "010011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "9288958707674363461632000",
      "max_numerator": "20368193738067884900352000"
    },
    {
      "path": "010100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8168223173503184220979200",
      "max_numerator": "16114148500294472407449600"
    },
    {
      "path": "010101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8184178075903069677158400",
      "max_numerator": "16100749501282762358784000"
    },
    {
      "path": "010110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8200132978302955133337600",
      "max_numerator": "16093126518490112458752000"
    },
    {
      "path": "010111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8216087880702840589516800",
      "max_numerator": "16096240652875670224896000"
    },
    {
      "path": "011000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8022982429766667164712960",
      "max_numerator": "15967768828296596501299200"
    },
    {
      "path": "011001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8050708697307880095744000",
      "max_numerator": "15973452334698081760051200"
    },
    {
      "path": "011010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8078374302486448884940800",
      "max_numerator": "15984257211870925239091200"
    },
    {
      "path": "011011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8106295004601863739801600",
      "max_numerator": "16000414328222423973888000"
    },
    {
      "path": "011100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8279961271710205240934400",
      "max_numerator": "20591210945037129587097600"
    },
    {
      "path": "011101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8305665793131147037900800",
      "max_numerator": "20481713334376017690624000"
    },
    {
      "path": "011110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8334126205749484742246400",
      "max_numerator": "20374361430955734859776000"
    },
    {
      "path": "011111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "8365440923985381467750400",
      "max_numerator": "20271692549474333648486400"
    },
    {
      "path": "100000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "16100749501282762358784000",
      "max_numerator": "47688015946371177224601600"
    },
    {
      "path": "100001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "16093126518490112458752000",
      "max_numerator": "47445494508056513347584000"
    },
    {
      "path": "100010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "16091158336564698493747200",
      "max_numerator": "47237591159734309748736000"
    },
    {
      "path": "100011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "16091536665481910943744000",
      "max_numerator": "47069920437531136386662400"
    },
    {
      "path": "100100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14551930235327893576089600",
      "max_numerator": "39128299713551310943027200"
    },
    {
      "path": "100101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14607011060210485690368000",
      "max_numerator": "39213523044133625344819200"
    },
    {
      "path": "100110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14662091885093077804646400",
      "max_numerator": "39312037863939039785779200"
    },
    {
      "path": "100111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14717172709975669918924800",
      "max_numerator": "39424219472586193502208000"
    },
    {
      "path": "101000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14542397015636675710156800",
      "max_numerator": "40979541179213779933593600"
    },
    {
      "path": "101001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14598073666749968941056000",
      "max_numerator": "40984303591423307415552000"
    },
    {
      "path": "101010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14653750317863262171955200",
      "max_numerator": "40996844478175190728704000"
    },
    {
      "path": "101011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "14709426968976555402854400",
      "max_numerator": "41016494145552500391936000"
    },
    {
      "path": "101100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "15966577205990812916121600",
      "max_numerator": "51114575359993880091033600"
    },
    {
      "path": "101101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "15967768828296596501299200",
      "max_numerator": "51024790072340124794880000"
    },
    {
      "path": "101110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "15973452334698081760051200",
      "max_numerator": "50936276784465380062003200"
    },
    {
      "path": "101111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "15984257211870925239091200",
      "max_numerator": "50851148103495840694272000"
    },
    {
      "path": "110000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "39055995326566489915392000",
      "max_numerator": "131430792519607466223206400"
    },
    {
      "path": "110001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "39128299713551310943027200",
      "max_numerator": "131224593456727359435571200"
    },
    {
      "path": "110010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "39213523044133625344819200",
      "max_numerator": "131074326562996601487360000"
    },
    {
      "path": "110011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "39312037863939039785779200",
      "max_numerator": "130985932281212130086092800"
    },
    {
      "path": "110100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "36927532092523612943155200",
      "max_numerator": "109106090684462186417356800"
    },
    {
      "path": "110101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37055162265738169181798400",
      "max_numerator": "109284607366806156764774400"
    },
    {
      "path": "110110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37183208386840340987904000",
      "max_numerator": "109484797318355411691110400"
    },
    {
      "path": "110111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37311670455830128361472000",
      "max_numerator": "109707128540755868516352000"
    },
    {
      "path": "111000",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37073210088933843114393600",
      "max_numerator": "109106090684462186417356800"
    },
    {
      "path": "111001",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37188204551459158622208000",
      "max_numerator": "109284607366806156764774400"
    },
    {
      "path": "111010",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37303199013984474130022400",
      "max_numerator": "109484797318355411691110400"
    },
    {
      "path": "111011",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "37418193476509789637836800",
      "max_numerator": "109707128540755868516352000"
    },
    {
      "path": "111100",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "40977999676974510676377600",
      "max_numerator": "131430792519607466223206400"
    },
    {
      "path": "111101",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "40978619051653082333184000",
      "max_numerator": "131224593456727359435571200"
    },
    {
      "path": "111110",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "40984303591423307415552000",
      "max_numerator": "131074326562996601487360000"
    },
    {
      "path": "111111",
      "nonnegative": true,
      "positive_count": 405,
      "zero_count": 0,
      "negative_count": 0,
      "min_numerator": "40996844478175190728704000",
      "max_numerator": "130985932281212130086092800"
    }
  ],
  "mixed_numerator": {
    "8,4,0": "-6",
    "6,4,0": "132",
    "4,4,0": "-228",
    "2,4,0": "132",
    "0,4,0": "-6",
    "8,2,0": "36",
    "6,2,0": "-1080",
    "4,2,0": "2232",
    "2,2,0": "-1080",
    "0,2,0": "36",
    "8,0,0": "-6",
    "6,0,0": "132",
    "4,0,0": "-228",
    "2,0,0": "132",
    "0,0,0": "-6",
    "5,3,0": "-960",
    "7,3,0": "192",
    "3,3,0": "960",
    "1,3,0": "-192",
    "5,1,0": "960",
    "7,1,0": "-192",
    "3,1,0": "-960",
    "1,1,0": "192",
    "6,6,1": "12",
    "4,6,1": "-12",
    "2,6,1": "12",
    "6,4,1": "-492",
    "4,4,1": "840",
    "2,4,1": "-492",
    "6,2,1": "492",
    "4,2,1": "-840",
    "2,2,1": "492",
    "6,0,1": "-12",
    "4,0,1": "12",
    "2,0,1": "-12",
    "5,5,1": "-240",
    "7,5,1": "48",
    "3,5,1": "240",
    "1,5,1": "-48",
    "5,3,1": "1488",
    "7,3,1": "-240",
    "3,3,1": "-1488",
    "1,3,1": "240",
    "5,1,1": "-240",
    "7,1,1": "48",
    "3,1,1": "240",
    "1,1,1": "-48",
    "8,4,1": "6",
    "0,4,1": "6",
    "8,2,1": "-6",
    "0,2,1": "-6",
    "6,6,2": "-84",
    "4,6,2": "120",
    "2,6,2": "-84",
    "6,4,2": "360",
    "4,4,2": "-624",
    "2,4,2": "360",
    "6,2,2": "-84",
    "4,2,2": "120",
    "2,2,2": "-84",
    "7,5,2": "-48",
    "5,5,2": "336",
    "3,5,2": "-336",
    "1,5,2": "48",
    "7,3,2": "48",
    "5,3,2": "-336",
    "3,3,2": "336",
    "1,3,2": "-48",
    "6,6,3": "72",
    "4,6,3": "-144",
    "2,6,3": "72",
    "6,4,3": "-72",
    "4,4,3": "144",
    "2,4,3": "-72"
  }
}
```
