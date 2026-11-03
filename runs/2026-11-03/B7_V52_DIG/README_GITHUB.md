# B7 V5.2 Dig candidate for chat independent implementation audit

2026-11-03 JST. **D0 8/8 PASS (previous audits). B7 overall 8/40 PASS; D1–D4 OPEN.**

- [Canonical ZIP](B7_V52_DIG_CANDIDATE_20261103.zip): 29 files, 71,666 bytes, SHA-256 `aad05860faf77ae53346e25e997004856ee485736ff5ead4e02f797781757f85`. **Use the ZIP for exact-byte audits.**
- [Implementation/audit instructions](README_DIG_V52_20261103.md)
- [V5.2 producer](v6_b7_unified_outerrem_v52.py)
- [ASTRA3 fourth cellwise floor](b7_astra3_v52.py)
- [V5.1→V5.2 checkpoint recertifier](dig_b7_v52_recert.py)
- [V5.1→V5.2 source diff](V51_TO_V52_DIFF_20261103.patch)
- [Manifest](SHA256_MANIFEST_V52_20261103.txt)
- [Synthetic test exact ledger](V52_TEST_RESULTS_20261103.json)
- [D1 6-box 256-leaf sampled effect (not evidence)](V52_ASTRA3_256_SAMPLE_D1_20261103.json)

V5.2 uses proven Astra second lemma F ≥ −b3[1−3ρ/2]+ with ρ=G²/T². Outer δ is split into rational slabs; the worst/slab MIN is used, never a sum. Existing MIDPOINT, ZEROTH, K floor and contact are unchanged. Synthetic 8-leaf source+recert tests PASS. Sample 1,536 active D1 K-floor small-p leaves show improvement, **not global certification**.

**V5.2 implementation independent audit PENDING. V5.1 production remains running; do not launch V5.2 32-box production until chat passes.**
