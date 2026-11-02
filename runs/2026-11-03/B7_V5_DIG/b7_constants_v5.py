"""B7 V5: exact rational floor constant from the Astra E3/SOS lemma.

The proved uniform inequality is F >= -275/4 on the full target domain.
This module leaves the contact-strip width and geometric grid unchanged.
"""
from fractions import Fraction as Q
KQ = Q(275, 4)
P0 = Q(5, 10**7)
SIGMA0 = 2*P0/(1+P0**2)
assert KQ == Q(275,4)
assert KQ*Q(3125,16) == Q(859375,64)
assert P0 == Q(1,2000000)
