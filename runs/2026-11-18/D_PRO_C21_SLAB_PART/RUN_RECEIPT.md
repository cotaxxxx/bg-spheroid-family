# D-PRO C21 partial slab adaptive H diagnostic receipt
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Execution state **PARTIAL_UNFINISHED**. Only λ∈[1279/256,5],
R∈[1/4,1/2], τ∈[0,1] (area **1/4**). NOT a global or full
λ-slab cover.

Frozen new MVT route: `PRE_RUN_FREEZE.md`, pre-run commit
`d71522c19b9998d6640adf9d8542227690fe560b`.
Controller committed before H experiment as `61069b5c94b795af8277fa60767fa7fabdcccf42`.
Original C21 source `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`,
R3 source pin `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`,
V37 `949e9dff7b48cf993cdb9fae95ec698f482cd591`.
All sign results are diagnostics; only binary zero inclusion directs
the adaptive algorithm.

## 1. Preregistered CE one-box MVT calibration
- Status: **COMPLETED**.
- Wall time: **109.190 seconds**.
- Signed H interval: **{'lower': '-192217485523408962060759644508675527973/5444517870735015415413993718908291383296', 'upper': '-70926846081474218447885346140134987045/5444517870735015415413993718908291383296', 'lo': -0.03530477630656751, 'hi': -0.01302720420162732, 'mid': -0.024165990254097415, 'halfwidth': 0.011138786052470095}**.
- Angular cell count: **6368**.
- Peak child RSS KiB: **30468**.
- No s-Simpson quadrature used.
- Fixed independent derivative parameters: rho', z, λ;
  physical primitive-E reference vertical coordinate p_z=λz.

## 2. Measured main partial-slab H work
- Initial 1/64×1/64 boxes: **1024 (16×64)**.
- Actual measured H jobs: **60**, unique:
  **60**.
- Decided nonzero boxes: **23**.
- EVALUATED terminal tube candidates (including per-box OPEN):
  **0**.
- PENDING / not yet evaluated: **1038**.
- Split parents: **37**.
- Main adaptive wall time **860.383s**.
- Total wall incl CE **969.573s**.
- W sample wall **0.000s**.
- Sum of all worker CPU wall times by route is below (not
  the same as whole elapsed wall).

### Exact unnormalized area in (R,τ)
- Decided **23/4096**.
- Evaluated tube candidates **0**.
- Pending not evaluated **1001/4096**.
- Exact sum **1/4** (=1/4).

### Relative to requested region of measure 1/4
- Decided **23/1024**.
- Evaluated tube **0**.
- Unmeasured pending **1001/1024**.
- Sum 1 exactly. Do not call uncomputed pending a measured tube.

### Special MVT routes: measured H halfwidth and cost (first25 of 16)
| Box ID | Route | H halfwidth | Worker s | Mesh cells | Peak RSS KiB |
|---|---|---:|---:|---:|---:|
| R16_T63 | AXIS_MVT | 0.014705832 | 132.563 | 6752 | 30916 |
| R17_T63 | AXIS_MVT | 0.015067043 | 132.182 | 6752 | 30792 |
| R18_T63 | AXIS_MVT | 0.01543953 | 133.471 | 6784 | 30868 |
| R19_T63 | AXIS_MVT | 0.015829068 | 133.351 | 6816 | 31040 |
| R20_T63 | AXIS_MVT | 0.016240792 | 141.961 | 6848 | 30920 |
| R21_T63 | AXIS_MVT | 0.016667506 | 143.194 | 6848 | 31152 |
| R22_T63 | AXIS_MVT | 0.017116795 | 135.333 | 6880 | 30964 |
| R23_T63 | AXIS_MVT | 0.017578645 | 135.601 | 6912 | 30968 |
| R24_T63 | AXIS_MVT | 0.018068518 | 142.954 | 6912 | 30940 |
| R25_T63 | AXIS_MVT | 0.018577758 | 136.752 | 6944 | 31152 |
| R26_T63 | AXIS_MVT | 0.019117351 | 144.227 | 6944 | 31152 |
| R27_T63 | AXIS_MVT | 0.01968946 | 144.255 | 6976 | 30388 |
| R28_T63 | AXIS_MVT | 0.020279345 | 143.582 | 6976 | 30892 |
| R29_T63 | AXIS_MVT | 0.020910305 | 144.637 | 7008 | 30812 |
| R30_T63 | AXIS_MVT | 0.021570351 | 147.283 | 7040 | 31108 |
| R31_T63 | AXIS_MVT | 0.022273842 | 137.764 | 7040 | 31200 |

### Measured H jobs and worker time by route
| Route | Jobs | Sum of worker wall seconds |
|---|---:|---:|
| AXIS_MVT | 16 | 2231.691 |
| SMALL_RHO_MVT | 0 | 0.000 |
| GENERAL | 44 | 7298.100 |
| CENTER_MVT | 0 | 0.000 |

### Depth counts
| Depth | Measured jobs | Terminal |
|---|---:|---:|
| 0 | 60 | 23 |

### Observed tube candidate distribution (first40)
| Immutable ID | R interval | τ interval | Area | Reason |
|---|---|---|---|---|
| — | — | — | — | No final tube candidates |

For ALL tube candidates and PENDING coordinates inspect `summary.json`.
Each executed box has a separate JSON and stdout/stderr log;
successful H intervals include rigorous rational endpoints and
cell-count, time, peak child RSS; timed-out boxes have null H
and sampled VmHWM KiB lower bounds, clearly labelled.

## 3. W three-box tube time and width
- Status **OPEN / DEFERRED**.
- The frozen rule selects first/middle/last sorted terminal tube
  IDs only after the entire requested subregion is finished or
  the genuine 24h wall cap is reached.
- This checkpoint does not silently substitute a small convenience
  sample. Full-tube W is NEVER calculated.

## 4. Cost outside the requested region
The current subregion has 1038
  pending boxes with exact measure 1001/4096.
  Therefore its *total* required H box count/time and its final
  unresolved tube area are NOT MEASURED.
  No full-Rτ-board or full-λ-range box count or time forecast is made.
  Hypothetical slab counts: uniform1/256 across [2,5] =768 slabs,
  or λ thickness1/1024 on [2,3] (1024) plus1/256 on [3,5]
  (512), total1536 slabs; neither justifies extrapolating the
  currently incomplete region or proves λ≈2 enclosure.

These cost statements, if present, remain
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**, and no all-λ theorem is claimed.

## 5. Reproducibility and audit scope
Sources `prolate_r4/c21_slabpart_*.py`, frozen rule
`PRE_RUN_FREEZE.md`, `state.json` checkpoint,
`summary.json`, checker `checker.json`.
Independent exact-fraction checker verifies partition and
source records but does not mathematically certify the Arb
quadrature. The old R3 chart-based distance heuristic is used
ONLY to generate the angular cell partition: because the MVT
extension point is not necessarily chart-aligned, it must NOT
be used as a distance proof. The integrand's independent
positive lower bound D≥1−(rho_hi+z_hi)>0 is applied to ALL
Taylor coefficients. Complete mathematical auditing remains OPEN.
No changes to main, STATE.md, Julia, or earlier branches.
