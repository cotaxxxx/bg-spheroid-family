"""Amendment A2 (fixed before run). The only unconfirmed piece of V52A is k000:b0 (E_z > 0 on t in [1/16, 3/32],
lambda in [9/20, 361/800]; worst lower -2.2e-4 after depth 5), where E_z itself is small (about 0.007).
Alternative route, logically equivalent for the claim: E_z(0,0) = 0 and E_zz(0,t) > 0 on [0, 3/32] imply
E_z(0,t) > 0 on (0, 3/32]. [0, 1/16] is already confirmed (k000:a); this run checks E_zz > 0 on [1/16, 3/32]."""
import json
from fractions import Fraction as F
import importlib.util, sys
spec = importlib.util.spec_from_file_location("A", "plans/V52A_axis_amendment.py"); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
r = A.cover(("k000:b0_alt_Ezz", 'ezz', F(9, 20), F(361, 800), F(1, 16), F(3, 32), +1))
print(json.dumps(r)); open(sys.argv[1], 'w').write(json.dumps(r) + "\n")
