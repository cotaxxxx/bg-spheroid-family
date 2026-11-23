# Paper I v0.5.3 — editorial revision archive (partial binary registration)

**Date:** 2026-11-23  
**Status:** EDITORIAL_CANDIDATE / NOT_YET_DIFFERENCE_AUDITED / SOURCE_REGISTERED / ORIGINAL_BINARIES_PENDING / NOT_PUBLISHED.  
**Parent version:** Paper I v0.5.2. The source diff against v0.4 is also preserved.

## Source and verification files

- `SOURCE_DIFF_v0_4_to_v0_5_3.patch` is the exact revision patch against the fixed v0.4 source.
- `SOURCE_DIFF_v0_5_2_to_v0_5_3.patch` contains the limited editorial follow-up.
- `Paper_I_v0_5_3_Revision_Notes_JA.md` preserves the Japanese revision report.
- `Paper_I_v0_5_3_ARTIFACT_SHA256SUMS.txt` records the hashes of the originally created PDF, ZIP, and patches.
- `main.tex` and `sections/core.tex` are exact source files reconstructed from the fixed v0.4 source and the v0.5.3 patch, with independently verified original ZIP SHA-256 values (recorded below), once present.

## Artifact identity and limitation

The *original v0.5.3 PDF and ZIP binaries are NOT yet included in this repository*. Their externally verified SHA-256 values are:

- `Paper_I_v0_5_3_Integrated_EN.pdf`: `2054ebe7eeb194351e836bb32ae10e5ff62a0073d03bfb8f5d198b77c196ccc4`.
- `Paper_I_v0_5_3_Manuscript_and_Verification.zip`: `5be67aae44517525180a1524b1336ea45a63a35f12905e0527caad67a3a56c5d`.

The original ZIP's internal 153 SHA-256 entries and ZIP CRC passed in the ChatGPT artifact workspace. This GitHub branch must not be labeled a full byte-identical binary release until the original PDF and ZIP are transferred and verified.

Source identity from original ZIP:
- `main.tex`: `7ce92fbaeb1f93a216a67eabd2f07b3765400b14dd12c8c4bf8479ed5c80099b`.
- `sections/core.tex`: `84532ef7cfb41b2abcb29ea94e5fc5d091a4ab6460ce2ad16989f6037ce220e0`.

## Evidence and certification scope

Theorem 3.1 remains conditional on C1–C6; no mathematical classification or evidence grade has been upgraded. The oblate verification applies only to `lambda in [2/5,33/50]`, and the sphere's Proposition 4.2 is analytic. Editorial revision addresses wording about AI-assisted audit, disclosure, path visibility, and metadata. This candidate has not been newly approved by an independent diff audit and has NOT been posted to Zenodo.

Primary oblate record: `cotaxxxx/bg-spheroid-family`, commit `127be52046e9498d1306fe3d35c3e02e91c636de`, path `runs/2026-11-16/D_OB_GLOBAL_CLOSED_V24/JUDGE_RULING_D_OB_GLOBAL_CLOSED_20261116.md` (original Japanese record; no mathematical proof status changed).

The v0.4 and v0.5 branches and `STATE.md` are unchanged.
