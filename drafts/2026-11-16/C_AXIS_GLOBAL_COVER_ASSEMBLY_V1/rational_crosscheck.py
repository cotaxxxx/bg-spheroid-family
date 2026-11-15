#!/usr/bin/env python3
"""C-axis v1 rational bookkeeping preflight. NOT mathematical evidence."""
from fractions import Fraction as F

l0,l1,l2,l3,l4=F(2,5),F(83,200),F(9,20),F(5,8),F(33,50)
xlo,xhi,rx=F(699,1600),F(281,640),F(703,1600)
qmin=l1*l1/4
umax=(1-l1*l1/2)**2
critical=F(1,2)*l2*l2/(1-l2*l2)
assert (qmin,umax,critical)==(
    F(6889,160000),F(5345218321,6400000000),F(81,638))
assert l0<l1<xlo<xhi<rx<l2<l3<l4
assert qmin>=F(1,25)
assert umax<=F(529,625) and umax<1
assert critical<F(25,78) and critical<1
assert 48+78+34==160
assert (F(83,200)-F(2,5))*3200==48
assert (F(703,1600)-F(83,200))*3200==78
assert (F(9,20)-F(703,1600))*3200==34
assert 159==35+124
assert 124==106+18
print("A1_EXACT_RATIONAL_REPLACEMENTS_PASS: qmin",qmin,"umax",umax,"critical",critical)
print("LAMBDA_ORDER_AND_160_TILE_COUNTS_PASS")
print("C1B_PARENT_ARITHMETIC_PASS: 159=35+124, 124=106+18")
print("NOT_EVIDENCE: DOES_NOT_PROVE_SIGNS_ROOT_COUNTS_OR_GLOBAL_CLOSED")
