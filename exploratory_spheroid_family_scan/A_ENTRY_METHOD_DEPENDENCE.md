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

---

# Follow-up: the endpoint is a proper integral

- **Claim class:** `VALIDATED_ENCLOSURE` for the signs below; `DIAGNOSTIC_ONLY`
  for every numerical value.
- **Still nothing is promoted.** No entry is added to `UPSTREAM_PINS.md`, and
  `a_entry_pro_diagnostic.py` remains unmodified.

## The `s` ladder is avoidable

Expand the `dE/dr` integrand at `r = 1` about `(theta, phi) = (pi/2, 0)`, with
`theta = pi/2 - a` and `phi = b`:

```text
q -> lam^2 a^2 + b^2,   gamma -> 0,   N -> -q,   gamma_r -> -q^(-1/2),
integrand -> -pi^2/4.
```

The integrand is **bounded** at the corner — non-analytic, which costs spectral
convergence, but not singular. So `b_pro(a)` is the value of a proper integral
at `r = 1`, not a limit that has to be approached.

Evaluating it directly, on a `gauss 256x512` grid:

| `a` | direct at `r = 1` | extrapolated `s`-ladder limit | difference |
|---|---:|---:|---:|
| 1.8 | +0.063216923214105 | +0.063216923214105 | `0.00e+00` |
| 2.0 | +0.014619074281089 | +0.014619074281089 | `-6.94e-18` |
| 2.4 | −0.065785510022537 | −0.065785510022537 | `0.00e+00` |

Agreement at double-precision roundoff. The endpoint regularization `r = 1 - s^2`
and the polynomial extrapolation in `s^2` are solving a problem that is not
there. This does not make the prototype wrong — the two routes agree on the same
grid to `2e-08` — it makes the machinery unnecessary, and it removes the
extrapolation as something that has to be justified.

## Why the rigorous path was failing, and what fixes it

The upstream kernel writes `q = ell - 2 r u + r^2`, a difference of nearly equal
quantities near the corner. Its *interval* enclosure therefore contains zero
across a box far wider than the true zero set, and `gamma_r = (lam/w) N q^(-3/2)`
encloses an infinite range. Measured at `a = 2.0`, `tol = 1e-3`:

| form | result at `r = 1` | time |
|---|---|---:|
| `q = ell - 2 r u + r^2` (upstream `F_arb`) | `nan`, radius `+/- inf` | 11.7 s |
| sum-of-squares `q` | `+0.0146 +/- 7.94e-03`, sign `+1` | 18.7 s |

At `r = 1`, with `P = ell - u^2 = s^2 sin^2(phi) + lam^2 cos^2(theta) >= 0` and
`V = 1 - u >= 0`,

```text
q = P + V^2,      N = -(u P + V^2 (1 + u)).
```

No cancellation. The earlier `nan` at `(r, a) = (0.99, 2.4)` recorded above has
the same cause, and is not evidence that the rigorous path is unsuited to this
problem.

## Certified sign brackets

| bracket | tolerance | enclosure at low | enclosure at high | width |
|---|---|---|---|---:|
| `(2.0, 2.4)` | `1e-3` | `+0.014748681 +/- 7.94e-03` → `+1` | `-0.065654807 +/- 8.32e-03` → `-1` | 0.4000 |
| `(2.060, 2.071)` | `1e-4` | `+0.001187516 +/- 4.19e-04` → `+1` | `-0.001220752 +/- 4.19e-04` → `-1` | **0.0110** |

Both enclosures in each row exclude zero, so the signs are validated and
opposite. Given continuity of `b_pro` in `a` — assumed, not proved — an entry
ratio lies strictly inside each bracket. Both brackets contain the
`DIAGNOSTIC_ONLY` value `2.065382293627`, and the wider one also contains the
prototype's `2.065421231115`.

Nothing here establishes uniqueness, and nothing rules out sign changes outside
the interval searched. These are enclosures produced by one implementation
against one hand-derived corner bound, with no independent checker and no
provenance record pinned to a run; they are not certificates in the sense
`RESEARCH_STATUS.md` uses.

## Consequence for `a_entry_pro_diagnostic.py`

Three of its parts are now known to be unnecessary rather than merely
uncertain: `r_from_s`, `extrapolate_b_pro`, and the `k0`/`k1`/`order` parameters
that feed them. What the file still needs is what it never had — a functional of
its own, evaluated on a quadrature whose rule and resolution are arguments.

## Reproduction

`cotaxxxx/basepoint-geometry-lab`, branch
`claude/root-spread-convergence-systeu`,
`experiments/exp13_interval_sign_bracket/` — `python run_bracket.py`, with
`bracket_receipt.json` alongside it. The enclosures need `python-flint`; the
first section runs without it.
