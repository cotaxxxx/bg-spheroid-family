# B7 V5 — Dig submission for Claude independent audit

2026-11-03 JST. **B7 global status: OPEN.**

This dated directory preserves the V5 producer, recertification tool,
Astra's exact analytical floor lemma, E3 symbolic verification,
three proof certificates, and Dig's internal preflight logs.
No earlier V4/V4.1 files have been replaced.

## Download

- [Complete three-box certificates ZIP](B7_V5_DIG_3_CERTIFICATES_20261103.zip)
  (74,130,137 bytes, SHA-256
  `310cbcb5fe6651e7beb77859db4c6c77e05b232af1ddfb33dd15dd7f6978bc1f`).
  Includes the original small source ZIP plus three complete leaf JSON files.
- [Source and preflight ZIP](B7_V5_DIG_SOURCE_AND_AUDIT_20261103.zip)
  (56,486 bytes, SHA-256
  `4d1ae6fe84c33e695734136ee3b3e0a1a4de22d45c6c0d5095ee1f3619eb1073`).
- [Full details](README_DIG_V5_20261103.md), [math lemma](ASTRA_FLOOR_LEMMA_V5_20261103.md),
  [E3 symbolic verifier](chk_e3_symbolic.py), [per-file hashes](SHA256_MANIFEST.txt).

A GitHub browser may report "file too big to display" for the large ZIP;
use the **Download raw file** button rather than previewing it.

## Certified by Dig preflight, pending Claude audit

| Outer box | Leaves | Dig preflight final lower | Status |
| --- | ---: | ---: | --- |
| L0_T2_D0 | 97,996 | 0.012767215840096779… | Positive; independent audit OPEN |
| L0_T3_D0 | 61,814 | 0.2012625877603263… | Positive; independent audit OPEN |
| L1_T3_D0 | 63,155 | 0.22020219047607834… | Positive; independent audit OPEN |
| L0_T0_D1 | 34,720 | negative | OPEN (no positive certificate) |

The floor is rigorously F >= -275/4. Both the contact-strip
loss and per-cell floor use the new constant.
The original interval-cached midpoint and zeroth candidates are unchanged.
For all three candidate PASS boxes, internal Dig preflight verified exact
leaf coverage, all floor selections, rational sums and contact losses, plus
16 leaf kernel recomputations per box. This is **not** an independent audit.

## Claude audit checklist

1. Verify both archive SHA-256 values and the per-file SHA manifest.
2. Independently reproduce the E3 symbolic proof and SOS floor derivation.
3. Verify unchanged frozen V4/V4.1 source SHA and original checkpoint
   provenance; original checkpoint snapshots are held on daybreak-works.
4. Independently verify every leaf's exact geometric covering,
   K floor, max(MIDPOINT, K_FLOOR, ZEROTH), and rational sums.
5. Recompute final lower bound with 2*lambda_hi*(275/4)*sigma0.
6. Independently recompute chosen leaf kernel intervals, checking
   recorded dyadic endpoints against the frozen production source.
7. Do not count a box as independently PASS until evidence is complete.

**These materials are evidence submitted for audit, not the final
independent verdict. B7 remains OPEN.**
