"""Exact polynomial algebra and analytic beta-series bounds; no parameter sampling."""
from fractions import Fraction as F
from math import comb,ceil
import json
from pathlib import Path
NVAR=6 # x,z,b,mu,lambda,q; Laurent exponents allowed
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
x,z,b,mu,lam,q=map(var,range(6))
ell=b*x+lam*mu*z;k=b*x+mu*z*lam**-1;v=x*x+z*z
d1=ell*q**-1-k
d2=-v*q**-1/2+3*ell**2*q**-2/2-k*ell*q**-1
d3=-3*ell*v*q**-2/2+5*ell**3*q**-3/2+k*v*q**-1/2-3*k*ell**2*q**-2/2
d4=3*v**2*q**-2/8-15*ell**2*v*q**-3/4+35*ell**4*q**-4/8+3*k*ell*v*q**-2/2-5*k*ell**3*q**-3/2
Ts=[d4-k*d3,d1*d3+d2**2/2-k*d1*d2,d1**2*d2/2-k*d1**3/6,d1**4/24]
# Convert phi-averaged coefficient to numerator P(c,y)/(lambda^s q^4).
def numerator(t,nx,nz,s):
 out={}
 for (ix,iz,ib,im,il,iq),v in t.items():
  if (ix,iz)!=(nx,nz) or ib%2:continue
  assert ib in (0,2,4) and im%2==0 and (il+s)%2==0
  L=(il+s)//2;Q=iq+4;B=ib//2
  assert L>=0 and Q>=0
  moment={0:F(1),2:F(1,2),4:F(3,8)}[ib]
  for a in range(L+1):
   for h in range(Q+1):
    for j in range(B+1):
     key=(a+h,im//2+h+j)
     val=v*moment*comb(L,a)*comb(Q,h)*comb(B,j)*(-1)**(a+h+j)
     out[key]=out.get(key,F(0))+val
 return {k:v for k,v in out.items() if v}
CLO=1-F(33,50)**2;CHI=1-F(119,200)**2
def bernstein(poly):
 # c=CLO+(CHI-CLO)t, then power -> tensor Bernstein on (t,y) in [0,1]^2.
 nc=max(k[0] for k in poly);ny=max(k[1] for k in poly)
 powers={}
 for (i,j),v in poly.items():
  for a in range(i+1):powers[a,j]=powers.get((a,j),F(0))+v*comb(i,a)*CLO**(i-a)*(CHI-CLO)**a
 rows=[]
 for k in range(ny+1):
  vals=[]
  for h in range(nc+1):
   vals.append(sum(v*F(comb(h,a),comb(nc,a))*F(comb(k,j),comb(ny,j)) for (a,j),v in powers.items() if a<=h and j<=k))
  rows.append(max(map(abs,vals)))
 return ny,rows
def beta_half(k,m):
 # Integral mu=-1..1 of mu^(2k)*(1-mu^2)^m, exact positive product.
 out=F(2,2*k+1)
 for j in range(1,m+1):out*=F(2*j,2*k+2*j+1)
 return out
def integral_upper(n,k,N=64):
 # Integral B_{k,n}(mu^2)/(1-2mu^2/3)^4.
 r=F(2,3)
 total=sum(F(comb(i+3,3))*r**i*beta_half(i+k,n-k) for i in range(N))
 ratio=r*F(N+4,N+1)
 tail=F(comb(N+3,3))*r**N*beta_half(N+k,n-k)/(1-ratio)
 return comb(n,k)*(total+tail)
R=[F(16,15),F(256,675),F(32,15)*F(8,15)**3,F(192,35)*F(8,15)**4]
result={'method':'exact tensor Bernstein numerator majorant + analytic beta-series, N=64; no sampling','gamma_lower':'7/8','R_bounds':[str(v) for v in R],'bounds':{}}
for name,nx,nz,s,factor in [('E40',4,0,0,24),('E22',2,2,2,4)]:
 terms=[];ub=F(0)
 for j,t in enumerate(Ts):
  p=numerator(t,nx,nz,s);n,bs=bernstein(p)
  integ=sum(v*integral_upper(n,k) for k,v in enumerate(bs))
  ub+=factor*R[j]*integ/F(119,200)**s
  terms.append({'j':j,'numerator':{f'{a},{b}':str(v) for (a,b),v in sorted(p.items())},'degree_y':n,'bernstein_abs_c_envelope':[str(v) for v in bs],'integral_upper':str(integ)})
 result['bounds'][name]={'integer_upper':ceil(ub),'exact_upper':str(ub),'terms':terms}
 assert ub < {'E40':23,'E22':18}[name]
 print(name,'absolute integer upper',ceil(ub))
 # Exact spherical specialization of the polynomial kernels (normalization check).
 sphere=F(0)
 for term in terms:
  integ=sum(F(v)*F(2,2*int(key.split(',')[1])+1) for key,v in term['numerator'].items() if key.split(',')[0]=='0')
  sphere-=factor*[F(1),F(-1,3),F(4,15),F(-12,35)][term['j']]*integ
 assert sphere == {'E40':F(-16,3),'E22':F(-16,9)}[name]
 result['bounds'][name]['sphere_specialization']=str(sphere)
assert 2*F(119,200)/(1+F(119,200)**2)>F(7,8)
Path('d4_center_rational_bounds_result.json').write_text(json.dumps(result,indent=2)+'\n')
