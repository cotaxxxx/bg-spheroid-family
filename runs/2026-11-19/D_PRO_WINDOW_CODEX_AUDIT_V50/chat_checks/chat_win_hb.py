import sys
exec(open('chat_win_spot.py').read().split('def show(')[0])
def H_b(lam):
    e2 = mp.mpf(1)/lam**2
    def f(t, ph):
        m2 = (1-t*t)*mp.cos(ph)**2; j = (1-t*t)*mp.sin(ph)**2; C = 1 + (lam**2-1)*m2; c = 1/C
        B = 1 - 4*(1-e2)*t*t*m2; T = mp.sqrt(c/B); g = min(mp.mpf(1), t*T)
        return T*t*t*(Fp(g)*c*(1-j*c) - Q(g)*j*(2-c)**2)
    return mp.quad(f, [0, 0.5, 1], [0, mp.pi/2, mp.pi])/mp.pi
lam = mp.mpf('2.0654')
print('H_b formula (9) at 2.0654:', mp.nstr(H_b(lam), 10), flush=True)
for k in [2, 3, 4]:
    print(f'chord H at rho=1-1e-{k}:', mp.nstr(H_chord(lam, 1-mp.mpf(10)**-k, 0), 10), flush=True)
a, b = H_b(mp.mpf('2.06538200')), H_b(mp.mpf('2.06538255'))
print(f"lambda_b by (9): left {mp.nstr(a,8)} right {mp.nstr(b,8)} sign change: {a > 0 > b}")
