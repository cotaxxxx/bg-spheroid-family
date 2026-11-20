import numpy as np, chat_tri_centre as C
def hc(s, t, nm, npf):
    xm, wm = np.polynomial.legendre.leggauss(nm); xp, wp = np.polynomial.legendre.leggauss(npf)
    MU, PH = np.meshgrid(xm, np.pi*(xp + 1)); W = np.outer(wp, wm)*np.pi/(4*np.pi)
    S_ = np.sqrt(1 - MU**2); E = np.stack([S_*np.cos(PH), S_*np.sin(PH), MU])
    Ld = np.array([1.0, s, s*t]); Cc = np.einsum('i,i...->...', Ld**2, E**2); B = np.einsum('i,i...->...', Ld**-2, E**2)
    T = 1/np.sqrt(Cc*B); P, Q = C.PQ(T); out = []
    for i in range(3):
        Li2 = Ld[i]**2; ei2 = E[i]**2
        f = T*(P*Li2/Cc*(1 - Li2*ei2/Cc) - Q*ei2*(1 - Li2/Cc)**2); out.append(round(float((f*W).sum()), 6))
    return out
if __name__ == "__main__":
  for st in [(1, 30), (1.25, 32), (6.186, 6.394), (4.825, 7.882), (12, 12), (2, 16)]:
      print(st, [hc(*st, n, 2*n) for n in (96, 384, 1536)])
