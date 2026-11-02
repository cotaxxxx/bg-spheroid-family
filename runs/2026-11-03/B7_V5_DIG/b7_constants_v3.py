"""V6-B7 V3 single-source exact rational constants. Theorem: Qhat >= -4.
Do not change without new source hash, fingerprint, and independent audit.
"""
from fractions import Fraction as Q

KQ = Q(859375, 64)
P0 = Q(5, 10**7)
SIGMA0 = 2*P0/(1+P0**2)

assert KQ == (2*Q(11, 10)*4)/Q(2, 5)**8
assert P0 > 0 and P0 < 1
assert SIGMA0 == 2*P0/(1+P0**2)