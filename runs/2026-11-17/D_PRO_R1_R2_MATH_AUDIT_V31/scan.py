import sys, time
sys.path.insert(0, sys.argv[1])
from dataclasses import replace
from flint import fmpq as Q
from prolate_r1 import api, Config
for order, bu, bv, dr in [(4,8,16,Q(1)),(4,16,32,Q(1)),(6,16,32,Q(1)),(6,16,32,Q(1,2)),(6,32,64,Q(1,2)),(6,32,64,Q(1,4))]:
    cfg = replace(Config(), order=order, base_u=bu, base_v=bv, distance_ratio=dr)
    t = time.time()
    r = api.angular_raw(Q(1,2), Q(1,2), Q(3), angle_kind="tau", config=cfg)
    t1 = time.time()-t; t = time.time()
    w = api.angular_quotient(Q(1,2), Q(1,2), Q(3), angle_kind="tau", config=cfg)
    print(order, bu, bv, dr, r.cells, [x.str(8) for x in r.balls], "W", w.enclosure.str(8), round(t1,1), round(time.time()-t,1), flush=True)
