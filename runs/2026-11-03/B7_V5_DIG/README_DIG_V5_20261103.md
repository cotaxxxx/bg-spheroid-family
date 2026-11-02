# B7 V5 — Dig handoff package (2026-11-03 JST)

Prepared on daybreak-works by Dig (ChatGPT). This package is NOT an independent chat/Muse audit.

## Mathematical change and implementation

The Astra E3/SOS lemma proves F >= -275/4 on the whole target domain.
Old K_Q = 859375/64; new K' = 275/4; ratio = 16/3125.
V5 is based on the FROZEN V4.1 producer and retains its search priority
(including the zero-gain queue-drop behavior). V5 is NOT V4.2.

The new exact-rational constant from b7_constants_v5.py is used BOTH
for contact loss (2*lambda_hi*K'*sigma0) and the per-cell K floor.
The producer's SHA, fingerprint and bound-policy tag are changed.
Midpoint and zeroth intervals remain exactly the original enclosures.
All 8 shared mathematical source files are byte-for-byte from V4.1.
The legacy b7_constants_v3.py remains bundled as an unchanged dependency
of the priority/grid helper; its contact() function is NOT called by V5.

V5 fingerprint:
60af4bcff222e9cd411b61926e22e6e1a784a6ef2d1935851a815a623aeab2dd
V5 producer SHA256:
3e7752ef6258246aefbbefb85c0e04b8a25ec02196a585692f85d301fb7e9f8f
V5 constants SHA256:
3d766084caabc5738ea3de70068d688635e6b565a0a8fbe29d14c18ccec3c9c0

## Supplied files

- v6_b7_unified_outerrem_v5.py — V5 exact producer
- b7_constants_v5.py — exact new constant
- dig_b7_v5_recert.py — old checkpoint-to-V5 recertifier
- dig_v5_preflight_audit.py — internal exact audit / sampled recomputation
- chk_e3_symbolic.py — E3 Groebner proof (original SHA 71da410f...)
- ASTRA_FLOOR_LEMMA_V5_20261103.md — formal proof
- unchanged shared production sources, prior lemma, SHA256_MANIFEST.txt
- REPORTS — small provenance reports and Dig preflight logs
- CERT_META — small result JSON metadata and leaf SHA256 values

Complete leaves files and immutable original checkpoint snapshots are
preserved on the authorized Ubuntu PC, but not in the small source ZIP.
A separate CERTIFICATES ZIP contains the three full leaf files.
Original snapshots are hundreds of MB and remain on the PC.

## Recertification process

Run from ~/B7_work/b7_v5_dig.
Use one fresh destination per origin (never the original output folder).

Example (L0_T3_D0):
python3 -u dig_b7_v5_recert.py --origin /home/daybreak/B7_work/b7_v41/full_v41_t3/L0_T3_D0_full.checkpoint --origin-version v41 --dest recertified_t3 --max-leaves 150000 --max-depth 24

Then generate the final result/leaf certificate from the V5 state:
python3 -O v6_b7_unified_outerrem_v5.py --mode full --workers 1 --max-leaves 150000 --max-depth 24 --checkpoint-every 200 --keys L0_T3_D0 --max-delta-boxes 16 --max-rem-parts 4 --max-rem-kernel-boxes 32 --out-dir recertified_t3

Internal exact preflight (not independent):
python3 -u dig_v5_preflight_audit.py recertified_t3/L0_T3_D0_full.json --version v5 --no-float --recompute 8

The recertifier:
1. makes a byte-for-byte snapshot of the ORIGINAL checkpoint;
2. verifies its source SHA/fingerprint and source compatibility;
3. checks old floor/selected bound and exact old aggregates on every leaf;
4. recomputes NEW floor and selected bound on every existing leaf;
5. updates the V5 contact loss, fingerprint, policy, heap scores and sums;
6. writes a NEW checkpoint with a separate provenance manifest.

It never overwrites the original. It refuses overwriting recert outputs.
Unpickle ONLY checkpoints from the authorized machine (pickle is unsafe
for untrusted files). The resulting future search order can differ.

## Actual results on 2026-11-03

key, origin, leaf count, V5 final lower (decimal display), Dig preflight
L0_T2_D0, V4,  97996, +0.012767215840096779, PASS
L0_T3_D0, V41, 61814, +0.2012625877603263,   PASS
L1_T3_D0, V41, 63155, +0.22020219047607834,  PASS
L0_T0_D1, V41, 34720, NEGATIVE,              OPEN

The three positive certificates passed:
- all source SHA and producer fingerprint checks;
- exact per-leaf K floor / three-way selection;
- exact partition (guillotine check), no gaps and overlaps;
- exact rational total, contact loss, and final positivity;
- 16 source-kernel leaf recomputations each; 0 mismatches.
These are Dig's own preflight checks, not independent chat/Muse PASS.

Full original checkpoint snapshots and recertified results on PC:
~/B7_work/b7_v5_dig/recertified_v4_t2/
~/B7_work/b7_v5_dig/recertified_t3/
~/B7_work/b7_v5_dig/recertified_d1_sample/

The D1 example has NEGATIVE final and cannot be certified positive.
Other D1-D4 boxes remain OPEN until separately recalculated and audited.

## Limitations and independent audit requirements

- V5 retains V4.1's gain<=0 queue-drop: search effectiveness OPEN.
- Recertified heap is reconstructed, not a byte-identical replay.
- Status PASS from producer is NOT final independent audit PASS.
- Original kernels are only reused after SHA equivalence and old
  per-leaf bookkeeping checks; sample the old kernel independently.
- Cover geometry from full final leaves and verify all NEW leaf floors,
  sums, and rational final bounds.
- No checkpoint is directly unpickled as an untrusted artifact.
- B7 GLOBAL STATUS: OPEN (all 40 outer boxes not yet certified).
