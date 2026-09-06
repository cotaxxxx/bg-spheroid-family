#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
exploratory_spheroid_family_scan.py
===================================
DIAGNOSTIC_ONLY / NOT_BINDING / NOT_CERTIFIED

chat-side clean re-implementation (new bytes, new SHA). This is NOT the
repository original pushed to
01_KAKURON_I/1_楕円体系列/exploratory_spheroid_family_scan/ ; it is an
independent reconstruction from the documented spec, with the same controls.

Object
------
Constant-volume ellipsoid family
    K = { x1^2/a1^2 + x2^2/a2^2 + x3^2/a3^2 <= 1 },  a1*a2*a3 = 1.
Shape plane:  u_i = ln a_i,  sum u_i = 0,
    p = (u1 - u2)/sqrt(2),   q = sqrt(3/2) * u3.
Mirror axes:  p = 0 (a1=a2),  q = -p/sqrt(3) (a2=a3),  q = +p/sqrt(3) (a1=a3).

Functional (cone-volume-weighted radial-normal angle, basepoint b in K):
    E(b) = (1/(3 Vol K)) \int_{dK} alpha(x,b)^2 (x-b)·nu dA,
alpha = angle between (x-b) and outward normal nu.
With x = A u (A = diag(a), u in S^2) and nu dA = det(A) A^{-1}u dmu dphi:
    E(b) = (1/4pi) \int_{-1}^{1} \int_0^{2pi} alpha^2 * D dphi dmu,
    m = A^{-1}u,  D = (x-b)·m = 1 - b·m,  cos(alpha) = D / (|x-b| |m|).

Center Hessian coefficients (principal axes; central symmetry E(b)=E(-b)):
    Q_i = d^2 E / d b_i^2 at b = 0,   sphere: Q_i = 4/3.
Computed as Richardson-extrapolated symmetric second differences,
    Q(h) = 2 (E(h e_i) - E(0)) / h^2,  Q = (4 Q(h/2) - Q(h)) / 3.

Controls
--------
  C1 sphere: Q_i = 4/3;  E(r)-E(0) vs (2/3)r^2 - (2/9)r^4 (truncated series).
  C2 spheroid-line zeros vs certified references:
       oblate  a_z = 0.40795886135 (lambda_c^ob, Q_3 = 0)
       prolate a_c in (4.72438, 4.72439)  (Q_1 = Q_2 = 0)
  C3 S3 symmetry: permuting axes permutes (Q_1,Q_2,Q_3).

Outputs
-------
  spheroid_family_scan.png   Morse-index map + Q_i = 0 curves + landmarks
  spheroid_family_scan.json  controls, landmark numerics, splitting data
  spheroid_family_scan.npz   (ps, qs, Q[3,n,n]) grid data
"""

import argparse
import json
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from scipy.optimize import brentq

SQ2 = np.sqrt(2.0)
SQ23 = np.sqrt(2.0 / 3.0)   # r = sqrt(2/3)*|ln axis ratio| on the spheroid line
SQ32 = np.sqrt(1.5)

AZ_REF = 0.40795886135          # certified lambda_c^ob (diagnostic reference)
AC_LO, AC_HI = 4.72438, 4.72439  # certified a_c bracket (paper 1)
AC_REF = 0.5 * (AC_LO + AC_HI)

# ----------------------------------------------------------------------
# quadrature: Gauss-Legendre in mu = cos(theta), trapezoid (spectral) in phi
# ----------------------------------------------------------------------
_node_cache = {}


def _nodes(nmu, nphi):
    key = (nmu, nphi)
    if key not in _node_cache:
        mu, wmu = np.polynomial.legendre.leggauss(nmu)
        phi = 2.0 * np.pi * np.arange(nphi) / nphi
        _node_cache[key] = dict(
            mu=mu, wmu=wmu,
            s=np.sqrt(np.clip(1.0 - mu * mu, 0.0, None)),
            cph=np.cos(phi), sph=np.sin(phi), wphi=2.0 * np.pi / nphi,
        )
    return _node_cache[key]


class Geometry:
    """Precomputed surface data for one ellipsoid (reused across basepoints)."""

    def __init__(self, a, nmu, nphi):
        nd = _nodes(nmu, nphi)
        a1, a2, a3 = a
        s = nd["s"][:, None]
        mu = nd["mu"][:, None]
        cph = nd["cph"][None, :]
        sph = nd["sph"][None, :]
        self.x1 = a1 * s * cph
        self.x2 = a2 * s * sph
        self.x3 = np.broadcast_to(a3 * mu, self.x1.shape)
        self.m1 = s * cph / a1
        self.m2 = s * sph / a2
        self.m3 = np.broadcast_to(mu / a3, self.x1.shape)
        self.M = np.sqrt(self.m1 ** 2 + self.m2 ** 2 + self.m3 ** 2)
        self.W = (nd["wmu"][:, None] * nd["wphi"]) / (4.0 * np.pi)

    def E(self, b):
        r1 = self.x1 - b[0]
        r2 = self.x2 - b[1]
        r3 = self.x3 - b[2]
        D = 1.0 - (b[0] * self.m1 + b[1] * self.m2 + b[2] * self.m3)  # x·m = 1
        R = np.sqrt(r1 * r1 + r2 * r2 + r3 * r3)
        C = np.clip(D / (R * self.M), -1.0, 1.0)
        return float(np.sum(np.arccos(C) ** 2 * D * self.W))


# ----------------------------------------------------------------------
# center Hessian coefficients
# ----------------------------------------------------------------------
def Q_center(a, nmu, nphi, h=0.02):
    g = Geometry(a, nmu, nphi)
    E0 = g.E((0.0, 0.0, 0.0))
    Q = np.empty(3)
    for i in range(3):
        b = np.zeros(3)
        b[i] = h
        Qh = 2.0 * (g.E(b) - E0) / h ** 2
        b[i] = 0.5 * h
        Qh2 = 2.0 * (g.E(b) - E0) / (0.5 * h) ** 2
        Q[i] = (4.0 * Qh2 - Qh) / 3.0
    return Q


def Q_axis(a, i, nmu, nphi, h=0.02):
    g = Geometry(a, nmu, nphi)
    E0 = g.E((0.0, 0.0, 0.0))
    b = np.zeros(3)
    b[i] = h
    Qh = 2.0 * (g.E(b) - E0) / h ** 2
    b[i] = 0.5 * h
    Qh2 = 2.0 * (g.E(b) - E0) / (0.5 * h) ** 2
    return (4.0 * Qh2 - Qh) / 3.0


# ----------------------------------------------------------------------
# shape-plane maps
# ----------------------------------------------------------------------
def axes_from_pq(p, q):
    u3 = q * SQ23
    u1 = p / SQ2 - 0.5 * u3
    u2 = -p / SQ2 - 0.5 * u3
    return (np.exp(u1), np.exp(u2), np.exp(u3))


def spheroid_axes(rho):
    """a1 = a2, axis ratio a3/a1 = rho, volume normalized."""
    return (rho ** (-1.0 / 3.0), rho ** (-1.0 / 3.0), rho ** (2.0 / 3.0))


def Q_pq(i, p, q, nmu, nphi):
    return Q_axis(axes_from_pq(p, q), i, nmu, nphi)


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=61, help="grid points per side")
    ap.add_argument("--extent", type=float, default=1.8)
    ap.add_argument("--nmu-scan", type=int, default=64)
    ap.add_argument("--nphi-scan", type=int, default=64)
    ap.add_argument("--nmu-hi", type=int, default=192)
    ap.add_argument("--nphi-hi", type=int, default=192)
    ap.add_argument("--prefix", default="spheroid_family_scan")
    args = ap.parse_args()
    HI = (args.nmu_hi, args.nphi_hi)
    out = {"status": "DIAGNOSTIC_ONLY / NOT_BINDING / NOT_CERTIFIED",
           "note": "chat-side clean re-implementation; double precision"}
    t0 = time.time()

    # ---- C1: sphere -------------------------------------------------
    Qs = Q_center((1.0, 1.0, 1.0), *HI)
    r = 0.1
    g = Geometry((1.0, 1.0, 1.0), *HI)
    dE = g.E((0.0, 0.0, r)) - g.E((0.0, 0.0, 0.0))
    model = (2.0 / 3.0) * r ** 2 - (2.0 / 9.0) * r ** 4
    out["control_sphere"] = {
        "Q": Qs.tolist(),
        "max_dev_from_4_3": float(np.max(np.abs(Qs - 4.0 / 3.0))),
        "series_r": r, "dE": dE, "series_model": model,
        "series_diff_O_r6": dE - model,
    }
    print(f"[C1] sphere  Q = {Qs}   max|Q-4/3| = "
          f"{out['control_sphere']['max_dev_from_4_3']:.3e}")
    print(f"[C1] sphere  E(r)-E(0) vs (2/3)r^2-(2/9)r^4 at r={r}: "
          f"diff = {dE - model:.3e} (O(r^6))")

    # ---- C2: spheroid-line zeros ------------------------------------
    q3_at_ref = Q_axis(spheroid_axes(AZ_REF), 2, *HI)
    q1_at_ref = Q_axis(spheroid_axes(AC_REF), 0, *HI)
    az = brentq(lambda rho: Q_axis(spheroid_axes(rho), 2, *HI),
                0.36, 0.46, xtol=1e-10)
    ac = brentq(lambda rho: Q_axis(spheroid_axes(rho), 0, *HI),
                4.3, 5.2, xtol=1e-9)
    out["control_spheroid_line"] = {
        "Q3_at_az_ref": q3_at_ref, "Q1_at_ac_ref": q1_at_ref,
        "az_root": az, "az_ref": AZ_REF, "az_diff": az - AZ_REF,
        "ac_root": ac, "ac_ref_bracket": [AC_LO, AC_HI],
        "ac_in_certified_bracket": bool(AC_LO < ac < AC_HI),
    }
    print(f"[C2] Q3(a_z_ref) = {q3_at_ref:+.3e}   Q1(a_c_ref) = {q1_at_ref:+.3e}")
    print(f"[C2] roots: a_z = {az:.9f} (ref {AZ_REF}, diff {az-AZ_REF:+.2e})")
    print(f"[C2]        a_c = {ac:.7f}  in certified ({AC_LO},{AC_HI}): "
          f"{AC_LO < ac < AC_HI}")

    # ---- C3: S3 symmetry --------------------------------------------
    a = axes_from_pq(0.5, 0.3)
    Qa = Q_center(a, *HI)
    Qp = Q_center((a[2], a[0], a[1]), *HI)          # cyclic permutation
    sym_dev = float(np.max(np.abs(Qp - Qa[[2, 0, 1]])))
    out["control_S3"] = {"max_dev": sym_dev}
    print(f"[C3] S3 symmetry max deviation = {sym_dev:.3e}")

    # ---- landmarks: triangle geometry -------------------------------
    r_vertex = SQ23 * np.log(ac)          # prolate points, 3 vertices
    r_edge = SQ23 * abs(np.log(az))       # oblate points, 3 edge midpoints
    inradius = 0.5 * r_vertex             # straight triangle inradius
    q_c, q_z = r_vertex, -r_edge
    Q3_vertex = Q_axis(spheroid_axes(ac), 2, *HI)
    Q1_edge = Q_axis(spheroid_axes(az), 0, *HI)
    out["triangle"] = {
        "r_vertex": r_vertex, "r_edge_midpoint": r_edge,
        "straight_inradius": inradius,
        "edge_bulges_outward": bool(r_edge > inradius),
        "Q3_at_vertex": Q3_vertex, "Q1_at_edge_midpoint": Q1_edge,
    }
    print(f"[tri] r_vertex = {r_vertex:.4f}  r_edge = {r_edge:.4f}  "
          f"inradius(straight) = {inradius:.4f}  "
          f"bulge = {r_edge > inradius}")
    print(f"[tri] Q3(vertex) = {Q3_vertex:.5f}   Q1(edge mid) = {Q1_edge:.5f}")

    # ---- vertex crossing angle of Q1=0 and Q2=0 ---------------------
    hpq = 0.01
    grads = {}
    for i in (0, 1):
        gp = (Q_pq(i, hpq, q_c, *HI) - Q_pq(i, -hpq, q_c, *HI)) / (2 * hpq)
        gq = (Q_pq(i, 0.0, q_c + hpq, *HI) - Q_pq(i, 0.0, q_c - hpq, *HI)) / (2 * hpq)
        grads[i] = np.array([gp, gq])
    cosang = float(grads[0] @ grads[1] /
                   (np.linalg.norm(grads[0]) * np.linalg.norm(grads[1])))
    ang = np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))
    ang_acute = min(ang, 180.0 - ang)
    out["vertex_crossing"] = {
        "grad_Q1_pq": grads[0].tolist(), "grad_Q2_pq": grads[1].tolist(),
        "angle_deg": ang, "angle_acute_deg": ang_acute,
    }
    print(f"[vtx] crossing angle Q1=0 / Q2=0 at a_c: {ang:.2f} deg "
          f"(acute {ang_acute:.2f} deg)")

    # ---- splitting along delta = ln(a1/a2), a3/sqrt(a1a2) = a_c -----
    L = np.log(ac)
    u0 = -L / 3.0

    def axes_delta(d):
        return (np.exp(u0 + d / 2.0), np.exp(u0 - d / 2.0), np.exp(2.0 * L / 3.0))

    d = 0.02
    Qm = Q_center(axes_delta(-d), *HI)
    Q0 = Q_center(axes_delta(0.0), *HI)
    Qp2 = Q_center(axes_delta(+d), *HI)
    central = ((Qp2 - Qm) / (2 * d)).tolist()
    forward = ((Qp2 - Q0) / d).tolist()
    backward = ((Q0 - Qm) / d).tolist()
    out["splitting_at_ac"] = {
        "delta_step": d, "Q_at_0": Q0.tolist(),
        "dQ_ddelta_central": central,
        "dQ_ddelta_forward_secant": forward,
        "dQ_ddelta_backward_secant": backward,
        "remark": ("a1<->a2 swap gives Q1(delta)=Q2(-delta), so the true "
                   "derivatives satisfy dQ1/dd = -dQ2/dd exactly at delta=0; "
                   "unequal magnitudes (e.g. +1.18 vs -1.29) arise from "
                   "one-sided secants picking up the O(delta) curvature term."),
    }
    print(f"[spl] dQ/ddelta central  = {np.round(central, 5)}")
    print(f"[spl] dQ/ddelta forward  = {np.round(forward, 5)}   "
          f"(one-sided, curvature-contaminated)")

    # ---- shape-plane scan -------------------------------------------
    n, ext = args.n, args.extent
    ps = np.linspace(-ext, ext, n)
    qs = np.linspace(-ext, ext, n)
    Qg = np.empty((3, n, n))
    t1 = time.time()
    for iq, q in enumerate(qs):
        for ip, p in enumerate(ps):
            Qg[:, iq, ip] = Q_center(axes_from_pq(p, q),
                                     args.nmu_scan, args.nphi_scan)
    t_scan = time.time() - t1
    print(f"[scan] {n}x{n} grid, {t_scan:.1f}s")
    index = np.sum(Qg < 0.0, axis=0)
    out["scan"] = {"n": n, "extent": ext,
                   "nmu": args.nmu_scan, "nphi": args.nphi_scan,
                   "index_values_present": sorted(int(v) for v in np.unique(index)),
                   "seconds": t_scan}
    np.savez(args.prefix + ".npz", ps=ps, qs=qs, Q=Qg, index=index)

    # ---- figure ------------------------------------------------------
    fig, axp = plt.subplots(figsize=(9.2, 8.0))
    cmap = ListedColormap(["#efefef", "#fdd9a6", "#f4907c", "#b93a26"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    pcm = axp.pcolormesh(ps, qs, index, cmap=cmap, norm=norm, shading="nearest")
    cb = fig.colorbar(pcm, ax=axp, ticks=[0, 1, 2, 3])
    cb.set_label("center Morse index  (# of negative Q_i)")

    cols = ["tab:blue", "tab:green", "tab:purple"]
    labs = ["Q_1 = 0  (x-direction)", "Q_2 = 0  (y-direction)",
            "Q_3 = 0  (z-direction)"]
    for i in range(3):
        axp.contour(ps, qs, Qg[i], levels=[0.0], colors=[cols[i]],
                    linewidths=2.0)

    tt = np.array([-ext, ext])
    for slope in (None, 1.0 / np.sqrt(3.0), -1.0 / np.sqrt(3.0)):
        if slope is None:
            axp.plot([0, 0], [-ext, ext], "--", color="0.4", lw=0.9)
        else:
            axp.plot(tt, slope * tt, "--", color="0.4", lw=0.9)

    axp.plot(0.0, q_z, "s", ms=10, mfc="yellow", mec="k")
    axp.plot(0.0, q_c, "o", ms=10, mfc="yellow", mec="k")
    axp.plot(0.0, 0.0, "*", ms=14, color="k")

    handles = [Line2D([], [], color=cols[i], lw=2, label=labs[i]) for i in range(3)]
    handles += [
        Line2D([], [], ls="", marker="s", ms=9, mfc="yellow", mec="k",
               label="a_z (oblate, certified target)"),
        Line2D([], [], ls="", marker="o", ms=9, mfc="yellow", mec="k",
               label="a_c (prolate, certified)"),
        Line2D([], [], ls="", marker="*", ms=12, color="k", label="sphere"),
    ]
    axp.legend(handles=handles, loc="lower left", fontsize=9, framealpha=0.9)
    axp.set_xlabel(r"$p=(u_1-u_2)/\sqrt{2}$    ($u_i=\ln a_i,\ \sum u_i=0$)")
    axp.set_ylabel(r"$q=\sqrt{3/2}\,u_3$")
    axp.set_title("Constant-volume ellipsoids: zero set of the center Hessian "
                  "coefficients\n(diagnostic, double precision; sixfold symmetry "
                  "from permuting axes)")
    axp.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(args.prefix + ".png", dpi=150)

    out["total_seconds"] = time.time() - t0
    with open(args.prefix + ".json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"[done] {out['total_seconds']:.1f}s -> {args.prefix}.png/.json/.npz")


if __name__ == "__main__":
    main()
