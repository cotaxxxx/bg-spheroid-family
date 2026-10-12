from gap1_producer import global_axial_c1b_kernel as k
from fractions import Fraction
import json,sys
k.ctx.prec=k.BITS;k.base.ctx.prec=k.BITS
q,ok=k.gap1_coarse_slabs();assert ok
s=q[125];assert (s.ll,s.lr)==(Fraction(281,640),Fraction(703,1600))
print('X_DIAGNOSTIC_NOT_EVIDENCE',s,flush=True)
r=k.attempt_x(s)
print('X_DIAGNOSTIC_RESULT',r[0],'reason',r[-1],'work',r[-2],flush=True)
print('X_DIAGNOSTIC_STAGE',r[1].get('x_lower_tube_stage'),flush=True)
print('X_DIAGNOSTIC_GUARDS',len(r[1].get('x_lower_tube_guards',[])),len(r[1].get('exterior_guards',[])),flush=True)
if not r[0]:sys.exit(3)
