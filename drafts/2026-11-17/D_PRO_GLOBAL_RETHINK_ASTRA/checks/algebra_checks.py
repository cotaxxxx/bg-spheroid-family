#!/usr/bin/env python3
"""EXACT_ALGEBRA / NOT_CERTIFICATE. Checks identities, not global signs."""
from fractions import Fraction as F
import json
from pathlib import Path
import sympy as s

x,z,X,Z,d,e=s.symbols('x z X Z d e', real=True)
C=1+d*z*z; B=1-e*Z*Z
T=d*x*z/C-e*X*Z/B
rot=lambda f:-z*s.diff(f,x)+x*s.diff(f,z)-Z*s.diff(f,X)+X*s.diff(f,Z)
Tp=d*(x*x-z*z)/C-2*(d*x*z/C)**2-e*(X*X-Z*Z)/B-2*(e*X*Z/B)**2
assert s.factor(rot(T)-Tp)==0

t,ll=s.symbols('t ll', real=True)
assert s.expand((1+(ll**2-1)*t**2)**2-4*ll**2*t**2*(1-t**2)-(1-(ll**2+1)*t**2)**2)==0
assert s.expand((1-e*t**2)**2-4*(1-e)*t**2*(1-t**2)-(1-(2-e)*t**2)**2)==0

a,b=s.Rational(3,5),s.Rational(4,5)
val=T.subs({x:-a,z:-b,X:-a,Z:-b,d:3,e:s.Rational(3,4)})
assert val==-s.Rational(189,949)
cap=F(301056,1125)*(F(1,65536)+F(1,33554432))
assert cap<F(1,240)

mu,lam,t=s.symbols('mu lam t', real=True)
D2=1-mu*mu+lam*lam*(mu-t)**2
assert s.expand(lam*lam*(1-t*mu)*(mu-t)-mu*D2-(1-mu*mu)*((lam*lam-1)*mu-lam*lam*t))==0

out={'classification':'EXACT_ALGEBRA / NOT_CERTIFICATE','rotation_T_derivative':True,'two_square_identities':True,'negative_density_example':True,'rational_cap_bound':True,'axial_e_identity':True}
Path(__file__).with_name('ALGEBRA_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
