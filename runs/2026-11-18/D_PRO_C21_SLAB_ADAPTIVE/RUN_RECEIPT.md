# C21 adaptive H slab: execution receipt

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Research scope: **only λ∈[1279/256,5]**, normalized
(R,τ)∈[0,1]². No broader λ region has been covered.
Frozen calibration commit and fixed adaptive plan are in the
GitHub new-branch history. H evaluation is 128-bit Arb using
frozen R3 spatial Taylor quadrature. Source version: python-flint 0.8.0.

## Calibration before adaptive cover

| Route | Status | H halfwidth | Wall s | Cells | Peak RSS KiB |
|---|---|---:|---:|---:|---:|
| AX | OPEN | — | 600.002 | — | — |
| CE | OPEN | — | 600.002 | — | — |
| BD | COMPLETED | 0.086068405 | 272.287 | 12672 | 34016 |

Calibration total elapsed wall 600.003 seconds.

## Actual measured adaptive counts

- Initial rational partition: **256 boxes**.
- H jobs actually executed: **12** (unique IDs:
  12).
- Resolved nonzero H boxes: **0**.
- Evaluated zero/min-width and timed-out/error tube candidates:
  **8**.
- Remaining UNCOMPUTED boxes: **252**.
- Zero-containing parent boxes split: **4**.
- Is the fixed λ slab fully evaluated? **False**.
- Cumulative total experiment wall including calibration:
  **1200.041s**.
- Adaptive H sessions wall:
  **600.037s**.
- Three-box W samples wall (separate): **0.000s**.

### Exact rational area ledger

- Decided: **0**
- Evaluated tube candidates: **1/32**
- Pending uncomputed: **31/32**
- Area sum: **1**
- Evaluated tube plus *uncomputed pending* worst-case upper area:
  **1**.

Do NOT count the pending area as a measured tube region.
The desired two-way identity (decided + tube =1) holds
**only when pending=0**. If partial, the three-way identity is the
appropriate exact check.

### Counts by H route

| Route | Number of measured jobs | Sum of worker execution seconds |
|---|---:|---:|
| AXIS | 0 | 0.000 |
| CENTER | 4 | 2400.007 |
| BOUNDARY | 0 | 0.000 |
| REGULAR | 8 | 1411.521 |

### Counts by split depth

| Depth | Evaluated | Terminal |
|---|---:|---:|
| 0 | 12 | 8 |

### Evaluated tube candidate distribution (up to first 30)

| ID | R bounds | τ bounds | Exact area | Reason |
|---|---|---|---|---|
| R00_T00 | 0..1/16 | 0..1/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R00_T04 | 0..1/16 | 1/4..5/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R00_T08 | 0..1/16 | 1/2..9/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R00_T12 | 0..1/16 | 3/4..13/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R08_T04 | 1/2..9/16 | 1/4..5/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R08_T08 | 1/2..9/16 | 1/2..9/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R12_T00 | 3/4..13/16 | 0..1/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |
| R12_T08 | 3/4..13/16 | 1/2..9/16 | 1/256 | TUBE_TIMEOUT_OR_ERROR |

All evaluated H-box inputs/outputs, finite enclosures, reasons
for OPEN, wall seconds, peak RSS and mesh cell counts are in
`boxes/`, `logs/`, `state.json`, and `summary.json`.
A per-box `H_interval=null` means no interval was produced.

## W: exactly three tube samples, if eligible

Selection rule: sorted evaluated tube IDs, first/middle/last,
frozen only when the slab is finished or the 24h cap is reached.
W uses pinned R3's second-order angular quotient, not CW7.
Status: **OPEN / not launched**.
There is NO tube-wide W calculation.

## Cost inference permitted by the observed data

Full slab incomplete: 252 uncomputed rectangles remain with exact area 31/32. NO all-λ cost extrapolation, and NO claimed final slab box count. Even an optimistic cost forecast cannot be grounded before pending regions are measured at the fixed rule.

The `N_H × t_H + N_W_tube × t_W` cost model must account for
W separately; no W tube count is assumed.

## Audit and reproducibility

- Any `checker.json` tests exact output consistency, not
  independent mathematics of the interval quadrature.
- Fixed rules: `CALIBRATION_RULE_FREEZE.md`,
  `COVER_RULE_FREEZE.md`, `INTERACTIVE_SUBRUN_FREEZE.md`.
- Restart: the controller reads `state.json`, including a
  recovered inflight batch if necessary, and writes atomically.
- Any shortened interactive run remains explicitly PARTIAL.
- Original R3, prior C21 branches, main, STATE.md and Julia
  have not been changed.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE. C21 global condition: OPEN.**
