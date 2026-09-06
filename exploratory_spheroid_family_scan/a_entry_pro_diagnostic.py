"""Diagnostic equatorial-entry locator for the prolate spheroid branch.

Evidence class: DIAGNOSTIC_ONLY / PROTOTYPE / NOT_AUDITED

Purpose
-------
Estimate the equatorial boundary-entry parameter a_entry_pro for the
nontrivial prolate stationary circle.  The endpoint r -> 1- is regularized by

    r = 1 - s^2,

and the limiting radial derivative

    b_pro(a) = lim_{r -> 1-} dE/dr(r, a)

is estimated by fitting a polynomial in s^2.

This module does NOT certify existence, uniqueness, endpoint regularity,
branch completeness, or absence of off-axis stationary points.  Any values
produced here remain DIAGNOSTIC_ONLY until replaced by a separate interval
certificate with an independent checker and fixed provenance.
"""

import mpmath as mp

mp.mp.dps = 80


EVIDENCE_CLASS = "DIAGNOSTIC_ONLY"
AUDIT_STATUS = "NOT_AUDITED"
IMPLEMENTATION_STATUS = "PROTOTYPE"


def r_from_s(s):
    """Equatorial endpoint regularization: r = 1 - s^2."""
    s = mp.mpf(s)
    return 1 - s * s


def b_pro_samples(a, dE_dr, k0=5, k1=14):
    """Return diagnostic samples approaching r -> 1-.

    Parameters
    ----------
    a : number
        Polar/equatorial axis ratio.
    dE_dr : callable
        Function dE_dr(r, a) returning the radial derivative of E.
    k0, k1 : int
        Sample s = 2^{-k} for k0 <= k <= k1.

    Returns
    -------
    list[dict]
        Diagnostic samples only.
    """
    a = mp.mpf(a)
    out = []

    for k in range(k0, k1 + 1):
        s = mp.power(2, -k)
        r = r_from_s(s)
        value = dE_dr(r, a)

        out.append({
            "k": k,
            "s": s,
            "r": r,
            "dE_dr": value,
        })

    return out


def extrapolate_b_pro(samples, order=2):
    """Estimate b_pro(a) from a polynomial fit in x = s^2.

    Fits

        dE_dr(1-s^2, a) = b0 + b1*s^2 + b2*s^4 + ...

    and returns b0 together with all fitted coefficients.

    This is DIAGNOSTIC_ONLY and must not be used as a certificate.
    """
    n = min(len(samples), order + 4)
    rows = samples[-n:]

    xs = [row["s"] ** 2 for row in rows]
    ys = [row["dE_dr"] for row in rows]

    A = mp.matrix([
        [x ** j for j in range(order + 1)]
        for x in xs
    ])
    y = mp.matrix(ys)

    coeff = mp.lu_solve(A.T * A, A.T * y)
    return coeff[0], coeff


def b_pro_diagnostic(a, dE_dr, k0=5, k1=14, order=2):
    """Compute one diagnostic estimate of b_pro(a)."""
    samples = b_pro_samples(a, dE_dr, k0=k0, k1=k1)
    b0, coeff = extrapolate_b_pro(samples, order=order)

    return {
        "a": mp.mpf(a),
        "b_pro_estimate": b0,
        "coefficients": coeff,
        "samples": samples,
        "evidence": EVIDENCE_CLASS,
        "audit_status": AUDIT_STATUS,
        "implementation_status": IMPLEMENTATION_STATUS,
    }


def scan_a_entry(a_left, a_right, n, dE_dr, k0=5, k1=14, order=2):
    """Coarsely scan for diagnostic sign changes of b_pro(a)."""
    a_left = mp.mpf(a_left)
    a_right = mp.mpf(a_right)

    result = []

    for i in range(n + 1):
        a = a_left + (a_right - a_left) * i / n
        rec = b_pro_diagnostic(
            a,
            dE_dr,
            k0=k0,
            k1=k1,
            order=order,
        )
        result.append((a, rec["b_pro_estimate"]))

    brackets = []

    for (a0, b0), (a1, b1) in zip(result[:-1], result[1:]):
        if b0 == 0:
            brackets.append((a0, a0))
        elif b0 * b1 < 0:
            brackets.append((a0, a1))

    return result, brackets


def refine_root(aL, aR, dE_dr, tol="1e-30", k0=5, k1=14, order=2):
    """Diagnostic bisection of a sign-changing b_pro bracket.

    The returned value remains DIAGNOSTIC_ONLY.  Do not promote it to a
    certified endpoint or use it as support for a manuscript claim.
    """
    aL = mp.mpf(aL)
    aR = mp.mpf(aR)
    tol = mp.mpf(tol)

    fL = b_pro_diagnostic(
        aL, dE_dr, k0=k0, k1=k1, order=order
    )["b_pro_estimate"]
    fR = b_pro_diagnostic(
        aR, dE_dr, k0=k0, k1=k1, order=order
    )["b_pro_estimate"]

    if fL * fR >= 0:
        raise ValueError("No diagnostic sign-changing bracket.")

    while aR - aL > tol:
        aM = (aL + aR) / 2
        fM = b_pro_diagnostic(
            aM, dE_dr, k0=k0, k1=k1, order=order
        )["b_pro_estimate"]

        if fL * fM <= 0:
            aR, fR = aM, fM
        else:
            aL, fL = aM, fM

    return (aL + aR) / 2
