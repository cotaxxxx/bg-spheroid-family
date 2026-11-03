# B7 V5.2 independent-audit certificate batch 001

Published 2026-11-04 JST. Certificates: L0_T2_D1, L0_T3_D1

Producer full PASS, local pre-audit ALL CHECKS PASS; independently confirmed only when each entry in MANIFEST.json says so. Formal B7 tally remains 9/40 until chat independent audits each new certificate.

Use source fingerprint 985c3abe248d1f17de15ae6cc11b71987978662a97c8fb31e06da88ad34ae70d. Sources are pinned by prior commit 37c75b3bf4f4f1cf5673f1a1172b9885248fff7b.

To audit each box, decompress <key>_full.leaves.json.zst to <key>_full.leaves.json, verify the raw SHA256 against MANIFEST.json, then run the independent checker chat_b7_pass_audit_v5.py <key>_full.json --version v52 --no-float. Every key has the original producer result and local pre-audit log for reference.
