#!/usr/bin/env python3
"""Rational boundary/rectangle coverage checker, not a mathematical sign proof.

Only checks that source scope rectangles cover the positive-t parameter domain.
All interval endpoints are exact fractions and all open/closed flags are explicit.
No sealed data, kernel, numerical integration, or Judge certification.
"""
from fractions import Fraction as Q
from itertools import product

L = [Q("2/5"), Q("83/200"), Q("9/20"), Q("5/8"), Q("33/50")]
T = [Q("0"), Q("1/2"), Q("31/32"), Q("1")]

# name, lambda low/high, t low/high, closed-lambda-left/right, closed-t-left/right
R = [
    ("C0", L[0], L[1], T[0], T[1], True, True, False, True),
    ("C1a", L[1], L[2], T[0], T[1], True, True, False, True),
    ("C1c", L[2], L[3], T[0], T[1], True, True, False, True),
    ("C1d", L[3], L[4], T[0], T[2], True, True, False, True),
    ("GAP1", L[0], L[2], T[1], T[3], True, False, False, True),
    ("C1b_plus_GAP2", L[2], L[3], T[1], T[3], True, True, True, True),
    ("BOUNDARY_BAND", L[3], L[4], T[2], T[3], True, True, True, True),
]

def interval_contains(x, left, right, close_left, close_right):
    return (x > left or close_left and x == left) and (
        x < right or close_right and x == right
    )

def sources_at(lam, t):
    return [
        r[0] for r in R
        if interval_contains(lam, r[1], r[2], r[5], r[6])
        and interval_contains(t, r[3], r[4], r[7], r[8])
    ]

def main():
    assert L == sorted(L) and T == sorted(T)
    assert len(R) == 7
    assert L[0] == Q("2/5") and L[-1] == Q("33/50")
    assert T[0] == 0 and T[-1] == 1
    for r in R:
        assert r[1] in L and r[2] in L and r[3] in T and r[4] in T
        assert r[1] < r[2] and r[3] < r[4]
    lam_interior = [(l + u) / 2 for l,u in zip(L,L[1:])]
    t_interior = [(l + u) / 2 for l,u in zip(T,T[1:])]
    cells = list(product(lam_interior, t_interior))
    assert len(cells) == 12
    for lam,t in cells:
        assert sources_at(lam,t), f"INTERIOR_GAP {lam} {t}"
    # Since rectangle endpoints are exactly the cuts, a single interior point
    # covers each open elementary cell. Test every line and corner separately.
    test_lams = sorted(set(L + lam_interior))
    test_ts = sorted(set(T[1:] + t_interior))
    asserts=0
    for lam,t in product(test_lams,test_ts):
        src=sources_at(lam,t)
        assert src, f"EDGE_OR_CORNER_GAP lam={lam}, t={t}"
        asserts+=1
    assert asserts == 54
    assert "GAP1" not in sources_at(Q("9/20"),Q("3/4"))
    assert "C1b_plus_GAP2" in sources_at(Q("9/20"),Q("3/4"))
    assert "BOUNDARY_BAND" in sources_at(Q("33/50"),Q("1"))
    assert "C1d" in sources_at(Q("33/50"),Q("31/32"))
    assert "C0" in sources_at(Q("2/5"),Q("1/2"))
    print("TILING_RATIONAL_GRID_PASS")
    print("STATUS: DRAFT, NOT_EVIDENCE, NOT_CLOSED")
    print("Lambda stripes: 4; t stripes: 3; interior cells: 12")
    print("Boundary+interior representative assertions: 54")
    print("Gap1 lambda right endpoint: OPEN; C1b left endpoint: CLOSED")
    print("Mathematical signs, root counts, and gluing: NOT TESTED")

if __name__=="__main__":
    main()
