"""W1 comparison kernel: rigorous even-order sequential midpoint Taylor quadrature.

DIAGNOSTIC_ONLY / NOT_EVIDENCE. Independent chat audit required.
Original prolate_p3/kernel.py is not modified.
The quadrature orders are 2, 4, 6; coefficients in all J arrays are
f^(k)/k!, enclosed at every base point in the input base interval.
"""
from dataclasses import dataclass
from functools import lru_cache
from math import factorial
from flint import arb, fmpq, ctx
from . import kernel as base

STATUS = 'DIAGNOSTIC_ONLY / NOT_EVIDENCE'
N_SERIES = 96
ORDERS = (2, 4, 6)


def exact(x):
    if not isinstance(x, fmpq):
        raise TypeError('expected exact flint.fmpq value')
    return x


class Jet:
    __slots__ = ('c',)

    def __init__(self, coeff):
        coeff = tuple(x if isinstance(x, arb) else arb(x) for x in coeff)
        if not coeff:
            raise ValueError('nonempty coefficient array required')
        self.c = coeff

    @classmethod
    def constant(cls, x, order, tangent=0):
        return cls([x, tangent] + [arb(0) for _ in range(order-1)])

    @classmethod
    def _to(cls, x, order):
        if isinstance(x, cls):
            if len(x.c) != order+1:
                raise ValueError('jet order mismatch')
            return x
        return cls.constant(x, order)

    @property
    def order(self):
        return len(self.c)-1

    def __add__(self, x):
        x = self._to(x, self.order)
        return Jet([a+b for a,b in zip(self.c,x.c)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-a for a in self.c])

    def __sub__(self, x):
        return self + -self._to(x,self.order)

    def __rsub__(self, x):
        return self._to(x,self.order)-self

    def __mul__(self, x):
        x = self._to(x, self.order)
        return Jet([sum((self.c[i]*x.c[k-i] for i in range(k+1)), arb(0))
                    for k in range(self.order+1)])

    __rmul__ = __mul__

    def reciprocal(self):
        b=[1/self.c[0]]
        for k in range(1,self.order+1):
            b.append(-b[0]*sum((self.c[i]*b[k-i] for i in range(1,k+1)),arb(0)))
        return Jet(b)

    def __truediv__(self,x):
        return self*self._to(x,self.order).reciprocal()

    def __rtruediv__(self,x):
        return self._to(x,self.order)*self.reciprocal()

    def sqrt(self):
        b=[self.c[0].sqrt()]
        den=2*b[0]
        for k in range(1,self.order+1):
            inner=sum((b[i]*b[k-i] for i in range(1,k)), arb(0))
            b.append((self.c[k]-inner)/den)
        return Jet(b)

    def sincos(self):
        s=[self.c[0].sin()]
        c=[self.c[0].cos()]
        for k in range(1,self.order+1):
            ds=sum((i*self.c[i]*c[k-i] for i in range(1,k+1)),arb(0))
            dc=sum((i*self.c[i]*s[k-i] for i in range(1,k+1)),arb(0))
            s.append(ds/k)
            c.append(-dc/k)
        return Jet(s), Jet(c)

    def sin(self):
        return self.sincos()[0]

    def cos(self):
        return self.sincos()[1]

    def cap(self, low, high):
        # A proven range may sharpen the value coefficient only. Do not cap
        # derivatives, and do not differentiate a numerical clipping operation.
        return Jet((base.clip(self.c[0],low,high),)+self.c[1:])

    def compose(self, derivatives):
        # derivatives[k] encloses f^(k)(x) at every x in self.c[0].
        if len(derivatives)!=self.order+1:
            raise ValueError('composition derivative array has wrong length')
        delta=Jet((arb(0),)+self.c[1:])
        acc=Jet.constant(0,self.order)
        power=Jet.constant(1,self.order)
        for k,d in enumerate(derivatives):
            acc=acc+power*(d/factorial(k))
            if k<self.order:
                power=power*delta
        return acc


@lru_cache(maxsize=8)
def rational_coeffs():
    out=[fmpq(1)]
    for k in range(N_SERIES+1):
        out.append(out[-1]*fmpq(k+1,2*k+3))
    return tuple(out)


def angle(g):
    # R(γ)=sum c_n q^n, γ in [0,1], q=1-γ. The full derivative
    # tail is enclosed with a strictly one-sided rational remainder.
    order=g.order
    if order not in ORDERS:
        raise ValueError('unsupported order')
    q=1-g.c[0]
    coeff=rational_coeffs()
    maxk=order+1
    p=[arb(0) for _ in range(maxk+1)]
    for n in range(N_SERIES,-1,-1):
        for k in range(maxk,0,-1):
            p[k]=p[k]*q+k*p[k-1]
        p[0]=p[0]*q+arb(coeff[n])
    d=[]
    for k in range(maxk+1):
        factor=1
        for j in range(k):
            factor*=N_SERIES+1-j
        r=fmpq(N_SERIES+2,2*(N_SERIES+2-k))
        assert r<fmpq(1)
        tail=coeff[N_SERIES+1]*factor/(1-r)
        enclosed=p[k]+base.hull(fmpq(0),tail)
        d.append(-enclosed if k%2 else enclosed)

    gpoly=arb(2*coeff[N_SERIES]/(N_SERIES+1))
    for n in range(N_SERIES-1,-1,-1):
        gpoly=gpoly*q+arb(2*coeff[n]/(n+1))
    g0=q*gpoly+base.hull(fmpq(0),4*coeff[N_SERIES+1]/(N_SERIES+2))
    gd=[g0]+[-2*d[k-1] for k in range(1,order+1)]
    return g.compose(gd),g.compose(d[:order+1]),g.compose(d[1:order+2])


def density(u, v, rho, z, lam, rmax, order, active=None):
    u=Jet.constant(u, order, int(active=='u'))*arb.pi()
    v=Jet.constant(v, order, int(active=='v'))*arb.pi()
    mu,st=u.cos(),u.sin()
    cv,sv=v.cos(),v.sin()
    xx,yy=st*cv,st*sv
    wz=lam*mu-z
    dsq=(xx-rho)*(xx-rho)+yy*yy+wz*wz
    d=dsq.cap((1-rmax)**2,(5*(1+rmax))**2).sqrt()
    w=(lam*lam*(1-mu*mu)+mu*mu).cap(1,25).sqrt()
    h=lam*(1-rho*xx)-z*mu
    gamma=(h/w/d).cap(0,1)
    gg,rr,rp=angle(gamma)
    t=(wz/d).cap(-1,1)
    nn=mu/w
    e=gamma*t-nn
    f=h*gg
    fz=-mu*gg-2*h*rr*e/d
    fzz=2*w/d*(gamma*gamma*rr*(1-t*t)-(2*rr+gamma*rp)*e*e)
    scale=st*arb.pi()/(2*lam)
    return tuple(x*scale for x in (f,fz,fzz))


@dataclass(frozen=True)
class Integration:
    balls: tuple
    cells: int
    density_evaluations: int
    order: int
    method: str = 'even_order_sequential_midpoint_peano'
    status: str = STATUS


def weight(h, k):
    # Centred mean of t^k is (h/2)^k/(k+1) for k even.
    if k%2:
        raise ValueError('even moment only')
    return arb(h**k/fmpq((2**k)*(k+1)))


def integrate(rho,z,lam,rmax,order=4,cells=(32,64)):
    if order not in ORDERS:
        raise ValueError('order must be 2,4,6')
    nu,nv=cells
    if type(nu) is not int or type(nv) is not int or min(nu,nv)<1:
        raise ValueError('invalid cell counts')
    hu,hv=fmpq(1,nu),fmpq(1,nv)
    total=[arb(0),arb(0),arb(0)]
    ncalls=0
    even_lower=list(range(2,order,2))
    vweights=[(k,weight(hv,k)) for k in even_lower]
    uweights=[(k,weight(hu,k)) for k in even_lower]
    wv=weight(hv,order)
    wu=weight(hu,order)

    for i in range(nu):
        iu=base.hull(i*hu,(i+1)*hu)
        mu=arb(fmpq(2*i+1,2)*hu)
        for j in range(nv):
            iv=base.hull(j*hv,(j+1)*hv)
            mv=arb(fmpq(2*j+1,2)*hv)
            # First apply even Taylor midpoint Peano in u; bound each lower
            # u-coefficient across the whole v interval; then apply Peano in v
            # to f(u_mid,v). The remainder intervals refer to full cells.
            v_mid=density(mu,mv,rho,z,lam,rmax,order,'v')
            v_full=density(mu,iv,rho,z,lam,rmax,order,'v')
            u_full=density(iu,iv,rho,z,lam,rmax,order,'u')
            if even_lower:
                u_line=density(mu,iv,rho,z,lam,rmax,order,'u')
                ncalls+=4
            else:
                u_line=None
                ncalls+=3

            for k in range(3):
                enclosed=v_mid[k].c[0]
                for m,coefficient in vweights:
                    enclosed+=coefficient*v_mid[k].c[m]
                enclosed+=wv*v_full[k].c[order]
                for m,coefficient in uweights:
                    enclosed+=coefficient*u_line[k].c[m]
                enclosed+=wu*u_full[k].c[order]
                # Range enclosure on the full cell, independent of the
                # Peano enclosure, so intersection preserves containment.
                enclosed=enclosed.intersection(u_full[k].c[0])
                total[k]+=enclosed*arb(hu*hv)

    if not all(v.is_finite() for v in total):
        raise ArithmeticError('non-finite W1 integral')
    return Integration(tuple(total),nu*nv,ncalls,order)


@dataclass(frozen=True)
class W1Box:
    enclosure: arb
    lower: arb
    width: arb
    cells: int
    density_evaluations: int
    route: str
    order: int
    status: str = STATUS


def V_box_details(R_iv,tau_iv,lam_iv,prec,order=4,cells=(32,64)):
    base.check_prec(prec)
    ra,rb=base.endpoints(R_iv)
    ta,tb=base.endpoints(tau_iv)
    la,lb=base.endpoints(lam_iv)
    if not (0<=ra<=rb<=fmpq(15,16) and
            0<=ta<=tb<=1 and 2<=la<=lb<=5):
        raise ValueError('box outside source-calibration domain')
    with ctx.workprec(prec):
        af=lambda t:(1-t*t)/(1+t*t)
        bf=lambda t:2*t/(1+t*t)
        rho=base.hull(ra*af(tb),rb*af(ta))
        zlo,zhi=la*ra*bf(ta),lb*rb*bf(tb)
        z=base.hull(zlo,zhi)
        lam=base.hull(la,lb)
        if zlo>0:
            result=integrate(rho,z,lam,rb,order,cells)
            if z>0:
                enclosure=result.balls[1]/z
            else:
                enclosure=result.balls[1]*base.hull(1/zhi,1/zlo)
            route='Ez_over_z'
        else:
            result=integrate(rho,base.hull(0,zhi),lam,rb,order,cells)
            enclosure=result.balls[2]
            route='Ezz_vertical_segment_hull'
        if not enclosure.is_finite():
            raise ArithmeticError('non-finite W1 V enclosure')
        return W1Box(enclosure,enclosure.lower(),2*enclosure.rad(),
                     result.cells,result.density_evaluations,route,order)
