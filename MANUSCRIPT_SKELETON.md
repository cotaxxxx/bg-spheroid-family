# Manuscript Skeleton — Paper I: Volume-Preserving Spheroid Family, Global (oblate → sphere → prolate)

Status: **ASSEMBLY / NOT_BINDING / SKELETON v0.3** (chat, 2026-10-10). Nothing here promotes a pin or certifies a claim.
v0.1 → v0.2: (i) prolate global is IN scope (user 2026-10-10); (ii) order oblate → sphere → prolate; (iii) series placement of Papers I–III;
(iv) submission target moved to **January 2027** ("a half-finished paper is the worst outcome"; user 2026-10-10).
v0.2 → v0.3: prolate window fixed to **λ ∈ [2, 5]** (Judge 2026-10-10); tails λ → 1⁺ and λ → ∞ removed from scope (P0 ruling); O2 status updated (R1 FAIL-CLOSED, R2 framework FROZEN at `fbadfc4d`).
Claim classes follow `RESEARCH_STATUS.md`. A row may say CERTIFIED_UPSTREAM only after its entry is verified in `UPSTREAM_PINS.md`
(currently: **no verified pins**). Pins below are locator hints for the promotion audit, not promotions.

## 0. Frame

**Series (user, 2026-10-10)**
| Paper | Object | Core result |
|---|---|---|
| I (this file) | volume-preserving spheroid family, oblate → sphere → prolate | **global** stationary structure on both sides of the sphere |
| II | volume-preserving triaxial ellipsoid family | the triangle (bifurcation set in shape space) |
| III | volume-preserving ellipsoid family | landscape and gradient field |

**Decisions in force**
| Date | Decision |
|---|---|
| 2026-09-05 | Prolate and oblate papers merged into one |
| 2026-09-06 | Venue Experimental Mathematics; oblate window λ ∈ [2/5, 33/50]; "closed world": every claim rests on a certificate, no conjecture |
| 2026-09-18 | Canon v3.3: λ gauge a₁=a₂=λ^(−1/3), a₃=λ^(2/3); λ<1 oblate, λ=1 sphere, λ>1 prolate |
| 2026-09-20 | Subject = the stationary-point structure; bifurcation is its λ-variation; certification is the method |
| **2026-10-10** | **Global on both sides is mandatory** (supersedes the 09-14/09-18 asymmetric scope and the D-PRO conditional/demotion rule). **Target: January 2027.** No partial theorem, no numbered conjecture in place of a global statement |
| **2026-10-10** | **Prolate window λ ∈ [2, 5]**: the minimal simple rational window containing λ_∂^pro ∈ [2.06538, 2.06539] (Item 0 Stage 1) and a_c ∈ (4.72438340452113340672, …673) (local certificate); left end inside the certified Item 0 range 1 ≤ λ ≤ 2.06539; right end non-degenerate (0.28 from a_c). Tails not treated |

## 1. Section plan

| § | Title (working) | Content | Main source / upstream | Status | Gap |
|---|---|---|---|---|---|
| 1 | Introduction | one family through the sphere; on both sides *boundary entry → transport → central pitchfork*; what changes is the degenerating symmetry component (axial 1-dim vs transverse 2-dim), the entry boundary (pole vs equator), the object (point pair vs circle) | 9/05 EM package intro; paper2 notes (09-03 corrected contrast) | narrative | write |
| 2 | Functional and invariances | cone-volume-weighted radial–normal angle E_K(p); probability measure; similarity invariance; volume gauge; rotation axis z (prolate repo uses y — App. C) | 9/05 EM package §3 | EXACT_ANALYTIC | reuse + gauge block |
| 3 | Basepoint bifurcation | S ⊂ Λ×P; labels (dim, normal index, nullity, isotropy) | 9/05 EM package §2 | EXACT_ANALYTIC | reuse |
| 4 | Oblate side I — the axis | axial branch t(λ): pole entry (B_ob, λ_∂^ob), transport, central pitchfork (λ_c^ob ≈ 0.4079); components C0, C1a, C1b, C1c, C1d, band [31/32,1] | bg-oblate-spheroid receipts (C1a `7f34c95d`, C1c `49cdcbb6`, C1b bridge `189ccc6d`, C0 `a2590b4c`, contract A `e56b751f`, contract B `0af9d6e1`, …) | components conditionally closed; **global cover NOT VERIFIED** (U_check = {1/2<t≤1, 2/5≤λ<9/20}) | cover diagram → C assembly |
| 5 | Oblate side II — meridian exclusion | H = E_ρ/ρ > 0 ⇒ no off-axis stationary points on [2/5, 33/50] | §2.1 below | **NOT_CERTIFIED** | D1–D6 |
| 6 | The sphere (λ = 1) | anchor theorem E′(r) > 0 | upstream to locate | TO VERIFY | locate proof + pin |
| 7 | Prolate side I — circle branch | local stationary-orbit bifurcation at a_c ∈ (4.72438340452113340672, …673), Q′<0, H₄<0, Q_z>0; equatorial entry λ_∂^pro ≈ 2.0654 (item2_circle); connected branch λ_∂^pro → a_c | basepoint-geometry manuscript `7cc5726d…`, evidence `68bc9828c3476e9db2d73d338e731c48c0931f54`; item2_circle Item 0; C-G-TUBE pilot (single slice) | local: certified upstream (not yet promoted); branch: **NOT CERTIFIED** | P1–P2 below |
| 8 | Prolate side II — meridian exclusion and window ends | E_z/z > 0 analogue ⇒ no stationary points off the equatorial plane / circle on λ ∈ [2, 5]; no branch leaves the window at λ = 2 or λ = 5 | §2.2 below | **NOT_CERTIFIED** | P3–P4 |
| 9 | Main theorem | complete classification of the stationary set along the whole family: oblate window [2/5, 33/50] and prolate window [2, 5] | §4–§8 | — | assembly |
| 10 | Phase diagram | one diagram oblate → sphere → prolate; certified values only | 09-03 figure v2 (needs R_eq/R_pol correction) | figure | redraw |
| 11 | Certification method and reproducibility | fail-closed; predeclare → audit → freeze; Bernstein / Arb certificates; exact rationals; pins | 9/05 EM package §9–10; audit records | method | write |
| 12 | Relation to center theory; outlook | Moszyńska; Herburt–Moszyńska–Peradzyński; Sakata; O'Hara; outlook to Paper II (triangle) and Paper III (landscape, gradient field; Morse-index table as input) | 9/05 EM package §11–12; literature ledger `manuscript/literature-ledger-w2` | — | write |
| App. A | Certificate checklist | theorem → certificate bytes → SHA-256 → commit | UPSTREAM_PINS.md | — | generated from pins |
| App. B | Analytic lemmas with full proofs | P1 note lemmas (3.1–3.4, 6.1, V); C-side lemmas; prolate window-end lemmas | bg-oblate-spheroid `69e10460…` and others | external audit pending | include proofs |
| App. C | Convention table | λ gauge; y↔z; D-PS = D-PRO; oblate/prolate = 扁平/扁長 | canon v3.3 TODO | — | write |

## 2. Global components

### 2.1 Oblate (D-OB), window λ ∈ [2/5, 33/50]
| # | Component | Status 2026-10-10 | Evidence / pins | Next gate |
|---|---|---|---|---|
| D1 | Pole-corner boundary face FT_q | DISCHARGED (conditional on P1 note audit); m₀ = 540861826035521/336806928254720000 | south 39′ CLOSED canonical `bbcfe6628a074d1f7b48e1f818542ee205e88f50`; Contract 45 CLOSED; Contract 43 CERTIFIED; 22″ v1.2 `d445b302…`; R-G, c_FT, BPL v1 | promote pins |
| D2 | Pole-corner interior L1 (old unresolved 4,078 points) | O1 CLOSED (P1-conditional); O2: v1 FROZEN, P0–P1 ADOPTED, v1.1-r1 (O2-A3) FROZEN, R1 FAIL-CLOSED, R2 framework FROZEN (`fbadfc4d`); O3–O6 open | branch `chatgpt/d-p2-o1-predeclare-v1-20261009` | R2 P2-b → run → O3 (hardest) → O4–O6 |
| D3 | L3–L1 connection | UNDETERMINED; Form II targeted (Judge 2026-10-10) | spec v1 `ecd31446…` | follows D2 |
| D4 | Centre band (λ ≈ 0.6–0.66; old unresolved 3,584 points) | NOT STARTED | — | method + design |
| D5 | General region (interval main run, roadmap No.28) | NOT RUN | old SPEC V2 producer/checker; resume `c0f099f9` | contract re-ruling → run → receipt |
| D6 | External audit bundle | P1 Lemma V + C-side 5 lemmas PENDING | — | send bundle / full proofs in App. B |

### 2.2 Prolate (D-PRO), window λ ∈ [2, 5]
| # | Component | Status 2026-10-10 | Evidence / pins | Next gate |
|---|---|---|---|---|
| P0 | Scope of the prolate global statement | **DECIDED**: λ ∈ [2, 5] (Judge 2026-10-10); tails not treated | basepoint-geometry main `abf704b8`, CERTIFICATES/prolate | — |
| P1 | Local bifurcation at a_c | certified upstream (9/05) | `68bc9828…`, `CERTIFICATES/prolate/local_bifurcation/SHA256SUMS.txt` | promote pins |
| P2 | Connected circle branch λ_∂^pro → a_c, incl. equatorial entry (item2_circle; B-KERNEL debt for λ > 2.0654) | pilot single slice only (C-G-TUBE r4); B-TUBE/B-LOCAL partially certified | basepoint-geometry Actions receipts; bg-prolate-spheroid (diagnostic) | transplant oblate C1b contract stack (λ-slab; ~2,400 slabs at width 1/800 on [2, 5], rough scaling, not certified) |
| P3 | Meridian exclusion on [2, 5] (no off-equator / off-circle stationary points), incl. (a_c, 5] after loss of center stability | NOT STARTED | D-OB tooling (FT_q-type boundary pair, Bernstein certificates) as template | design (E_z/z > 0 form, 09-17) |
| P4 | Window ends: equator has only the center at λ = 2 (Item 0, certified for 1 ≤ λ ≤ 2.06539); structure at λ = 5 non-degenerate and no branch exits | λ = 2 side covered by Item 0; λ = 5 side NOT STARTED | Item 0 (2048 leaves) | design |
| P5 | External audits (prolate lemmas) | — | — | with D6 |

## 3. Plan to January 2027

Owners (suggestion): D-OB interior D2 (ChatGPT) ∥ D4 centre band (Astra) ∥ D5 run (Code / research PC) ∥ P4 window ends (Astra, after D4 design) ∥ P2/P3 (Code + ChatGPT) ∥ manuscript and pin promotion (chat drafts and audits; user commits).

| By | Milestone |
|---|---|
| 10/17 | (P0 decided 10/10: [2, 5]); D5 contract re-ruled and run started; D4 method fixed; U_check checked; first pins promoted (south 39′, prolate local); §1–3, §7 (local part) drafted |
| 10/31 | D2 O2 R2 run status (closure not guaranteed); D4 certificates; P3 design frozen; P4 plan |
| 11/07 | Checkpoint 1: remaining work quantified for both sides; submission month confirmed |
| 11/30 | **Oblate global closed** (D1–D5, §4 cover); §4–§5 drafted |
| 12/25 | **Prolate global closed** on [2, 5] (P2–P4); §7–§8 drafted |
| 1/15 | Full assembly; App. A generated from verified pins; internal final audit |
| 1/31 | Submission (EM) |

Consequence to record: Paper II (triaxial) start, planned for December (09-06), moves after Paper I submission.

## 4. Rules for this file

- Version-up only; never edit a promoted pin row in place.
- A section moves from "write" to "drafted" only with a commit hash of the draft.
- No number enters the manuscript unless its certificate is pinned in `UPSTREAM_PINS.md`; diagnostic values never enter theorem statements.
