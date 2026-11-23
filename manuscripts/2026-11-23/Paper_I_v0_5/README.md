# Paper I v0.5 — revision record and source patch

**Date:** 2026-11-23  
**Basis:** [v0.4 fixed branch](https://github.com/cotaxxxx/bg-spheroid-family/tree/a5ab9b5016c8df9b7f94cbfd7cd0e82aeba8dd28/manuscripts/2026-11-20/Paper_I_v0_4).  
**Status:** EDITORIAL_REVISION / CONDITIONAL_THEOREM / ORIGINAL_ZIP_REGISTERED / EMBEDDED_PDF_REGISTERED. Separate standalone PDF remains pending.

## Contents registered here

- `SOURCE_DIFF_v0_4_to_v0_5.patch`: exact source diff of v0.4 `main.tex` and `sections/core.tex` to v0.5, SHA-256 `5c5fd13441dc0fadb46953e1cef116dd5d00961b3a4e6e7efa7a3fbfd67923a2`.
- `Paper_I_v0_5_Revision_Notes_JA.md`: original Japanese revision notes, SHA-256 `1425d76b85d2b4db296f622557be3c548103e13fb544377dcdd6a8e028324fa7`.
- `ARTIFACT_SHA256SUMS.txt`: records the SHA-256 of the external standalone PDF and original ZIP.
- `REGISTERED_BINARIES_SHA256SUMS.txt`: records the binary hashes actually committed here.
- `Paper_I_v0_5_Manuscript_and_Verification.zip`: the **byte-identical original source+verification bundle**; SHA-256 `ed0c20f1cb8830e7d72a94e9d3d9f7aca5a1be1b56afbb85cc44f21d1a8ab814`.
- `Paper_I_v0_5_Integrated_EN.pdf`: **the PDF embedded in the original ZIP, extracted byte-for-byte**; SHA-256 `91c5f11cd02922080ce9c2aaad9ee233d393f44e32d6977a63ffce630c6da300`.

**Binary provenance:** Both ZIP and ZIP-embedded PDF are now committed and hash-verified. The originally distributed **separate standalone PDF** (SHA-256 `c611ecc046c11eb6b5c833254dc46f969470cdc6e583b262c7edfd67d0b5a973`) has the same extracted 36-page text as the embedded PDF but **different bytes** and is **not** committed. Do not assert that the PDF in this GitHub tree is the byte-identical standalone PDF. The exact standalone PDF remains available as an earlier ChatGPT attachment until it is separately transferred and verified.

The original v0.4 branch, source evidence, and proof certification grades remain untouched. No new mathematical certification or Zenodo DOI is claimed.

## Exact edited TeX source files

The new `main.tex` and `sections/core.tex` in this directory are reconstructed from the pinned v0.4 source ZIP and the exact registered patch, then checked against the original v0.5 artifact:

- `main.tex`: SHA-256 `c12aa0df521848f7e149b05e1c7b11c86a9565f13126e259508eaa17f4c6c68c`.
- `sections/core.tex`: SHA-256 `25541c80dcf365a00a6146c2874c8b5cbedda291f9708eb7aa97935f7f028d22`.

Other source files and computational evidence are inherited from the unchanged v0.4 archive. The ZIP original is now present; the PDF here is the verified ZIP-embedded PDF, not the distinct standalone PDF.

## Reconstruction

Use v0.4's `Paper_I_v0_4_Manuscript_and_Verification.zip` (SHA-256 `57ee540bb8f3679e1b5abfaf043d6c961d934a981bddfb9d0dba0bd32a4c4d91`). Extract and apply the registered unified diff from the extracted root with `patch -p1 < SOURCE_DIFF_v0_4_to_v0_5.patch`. This restores the textual v0.5 manuscript changes; it does not guarantee byte-identical PDF typesetting or ZIP compression.

## Certification scope

- Theorem 3.1 remains conditional on computational Assertions C1–C6 and full-family status remains OPEN.
- Judge V24 CLOSED only on the oblate window λ∈[2/5,33/50].
- The sphere's Proposition 4.2 is analytic and SP-01 closed; the boundary dominated-convergence and parity passages were explanatory edits only.
- No new computational certification, Zenodo DOI, or publication is claimed.
- The v0.4 branch, `main` and `STATE.md` remain unchanged.
