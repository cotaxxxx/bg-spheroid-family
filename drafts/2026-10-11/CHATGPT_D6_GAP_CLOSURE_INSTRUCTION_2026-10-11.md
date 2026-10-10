# Instruction to ChatGPT — D6 GAP closure record (chat, 2026-10-11)

**Precondition.** Do not start until the Judge confirms that the main commit saving the following is verified:
- STATE v1.17 `45841924`;
- ruling record `97860a25`;
- chat review `a2804dae`;
- Code report `6d83cba5`;
- Code addendum `587e617c`.

## Object
- `analysis/OBLATE_ENDPOINT_C1_LEMMA.md` blob `5afa815f`: EL, 109 lines.
- `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md` blob `7cb9b809`: C2, 250 lines.
- Both are in bg-oblate-spheroid `design/d-ob-p2` @ `bbcfe662`.
- **Do not modify these blobs.** No v1.1 of the lemmas and no v7.1 of the contract in this step.

## Deliverable
One file: `D6_GAP_CLOSURE_RECORD_V0.md`. Report its SHA-256 and line count.

## Required items (binding: chat review `a2804dae` §3)
Use one section per item, in this order. Each section gives:
- (a) the exact line(s) of the blob it refers to;
- (b) the statement as it should be read;
- (c) a complete short proof, or a pointer to an exact line of a pinned file that contains one.

Use "ChatGPT report L…" only together with the derivation written out again in full.

| # | Item | Expected closure |
|---|---|---|
| 1 | E-G1 | Define R := Ψ(1 − γ²) with Ψ(0) = 1; it equals α/sin α for γ < 1 |
| 2 | E-G2 | Lemma 1 holds for t ∈ [0, 1). Show why A > 0 needs t ≥ 0, and that every use is in t ∈ [1/2, 1) |
| 3 | E-G3 | ∂_t at t = 1/2 is one-sided. List every place where ① or ② uses ∂_t g at t = 1/2, and show that only one-sided or interior derivatives are needed |
| 4 | E-G4 | Continuity of g on [1/2, 1), by dominated convergence (F_t continuous in t, \|F_t\| ≤ M) |
| 5 | C-G1 | Pin the premise of C2 L50: EL `5afa815f` Lemma 3 and Lemma 5 (I = [5/8, 33/50]) |
| 6 | C-G2 | R_γ := −2γΨ′(1 − γ²) on all of §2–§4; the value at γ = 1 is −1/3 |
| 7 | C-G3 | \|H\| ≤ 2 + 2λ₊² < 4 for s ∈ [0, 1] and δ ∈ [0, 1] |
| 8 | C-G4 | −1 ≤ R_γ ≤ 0. Lower bound via R_γ + 1 = γ(R − γ)/(1 − γ²); upper bound via (sin α − α cos α)′ = α sin α ≥ 0; then the continuous extension at γ = 1 |
| 9 | C-G6 | ∂_t g is continuous on [63/64, 1), so the fundamental theorem of calculus applies |
| 10 | C-G5 (note) | No lower bound on γ is needed. R and R_γ are continuous on (−1, 1], and γ maps the compact south set into (0, 1]. Record it; do not omit it |
| 11 | ChatGPT note 2 | C2 §4 "compact north rectangle": state that (s, t) = (0, 1) is excluded and that the bounds hold uniformly for t < 1 |

## Rules
- Paper proofs only. No computation, no certificate, no change to any existing file.
- Do not touch C2 §7 item 5 (the machine Gt identity, `50ca0315`). It is out of scope.
- If any item cannot be closed without changing a lemma's **statement** (beyond E-G2's range), report it as OPEN. Do not patch it silently.
- End with a table showing items 1–11 → CLOSED / NOTE / OPEN.

## After delivery
- chat and Code audit the record.
- A PASS moves D6 to CROSS_LINEAGE_AI_AUDIT_PASS, which is the FREEZE input.
- Astra and the human external audit remain conditions for writing CLOSED in the paper.
