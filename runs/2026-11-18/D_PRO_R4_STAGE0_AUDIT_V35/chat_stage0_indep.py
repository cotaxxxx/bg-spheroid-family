"""chat V35: independent check of Dig stage-0 coefficient integrals (constant + 3 first-order) on the stage-0 cell.
Kernel = chat's V33 transcription of Astra (C4)-(C7) (checked there against primitive geometry, 1e-40), written in (R,t,q).
Integral of K * (1/2) dh dv dw over h in [0,1/8], v in [1/4,3/8], w in [1/4,3/8], theta = pi v/2; tensor Gauss-Legendre 10/14 nodes."""
import sys, json, mpmath as mp
from fractions import Fraction as Fr
mp.mp.dps = 30
def K(R, t, q, h, v, w):
    th = mp.pi*v/2; vz2 = (1-h*h)*mp.cos(th)**2; y2 = (1-h*h)*mp.sin(th)**2; d = 1-q
    Sig = (1-R)**2 + 2*R*(1-h); k = 1-R*h
    def polys(t):
        Uc = (1-t)*vz2 + t*(h-R)**2; Vc = (1-t)*vz2 - t*(h-R)**2
        Bs = q + d*y2; Ub = (1-t)*h*h + t*vz2; Vb = (1-t)*h*h - t*vz2
        p = Bs*(q*Sig + d*Uc) + q*Sig*d*Ub + d*d*(t*(1-t)*(h*(h-R)-vz2)**2 + vz2*((1-t)*h - t*(h-R))**2)
        c = q*q*Sig*Sig + 2*q*d*Sig*Uc + d*d*Vc**2; b = Bs**2 + 2*Bs*d*Ub + d*d*Vb**2
        return p, c*b
    p, dl = polys(t); pt = mp.diff(lambda x: polys(x)[0], t); dlt = mp.diff(lambda x: polys(x)[1], t)
    a = k*k*(1-w*w); s = q*q*a*a + 2*q*a*w*w*p + w**4*dl
    n = q*a*dlt/2 + w*w*(p*dlt - dl*pt); U = 2*q*k**3*n
    return U/(R*R*dl*s)
def cell_int(R, t, q, n):
    xs, ws = zip(*[(x, wt) for x, wt in zip(*mp.gauss_legendre_nodes(n))]) if hasattr(mp, 'gauss_legendre_nodes') else (None, None)
    return None
def gl(n):
    import mpmath
    x = []; wts = []
    for i in range(1, n+1):
        r = mp.cos(mp.pi*(i-mp.mpf(1)/4)/(n+mp.mpf(1)/2))
        for _ in range(50):
            p0, p1 = mp.mpf(1), r
            for k in range(2, n+1): p0, p1 = p1, ((2*k-1)*r*p1-(k-1)*p0)/k
            dp = n*(r*p1-p0)/(r*r-1); r -= p1/dp
        x.append(r); wts.append(2/((1-r*r)*dp*dp))
    return x, wts
def integ(R, t, q, n):
    x, wt = gl(n); s = mp.mpf(0)
    H = (mp.mpf(0), mp.mpf(1)/8); V = (mp.mpf(1)/4, mp.mpf(3)/8); Wr = (mp.mpf(1)/4, mp.mpf(3)/8)
    m = lambda I, xi: (I[0]+I[1])/2 + (I[1]-I[0])/2*xi
    for i in range(n):
        for j in range(n):
            for l in range(n):
                s += wt[i]*wt[j]*wt[l]*K(R, t, q, m(H, x[i]), m(V, x[j]), m(Wr, x[l]))
    return s*(H[1]-H[0])*(V[1]-V[0])*(Wr[1]-Wr[0])/8/2
fr = lambda s: mp.mpf(Fr(s).numerator)/Fr(s).denominator
st = json.load(open(sys.argv[1])); C = [fr(x) for x in st["outer_center"]]; RAD = [fr(x) for x in st["outer_radii"]]
coef = {tuple(c["alpha"]): (fr(c["integral"][0]), fr(c["integral"][1])) for c in st["coefficients"]}
n = int(sys.argv[2]); ok = True
I0 = integ(*C, n); lo, hi = coef[(0, 0, 0)]; r = lo <= I0 <= hi; ok &= r
print(f"alpha=(0,0,0): chat {mp.nstr(I0,15)}  Dig [{mp.nstr(lo,15)}, {mp.nstr(hi,15)}]  {'IN' if r else 'OUT'}", flush=True)
hh = mp.mpf(10)**-6
for i in range(3):
    e = [0, 0, 0]; e[i] = 1; a = tuple(e)
    Cp = list(C); Cm = list(C); Cp[i] += hh; Cm[i] -= hh
    d = (integ(*Cp, n) - integ(*Cm, n))/(2*hh)*RAD[i]; lo, hi = coef[a]; r = lo - mp.mpf(10)**-12 <= d <= hi + mp.mpf(10)**-12; ok &= r
    print(f"alpha={a}: chat {mp.nstr(d,12)}  Dig [{mp.nstr(lo,12)}, {mp.nstr(hi,12)}]  {'IN' if r else 'OUT'}", flush=True)
print("SUMMARY", "PASS" if ok else "FAIL")
