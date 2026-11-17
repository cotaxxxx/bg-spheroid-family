"""chat V35 diagnostic (pointwise, not an enclosure): with Dig's own majorant() (outer degree 4, box 2),
what is the pointwise tail B4 at the 5x5x5 preflight points and on a finer 9x9x9 grid, and what integrated tail
would a 'convergence (A<1) + tail budget' rule face, instead of the fixed A<=1/8 threshold?"""
import sys, itertools
sys.path.insert(0, sys.argv[1])
from flint import ctx, fmpq as Q
from majorant import majorant
ctx.prec = 128
def run(n):
    hs = [Q(-1) + Q(2*i, n-1) for i in range(n)]; vs = [Q(i, n-1) for i in range(n)]
    tw = lambda m: [Q(1, 2*(m-1)) if i in (0, m-1) else Q(1, m-1) for i in range(m)]   # trapezoid on [0,1]
    wh = [2*x for x in tw(n)]; wv = tw(n)
    est = Q(0); amax = Q(0); tmax = Q(0); worst = None; cnt = 0
    for (i, h), (j, v), (k, w) in itertools.product(enumerate(hs), enumerate(vs), enumerate(vs)):
        m = majorant(((h, h), (v, v), (w, w)))
        if not m['convergent']: print("NONCONVERGENT", h, v, w); continue
        t = m['tail_upper']; est += Q(1, 2)*wh[i]*wv[j]*wv[k]*t
        if m['A'] > Q(1, 8): cnt += 1
        if t > tmax: tmax, worst = t, (str(h), str(v), str(w), int(m["A"].p)/int(m["A"].q))
        amax = max(amax, m['A'])
    print(f"grid {n}^3: A>1/8 at {cnt}, max A {int(amax.p)/int(amax.q):.4f}, max pointwise tail {int(tmax.p)/int(tmax.q):.5f} at {worst}, trapezoid-integrated tail {int(est.p)/int(est.q):.5f}", flush=True)
run(5); run(9)
