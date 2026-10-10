# CHAT AUDIT — three predeclare drafts v0 (2026-10-10)

Baseline: bg-spheroid-family main `32218d7855e3e6218dddbe315eacb38cd2dd8295` (STATE v1.12), with the audit record `b77fbc17…67e4`.
Drafts audited: (1) C gap ① v0, (2) C gap ② v0, (3) prolate local second-lineage v0. All three are labelled DRAFT / NOT FROZEN / EXECUTION PROHIBITED.
No computation was run for this audit. The sources were read on GitHub only.

## Overall result

| Draft | Verdict | Can it be FROZEN now? |
|---|---|---|
| ① U_1 | CONDITIONAL PASS as a framework; revise to v1 (M1–M5) | No. The numeric contract is missing (the draft itself says CONTRACT_INCOMPLETE) |
| ② U_2 | CONDITIONAL PASS as a framework; revise to v1 (N1–N4) | No. The same applies |
| ③ prolate second lineage | CONDITIONAL; revise to v1 (P1–P5). P4 needs a Judge decision first | No |

The good parts, kept as they are:
- ① and ② agree on the boundary λ = 9/20. ① covers λ < 9/20 only, and ② covers λ = 9/20 together with 31/32 < t < 1. The interior of t = 1/2 is excluded from ①. There is no overlap and no gap.
- ② fixes the method and the obligations **before** the ledger is read, and uses the ledger only to list cells. This is the order I asked for.
- ③ requires that formulas are not copied, and says explicitly that translating the ₀F₁ chain into another language does not count as independent.

---

## (1) C gap ① — U_1 = {1/2 < t ≤ 1, 2/5 ≤ λ < 9/20}

**M1 (major) — identifying the machine quantity with ∂_t g.** The C1b Judge request (`f7d59da0`) explicitly does not claim that the machine quantity Gt equals ∂_t g. G2 and G4 need exactly that identification on λ ∈ [2/5, 9/20] and t ∈ [1/2, 1). Make it a named proof obligation (an interchange lemma on this domain). The existing C2 interchange lemma covers only [5/8, 33/50] × [63/64, 1].

**M2 (major) — "接する根" (tangent root) at λ = λ_x is the wrong picture.**
- C1a certifies that F_x = 2g(1/2,·) is strictly increasing. So at λ = λ_x the root **crosses** t = 1/2; it does not touch it tangentially.
- Transversality at the point itself already follows from the existing receipts. Write g = tΦ(t²). Then ∂_t g(1/2, λ) = Φ(1/4, λ) + (1/2)∂_τΦ(1/4, λ). At λ_x, Φ(1/4, λ_x) = 0, so ∂_t g(1/2, λ_x) = (1/2)∂_τΦ(1/4, λ_x). C1a gate A (∂³g < 0 on [0,1/2]) gives ∂_τΦ < 0 through the C0 contract identity, so ∂_t g(1/2, λ_x) < 0. This step is conditional on lemma 6fba6e4f (external audit pending).
- What remains is not a bifurcation question. It is the uniform statement ∂_t g < 0 on [1/2, t_R] × [699/1600, 281/640], and M3 supplies exactly that. The branch from the center pitchfork (λ_c) then passes from (0,1/2) into (1/2,1] at λ_x. No separate "local bifurcation lemma" is required.

**M3 (recommended structure) — replace G2/G3/G4 with one per-slab form.** For each exact rational λ-slab Λ:
- (i) ∂_t g < 0 on [1/2, t_R] × Λ;
- (ii) g < 0 on [t_R, 1] × Λ, where the face t = 1 is B_ob;
- (iii) then g(·,λ) has at most one zero in (1/2, 1], and the sign of g(1/2,λ) (C0b/C1a) decides whether it is 0 or 1.

This handles λ ≤ λ_x and λ > λ_x the same way. It avoids splitting at the irrational λ_x. The only special handling is the λ_x box, and M2 covers it. It is also the same logical shape as C1b, so G5 (joining at 9/20) reduces to closed boxes overlapping on the line λ = 9/20.

**M4 (minor) — "原典で定義された axial census の要件" must be cited by path and blob.** As written it is not checkable.

**M5 (blocker, already acknowledged) — the numeric contract.** Fix in v1: the slab width, the cap, how many stages, the precision, how boxes that touch t = 1 are evaluated (see N2), a separate checker, the work ceiling, and the FAIL-CLOSED words.

G1 (B_ob < 0 on [2/5, 9/20]) is correctly stated as an unproven premise. Keep the rule that if it fails there is a new draft and no switching of methods during a run.

## (2) C gap ② — U_2

**N1 (major) — define U_2 exactly.** "t > t_plus(λ) または既存 tube/exterior で未被覆" is too loose. Use

U_2 = ⋃ over unclamped accepted slabs Λ of Λ × (max(31/32, t_plus(Λ)), 1).

Here t_plus(Λ) is per-slab ledger data. The exterior cover in contract §5 ends at 31/32, and the tube covers up to t_plus. Λ_unclamped is the union of those slabs and does not have to be an interval (unclamped slabs can sit between clamped ones above 931/1600).

**N2 (major) — boxes that touch t = 1.** "t=1 は端点補題で処理" is not a method. A closed sign certificate on (t*, 1) needs enclosures that stay valid up to t = 1. The C1b history includes an endpoint non-finite amendment (v2.6), so this point is known to be fragile.
- Declare the evaluation that will be used for boxes [t_k, 1] × Λ. Candidates: the two-chart B_ob kernel, or a stated interchange lemma for this λ range.
- Alternatively, declare a fixed cut-off t_e < 1 plus a separate argument on [t_e, 1].

**N3 (minor) — name the ledger.** Give the ledger file path and its blob or SHA-256 in v1, before anyone reads it. The draft says "the sealed ledger"; the audit needs the exact object.

**N4 (minor) — use the same words as ①.** "g < 0 on [t_plus, 1]" is per slab, so N2 also covers ①'s boxes near t = 1. It would be cleaner to declare one shared endpoint method used by both ① and ②.

## (3) Prolate local — second lineage on `abf704b8`

**P1 (resolved — the source is available).** The R3 manuscript is in basepoint-geometry, branch `paper1-certchain-202609`, path `01_KAKURON_I/1_楕円体系列/1-2_長球/submission_experimental_mathematics/manuscript.tex`, last change `7cc5726d62f063803b6d83cb9ba5fda5fd91f72c`, SHA-256 `4b30c2b2ed4dbbc6eb9439c74eb0d30ef95187df8ff70c9c9820bf886c74a257`.
- It gives the full 20-digit bracket 4.72438340452113340672 < a_c < 4.72438340452113340673.
- It gives the definition Q_z(a) = ∫₀^{π/2} s F_z″(0) dθ.
- It gives the bound "rigorous lower bound 0.0885587746621582".
- So item 4's SOURCE_INCOMPLETE condition does not arise. Pin this file in v1.

**P2 (major) — SageMath RBF is not independent.** SageMath's RBF is Arb, the same FLINT ball arithmetic that lineage 1 uses through python-flint. Using it shares the arithmetic core.
- Remove RBF as an option, or label it "partial independence (formula only)".
- Fully independent choices: Julia IntervalArithmetic.jl, mpmath `iv`, or MPFI/INTLAB.
- Julia has no built-in rigorous integrator, so a validated quadrature with an explicit remainder bound has to be written and audited. That is real work; the effort estimate must include it.

**P3 (major) — how clean-room independence is enforced.** Code can reach the basepoint-geometry repository, so "参照しない" needs a mechanism:
- a fresh sandbox with no clone of the repository;
- an input pack containing only the manuscript definitions (pinned by SHA);
- a signed independence attestation;
- Astra's formula audit done before any comparison with lineage 1.

**P4 (Judge decision needed) — two gates are tied to lineage-1 artefacts.**
- **Qz gate.** The threshold 0.0885587746621582 is lineage 1's worst lower endpoint, 0.08855877466215827082…, rounded down. The margin is only about 7×10⁻¹⁸. The worst lower endpoint over a parameter box depends on the method and on the partition. A sound second lineage can fall below this threshold even though Q_z is in fact far above it. That outcome would be a false FAIL caused by the method, not by the mathematics.
- **20-digit a_c.** A bracket of width 10⁻²⁰ needs absolute accuracy around 10⁻²¹ to 10⁻²² in Q. With a validated quadrature written from scratch this is the most expensive gate by far.
- In the manuscript, the proof itself uses only Q_z(a_c) > 0 and a_c inside the bracket. The specific numbers are reported quantities.
- The paper needs to state only what two lineages can certify. See the question to the Judge.

**P5 (minor) — two failure classes.** CERTIFICATE_FAILED (inconclusive enclosure) and a genuine sign contradiction between the lineages must be recorded separately. A genuine contradiction stops everything and triggers an audit of both lineages.

---

## Summary of what each draft needs for v1

| Draft | v1 must add |
|---|---|
| ① | M1 interchange obligation, M2 transversality on the λ_x box, M3 per-slab structure (recommended), M4 census citation, M5 numeric contract, a shared endpoint method (N2) |
| ② | N1 exact U_2, N2 endpoint method, N3 ledger path and SHA, the numeric contract |
| ③ | P1 manuscript pin, P2 library (no Arb), P3 enforcement of independence, P4 per the Judge's ruling, P5 failure classes, effort including the validated quadrature |

Nothing is frozen. No computation is authorized.

---

## Judge rulings (2026-10-10, after this audit)

1. **P4: tiered gates.**
   - Required gates for the second lineage: Q_z ≥ q₂ > 0 on [4.7, 4.75], where q₂ is a rational number fixed in v1 before any run; the 5-digit bracket 4.72438 < a_c < 4.72439; Q′ < 0 and H4 < 0 on [4.7, 4.75].
   - Separate gates: the 20-digit bracket, and Q_z ≥ 0.0885587746621582. Failing a separate gate does not fail the required gates; it is recorded with its own outcome.
   - Paper I states as certified only the values that both lineages pass.
2. **All three drafts: revise to v1.** ChatGPT drafts complete v1 versions that include M1–M5, N1–N4 and P1–P5. chat audits each v1, and only then is FREEZE considered. Nothing runs before that.
