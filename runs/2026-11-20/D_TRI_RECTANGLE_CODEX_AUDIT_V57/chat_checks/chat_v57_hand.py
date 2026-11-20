"""chat V57: exact/rational re-check of the analytic constants in Codex's rectangle report (no Codex code)."""
from fractions import Fraction as Fr
from mpmath import mp, mpf, pi, e, exp, sqrt, quad, cosh, inf, log
mp.dps = 30
def ok(name, cond, *v): print(f"{'OK ' if cond else 'FAIL'} {name}:", *[mp.nstr(x, 10) if not isinstance(x, (int, Fr)) else x for x in v])
# (3) at K = 6 and K = 2, and chat's own re-derivation of the coefficients (see V57 sec 2)
c3 = lambda K: K*pi*(14*K**2 + 16*(1+K)**2 + 30*K*(1+K))
chat3 = lambda K: K*pi*(10*K**2 + 16*(1+K)**2 + 30*K*(1+K))
ok("(3) K=6 < 50000", c3(6) < 50000, c3(6), "chat-derived", chat3(6))
ok("(3) K=2 < 2500", c3(2) < 2500, c3(2))
ok("<1/|xi-q|> = 1 inside (Newton shell), q=0.7", abs(quad(lambda m: 0.5/sqrt(1 - 2*mpf('0.7')*m + mpf('0.49')), [-1, 1]) - 1) < 1e-25, 1)
ok("<1/|xi-q|> = 1 at |q|=1", abs(quad(lambda m: 0.5/sqrt(2 - 2*m), [-1, 1]) - 1) < 1e-12, 1)
eps = mpf(2)**-39
W3 = mpf(3341881)/2**36 - 50000*eps; ok("explicit band W3 margin > 0", W3 > 0, W3)
ok("C12 band: 0.00018 - 41943040*2^-39 > 0.0001", mpf('0.00018') - 41943040*eps > mpf('0.0001'), mpf('0.00018') - 41943040*eps)
ok("41943040 = 20*32*256^2", 20*32*256**2 == 41943040, 20*32*256**2)
# B2 chain
a1 = exp(mpf(1)/32) - 1 + 6*sqrt(2)*exp(mpf(1)/32)/256; a2 = exp(mpf(1)/32) - 1
ok("B2 a1 < .07", a1 < .07, a1); ok("B2 a2 < .032", a2 < .032, a2)
ok("B2 2a+a^2 < .15/.07", 2*a1 + a1**2 < .15 and 2*a2 + a2**2 < .07, 2*a1 + a1**2, 2*a2 + a2**2)
ok("B2 inverse product < .13", (1 - mpf('.15'))**-0.5*(1 - mpf('.07'))**-0.5 - 1 < .13, (1 - mpf('.15'))**-0.5*(1 - mpf('.07'))**-0.5 - 1)
ok("B2 dk/(DS) < .034", 6*sqrt(2)/256 < .034, 6*sqrt(2)/256)
ok("B2 dg < .18", mpf('.13') + mpf('.034')*mpf('1.13') < .18, mpf('.13') + mpf('.034')*mpf('1.13'))
ok("B2 |P| <= pi/.8 < 4", pi/mpf('.8') < 4, pi/mpf('.8'))
ok("B2 density 1.01*1.2*4*(1.2^2+1.2^2) < 20", mpf('1.01')*mpf('1.2')*4*2*mpf('1.44') < 20, mpf('1.01')*mpf('1.2')*4*2*mpf('1.44'))
# P(z) = 2 int dv/(cosh v + z): check P(0) = pi, P(1) = 2, P'(0), P''(0) vs m! pi
P = lambda z: 2*quad(lambda v: 1/(cosh(v) + z), [0, inf])
ok("P(0)=pi, P(1)=2", abs(P(0) - pi) < 1e-20 and abs(P(1) - 2) < 1e-20, P(0), P(1))
dP0 = 2*quad(lambda v: 1/cosh(v)**2, [0, inf]); ddP0 = 4*quad(lambda v: 1/cosh(v)**3, [0, inf])
ok("|P'(0)| <= pi, |P''(0)| <= 2 pi", dP0 <= pi and ddP0 <= 2*pi, dP0, ddP0)
# near sphere: E'(r)/r lower bound and window
ok("near sphere 1/24 - 2500e-5 > 0", Fr(1, 24) - Fr(2500, 10**5) > 0, float(Fr(1, 24) - Fr(2500, 10**5)))
# Appendix C centre ball
a = mpf('19.2')/128; m = (1 - 2*a - a**2)**-0.5
ok("C a=.15, mult<1.22", a == mpf('0.15') and m < 1.22, a, m)
ok("C dg < .23", mpf('.22') + mpf('1.22')/128 < .23, mpf('.22') + mpf('1.22')/128)
ok("C |P|<4.1 (pi/.77)", pi/mpf('.77') < 4.1, pi/mpf('.77')); ok("C |P'|< 5.4 (2/.77^2)", 2/mpf('.77')**2 < 5.4, 2/mpf('.77')**2)
ok("C |b|<28 (19.2*1.15*1.22)", mpf('19.2')*mpf('1.15')*mpf('1.22') < 28, mpf('19.2')*mpf('1.15')*mpf('1.22'))
t1 = mpf('4.1')*mpf('1.23')**2*(400 + 28**2)*mpf('1.22'); Qb = 2*mpf('4.1') + mpf('1.23')*mpf('5.4'); t2 = Qb*(1 + mpf('1.23')*28)**2*mpf('1.22')
ok("C |H33| < 40000 (chat's term-by-term)", t1 + t2 < 40000, t1, t2, t1 + t2)
x = mpf(128)/2**16; tail = 40000*x**2/(1 - x**2); ok("C W3 > 0.51 from h3 > 0.6714", mpf('0.6714') - tail > 0.51, tail, mpf('0.6714') - tail)
a = mpf('19.2')*sqrt(2)/128; m = (1 - 2*a - a**2)**-0.5; ok("C eq a<.213, mult<1.38", a < .213 and m < 1.38, a, m)
dg = mpf('.38') + mpf('1.38')*sqrt(2)/128; ok("C eq dg<.4", dg < .4, dg)
T12 = (1 + sqrt(2)/128)*mpf('1.4')*(pi/mpf('.6'))*(mpf('1.68')**2 + 1); ok("C eq |T12| < 30", T12 < 30, T12)
y = mpf(128)/2**20; r = 30*128**2*((1 - y**2)**-2 - 1); ok("C eq C12 > 0.016", mpf(1)/32 - r > 0.016, r, mpf(1)/32 - r)
H = 20*pi*(400 + 3*21**2); ok("C long axis 20pi(400+3*21^2) < 110000", H < 110000, H)
ok("C cylinder (11/16)0.0002149 - 110000 2^-30 > 0", mpf(11)/16*mpf('0.0002149') - 110000*mpf(2)**-30 > 0, mpf(11)/16*mpf('0.0002149') - 110000*mpf(2)**-30)
# B3 small-radius Cauchy chain
b1 = exp(mpf(1)/32) - 1 + 6*exp(mpf(1)/32)/31; ok("B3 a < .233", b1 < .233, b1)
ok("B3 2a+a^2 < .521 / .066", 2*b1 + b1**2 < .521 and 2*a2 + a2**2 < .066, 2*b1 + b1**2, 2*a2 + a2**2)
ip = (1 - mpf('.521'))**-0.5*(1 - mpf('.066'))**-0.5 - 1; ok("B3 inverse product < .50", ip < .5, ip)
dg = mpf('.5') + mpf(6)/31*mpf('1.5'); ok("B3 dg < .80", dg < .8, dg)
ok("B3 |P| <= pi/.19 < 17", pi/mpf('.19') < 17, pi/mpf('.19'))
dens = mpf('1.81')*17*(1 + mpf(2)/32); ok("B3 density < 40", dens < 40, dens)
C4 = 40*32*24*32**4; ok("B3 |d_eps e''''|/3 * 2^-39", True, C4, mpf(C4)/3*eps)
ok("B3 r>=1/32: 100000*1024*2^-39", True, 100000*1024*eps)
