import mpmath as mp
mp.mp.dps = 20
lam = mp.mpf(1)/32
def pos(z):
    z = mp.mpf(z)
    f = lambda mu: 2*lam*(1 - mu*z)*(1 - mu*mu)/((1 - mu*mu) + lam**2*(mu - z)**2)**2
    return mp.quad(f, [-1, -0.5, 0, z - 0.01, z, z + 0.01, 1] if z < 0.98 else [-1, 0, 0.5, z, 1])/2
print("§2 positive part <2 lam k s^2/D^4> at lambda = 1/32 (claim <= 6 lam [1 + log(1 + lam^-2)] =", mp.nstr(6*lam*(1 + mp.log(1 + lam**-2)), 6), ")")
for z in ('0', '0.5', '0.9', '0.99'): print(' ', z, mp.nstr(pos(z), 8))
# (9) H_b by mpmath (independent of Codex §7) at lambda = 0.5, 0.1
def PJK(g):
    g = min(max(g, mp.mpf(0)), mp.mpf(1)); a = mp.acos(g); P = 2*a/mp.sin(a) if a > 0 else mp.mpf(2); return P
def Q(g):
    return 2*PJK(g) + g*mp.diff(PJK, g) if g < 1 - 1e-6 else mp.mpf(10)/3
def hb9(l):
    l = mp.mpf(l)
    def f(t, ph):
        m2 = (1 - t*t)*mp.cos(ph)**2; j = (1 - t*t)*mp.sin(ph)**2; C = 1 + (l*l - 1)*m2; c = 1/C
        B = 1 - 4*(1 - 1/l**2)*t*t*m2; T = mp.sqrt(c/B); g = min(t*T, 1)
        return T*t*t*(PJK(g)*c*(1 - j*c) - Q(g)*j*(2 - c)**2)
    return mp.quad(f, [0, 0.5, 1], [0, mp.pi/2, mp.pi])/mp.pi
print("(9) H_b vs Codex §7 (0.41032294 at 0.5, 0.1723500785 at 0.1)")
for l in ('0.5', '0.1'): print(' ', l, mp.nstr(hb9(l), 10))
