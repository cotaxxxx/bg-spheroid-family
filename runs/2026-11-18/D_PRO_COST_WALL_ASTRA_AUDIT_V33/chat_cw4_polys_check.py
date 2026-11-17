"""chat V33: does the CW4/CW5 code's polys() (the polynomials actually used for the 0.0201 / 0.00445 numbers)
equal the report's (C4)-(C7) and chat's primitive geometry?  Float sampling, scalar inputs."""
import sys, random, math
src = open(sys.argv[1]).read()
ns = {}; exec(src[:src.index("def inverse_majorant")], ns)       # numpy interval helpers + polys (no execution of run())
polys = ns["polys"]
import mpmath as mp
gsrc = open(sys.argv[2]).read(); g = {}; exec(gsrc[:gsrc.index("# 1) pointwise kernel identity")], g)
F, PD = g["F"], g["PD"]
random.seed(7); worst = 0.0
for _ in range(40):
    lam = random.uniform(2, 5); R = random.uniform(0.1, 0.95); t = random.uniform(0.02, 0.98)
    while True:
        x = [random.gauss(0, 1) for _ in range(3)]; n = math.sqrt(sum(c*c for c in x))
        if n > .1: break
    h, ey, v = [c/n for c in x]; q = 1/lam**2; w = random.uniform(0, 1)
    U, D, S = polys(R, t, q, h, v*v, w)
    Kc = float(U)/(R*R*float(D)*float(S))
    # chat: (R^2/2) int K dw = dF/dt ; compare pointwise K(w) against R4-1 integrand built from geometric P, Delta
    m = mp.mpf; lamm, Rm, tm = m(lam), m(R), m(t); eta = (m(h), m(ey), m(v))
    P, Dl = PD(lamm, Rm, tm, eta); Pt = mp.diff(lambda s: PD(lamm, Rm, s, eta)[0], tm); Dt = mp.diff(lambda s: PD(lamm, Rm, s, eta)[1], tm)
    k = 1-Rm*eta[0]; Sig = (1-Rm)**2 + 2*Rm*(1-eta[0]); a0 = k*k/Sig; A = a0*(1-m(w)**2)
    Sx = A*A + 2*A*m(w)**2*P + m(w)**4*Dl; Nx = A/2*Dt + m(w)**2*(P*Dt - Dl*Pt)
    Kg = float(2*k*a0*Nx/(Rm*Rm*Dl*Sx))
    worst = max(worst, abs(Kc-Kg)/(1+abs(Kg)))
print("CW4 polys() kernel vs chat geometric R4-1 integrand: max rel diff =", worst, "PASS" if worst < 1e-9 else "FAIL")
