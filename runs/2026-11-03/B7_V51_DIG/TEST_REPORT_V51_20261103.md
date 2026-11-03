# B7 V5.1 — diagnostic test outcomes
Date 2026-11-03 JST. This is a **synthetic band test only**; NOT a proof of B7.

## Exact dyadic interval comparison
All 64 initial leaves: same intervals for main, zeroth, four remainder terms, total; same K floor and selected lower. Mismatches: **0**.

## Same 64-cell difficult band (L0_T3_D0)
y interval [0.562341325190349...,1], p=[0.00001,0.0001], t,u each split into four quarters.
The test monkeypatches contact loss to 10 for both versions, forcing computation to avoid premature PASS. Source files on disk are not changed.

| refinement settings | V5 inner splits | V5.1 inner splits | V5 leaves | V5.1 leaves |
| --- | ---: | ---: | ---: | ---: |
| inner-only (1,1,1); delta/rem=1 | 0 | 150 | 64 | 214 |
| normal (2,2,4); delta=16, rem=4 | 0 | 150 | 64 | 214 |

J lower at displayed precision for both: **-0.018312539812744152**.
Exact difference V5.1 minus V5: **-9/42535295865117307932921825928971026432 = -72/2^128**, due to outward rounding on newly split leaves. This is not a lower-bound improvement.

## Interrupted run / resumed run
At 20 inner splits, os._exit(42) ran immediately after a durable, atomically replaced checkpoint.
Resume to 150 splits matched uninterrupted execution exactly.
Leaf SHA256: `6b04863eaf217f0e41baa99d9f3c0f292a4f89822182d3f0caf900e226f00129`.

## V5.1 reauthentication from V4.1 checkpoint
L0_T0_D1, 38,749 leaves, exact old SHA and new fingerprint PASS in smoke test; final lower still NEGATIVE. No D1 PASS is asserted.

**Verdict: V5.1 algorithmic fallback, 64-cell interval equivalence, and checkpoint resume — diagnostic PASS.**
**Independent Claude production audit still pending. D1-D4 NOT started.**