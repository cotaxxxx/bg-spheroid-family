# `a_entry_pro`: where the method dependence is

- **Claim class:** `DIAGNOSTIC_ONLY`
- **Concerns:** `exploratory_spheroid_family_scan/a_entry_pro_diagnostic.py` (unmodified)
- **Nothing here is promoted.** No entry is added to `UPSTREAM_PINS.md` and no
  value in this note is `CERTIFIED_UPSTREAM` or a `HIGH_PRECISION_CANDIDATE`.

## Summary

`a_entry_pro_diagnostic.py` reaches `b_pro(a) = lim_{r -> 1-} dE/dr(r, a)` by a
single route — sample `r = 1 - s^2`, least-squares fit a polynomial in `s^2`,
take the constant term — and the open question against it was single-method
dependence.

Varying the endpoint limit and the quadrature separately shows the dependence is
**not** in the extrapolation:

| varied | spread in `b_pro(2.0)` |
|---|---:|
| endpoint limit — fit orders 1–3 × windows 5–7, and Neville/Richardson × windows 5–7 (12 limits) | `2.70e-11` |
| quadrature rule and resolution (8 grids) | `9.00e-06` |

A factor of about `3e5`. Adding an independent Richardson path to the fit closes
a gap that is already eleven decimal places wide.

## Where it comes from

`a_entry_pro_diagnostic.py` contains no functional of its own; `dE_dr` is
supplied by the caller. The available implementation is the clean-room kernel at
`cotaxxxx/basepoint-geometry`,
`CERTIFICATES/prolate/item2_circle/vendor/prolate_circle_F_cleanroom.py`.

Two things about that module matter here.

**Naming.** Its `F` *is* `dE/dr`; its `dFdr` is the second derivative. The
harness wants `F_float`.

**Its float path is a fixed grid**, and its own source says so:

```text
# Non-rigorous fixed midpoint grid for B-SEED only. The rigorous functions
# above never use this path.
_FLOAT_N_THETA = 64
_FLOAT_N_PHI = 128
```

Midpoint converges at `O(N^-2)` over `theta in [0, pi/2]` because neither
endpoint is periodic. Gauss-Legendre over the same patch converges spectrally.

## Effect on the entry ratio

| rule | grid | `a_entry_pro` | shift |
|---|---|---:|---:|
| midpoint | **64×128** (what the pipeline gets) | 2.065421231115004 | **+3.894e-05** |
| midpoint | 128×256 | 2.065392226957119 | +9.933e-06 |
| midpoint | 256×512 | 2.065384802267508 | +2.509e-06 |
| midpoint | 512×1024 | 2.065382923978847 | +6.304e-07 |
| gauss | 32×64 | 2.065382300257701 | +6.630e-09 |
| gauss | 64×128 | 2.065382293735419 | +1.080e-10 |
| gauss | 128×256 | 2.065382293629138 | +1.708e-12 |
| gauss | 256×512 | 2.065382293627430 | — |

The midpoint column falls by a factor of four per doubling, confirming the
`O(N^-2)` reading. Gauss reaches `6.6e-09` at 32×64 — eight times cheaper than
the grid currently in use.

Root searched from a sign change inside `(2.0, 2.4)` only. This is not a global
search and no uniqueness argument is made.

## Two consequences for the prototype

**The `s` ladder cannot detect this.** Successive sample differences fall by
exactly four, so the expansion in `s^2` is clean and every order and window
agrees to `1e-11`. The ladder converges beautifully onto a limit that is wrong
by the grid's own error. Order stability, window stability, and agreement
between two independent extrapolations all report success.

**`refine_root(tol="1e-30")` is about 25 orders of false precision.** With
uncertainty `9.0e-06` in `b_pro` and `|db_pro/da| ~ 0.219`, the entry ratio is
pinned to `±4.11e-05` — roughly 4.7 significant digits.

## Verification of the comparison value

The implementation used for the right-hand column is a re-derivation, not a copy
of the vendored kernel: `gamma_r`'s numerator `N = u(1-ell) + r(u^2-1)` was
obtained by differentiating `lam W / (w sqrt q)` directly.

| check | result |
|---|---|
| re-derivation vs upstream `F_float`, same 64×128 midpoint grid | `3e-16` |
| `gauss 256x512` vs mpmath adaptive quadrature at `(r, a) = (0.9, 2.0)` | `1.4e-15` |
| `gauss 256x512` vs validated `arb` enclosure at `(0.9, 2.0)` (`tol=1e-10`, radius `4.6e-10`) | inside, `-1.4e-15` from its centre |
| upstream 64×128 midpoint vs that same enclosure | **outside**, `+8.8e-06` from its centre |
| end-to-end vs the real prototype pipeline, `b_pro(2.0)` | `2.3e-17` |

The last row runs this repository's harness and the upstream kernel unchanged,
so the comparison is against the prototype itself and not a paraphrase.

One negative result: the validated `arb` path returned `nan` with infinite radius
at `(r, a) = (0.99, 2.4)` with `tol=1e-10, depth=12`. The rigorous path is
hardest exactly where the endpoint limit needs its samples.

## Status of `2.065382293627`

`DIAGNOSTIC_ONLY`. It is a double-precision value, reproducible across two
quadrature rules and four resolutions and consistent with a validated enclosure
at two sampled points. It is not an interval-certified endpoint. Promotion to
`HIGH_PRECISION_CANDIDATE` would need the endpoint limit itself carried in
interval arithmetic, not only the integrand at fixed `r`.

What this note establishes is narrower than a replacement value: the prototype's
result and the converged result **disagree by `3.9e-05`**, and the disagreement
shrinks monotonically in the direction of the converged rule.

## Reproduction

`cotaxxxx/basepoint-geometry-lab`, branch
`claude/root-spread-convergence-systeu`,
`experiments/exp12_a_entry_method_dependence/` — `python run_ladder.py`, with
`ladder_receipt.json` alongside it. The bridge that imports this repository's
prototype unchanged is `basepoint_geometry.adapters.prolate_entry`.

## Not changed by this note

`a_entry_pro_diagnostic.py` is left exactly as it is. The old value and the new
one are both of interest, and the difference between them is the diagnostic.
