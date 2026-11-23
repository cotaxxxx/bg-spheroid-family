# Paper I v0.5.4 — major-revision response candidate (2026-11-23)

**Parent:** Paper I v0.5.3, source branch paper/paper-i-v0.5.3-20261123, commit 354ffaabc1be34618c182fcc9aebbb20e7e73333.

**Review prompting this version:** Codex review dated 2026-11-23, governance repository cotaxxxx/experimental-mathematics-ai-collaboration commit f5f345f0e580dfaec91b123a8b7af566205ebfb0, docs/CODEX_REVIEW_PAPER_I_V0_5_3_20261123.md.

**Status:** EDITORIAL/ARGUMENT-ASSEMBLY REVISION; C1–C6 CONDITIONAL; FRESH INDEPENDENT REPLAY NOT CLAIMED; AUTHOR VALIDATION PENDING; JOURNAL HOLD; NOT PUBLISHED ON ZENODO.

## Files
- main.tex: the same full title and conditional classification, with sphere and thin-oblate analytic results stated in the abstract.
- sections/core.tex: oblate axial branch-end limits derived conditionally from C1–C2, and separated use of C4 H_lambda.
- sections/computational_evidence.tex: ten-case C2 root count and endpoint ownership, explicitly conditional on the archived sign gates.
- sections/numerical_discussion.tex: source map and accurate unresolved AI first-draft provenance.
- C2_AXIS_CENSUS_TRACE_v0_5_4.md: ten-case gate/source map from the fixed axial assembly.
- CURRENT_REPRODUCTION_v0_5_4.md: C1–C6 source, ledger, input and command map; full-domain coverage and selected independent checks are distinguished.
- AI_PROVENANCE_REVIEW_v0_5_4.md: items requiring author attestation before possible journal submission.
- REVISION_v0_5_4_JA.md: original Japanese audit-oriented revision record.
- SOURCE_DIFF_v0_5_3_to_v0_5_4.patch and SOURCE_DIFF_v0_4_to_v0_5_4.patch: precise source diffs.

## Source identity and audit scope
The four edited TeX files were reconstructed from v0.5.3 and agree by SHA-256 with the locally prepared v0.5.4 bundle. The C2 and reproduction/provenance documents also match the bundle SHA-256. No computational code, ledger, source identity or evidence grade is changed by this manuscript-only branch.

A separate 37-page PDF was produced on the research PC from the four SHA-matched TeX files, under Paper_I_v0_5_4_Integrated_EN_GitHubBuild.pdf (SHA-256 f705d35a06886c511af75747bfc7332739ae29db6343d130fc277c702965c353). It is not byte-identical to the standalone ChatGPT artifact PDF (SHA-256 6fa3a41e1ea1f5e79a65e4f5b1f805d67827bbd583c7c6b9ef023b0e5de722bb). The original standalone PDF and source ZIP hashes are separately listed in PAPER_I_V054_EXTERNAL_ARTIFACT_SHA256SUMS.txt. Neither GitHub registration nor compiling the document certifies C1–C6 or amounts to Zenodo publication.

## Building
Use the immutable v0.4 source ZIP SHA-256 57ee540bb8f3679e1b5abfaf043d6c961d934a981bddfb9d0dba0bd32a4c4d91 and apply SOURCE_DIFF_v0_4_to_v0_5_4.patch to the extracted source root, or overlay the four edited TeX files on it, then run latexmk -pdf main.tex with the original bibliography and figures. The archive has not been altered in place.

## Open work
Codex requests a more completely reproducible original-input chain, especially C2. The ten-case table makes the frozen sign-gate dependence inspectable; it does not replace missing independent replay. The Taylor & Francis AI first-draft provenance remains unresolved and requires an author-led manuscript audit. Do not resume journal submission without a separate Judge decision.
