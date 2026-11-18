# Explicit short interactive run: pre-run frozen subset of 24h slab experiment
2026-11-18 — DIAGNOSTIC_ONLY / NOT_EVIDENCE

Purpose: exercise actual 12-worker execution, atomic checkpoints, exact
area accounting, and measured wall/RSS on a genuine, fixed subset.
**NOT** the full 24-hour slab experiment.

At the first run only:
`python -m prolate_r4.slab_adaptive --workers 12 --max-batches 1 --session-seconds 620`.

- One initial batch of exactly 12 boxes, selected by the immutable
  bit-reversed Morton order in `COVER_RULE_FREEZE.md`.
- All box timeout limits as frozen in that document (AX/CENTER600,
  BOUNDARY300, REGULAR180). Session 620 sec gives each member
  its FULL individual timeout, with 2-sec controller reserve.
- Settle all 12 results in deterministic ID order and checkpoint.
- Stop and produce a PARTIAL summary; do not claim decided + evaluated
  tube area = 1 while pending boxes remain.
- Resume may continue with the same branch and `--session-seconds`,
  charging cumulative elapsed time toward the overall 86400-sec cap.
- W selection and 3-box W sample are deferred until a completed
  slab or the actual overall hard cutoff, per `COVER_RULE_FREEZE.md`.

This subrun's results are **empirical measured partial slab data**,
not a claimed full slab survey or global extrapolation.
