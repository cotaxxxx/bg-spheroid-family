"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed local checks of the 2026-11-19 derivation."""
import json
import math
import platform
import sys
from fractions import Fraction as F
from functools import lru_cache
from time import perf_counter

import mpmath as mp

STATUS = "DIAGNOSTIC_ONLY / NOT_EVIDENCE"
mp.mp.dps = 55
results = []


def check(name, ok, **details):
    results.append(bool(ok))
    print(json.dumps(dict(check=name, matched=bool(ok), **details), ensure_ascii=False),
          flush=True)


def short(x):
    return mp.nstr(x, 18)


def constants():
    pi, log2, emax = F(22, 7), F(7, 10), F(11, 4)
    def rational_check(key, lhs, rhs):
        check(key, lhs < rhs, lhs=str(lhs), relation="<", rhs=str(rhs))

    rational_check("near small S", F(65, 64)*(F(5, 2)+log2)
                   + F(4, 3)*(2+log2)+3*pi/16, F(15, 2))
    rational_check("near large S", F(17, 8)*(2+log2)+4, 10)
    for h, root, logpow, bound in ((F(1,8), F(1,2), 30, 7),
                                    (F(1,256), F(1,10), 35, F(9,2))):
        j = F(1,18)+h/3+2*root*F(3,5)/9+2*h*root*F(3,5)
        total = pi/2 + pi*h*h*logpow*log2/2 + (pi+3)*(F(1,3)+h/2)+3*pi*j
        rational_check("far rational envelope h="+str(h), total, bound)
    eps = F(1,4096)
    wedge = 18*eps*(F(3,8)+log2) + 18*eps*14*log2 + 4*F(3,2)/64
    wedge += pi*(64*eps**2 + eps*13*log2)
    rational_check("small S positive mass", wedge, F(3,20))
    neg_mass=F(1,4)*F(5,8)*F(3,4)*F(10,3)*F(3,4)
    check("restored negative mass", neg_mass == F(75,256), exact=str(neg_mass))
    rational_check("small S residual negative", -F(512,10)+12*pi, 0)
    for arg, power in ((7680, F(19,2)), (4096, F(17,2)), (128, F(5)), (8, F(2))):
        rational_check("asinh lower "+str(arg), emax**power.numerator,
                       (2*arg)**power.denominator)
    rational_check("asinh upper 32768", 65537, F(8,3)**12)
    for x, target in ((F(5,2), 6), (F(2), F(16,5)), (F(5,4), F(3,2))):
        partial = sum(x**j/math.factorial(j) for j in (1,3,5,7))
        rational_check("sinh lower at "+str(x), target, partial)
    for multiplier in (F(149,32), F(39,8), F(21,4)):
        rational_check("exact budget multiplier "+str(multiplier),
                       F(29,2), multiplier*F(25,8))
    base=F(47473218194072764542240096942353646083, 2**127)
    rational_check("audited G10 margin for extension", F(17,64), base)
    rational_check("full G9 Lipschitz cost", 2*(4*142+5*600)+1+10, 8192)
    check("G9 allowed loss", 8192*F(1,2**19)==F(1,64))
    check("axial coefficient", F(1,2)*F(1,2)*F(4,5)*2*F(3,4)==F(3,10))


@lru_cache(maxsize=None)
def legendre(n):
    xx, ww = mp.gauss_quadrature(n, "legendre")
    return tuple(zip(xx, ww))


def rule(a, b, n):
    mid, half = (a+b)/2, (b-a)/2
    for x, weight in legendre(n):
        yield mid+half*x, half*weight


def axial_nodes(z, eps, half):
    top=mp.pi/(2 if half else 1)
    bounds={top*i/16 for i in range(17)}
    for centre in (z, -z):
        scale=eps*mp.sqrt(1-z*z)
        for mult in (-1,0,1):
            mu=centre+mult*scale
            if -1 < mu < 1:
                theta=mp.acos(mu)
                if 0 < theta < top:
                    bounds.add(theta)
    bounds=sorted(bounds)
    return [(mp.cos(theta),mp.sin(theta),weight*mp.sin(theta))
            for a,b in zip(bounds,bounds[1:]) for theta,weight in rule(a,b,48)]


def energy(nodes, z, eps):
    # Original k*angle^2. Dot and planar determinant give atan2 without acos cancellation.
    value=mp.mpf(0)
    for mu,s,weight in nodes:
        k=1-z*mu
        angle=mp.atan2(s*((1-eps**2)*mu-z), eps*k)
        value+=weight*k*angle**2
    return value/2


def axis_check(lam,z):
    eps=mp.mpf(1)/lam
    nodes=axial_nodes(z,eps,False)
    step=mp.mpf("1e-7")
    vals={j:energy(nodes,z+j*step,eps) for j in (-2,-1,0,1,2)}
    if z==0:
        ref=(-vals[2]+16*vals[1]-30*vals[0]+16*vals[-1]-vals[-2])/(12*step**2)
    else:
        ref=(-vals[2]+8*vals[1]-8*vals[-1]+vals[-2])/(12*step*z)
    pair=mp.mpf(0)
    max_sin_error=mp.mpf(0)
    for mu,s,weight in axial_nodes(z,eps,True):
        base=mp.atan(eps*mu/s)
        plus,minus=mp.atan((mu+z)/(eps*s)),mp.atan((mu-z)/(eps*s))
        sigma=plus+minus-2*base
        lp,lm=(mu+z)**2+(eps*s)**2,(mu-z)**2+(eps*s)**2
        B=s*s+(eps*mu)**2
        sin_model=2*eps*mu*s*(1-z*z-eps*eps)/(B*mp.sqrt(lp*lm))
        max_sin_error=max(max_sin_error,abs(mp.sin(sigma)-sin_model))
        quotient=(plus-minus)/z if z else 2*eps*s/lp
        pair+=weight*quotient*(3*mu*sigma+2*eps*s/B)/2
    check("original E and signed-axis pair", abs(pair-ref)<mp.mpf("1e-13")
          and max_sin_error<mp.mpf("1e-45") and pair>=3*eps**2/10,
          lam=lam,z=short(z),reference=short(ref),pair=short(pair),
          absolute_error=short(abs(pair-ref)),sine_max_error=short(max_sin_error))


def transverse(lam,S,rho_fraction):
    eps=mp.mpf(1)/lam
    rho=rho_fraction*S
    z=mp.sqrt(1-S*S)
    angle_rule=[(mp.cos(ph),mp.sin(ph)**2,w/mp.pi) for ph,w in rule(0,mp.pi,24)]
    raw, residual=mp.mpf(0),mp.mpf(0)
    for side in (-1,1):
        end=mp.asinh((1-side*z)/(eps*S))
        for panel in range(12):
            for v,weight in rule(end*panel/12,end*(panel+1)/12,20):
                t=side*S*mp.sinh(v)
                dt=weight*S*mp.cosh(v)/2
                mu=z+eps*t
                s=mp.sqrt(1-mu**2)
                B=s*s+(eps*mu)**2
                sqrtB=mp.sqrt(B)
                for cosphi,sin2phi,angular_weight in angle_rule:
                    k=1-z*mu-rho*s*cosphi
                    A=(s-rho)**2+2*s*rho*(1-cosphi)
                    D2=t*t+A
                    D=mp.sqrt(D2)
                    gamma=k/(D*sqrtB)
                    if not 0 < gamma < 1:
                        raise ArithmeticError("interior quadrature gamma outside (0,1)")
                    fp=2*mp.acos(gamma)/mp.sqrt(1-gamma**2)
                    Q=2*fp+gamma*(gamma*fp-2)/(1-gamma**2)
                    kernel=sqrtB/D*fp*gamma**2*(1-s*s*sin2phi/D2)
                    kernel-=s*s/(sqrtB*D)*sin2phi*Q*(1-k/D2)**2
                    c=-2*mp.pi*S*sin2phi
                    d=6*(S*S-rho*S*cosphi)*sin2phi
                    mass=dt*angular_weight
                    raw+=mass*kernel
                    residual+=mass*(kernel-c/mp.sqrt(1+t*t)-d/(1+t*t))
    aa=sum(mp.asinh(lam*(1+sg*z)) for sg in (-1,1))
    bb=sum(mp.atan(lam*(1+sg*z)) for sg in (-1,1))
    budget=(mp.pi*aa-3*S*bb)/2
    err=abs(residual/S-(raw/S+budget))
    check("direct two-tail integration", err<mp.mpf("1e-9") and residual/S<mp.mpf(29)/2
          and raw<0 and budget>mp.mpf(29)/2,
          lam=lam,S=short(S),rho_over_S=short(rho_fraction),lambda_H=short(raw),
          R2_over_S=short(residual/S),exact_budget=short(budget),identity_error=short(err))


def main():
    start=perf_counter()
    print(STATUS, file=sys.stderr, flush=True)
    print(json.dumps(dict(status=STATUS, python=platform.python_version(),
                          mpmath=mp.__version__, decimal_digits=mp.mp.dps)),flush=True)
    constants()
    axis=[(5,mp.mpf(0)),(5,mp.mpf(1)/2),(5,mp.sqrt(24)/5),(8,mp.mpf(255)/256)]
    for lam,z in axis:
        axis_check(lam,z)
    for S,frac in ((mp.mpf(3)/4,mp.mpf(1)/2),(mp.mpf(1)/1024,mp.mpf(31)/32)):
        transverse(4096,S,frac)
    print(json.dumps(dict(status=STATUS,checks=len(results),matched=sum(results),
                          wall_seconds=round(perf_counter()-start,3))),flush=True)
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
