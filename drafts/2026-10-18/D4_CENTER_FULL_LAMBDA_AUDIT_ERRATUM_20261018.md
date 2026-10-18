# D4 centre all-λ audit — typo erratum (2026-10-18)

Status: **ANNOTATION ONLY**. The submitted audit and the original audit request in this directory are preserved byte-for-byte; neither is amended.

## Location

- Source: `D4_CENTER_FULL_LAMBDA_AUDIT_20261018.md`
- Section: **§3 N の下界・適用域 — PASS**
- Boxed identity `N-B(λ)`: the addition sign between the two terms is missing in the audit text.

## Correct reading (Judge-checked)

\[
N-B(\lambda)
=\left(c-\frac12\right)(1-y)
+ c^2\left[\frac4{27}-y^2(1-y)\right]\ge0.
\]

The audit file prints these two terms on separate lines without the `+`. Judge checked the identity independently and determined that this is a typographic omission only; the mathematical claim and conditional PASS are unchanged.

## Scope and provenance

- **Audit judgment:** PASS conditional on P1 §1 normalization, interior differentiation/integration exchange, and centre identification of `H` (P1 §2, Lemma V(b), Lemma 6.1 internal portion); 0 blocking findings.
- **Not asserted:** a fully information-isolated clean-room audit; positive `H` beyond the centre; a certified D4 box, a V4 selection, FREEZE, or execution authorization.
- Audit attribution: Code rederivation, as declared in the unchanged audit file. Judge noted the notation erratum on 2026-10-18.
