# Paper I v0.5 — revision record and source patch

**Date:** 2026-11-23  
**Basis:** [v0.4 fixed branch](https://github.com/cotaxxxx/bg-spheroid-family/tree/a5ab9b5016c8df9b7f94cbfd7cd0e82aeba8dd28/manuscripts/2026-11-20/Paper_I_v0_4).  
**Status:** EDITORIAL_REVISION / CONDITIONAL_THEOREM / PARTIAL_ARTIFACT_REGISTRATION.

## Contents registered here

- `SOURCE_DIFF_v0_4_to_v0_5.patch`: exact source diff of v0.4 `main.tex` and `sections/core.tex` to v0.5, SHA-256 `5c5fd13441dc0fadb46953e1cef116dd5d00961b3a4e6e7efa7a3fbfd67923a2`.
- `Paper_I_v0_5_Revision_Notes_JA.md`: original Japanese revision notes, SHA-256 `1425d76b85d2b4db296f622557be3c548103e13fb544377dcdd6a8e028324fa7`.
- `ARTIFACT_SHA256SUMS.txt`: identifies original v0.5 PDF and ZIP bytes in the ChatGPT artifact workspace.

**Important limitation:** The finished v0.5 **PDF and verification ZIP are not present in this GitHub tree**. This directory preserves their hashes and the exact editorial source patch, not their binary payloads. Do not label it a complete archived PDF release. To finish the original-byte registration, the matching PDFs and ZIP must be transferred into the GitHub-capable filesystem and their SHA-256 values checked before commit. Do not silently replace them with a fresh LaTeX build.

## Reconstruction

Use v0.4's `Paper_I_v0_4_Manuscript_and_Verification.zip` (SHA-256 `57ee540bb8f3679e1b5abfaf043d6c961d934a981bddfb9d0dba0bd32a4c4d91`). Extract and apply the registered unified diff from the extracted root with `patch -p1 < SOURCE_DIFF_v0_4_to_v0_5.patch`. This restores the textual v0.5 manuscript changes; it does not guarantee byte-identical PDF typesetting or ZIP compression.

## Certification scope

- Theorem 3.1 remains conditional on computational Assertions C1–C6 and full-family status remains OPEN.
- Judge V24 CLOSED only on the oblate window λ∈[2/5,33/50].
- The sphere's Proposition 4.2 is analytic and SP-01 closed; the boundary dominated-convergence and parity passages were explanatory edits only.
- No new computational certification, Zenodo DOI, or publication is claimed.
- The v0.4 branch, `main` and `STATE.md` remain unchanged.
