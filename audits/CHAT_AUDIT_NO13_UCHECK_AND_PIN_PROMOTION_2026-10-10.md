# CHAT AUDIT — No.13 U_check receipt reconciliation and pin promotion #1 (2026-10-10)

Status: CHAT AUDIT RECORD / NOT_BINDING. No new computation was run. Every machine step below is a replay of pinned scripts, unchanged, in fresh directories.
Baseline: bg-spheroid-family main `87cd7181456ba44a57a86256e7177bd764599db4` (STATE.md v1.11 and the workflow table).
Approved scope (Judge, 2026-10-10): No.13 U_check reconciliation; pin promotion audit of south 39′ (`bbcfe662`) and of prolate local (`68bc9828`). D5 is out of scope.

---

## Part 1. No.13 — U_check = {1/2 < t ≤ 1, 2/5 ≤ λ < 9/20}

Source: bg-oblate-spheroid, branch `design/d-ob-p2`, tip `bbcfe6628a074d1f7b48e1f818542ee205e88f50` (fetched 2026-10-10).
Search: every file on `design/d-ob-p2`, `main`, `design/d-ob-p1` and `analytic-endpoint-limit-78c178f` that mentions t > 1/2 together with λ < 9/20. The only hit is the C0 Judge receipt, and it is an exclusion.

### 1.1 Receipts read and what they cover

| Receipt (blob) | Status read from file | Domain actually certified |
|---|---|---|
| C0 Judge receipt `fc41e71f` | JUDGE_PASS / CONDITIONAL_ON_TWO_LEMMAS / EXTERNAL_AUDIT_PENDING | t ∈ [0,1/2], λ ∈ [2/5,83/200]: ∂³g < 0 and g(1/2,λ) < 0. **Explicitly excludes 1/2 < t < 31/32** |
| C1a machine receipt `e494e789` (commit `7f34c95d`) | MACHINE_PASS / C1A_CLOSED / NOT_EXTERNAL_JUDGE_BINDING | ∂³g < 0 on [0,1/2] × [83/200,9/20]; F_x = 2g(1/2,λ) has exactly one zero λ_x ∈ (83/200, 9/20). Only t ≤ 1/2 |
| C1 crossing/tube contract `77210a54` | PREDECLARED_CONTRACT / MACHINE_NOT_RUN / NOT_BINDING | Originally placed C1b on λ ∈ [83/200,9/20] with t ∈ [1/2,31/32] |
| C1b pre-run amendment `8e04e2ef` | PREDECLARED_AMENDMENT | **Moves C1b to λ ∈ [9/20,5/8]** on the ground that "C1a already covers the crossing bridge through λ_J = 9/20" |
| C1b machine receipt `bdcafce7` | MACHINE_PASS / C1B_MACHINE_CLOSED / JUDGE_NOT_YET_ISSUED | λ ∈ [9/20,5/8], 159 accepted slabs, exact cover |
| C1b B_ob subgate `0f19e387` | MACHINE_PASS / C1B_SUBGATE_ONLY | B_ob(λ) = g(1,λ) < 0 on [9/20,5/8] |
| Band Judge receipt `d6b0a787` | JUDGE_PASS / CONDITIONAL_ON_TWO_LEMMAS | t ∈ [31/32,1], λ ∈ [5/8,33/50] only; §7 excludes every λ outside this |
| C1c / C1d / lower slab | as in STATE | λ ≥ 9/20 (C1c) or λ ≥ 5/8 (C1d, lower slab) |

### 1.2 Finding: U_check is entirely uncovered

The amendment `8e04e2ef` relies on C1a for λ < 9/20. But C1a certifies only the sign change of g at the single height t = 1/2. It says nothing about t > 1/2. When C1b moved right, the strip t > 1/2 for λ < 9/20 lost its only planned cover. No later document restores it.

| Part of U_check | Covered? | Reason |
|---|---|---|
| 1/2 < t < 1, 2/5 ≤ λ < 9/20 | **UNCOVERED** | No receipt. The C0 receipt excludes it explicitly; C1a stops at t = 1/2; C1b starts at λ = 9/20 |
| t = 1 (boundary point), 2/5 ≤ λ < 9/20 | **UNCOVERED** | B_ob < 0 is certified only on [9/20,5/8] and [5/8,33/50] |

What is known on the edges (outside U_check, used only to describe it):
- **t = 1/2, closed edge, covered:** g(1/2,λ) < 0 on [2/5,83/200] (C0b). On [83/200,9/20], F_x is increasing with one zero λ_x (C1a). So g(1/2,λ) < 0 for λ < λ_x, = 0 at λ_x, and > 0 for λ > λ_x.
- **λ = 9/20, closed right edge of U_check's complement:** t ∈ [1/2,31/32] is covered by the first C1b slab (left exterior plus tube). t = 1 is covered by B_ob. t ∈ (31/32,1) is not covered; see 1.3.

Mathematical consequence (from the receipts, no new claim): for λ ∈ (λ_x, 9/20), g(1/2,λ) > 0 and C0/C1a exclude roots on (0,1/2]. So the nonzero axial root branch for these λ, if it exists, lies in (1/2,1]. That is exactly in U_check. **Neither its existence nor its uniqueness is covered by any receipt.** For λ ≤ λ_x, extra roots in (1/2,1] are not excluded either.

Partial items that do **not** cover it:
- `analysis/OBLATE_ENDPOINT_C1_LEMMA.md` (blob `5afa815f`, EXTERNAL_AUDIT_PENDING / NOT_BINDING), Lemma 5, and `analysis/D_OB_P1_DESIGN_NOTE.md` §7 (blob `f81e120e`, NOT_BINDING).
  - Their scope admits λ ∈ [2/5, 93/200].
  - They give g(·,λ) continuous on [1/2,1] and g(1⁻,λ) = B_ob(λ).
  - They claim no sign. This is a value identity only. It may serve as a regularity premise for a future certificate.
- A floating-point diagnostic, `diagnostics/oblate_fold_scan_result.json` (DIAGNOSTIC_ONLY, NOT_EVIDENCE), places a root near t ≈ 0.516 at λ = 0.44, inside the gap. This is recorded only to show that the gap holds the actual root branch.

Independent check: a separate agent, given only the question, searched all 280 files on the ref. It found no sign, root or B_ob statement for t > 1/2 and λ < 9/20. It confirmed that no executed C1b document uses [83/200, 9/20], and that the C1b code fixes `L_LO, L_HI = 9/20, 5/8`. It also confirmed the λ_x bracket [699/1600, 281/640] from C1a.

### 1.3 A second gap found during reconciliation (outside U_check, inside No.13)

| Part | Covered? | Reason |
|---|---|---|
| 31/32 < t < 1 on the unclamped C1b slabs (at least λ ∈ [9/20, 931/1600)) | **UNCOVERED** | The C1b exterior cover is limited to [1/2,31/32] (contract §5). The band receipt starts at λ = 5/8. B_ob covers only the point t = 1. The C1b receipt itself says "No claim g(31/32,λ) > 0 is extended below λ = 5/8" |
| same strip on the 35 right-clamped slabs (λ ∈ [931/1600, 5/8]) | covered at machine level | The tube runs up to t_plus = 1 and is not cut at 31/32 (receipt §5.2) |

The exact λ-extent of the unclamped slabs with t_plus < 1 must be read from the sealed slab ledger. This audit did not open it. The gap is therefore stated as "at least [9/20, 931/1600)".

### 1.4 Receipt validity (separate from coverage)

| Component | Usable as | Open condition |
|---|---|---|
| C0 | Judge PASS, conditional | Lemmas 6fba6e4f and 963b03be (external audit) |
| C1a | Machine CLOSED | No Judge issued |
| C1b | Machine enclosures only | The Judge request excludes root existence, root uniqueness, the identification Gt = ∂_t g, and regularity on [9/20,5/8]. A separate regularity obligation is declared but not yet predeclared |
| C1c | Judge PASS + analytic assembly | Lemma 6fba6e4f |
| C1d | Machine PASS | Lemma 35656381; no Judge issued |
| Band [31/32,1] | Judge PASS, conditional | Lemmas aefa8ed2 and f66ffe5a |

### 1.5 No.13 verdict

**U_check: UNCOVERED (whole region, including t = 1).** A second strip is also uncovered: (31/32,1) on the unclamped C1b slabs.
Nothing was filled by inference. Closing either strip needs a new predeclared certificate, which needs a Judge decision.

---

## Part 2. Pin promotion audit

### 2.1 Target A — south 39′, bg-oblate-spheroid `bbcfe6628a074d1f7b48e1f818542ee205e88f50`

| Check | Result |
|---|---|
| Source | Commit exists and is the tip of `design/d-ob-p2` (retaining ref). 18 files. The proof file matches the audited source copy: basepoint-geometry `05668a47`, `tools/d_ob_p2/ftq_paper_proof/…_DRAFT.md`, SHA-256 `f320acb9…3d3c`. **PASS** |
| Pins | All 18 files hash to the values in the south proof §0 and the chat audit record §1/§4. The four code certificates also match their basepoint-geometry pins (f74e1221, 6621f3d9, 1ac44469). **PASS** |
| Certificates (replay) | Python 3.13.16, SymPy 1.14.0, exact arithmetic, fresh directories. bernstein_G, bernstein_south_A, theta_14_over_5, kernel_extension and the Astra exact script: exit 0, empty stderr. **All 7 stdout files are byte-identical to the committed ones.** The Astra `--write-certificate` output is identical to the received JSON (`853d022e…`). **PASS** |
| Independent verification | Two lineages. Astra produced the 144 Π_t coefficients. chat `chk144.py` rebuilt Π_t from the paper definitions and checked them (PASS, minima 106592/1953125 and 40192/1953125). Code re-derived Lemma A. **PASS** |
| Dependencies | FT_q reduction, P decomposition, C0/B1 root structure, B1 ordering, contracts 20″–23″ and v1.1: all present at bbcfe662, SHA-256 equal to the pins, commits are ancestors. **Inherited condition:** the reduction uses P1 Lemma 6.1 and the P1 trap −1 ≤ R_γ ≤ 0. These belong to No.15a (external audit pending) |
| Scope | Boundary face only, μ ∈ [−1,1/2], P units, box λ ∈ [2/5,93/200] and τ ∈ [7/8,1]. The result is S″_lb = 635530452759/817216000000, a bound for the whole interval and not to be added to older bounds. Not claimed: north and near residuals, c_FT, m0, D-P2. Spot check of Lemma C: monotonicity of C0 in m and L, the factor 3/10, and 2·(13/10)^(−3/2) > 5/4 all hold. **PASS** |
| Wording | The proof file's own header still reads "DRAFT / NOT CANONICAL". The pinned bytes are not edited (version-up only). Status is taken from the chat audit record. **Note only** |

**Verdict A: PASS. Readback complete, so South 39′ is CLOSED within scope, conditional on P1 (No.15a).** It is eligible for registration.

### 2.2 Target B — prolate local, basepoint-geometry `68bc9828c3476e9db2d73d338e731c48c0931f54`

| Check | Result |
|---|---|
| Source | Commit exists and is reachable from main. Its manifest `SHA256SUMS.txt` (SHA-256 `d764cd37…3874`) matches all 11 objects. **PASS** |
| Certificates (replay) | python-flint 0.9.0 / FLINT 3.6.0, the pinned reference parameters. cap (dps 50), ac (dps 100, tol 1e-40) and Qz (dps 70, tol 1e-28): status CERTIFIED and all conditions true. **The JSON is identical to the archived file except for the timestamp and environment.** B2, H4 and Qz symbolic audits: PASS. **PASS** |
| Is it current? | **FAIL.** Two later commits on main change this object set. `d5ac2f4` adds `prolate_h_chain_symbolic_audit.py`, which closes the "previously unaudited link" from h = arccos² to the ₀F₁ derivative formulas. `abf704b` replaces the Qz certificate gate and the Qz symbolic audit. In 68bc9828, the Qz `CERTIFIED` status did not depend on the manuscript threshold, and that threshold was 0.0885587658854469. The R3 manuscript value is 0.0885587746621582. The release record still names 68bc9828 and says "eleven objects"; it was written before the two later commits |
| Independent verification | **Not present as a separate lineage.** ac and Qz import their functions from `prolate_cap_arb_certificate.py`. stage1 is exploratory and not interval-certified. No second-lineage checker was found on any branch |
| Scope | Q(4.7) > 0, Q(4.75) < 0, Q′ < 0 and H4 < 0 on [4.7,4.75]; a_c ∈ (4.72438340452113340672, …673); Qz > 0 on [4.7,4.75]. A local statement only, inside the window [2,5] |

**Verdict B for 68bc9828 as named: FAIL-CLOSED (superseded). Do not register.**

Replacement candidate, recorded but not promoted: `abf704b8701f3da8eb41d8a99408570a413b2214` (on main; last change to the directory).
- `SHA256SUMS.txt` SHA-256 `3b6fc57de63c6154165bb22ea96905cc669e8be89680175aadb0b36a9f05c11d`; 12 of 12 objects match.
- Replay: cap, ac and Qz CERTIFIED, JSON identical apart from timestamp and environment. Qz, h_chain, B2 and H4 symbolic audits all PASS.
- Still open: independent second-lineage verification.

Retargeting and the independence requirement are Judge decisions.

---

## Part 3. Replay environment and outputs

Python 3.13.16, SymPy 1.14.0, mpmath 1.3.0, python-flint 0.9.0, FLINT 3.6.0.
South scripts ran with `python3 -I` in fresh directories. The prolate scripts import a sibling module, so they ran with `python3 -E -s` from a directory holding only SHA-verified files.

## Part 4. Deviations

None this audit. Note: the summary carried over from an earlier session stated "C1b covers λ ∈ [9/20,5/8]" and "the crossing tube contract covers t ∈ [1/2,31/32] on C1b slabs" without the amendment history. Part 1.2 records that history explicitly.
