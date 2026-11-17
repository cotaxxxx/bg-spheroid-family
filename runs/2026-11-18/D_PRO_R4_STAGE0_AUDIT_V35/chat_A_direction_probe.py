"""chat V35 diagnostic: which outer direction (R, t, q) drives A_j(1) and the pointwise tail at the worst points?
Monkeypatches the outer radii seen by Dig's majorant() (read-only use of their code)."""
import sys
sys.path.insert(0, sys.argv[1])
from flint import ctx, fmpq as Q
import majorant as M
ctx.prec = 128
full = M.RAD
f = lambda x: int(x.p)/int(x.q)
for pt in ((Q(1), Q(0), Q(1)), (Q(1), Q(1, 2), Q(1, 2)), (Q(-1), Q(0), Q(0)), (Q(0), Q(1, 2), Q(1, 2))):
    row = []
    for name, rad in (("all", full), ("R", (full[0], Q(0), Q(0))), ("t", (Q(0), full[1], Q(0))), ("q", (Q(0), Q(0), full[2])),
                      ("all/2", tuple(r/2 for r in full)), ("all/3", tuple(r/3 for r in full))):
        M.RAD = rad
        m = M.majorant(((pt[0], pt[0]), (pt[1], pt[1]), (pt[2], pt[2])))
        row.append(f"{name}: A={f(m['A']):.4f} tail={f(m['tail_upper']) if m['tail_upper'] is not None else float('nan'):.2e}")
    print("point (h,v,w)=", tuple(str(x) for x in pt), " | ".join(row), flush=True)
