# B7 D0 independent audit — Judge's report, 2026-11-03 JST

**Provenance:** Judge reported the chat independent audit outcome to Dig.
This is a transcription of that report, not an independently re-run
audit by Dig. The specifically named original files
CHAT_V5_RECERT_AUDIT_3BOXES_20261103.txt and
chat_b7_pass_audit_v5.py were NOT supplied as standalone byte files in
this Dig handoff; their original SHA-256 values are not asserted here.

## Status

D0 8/8 outer boxes: Judge reports independently audited PASS.
B7 overall 8/40: OPEN; D1-D4 (remaining 32) OPEN.

Existing V4 PASS boxes:
L0_T0_D0, L0_T1_D0, L1_T0_D0, L1_T1_D0, L1_T2_D0.

Three V5 reauthenticated, chat independently audited per Judge:

| key | prior -> V5 | leaves | J lower approx | final lower approx |
| --- | --- | ---: | ---: | ---: |
| L0_T2_D0 | V4 -> V5 | 97996 | +0.0504 | +0.01277 |
| L0_T3_D0 | V4.1 -> V5 | 61814 | +0.791 | +0.2013 |
| L1_T3_D0 | V4.1 -> V5 | 63155 | +0.800 | +0.2202 |

Judge reports archive SHA256:
310cbcb5fe6651e7beb77859db4c6c77e05b232af1ddfb33dd15dd7f6978bc1f.
Recomputed producer source fingerprint:
60af4bcff222e9cd411b61926e22e6e1a784a6ef2d1935851a815a623aeab2dd.

Judge reports ALL CHECKS PASS in each box for:
- exact source SHA/fingerprint and byte-identical common kernels;
- every leaf: independent rational K'=275/4 floor, selected max,
  tie-breaking and main/remainder bookkeeping;
- rigorous disjoint leaf coverage with no gaps;
- exact rational sum, contact loss and final lower;
- 80 sampled leaf kernel recomputations per box (240 total),
  byte-for-byte integer endpoint match using the frozen producer kernel;
- floating-point reference checks across three outer sample points,
  no detected violations.

Limitations explicitly acknowledged by Judge:
- only 240 sampled leaves recomputed, not all leaf kernel bounds;
- sampled recomputation uses the frozen production kernel, not an
  independently implemented interval kernel;
- original checkpoint copies on Ubuntu PC not checked by chat;
- final global 40-box theorem not established.

This record is supplied for Claude's V5.1 audit and does NOT
assert an independent V5.1 audit result.

**D0 8/8 reported PASS; B7 overall OPEN.**