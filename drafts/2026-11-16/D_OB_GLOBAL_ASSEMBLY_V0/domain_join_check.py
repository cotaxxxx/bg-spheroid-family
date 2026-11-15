"""Bookkeeping-only exact-rational C/D domain join, NOT proof evidence."""
from fractions import Fraction as F

I=(F(2,5),F(33,50))
lam_c=(F(2,5),F(83,200))
lam_x=(F(83,200),F(9,20))
lam_boundary=(F(5,8),F(33,50))
assert I[0]<lam_c[1]<lam_x[1]<lam_boundary[0]<lam_boundary[1]
regions=[
 ("center",F(0),F(1,8)),
 ("general",F(1,8),F(15,16)),
 ("plan_b",F(15,16),F(1)-F(1,65536)),
 ("thin_collar",F(59999,60000),F(1)),
 ("outer_face",F(1),F(1))
]
for i,x in enumerate(regions):
 assert x[1]<=x[2], x
 if i: assert regions[i-1][2]>=x[1],(regions[i-1],x)
assert regions[0][1]==0 and regions[-1][2]==1
assert F(59999,60000)<F(1)-F(1,65536)
assert F(48+78+34)==F(160)
assert F(159)==F(124+35)
assert [1+2*n for n in (0,1,0)]==[1,3,1]
print("D_OB_RATIONAL_CLOSED_R_COVER_PASS")
print("D_OB_PLAN_B_COLLAR_OVERLAP_PASS")
print("C_AXIS_TO_INTERIOR_STATIONARY_BOOKKEEPING_1_3_1_PASS")
print("NOT_EVIDENCE; C/D MATH GLUE REQUIRES CHAT AUDIT; GLOBAL_OPEN")
