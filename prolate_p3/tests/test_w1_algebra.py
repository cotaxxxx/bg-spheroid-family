"""W1 algebra regression tests, DIAGNOSTIC_ONLY / NOT_EVIDENCE.

These verify finite-degree jet coefficients and angle-series limits.
They are not an independent proof of full quadrature soundness.
"""
from math import factorial
from flint import arb, fmpq, ctx
from prolate_p3 import kernel_w1 as w1
from prolate_p3 import kernel as old


def covered(x, exact):
    assert x.lower().fmpq() <= fmpq(exact) <= x.upper().fmpq(), (str(x),str(exact))


def check_jet(order):
    t=w1.Jet.constant(fmpq(0),order,1)
    one=w1.Jet.constant(fmpq(1),order,1)
    inverse=one.reciprocal()
    square_root=one.sqrt()
    s,c=t.sincos()
    coeff=fmpq(1)
    for k in range(order+1):
        covered(inverse.c[k],fmpq(-1 if k%2 else 1))
        if k:
            coeff=coeff*(fmpq(1,2)-(k-1))/k
        covered(square_root.c[k],coeff)
        sin_term=(fmpq((-1)**((k-1)//2),factorial(k)) if k%2 else fmpq(0))
        cos_term=(fmpq((-1)**(k//2),factorial(k)) if k%2==0 else fmpq(0))
        covered(s.c[k],sin_term)
        covered(c.c[k],cos_term)
    return True


def check_angle_limit(order):
    gamma=w1.Jet.constant(fmpq(1),order,1)
    G,R,Rp=w1.angle(gamma)
    coeff=w1.rational_coeffs()
    for k in range(order+1):
        covered(R.c[k],((-1)**k)*coeff[k])
        covered(Rp.c[k],((-1)**(k+1))*(k+1)*coeff[k+1])
        g0=(fmpq(0) if k==0 else (-1)**k*2*coeff[k-1]/k)
        covered(G.c[k],g0)
    return True


def check_peano_moment(order):
    # On [-1/2,1/2] the exact mean of t^m is 1/(2^m(m+1)).
    # The m-th Taylor coefficient of f=t^m is 1.
    assert w1.weight(fmpq(1),order).contains(fmpq(1,(2**order)*(order+1)))
    return True


def check_kernel_overlap():
    box=((fmpq(15,128),fmpq(17,128)),
         (fmpq(0),fmpq(1,64)),
         (fmpq(2),fmpq(513,256)))
    orig=old.V_box_details(*box,128,cells=(4,4)).enclosure
    ours=[w1.V_box_details(*box,128,order,cells=(4,4)).enclosure for order in (2,4,6)]
    for result in ours:
        assert result.intersection(orig).is_finite()
    return True


def main():
    with ctx.workprec(128):
        for order in (2,4,6):
            check_jet(order)
            check_angle_limit(order)
            check_peano_moment(order)
            print("W1_ORDER",order,"JET_AND_LIMIT_AND_PEANO_SMOKE_PASS")
        check_kernel_overlap()
        print("W1_COARSE_BOX_INTERVAL_OVERLAP_PASS")
    print("DIAGNOSTIC_ONLY_NOT_EVIDENCE_CHAT_AUDIT_REQUIRED")


if __name__=="__main__":
    main()
