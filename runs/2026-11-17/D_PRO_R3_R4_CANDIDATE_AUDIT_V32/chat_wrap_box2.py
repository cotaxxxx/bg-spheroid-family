"""chat V32 diagnostic: where does the box-2 derivative enclosure d/dx of the W integrand come from?
Compares (i) L1 and signed sums of the pointwise derivative at cell midpoints and the box centre,
(ii) width with parameters as balls but (u,v) at midpoints, (iii) parameters at the centre but (u,v) as cell balls."""
import sys, json
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q, arb, ctx
from prolate_r1 import api, Config
from prolate_r1.intervals import ball, midpoint, mag
from prolate_r1.density import evaluate
cfg = Config()
B = ((Q(95,128), Q(97,128)), (Q(15,128), Q(17,128)), (Q(1279,256), Q(5)))
with ctx.workprec(cfg.precision):
    R, T, L = B
    dom = api.domain_for(R, L, cfg); mesh = api.make_mesh(R, dom.kappa, cfg, lam=L)
    PB = tuple(ball(x) for x in B); p0 = tuple(arb(midpoint(x)) for x in B)
    for name in ("x", "R"):
        l1 = arb(0); signed = arb(0); wpar = arb(0); wcell = arb(0); wboth = arb(0); maxmid = arb(0)
        for c in mesh:
            area = arb((c.u[1]-c.u[0])*(c.v[1]-c.v[0]))
            um, vm = arb(midpoint(c.u)), arb(midpoint(c.v)); ub, vb = ball(c.u), ball(c.v)
            d = lambda u, v, P: evaluate(u, v, P, dom, (name,), (1,), "W")[0].coeff(1)
            m = d(um, vm, p0); signed += m*area; l1 += abs(m.mid())*area
            maxmid = max(maxmid, abs(m.mid()))
            wpar += d(um, vm, PB).rad()*area; wcell += d(ub, vb, p0).rad()*area; wboth += d(ub, vb, PB).rad()*area
        r = {"signed_midpoint_sum": signed.str(6), "L1_pointwise": l1.str(6), "max_pointwise": maxmid.str(6),
             "width_from_parameter_balls": wpar.str(6), "width_from_cell_balls": wcell.str(6), "width_both": wboth.str(6)}
        print(name, json.dumps(r), flush=True)
