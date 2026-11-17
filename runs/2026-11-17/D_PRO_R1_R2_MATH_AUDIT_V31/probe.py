import sys, time
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q
from prolate_r1 import api
for f, args in [(api.angular_raw, (Q(1,2), Q(1,2), Q(3))), (api.angular_quotient, (Q(1,2), Q(1,2), Q(3))),
                (api.axis_g, (Q(1,2), Q(3))), (api.equatorial_phi_s, (Q(1,4), Q(3)))]:
    t = time.time()
    kw = {"angle_kind": "tau"} if f in (api.angular_raw, api.angular_quotient) else {}
    r = f(*args, **kw)
    print(f.__name__, r.route, r.cells, [x.str(10) for x in r.balls], round(time.time()-t, 2))
