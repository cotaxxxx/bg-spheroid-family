import mpmath as mp
mp.mp.dps = 25
def E_ref(lam, px, pz):
    lam = mp.mpf(lam)
    def f(mu, phi):
        s = mp.sqrt(1-mu*mu); xi = s*mp.cos(phi); eta = s*mp.sin(phi)
        w = mp.sqrt(lam**2*(1-mu*mu)+mu*mu); h = lam*(1-px*xi)-pz*mu
        D = mp.sqrt((xi-px)**2+eta**2+(lam*mu-pz)**2)
        return h*mp.acos(h/(w*D))**2
    return mp.re(2*mp.quad(f, [-1, -0.5, 0, 0.5, 1], [0, mp.pi/4, mp.pi/2, mp.pi])/(4*mp.pi*lam))
H = mp.mpf('0.004')
def stencil(F, second=True):
    e = {k: F(k*H) for k in (-2, -1, 0, 1, 2)}
    d1 = (8*(e[1]-e[-1]) - (e[2]-e[-2]))/(12*H)
    d2 = (16*(e[1]+e[-1]) - (e[2]+e[-2]) - 30*e[0])/(12*H*H)
    return e[0], d1, d2
def fq(x): return mp.mpf(int(x.p))/int(x.q)
def lohi(b): return mp.mpf(b.lower().str(30, radius=False)), mp.mpf(b.upper().str(30, radius=False))
