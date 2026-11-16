#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY. Implements PLAN_BEFORE_RUN.md; not interval arithmetic."""
import hashlib
import json
from pathlib import Path
import numpy as np

LAM = [2, 206539/100000, 5/2, 3, 4, 118/25,
       472438/100000, 472439/100000, 19/4, 5]
RAD = [0, 1/8, 1/2, 15/16, 63/64, 255/256, 59999/60000, 1]
TAU = [0, 1/16, 1/4, 1/2, 3/4, 15/16, 1]
POINTS = [(l, r, t) for l in LAM for r in RAD for t in TAU]
POINTS += [(118/25, r, 0) for r in [1/64, 15/512, 11/256]]

def quadrature(n, m):
    x, w = np.polynomial.legendre.leggauss(n)
    edges = [0.] + [2.**k for k in range(-12, 1)]
    u = np.concatenate([(a+b)/2+(b-a)*x/2 for a,b in zip(edges,edges[1:])])[:,None]
    wu = np.concatenate([(b-a)*w/2 for a,b in zip(edges,edges[1:])])[:,None]
    theta = (np.arange(m)+0.5)*(2*np.pi/m)
    q = 8*u*u/(1+u*u)**2
    sinpsi = 4*u*(1-u*u)/(1+u*u)**2
    jac = 16*u*(1-u*u)/(1+u*u)**3
    return q, sinpsi, np.cos(theta)[None,:], np.sin(theta)[None,:], wu*jac*(2*np.pi/m)

def angle(c):
    c = np.clip(c, 0., 1.)
    v = 1-c*c
    near = v < 0.01
    R = np.empty_like(c)
    Rp = np.empty_like(c)
    R[~near] = np.arccos(c[~near])/np.sqrt(v[~near])
    Rp[~near] = (c[~near]*R[~near]-1)/v[~near]
    coeff = [1.]
    for k in range(7):
        coeff.append(coeff[-1]*(2*k+1)**2/((2*k+2)*(2*k+3)))
    R[near] = np.polynomial.polynomial.polyval(v[near], coeff)
    Rp[near] = -2*c[near]*np.polynomial.polynomial.polyval(v[near], [k*coeff[k] for k in range(1,8)])
    return v*R*R, R, Rp

def values(lam, rad, tau, quad):
    q, sp, ct, st, weight = quad
    a, b = (1-tau*tau)/(1+tau*tau), 2*tau/(1+tau*tau)
    d = 1-rad
    vx = (d-q)*a-b*sp*ct
    vy = sp*st
    vz = lam*((d-q)*b+a*sp*ct)
    mu = b*(1-q)+a*sp*ct
    D = np.sqrt(vx*vx+vy*vy+vz*vz)
    w = np.sqrt(lam*lam*(1-mu*mu)+mu*mu)
    h = lam*(d+rad*q)
    c = np.clip(h/(w*D),0.,1.)
    G, R, Rp = angle(c)
    T, nz = vz/D, mu/w
    e = c*T-nz
    fz = -mu*G-2*h*R*e/D
    fzz = 2*w/D*(c*c*R*(1-T*T)-(2*R+c*Rp)*e*e)
    ezz = np.sum(weight*fzz)/(4*np.pi*lam)
    z = lam*rad*b
    v = ezz if z == 0 else np.sum(weight*fz)/(4*np.pi*lam)/z
    return float(v), float(ezz)

def main():
    root = Path(__file__).resolve().parent
    # A local pre-run seal is created separately before this script is run.
    pins = json.loads((root/'PRE_RUN_SHA256.json').read_text())
    for name in ['PLAN_BEFORE_RUN.md','diagnostic_only.py']:
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != pins[name]:
            raise RuntimeError('DIAGNOSTIC_ONLY pre-run seal mismatch')
    answer = [True, True]
    for n, m in [(8,64),(16,128)]:
        quad = quadrature(n,m)
        for point in POINTS:
            try:
                with np.errstate(all='raise'):
                    v, ezz = values(*point,quad)
                answer[0] = bool(answer[0] and np.isfinite(v) and v > 0)
                answer[1] = bool(answer[1] and np.isfinite(ezz) and ezz > 0)
            except Exception:
                answer = [False, False]
    (root/'DIAGNOSTIC_ONLY_OUTPUT.json').write_text(json.dumps({
        'Q1_all_sampled_V_positive_both_rules':answer[0],
        'Q2_all_sampled_Ezz_positive_both_rules':answer[1]
    },indent=2)+'\n')

if __name__ == '__main__':
    main()
