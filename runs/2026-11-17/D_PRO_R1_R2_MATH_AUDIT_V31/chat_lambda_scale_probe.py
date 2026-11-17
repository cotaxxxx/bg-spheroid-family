"""chat V31 diagnosis: does the width blow-up with lambda come from the cell rule using sigma instead of sigma/lambda?"""
import sys, time
sys.path.insert(0, sys.argv[1])
from dataclasses import replace
from flint import fmpq as Q
from prolate_r1 import api, Config
for dr in (Q(1, 2), Q(1, 5), Q(1, 10)):
    cfg = replace(Config(), order=6, base_u=32, base_v=64, distance_ratio=dr, max_cells=400000)
    t = time.time()
    r = api.angular_raw(Q(1, 2), Q(1, 2), Q(5), angle_kind="tau", config=cfg)
    print("lam=5 ratio", dr, "cells", r.cells, "E/Eb/Ebb", [x.str(6) for x in r.balls], round(time.time()-t, 1), "s", flush=True)
