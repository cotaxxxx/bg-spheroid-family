"""chat V32 diagnostic (width only): do the box-level derivative enclosures of the W integrand shrink when the
integrand is first averaged over the reflection pair eta_z -> -eta_z (v -> 1-v)?  Valid: the full v-range [0,1]
is symmetric, so the pointwise average has the same integral for every parameter value. R3 internals read-only."""
import sys, time, json
sys.path.insert(0, sys.argv[1])
from math import factorial
from flint import fmpq as Q, arb, ctx
from prolate_r1 import api, Config
from prolate_r1.intervals import bounds, ball, midpoint, radius, sym
from prolate_r1.density import evaluate
from prolate_r1.quadrature import range_integral
cfg = Config()
B = ((Q(95,128), Q(97,128)), (Q(15,128), Q(17,128)), (Q(1279,256), Q(5)))
out = {}
with ctx.workprec(cfg.precision):
    R, T, L = B
    dom = api.domain_for(R, L, cfg); mesh = api.make_mesh(R, dom.kappa, cfg, lam=L)
    PB = tuple(ball(x) for x in B)
    for names, orders in ((("x",), (1,)), (("R",), (1,)), (("x",), (2,)), (("R", "x"), (1, 1)), (("R",), (2,))):
        fac = 1
        for n in orders: fac *= factorial(n)
        def cb(u, v):
            a = evaluate(u, v, PB, dom, names, orders, "W")[0].coeff(*orders)
            b = evaluate(u, 1-v, PB, dom, names, orders, "W")[0].coeff(*orders)
            return ((a+b)*fac/2,)
        t = time.monotonic(); d = range_integral(cb, mesh)[0]
        key = ",".join(f"{n}^{o}" for n, o in zip(names, orders))
        out[key] = {"reflected_enclosure": d.str(8), "seconds": round(time.monotonic()-t, 1)}
        print(key, out[key], flush=True)
print(json.dumps(out, indent=1))
