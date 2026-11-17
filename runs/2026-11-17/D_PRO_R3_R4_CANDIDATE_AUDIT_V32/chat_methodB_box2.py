"""chat V32 diagnostic (width only, no sign use): Method B = direct middle-chart W on R3 box 2.
Calls R3 internals read-only; route forced to the existing 'middle' formula (mode W, mean-value form, cap once)."""
import sys, time, json
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q, ctx
from prolate_r1 import api, Config
from prolate_r1.intervals import bounds
cfg = Config()
B = ((Q(95,128), Q(97,128)), (Q(15,128), Q(17,128)), (Q(1279,256), Q(5)))
out = {}
with ctx.workprec(cfg.precision):
    R, T, L = B
    t = time.monotonic()
    dom = api.domain_for(R, L, cfg); mesh = api.make_mesh(R, dom.kappa, cfg, lam=L)
    pt, corr = api.mv_integral((R, T, L), dom, mesh, "W", cfg)
    cap = api.W_cap(R, dom.kappa)
    tot = pt[0]+corr[0]+cap
    for k, x in (("point_at_box_centre", pt[0]), ("mean_value_correction", corr[0]), ("cap", cap), ("box_W", tot)):
        print(k, x.str(12), flush=True); lo, hi = bounds(x); fl = lambda r: int(r.p)/int(r.q); out[k] = {"lo": fl(lo), "hi": fl(hi), "half_width": fl((hi-lo)/2), "ball": x.str(15)}
    out["cells"] = len(mesh); out["seconds"] = time.monotonic()-t
print(json.dumps(out, indent=1))
