"""chat V32 diagnostic (width only, no sign use): box 2, middle-chart W.
(a) R3 first-order mean-value correction split by parameter;
(b) second-order form: I(P) in I(p0) + grad I(p0).s + 1/2 s^T H(P) s, with grad I(p0) by the 6th-order Taylor quadrature
    at the centre and the Hessian enclosed over the whole box (cell ranges). Uses R3 internals read-only."""
import sys, time, json
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q, arb, ctx
from prolate_r1 import api, Config
from prolate_r1.intervals import bounds, ball, midpoint, radius, sym, hull
from prolate_r1.jets import Jet
from prolate_r1.density import evaluate
from prolate_r1.quadrature import integrate
cfg = Config()
B = ((Q(95,128), Q(97,128)), (Q(15,128), Q(17,128)), (Q(1279,256), Q(5)))
names = ("R", "x", "lam")
def hw(x): lo, hi = bounds(x); return float(int(((hi-lo)/2).p))/int(((hi-lo)/2).q)
out = {}
with ctx.workprec(cfg.precision):
    R, T, L = B
    T0 = time.monotonic()
    dom = api.domain_for(R, L, cfg); mesh = api.make_mesh(R, dom.kappa, cfg, lam=L)
    p0 = tuple(arb(midpoint(x)) for x in B); PB = tuple(ball(x) for x in B); h = [radius(x) for x in B]
    pt = integrate(api.cb_for(p0, dom, "W"), mesh, cfg.order)[0]
    out["point"] = pt.str(12); print("point", pt.str(12), flush=True)
    first = {}
    for i, n in enumerate(names):
        d = api.deriv_integral(PB, dom, mesh, "W", (n,), (1,))[0]
        first[n] = {"dI_over_box": d.str(8), "correction_half_width": hw(d*sym(h[i]))}
        print("first-order", n, first[n], flush=True)
    out["first_order"] = first
    grad = {}
    for i, n in enumerate(names):
        def cb(u, v, a, k, n=n):
            j = evaluate(u, v, p0, dom, (a, n), (k, 1), "W")[0]
            return (Jet((k,), [j.coeff(m, 1) for m in range(k+1)]),)
        g = integrate(cb, mesh, cfg.order)[0]; grad[n] = g
        print("grad at p0", n, g.str(10), flush=True)
    out["grad_at_p0"] = {n: g.str(10) for n, g in grad.items()}
    H = {}
    for i in range(3):
        for j in range(i, 3):
            nm = (names[i],) if i == j else (names[i], names[j]); od = (2,) if i == j else (1, 1)
            H[(i, j)] = api.deriv_integral(PB, dom, mesh, "W", nm, od)[0]
            print("Hessian", names[i], names[j], H[(i, j)].str(8), flush=True)
    out["hessian_over_box"] = {f"{names[i]},{names[j]}": v.str(8) for (i, j), v in H.items()}
    lin = sum((grad[n]*sym(h[i]) for i, n in enumerate(names)), arb(0))
    quad = arb(0)
    for (i, j), v in H.items():
        quad += (v*hull(Q(0), h[i]**2)/2) if i == j else (v*sym(h[i]*h[j]))
    tot = pt + lin + quad
    out.update({"linear_term": lin.str(8), "quadratic_term": quad.str(8), "box_W_second_order": tot.str(10),
                "box_half_width_second_order": hw(tot), "cells": len(mesh), "seconds": time.monotonic()-T0})
print(json.dumps(out, indent=1))
