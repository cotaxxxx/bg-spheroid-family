"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.

Arb interval quadrature, with a sequential midpoint Peano remainder.
Public geometric inputs are fmpq; intervals are pairs of fmpq endpoints.
No binary floating-point geometry, tolerances, or sign decisions.
"""
from dataclasses import dataclass
from functools import lru_cache
from math import prod
from flint import arb, fmpq, ctx

STATUS = 'DIAGNOSTIC_ONLY / NOT_EVIDENCE'
DEFAULT_CELLS = (32, 64)
SERIES_N = 96


def rational(x):
    if not isinstance(x, fmpq):
        raise TypeError('geometric inputs must be flint.fmpq, never float')
    return x


def endpoints(iv):
    if not isinstance(iv, (tuple, list)) or len(iv) != 2:
        raise TypeError('interval must be a pair of fmpq endpoints')
    a, b = map(rational, iv)
    if a > b:
        raise ValueError('reversed interval')
    return a, b


def hull(a, b):
    """Arb hull; radius is rounded OUTWARD by Arb, not by Python float."""
    return arb(a).union(arb(b))


def clip(x, lo, hi):
    """Intersect a value enclosure with a proven geometric range.

    The output ball may protrude slightly beyond the intersection because
    Arb radii have finite precision. No later step assumes exact endpoints.
    """
    a = max(x.lower().fmpq(), fmpq(lo))
    b = min(x.upper().fmpq(), fmpq(hi))
    if a > b:
        raise ArithmeticError('empty geometric intersection')
    return hull(a, b)


class J:
    """Univariate Taylor coefficients (value, derivative, derivative/2!).

    The expansion base ranges over an interval: coefficients enclose the
    derivatives at EVERY base point, as in D5 chat_m40iv.J (DA=0, DB=2).
    """
    __slots__ = ('c',)

    def __init__(self, a, b=0, c=0):
        self.c = tuple(x if isinstance(x, arb) else arb(x) for x in (a,b,c))

    @staticmethod
    def lift(x):
        return x if isinstance(x, J) else J(x)

    def __add__(self, x):
        x = self.lift(x)
        return J(*(a+b for a,b in zip(self.c, x.c)))

    __radd__ = __add__

    def __neg__(self):
        return J(*(-a for a in self.c))

    def __sub__(self, x):
        return self + (-self.lift(x))

    def __rsub__(self, x):
        return self.lift(x) - self

    def __mul__(self, x):
        x = self.lift(x)
        return J(*(sum((self.c[k]*x.c[n-k] for k in range(n+1)), arb(0))
                   for n in range(3)))

    __rmul__ = __mul__

    def compose(self, f0, f1, f2):
        return J(f0, f1*self.c[1], f1*self.c[2]+f2*self.c[1]*self.c[1]/2)

    def recip(self):
        a = 1/self.c[0]
        return self.compose(a, -a*a, 2*a*a*a)

    def __truediv__(self, x):
        return self * self.lift(x).recip()

    def __rtruediv__(self, x):
        return self.lift(x) * self.recip()

    def sqrt(self):
        a = self.c[0].sqrt()
        # Sequential reciprocals avoid a widened product ball crossing zero.
        return self.compose(a, (1/a)/2, -((1/a)/a)/a/4)

    def sin(self):
        s, c = self.c[0].sin(), self.c[0].cos()
        return self.compose(s, c, -s)

    def cos(self):
        s, c = self.c[0].sin(), self.c[0].cos()
        return self.compose(c, -s, -c)

    def cap(self, lo, hi):
        return J(clip(self.c[0], lo, hi), self.c[1], self.c[2])


@lru_cache(maxsize=16)
def coefficients(n, prec):
    """Exact c_n, then correctly rounded Arb coefficients, cached by precision."""
    c = [fmpq(1)]
    for k in range(n+1):
        c.append(c[-1]*fmpq(k+1, 2*k+3))
    rows, tails = [], []
    for k in range(4):
        rows.append(tuple(arb(c[j]*prod(range(j-k+1, j+1)))
                          for j in range(k,n+1)))
        ratio = fmpq(n+2, 2*(n+2-k))
        tails.append(c[n+1]*prod(range(n+2-k,n+2))/(1-ratio))
    grow = tuple(arb(2*c[j]/(j+1)) for j in range(n+1))
    return tuple(rows), tuple(tails), grow, 4*c[n+1]/(n+2)


def horner(row, q):
    out = row[-1]
    for a in reversed(row[:-1]):
        out = out*q+a
    return out


def angle_values(g):
    """G,R,R' jets, including gamma=1, using one-sided rigorous tails."""
    q = 1-g.c[0]
    rows, tails, grow, gtail = coefficients(SERIES_N, ctx.prec)
    d = []
    for k in range(4):
        val = horner(rows[k],q)+hull(0,tails[k])
        d.append(val if k % 2 == 0 else -val)
    gv = q*horner(grow,q)+hull(0,gtail)
    return (g.compose(gv,-2*d[0],-2*d[1]),
            g.compose(*d[:3]), g.compose(*d[1:]))


def density(u, v, rho, z, lam, rmax, active=None):
    """Complete density on u=theta/pi, v=phi/pi in [0,1]^2.

    y-reflection doubles this half-sphere; normalizing factor is pi/(2 lam).
    rho,z can be dependent boxes: rmax bounds the TRUE mapped points only.
    Value caps do not alter derivative coefficients.
    """
    u = J(u, int(active == 'u'))*arb.pi()
    v = J(v, int(active == 'v'))*arb.pi()
    mu, st = u.cos(), u.sin()
    xx, yy = st*v.cos(), st*v.sin()
    wz = lam*mu-z
    dsq = (xx-rho)*(xx-rho)+yy*yy+wz*wz
    d = dsq.cap((1-rmax)**2, (5*(1+rmax))**2).sqrt()
    w = (lam*lam*(1-mu*mu)+mu*mu).cap(1,25).sqrt()
    h = lam*(1-rho*xx)-z*mu
    g = (h/w/d).cap(0,1)
    gg, rr, rp = angle_values(g)
    tt = (wz/d).cap(-1,1)
    nn = mu/w
    ee = g*tt-nn
    f = h*gg
    fz = -mu*gg-2*h*rr*ee/d
    fzz = 2*w/d*(g*g*rr*(1-tt*tt)-(2*rr+g*rp)*ee*ee)
    scale = st*arb.pi()/(2*lam)
    return tuple(x*scale for x in (f,fz,fzz))


@dataclass(frozen=True)
class IntegralResult:
    balls: tuple
    cells: int
    density_evaluations: int
    method: str = 'sequential_midpoint_Peano_intersect_cell_range'
    status: str = STATUS


def integrate(rho, z, lam, rmax, cells=DEFAULT_CELLS):
    """Internal: arguments already enclosed in Arb; ctx.prec set by caller.

    For each complete transformed density f, use
      |C|*(f(mid)+hu^2/24*f_uu(C)+hv^2/24*f_vv(mid_u,Iv)).
    Intersect with |C|*f(C). Both enclose the SAME cell integral.
    """
    nu,nv = cells
    if type(nu) is not int or type(nv) is not int or min(nu,nv) < 1:
        raise ValueError('positive integer cell counts required')
    hu,hv = fmpq(1,nu), fmpq(1,nv)
    total = [arb(0) for _ in range(3)]
    for i in range(nu):
        ui = hull(i*hu,(i+1)*hu)
        um = arb((2*i+1)*hu/2)
        for j in range(nv):
            vi = hull(j*hv,(j+1)*hv)
            vm = arb((2*j+1)*hv/2)
            mid = density(um,vm,rho,z,lam,rmax)
            uu = density(ui,vi,rho,z,lam,rmax,'u')
            vv = density(um,vi,rho,z,lam,rmax,'v')
            for k in range(3):
                bound = mid[k].c[0]+arb(hu*hu/12)*uu[k].c[2]+arb(hv*hv/12)*vv[k].c[2]
                total[k] += bound.intersection(uu[k].c[0])*arb(hu*hv)
    if not all(x.is_finite() for x in total):
        raise ArithmeticError('non-finite integral enclosure')
    return IntegralResult(tuple(total),nu*nv,3*nu*nv)


def check_prec(prec):
    if type(prec) is not int or prec < 64:
        raise ValueError('precision must be an integer >= 64 bits')


def _point_inputs(rho,z,lam):
    rho,z,lam = map(rational,(rho,z,lam))
    if not (lam == 1 or 2 <= lam <= 5):
        raise ValueError('lambda=1 control or lambda in [2,5] required')
    if rho*rho+(z/lam)**2 > fmpq(15,16)**2:
        raise ValueError('point outside R<=15/16')
    return rho,z,lam


@lru_cache(maxsize=256)
def _point_cached(rho,z,lam,prec,cells):
    # Cache stores balls, not decimal serializations; precision is part of key.
    with ctx.workprec(prec):
        r2 = rho*rho+(z/lam)**2
        rmax = min(arb(r2).sqrt().upper().fmpq(),fmpq(15,16))
        return integrate(arb(rho),arb(z),arb(lam),rmax,cells)


def point_balls(rho,z,lam,prec,cells=DEFAULT_CELLS):
    check_prec(prec)
    return _point_cached(*_point_inputs(rho,z,lam),prec,tuple(cells))


def E_ball(rho,z,lam,prec):
    return point_balls(rho,z,lam,prec).balls[0]


def Ez_ball(rho,z,lam,prec):
    return point_balls(rho,z,lam,prec).balls[1]


def Ezz_ball(rho,z,lam,prec):
    return point_balls(rho,z,lam,prec).balls[2]


def V_ball(rho,z,lam,prec):
    """Point V enclosure: intersect direct quotient with FTC line enclosure.

    A tiny nonzero z amplifies quadrature error in Ez/z. This additional
    point helper avoids treating that wide quotient as the only enclosure.
    The mandated box routing in V_box_details is unchanged.
    """
    check_prec(prec)
    rho,z,lam = _point_inputs(rho,z,lam)
    if not z:
        return Ezz_ball(rho,z,lam,prec)
    with ctx.workprec(prec):
        rmax = min(arb(rho*rho+(z/lam)**2).sqrt().upper().fmpq(),fmpq(15,16))
        line = integrate(arb(rho),hull(min(fmpq(0),z),max(fmpq(0),z)),arb(lam),rmax)
        return line.balls[2].intersection(Ez_ball(rho,z,lam,prec)/arb(z))


@dataclass(frozen=True)
class BoxResult:
    enclosure: arb
    lower: arb
    width: arb
    cells: int
    density_evaluations: int
    route: str
    status: str = STATUS


def V_box_details(R_iv,tau_iv,lam_iv,prec,cells=DEFAULT_CELLS):
    check_prec(prec)
    ra,rb = endpoints(R_iv)
    ta,tb = endpoints(tau_iv)
    la,lb = endpoints(lam_iv)
    if not (0 <= ra <= rb <= fmpq(15,16) and 0 <= ta <= tb <= 1 and 2 <= la <= lb <= 5):
        raise ValueError('box outside required domain')
    with ctx.workprec(prec):
        # a decreases and b increases on [0,1]. Exact endpoint maps.
        af = lambda t: (1-t*t)/(1+t*t)
        bf = lambda t: 2*t/(1+t*t)
        rho = hull(ra*af(tb),rb*af(ta))
        zlo,zhi = la*ra*bf(ta),lb*rb*bf(tb)
        z = hull(zlo,zhi)
        lam = hull(la,lb)
        if zlo > 0:
            result = integrate(rho,z,lam,rb,cells)
            if z > 0:
                enclosure = result.balls[1]/z
            else:
                # Arb's fixed-precision radius may inflate a very wide positive
                # interval across zero. Exact rational reciprocal endpoints
                # still enclose 1/z for the TRUE interval [zlo,zhi].
                enclosure = result.balls[1]*hull(1/zhi,1/zlo)
            route = 'Ez_over_z'
        else:
            result = integrate(rho,hull(0,zhi),lam,rb,cells)
            enclosure = result.balls[2]
            route = 'Ezz_vertical_segment_hull'
        if not enclosure.is_finite():
            raise ArithmeticError('non-finite V enclosure')
        return BoxResult(enclosure,enclosure.lower(),2*enclosure.rad(),
                         result.cells,result.density_evaluations,route)


def V_box_lower(R_iv,tau_iv,lam_iv,prec):
    """Exact dyadic Arb lower bound. Details include full enclosure and width."""
    return V_box_details(R_iv,tau_iv,lam_iv,prec).lower
