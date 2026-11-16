"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Independent mpmath numerical references.

These quadratures have NO rigorous error bound; they are not exact values.
The interval kernel's mathematical error control is a separate calculation.
"""
from functools import lru_cache
import mpmath as mp


def m(q):
    return mp.mpf(str(q.numerator))/int(q.denominator)


def sphere_f(r):
    def integrand(c):
        d=mp.sqrt(1-2*r*c+r*r)
        g=(1-r*c)/d
        # atan2 avoids acos near 1, and this expression is analytic in r>0.
        angle=mp.atan2(r*mp.sqrt(1-c*c),1-r*c)
        return (1-r*c)*angle*angle/2
    return mp.quad(integrand,[-1,0,1])


def sphere_reference(rho,z):
    # Exactly the user's 1D integral, with acos written as atan2 on r>0.
    with mp.workdps(30):
        rho,z=m(rho),m(z)
        r=mp.sqrt(rho*rho+z*z)
        fp=mp.diff(sphere_f,r)
        fpp=mp.diff(sphere_f,r,2)
        v=fp/r
        ezz=v+(fpp-v)*z*z/(r*r)
        return +sphere_f(r),+v,+ezz


@lru_cache(maxsize=8)
def quadrature(n,dps):
    with mp.workdps(dps):
        x,w=mp.gauss_quadrature(n,'legendre')
        return tuple((+x[i],+w[i]) for i in range(n))


def numerical(rho,z,lam,n=32):
    """E, Ez, Ezz from direct formulas; independent of Arb and jets."""
    with mp.workdps(35):
        rho,z,lam=map(m,(rho,z,lam))
        out=[mp.mpf(0) for _ in range(3)]
        for mu,wm in quadrature(n,35):
            a=mp.sqrt(1-mu*mu)
            w=mp.sqrt(lam*lam*(1-mu*mu)+mu*mu)
            for t,wt in quadrature(2*n,35):
                phi=mp.pi*(t+1)/2
                xx=a*mp.cos(phi)
                d=mp.sqrt(1+rho*rho-2*rho*xx+(lam*lam-1)*mu*mu-2*lam*mu*z+z*z)
                h=lam*(1-rho*xx)-z*mu
                g=h/(w*d)
                angle=mp.acos(g)
                rr=angle/mp.sqrt(1-g*g) if g!=1 else mp.mpf(1)
                rp=(g*rr-1)/(1-g*g) if g!=1 else -mp.mpf(1)/3
                dz=(z-lam*mu)/d
                gz=-mu/(w*d)-g*dz/d
                dzz=(1-dz*dz)/d
                gzz=mu*dz/(w*d*d)-gz*dz/d-g*dzz/d+g*dz*dz/(d*d)
                vals=(h*angle*angle,-mu*angle*angle-2*h*rr*gz,
                      4*mu*rr*gz-2*h*rp*gz*gz-2*h*rr*gzz)
                for k in range(3):
                    out[k]+=wm*wt*vals[k]/(4*lam)
        return tuple(+x for x in out)
