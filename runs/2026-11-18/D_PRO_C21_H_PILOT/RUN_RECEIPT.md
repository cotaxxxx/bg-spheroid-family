# D-PRO (C21) representative pilot: reproducible run receipt

2026-11-18 / **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## Scope

Judge chose the (C21) route. This run is strictly a **representative
box cost-and-width survey**, NOT a global covering, sign certificate
or proof of the large prolate theorem. No H or W sign was used to choose
the algorithm. All raw JSON and logs, including failures, are retained.

All runtime measurements: daybreak-works, Python3.11.16,
python-flint0.8.0, 128-bit Arb, one measured process at a time.

## Direct horizontal geometry and special branches

- Direct lab horizontal `f_rho` for regular boxes; the full primitive
  derivation and the `f_rho_rho` formula are in
  `prolate_r4/ANALYSIS_C21.md`.
- AX, CE and STRIP_00: apply the evenness identity
  `H = integral_0^1 E_rho_rho(s rho,z) ds`, with the four-panel
  Simpson-in-s and an interval 4th-derivative remainder.
- BD and STRIP_15: fixed contact cap kappa=1/4096; single final cap
  correction uses the proven `|f_rho| <= pi^2/4 + pi(1+lambda_max)`.
- All signed angular integrals (including external gradients) use
  degree-4 spatial Taylor, not CW7 range×area summation.
- Frozen first-pass mesh: 8×16, ratio2; timeout120s.
- Derived horizontal 2nd derivative and frozen R3 `fxx` agree
  in all 9 fixed pointwise interval tests. This is not an independent
  proof of the complete spatial integrator.

## All 23 preselected first-pass representative boxes

**Each H interval and directional contribution is a producer Arb
interval pending independent mathematical audit.** Last column lists
(R, tau, lambda) correction halfwidths.

| Box | H producer interval (display) | Halfwidth | Contains zero (record only) | Wall s | Peak RSS KiB | Cells | Outer directional halfwidths |
|---|---|---:|---|---:|---:|---:|---|
| G2 | [-69.50896, 69.94866] | 69.72881 | YES | 3.38776 | 29292 | 160 | 11.48118, 15.22105, 0.83758 |
| G35 | [-31.16344, 31.29934] | 31.23139 | YES | 6.63155 | 29448 | 320 | 4.97689, 9.46328, 0.27712 |
| AX | OPEN | — | — | — | — | — | — |
| EQ | [-1.38407, 1.25109] | 1.31758 | YES | 11.11783 | 29184 | 528 | 0.16856, 0.58376, 0.00652 |
| CE | [-22.03663, 22.23124] | 22.13394 | YES | 102.46436 | 29232 | 432 | 4.93017, 11.49818, 0.23648 |
| BD | [-3.80914, 3.08401] | 3.44657 | YES | 19.29651 | 29724 | 928 | 0.65038, 1.46478, 0.01410 |
| STRIP_00 | [-7.89117, 8.27890] | 8.08503 | YES | 61.17936 | 29552 | 256 | 0.97922, 3.54316, 0.06876 |
| STRIP_01 | [-85.46773, 85.84246] | 85.65510 | YES | 5.38698 | 29368 | 256 | 53.26566, 19.92924, 0.49206 |
| STRIP_02 | [-44.98274, 45.40318] | 45.19296 | YES | 5.37362 | 29836 | 256 | 23.46636, 12.00966, 0.30911 |
| STRIP_03 | [-34.80232, 35.27478] | 35.03855 | YES | 5.34449 | 29640 | 256 | 16.41676, 9.42494, 0.24884 |
| STRIP_04 | [-30.54144, 31.01792] | 30.77968 | YES | 5.34218 | 29300 | 256 | 13.54564, 8.10252, 0.21854 |
| STRIP_05 | [-22.54255, 22.86562] | 22.70409 | YES | 6.07371 | 29208 | 288 | 9.11673, 6.26504, 0.15807 |
| STRIP_06 | [-19.27813, 19.58296] | 19.43054 | YES | 6.29603 | 29212 | 304 | 7.50648, 5.54701, 0.13969 |
| STRIP_07 | [-17.74191, 18.01358] | 17.87774 | YES | 6.66078 | 29652 | 320 | 6.87209, 5.18923, 0.13074 |
| STRIP_08 | [-16.81060, 17.05653] | 16.93357 | YES | 6.79756 | 29600 | 320 | 6.52928, 4.93872, 0.12366 |
| STRIP_09 | [-16.10737, 16.32755] | 16.21746 | YES | 6.77611 | 29168 | 320 | 6.32241, 4.70999, 0.11723 |
| STRIP_10 | [-15.51215, 15.70066] | 15.60641 | YES | 6.77110 | 29216 | 320 | 6.22342, 4.49779, 0.11118 |
| STRIP_11 | [-13.77934, 13.89685] | 13.83810 | YES | 7.74660 | 29416 | 368 | 5.27322, 4.14571, 0.09995 |
| STRIP_12 | [-12.89574, 12.93176] | 12.91375 | YES | 8.02192 | 29672 | 384 | 4.95374, 3.90267, 0.09157 |
| STRIP_13 | [-11.98355, 11.94812] | 11.96584 | YES | 8.94932 | 29492 | 432 | 4.54399, 3.65619, 0.08376 |
| STRIP_14 | [-11.54566, 11.42693] | 11.48630 | YES | 9.98375 | 29396 | 480 | 4.55184, 3.44146, 0.07681 |
| STRIP_15 | [-10.80278, 10.57326] | 10.68802 | YES | 11.23855 | 29416 | 528 | 4.44895, 3.11673, 0.06765 |
| LW | [-186.35066, 186.71321] | 186.53194 | YES | 3.37455 | 29388 | 160 | 16.89977, 26.48667, 99.48959 |

**First pass:** 22/23 completed.
AX 4-panel Simpson timed out at the frozen 120-second cap
and is **OPEN**; no partial interval was substituted.
A separately frozen AX fallback using the uniform `s in [0,1]`
interval and signed angular Taylor did produce an enclosure,
but its width is much larger, and it is not a retroactive
replacement for the AX initial run.

## Separate pre-registered fine-mesh calibrations

These are DIFFERENT mesh policies, not repairs to the first-pass
result. Base_u=16, base_v=32, ratio=1/2, order4.
The original four-case refinement is documented in
`FIXED_CALIBRATION_V2.md`; LW is a separate pre-registered case.

| Box | H interval | Halfwidth | Wall s | Cells |
|---|---|---:|---:|---:|
| G2 | [0.38333,0.56977] | 0.09322 | 28.18108 | 1344 |
| G35 | [-0.04384,0.18835] | 0.11609 | 80.55494 | 3840 |
| EQ | [-0.12816,-0.03572] | 0.04622 | 146.79810 | 7040 |
| STRIP_08 | [-0.11859,0.26096] | 0.18978 | 86.11144 | 4064 |
| LW | [-0.51064,1.36056] | 0.93560 | 38.45853 | 1824 |

## Independent numerical primitive-E references

The 25-digit mpmath primitive E 5-point rho derivative was
integrated by 96×96 and 160×160 Gauss-Legendre rules, with
h=0.004, holding z fixed. These do **not** have rigorous
truncation or quadrature error enclosures. Their 2-grid
disagreement measures only an observed numerical change.

| Box | 160×160 H numerical value | 96/160 difference | In coarse producer interval | In fine producer interval |
|---|---:|---:|---|---|
| G2 | 0.5639325459077927642075065 | 1.033310143792120829132138e-20 | True | True |
| G35 | 0.1309029244860698215418875 | 3.754690759122298102679331e-12 | True | True |
| EQ | -0.08192497439761630943530821 | 0.0000006903463127672758635500261 | True | True |
| CE | -0.02414805166929792689786304 | 4.964902488449526296482384e-10 | True | None |
| BD | -0.1134787485561777357515025 | 0.000002378886011662740672300047 | True | None |
| AX | -0.02629883743599832532311567 | 4.725956352952835801147439e-10 | None | None |
| LW | 0.5111072314623152664608892 | 3.485149993605956012510919e-19 | True | None |
| STRIP_00 | 0.1650972455129270387191951 | 2.212029528480200005129118e-14 | True | None |
| STRIP_08 | 0.07121324499570156739208659 | 9.968677716840299329543974e-9 | True | True |
| STRIP_15 | -0.1745157629190713394271423 | 0.0001409470980733115271507011 | True | None |

The AX coarse producer interval is OPEN, so its pointwise
containment is reported as null, not FAIL.

## W tube B4 gate

The v35 child layout R×tau=2×2, unsplit lambda, A<=1/4,
B4 integral<=0.03 was preserved.
The shared depth cap was first replaced by **per-axis depth16**
(frozen first variant); a second **u=tan(psi/4) contact coordinate**
variant was also independently frozen before its run.

| Fixed variant | Child | Full B4 cover | Stop | Partial accepted patches (not an enclosure) | Wall s |
|---|---|---|---|---:|---:|
| AxisDepth16 | [0, 0] | False | LEAF_LIMIT | 32583 | 7.95672 |
| AxisDepth16 | [0, 1] | False | LEAF_LIMIT | 32584 | 7.95438 |
| AxisDepth16 | [1, 0] | False | LEAF_LIMIT | 32581 | 7.94527 |
| AxisDepth16 | [1, 1] | False | LEAF_LIMIT | 32585 | 8.00507 |
| ContactU | [0, 0] | False | LEAF_LIMIT | 32754 | 7.89434 |
| ContactU | [0, 1] | False | LEAF_LIMIT | 32760 | 7.84647 |
| ContactU | [1, 0] | False | LEAF_LIMIT | 32741 | 7.81522 |
| ContactU | [1, 1] | False | LEAF_LIMIT | 32738 | 7.88918 |

**Neither variant produced a complete B4 integral over a child.**
The signed 35-coefficient W integration was NOT started. No W
tube cost or zero-exclusion proof can be claimed.

## Empirical cost and global-scope caution

Regular-route first-pass cost regression **on measured boxes only**:

`0.0526 + (0.0208) * mesh_cells`.
Fitted R²: 0.9995794324153089.
This is principally a per-cell micro-cost calibration; it does
NOT predict the number of cells needed for a new box or
the sign width.

For the 5 separate fine-mesh cases, median elapsed
`80.55494` seconds. Hypothetical counts below use that median
and 12 ideal workers (70% efficiency second column); none of the
listed box counts is a validated global H cover:

| Hypothetical H boxes | Ideal 12-worker time | At assumed 70% efficiency |
|---|---:|---:|
| 24,576 | 1.91 days | 2.73 days |
| 49,152 | 3.82 days | 5.46 days |
| 196,608 | 15.28 days | 21.82 days |

**H≈0 tube cost is separate and unknown**:
`T_total ~ N_H*t_H/workers + N_W_tube*t_W/workers`.
No tube box count, global coverage or W child cost is established.
In particular, extending sign resolution to AX/CE/BD and
lambda widths beyond the sampled cases remains OPEN.

## Record integrity and audit status

The standard-library `c21_checker.py` checks exact rational
bounds, first-order contribution sums, the fixed input boxes,
and zero flags against the stored JSON. It is NOT an independent
derivation or verification of R3 quadrature.
The complete symbolic identities, near-axis construction, and
cap error estimates must be independently audited before being
used for evidence. The parent R3 source is pinned read-only,
with file-by-file SHA-256 comparison in the final package.

No changes to main, STATE.md, R3, old v2/v3 branches, or Julia.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE. Global condition A and (C21)
exclusion theorem: OPEN.**
