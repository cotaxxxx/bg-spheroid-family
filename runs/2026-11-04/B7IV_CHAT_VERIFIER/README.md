# B7 independent verifier (chat audit tool) — 2026-11-04

Judge decision #1: recompute every B7 leaf with an independent kernel.
This folder holds chat's verifier. It imports no Dig producer module.

- `B7IV_CHAT_VERIFIER_20261104.zip`: the package to run (SHA-256 975d31c58df4908b5f56f32b4daf0b4acdc5a64b906bf497408c74eb51c2790e). Its contents are also unpacked in `src/`.
- `evidence/`: the selftest log, the L0_T3_D1 run log and the per-leaf output of that run, all produced in chat's container.

## How to run (daybreak-works)

```
cd ~/B7_work && git -C ~/bg-spheroid-family fetch origin audit/b7iv-chat-verifier-20261104 \
  && mkdir -p b7iv && cd b7iv \
  && git -C ~/bg-spheroid-family show origin/audit/b7iv-chat-verifier-20261104:runs/2026-11-04/B7IV_CHAT_VERIFIER/B7IV_CHAT_VERIFIER_20261104.zip > B7IV.zip \
  && sha256sum B7IV.zip && unzip -o B7IV.zip && python3 -I b7iv_all.py ~/B7_work --workers 10
```

Result: `~/B7_work/b7iv/B7IV_SUMMARY.txt`. The verifier needs only numpy.
The method and its relation to the producer are described in `src/README_B7IV.md`.
