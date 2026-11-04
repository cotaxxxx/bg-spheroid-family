# Muse B7 verifier audit package — independent receipt verification

Date: 2026-11-04
Source: user-uploaded `MUSE_PACKAGE_B7_VERIFIER_20261104.zip`
SHA-256 recomputed locally: `bda22ab559753a4b883a4bb96f7b2d487aa0af7e8e999c503a58cfdf4159dfd6`
Muse report SHA-256: `bda22ab559753a4b883a4bb96f7b2d487aa0af7e8e999c503a58cfdf4159dfd6`
Result: **MATCH (64/64 hex digits)**.

The ZIP contains 23 archive entries (including directories and cached Python bytecode). The 13 files listed in Muse's SHA table were individually extracted in memory and hashed. **All 13 matched** the SHA-256 values reported in `MUSE_INDEPENDENT_CODE_AUDIT_20261104.md`.

Additional verified SHA-256 values:

- `MUSE_REQUEST_B7_VERIFIER_20261104.md`: `5a21233ea6eb15710268bcd3e15514a9166d4fba80f82ec617f67875f18f32ae`
- `src/SHA256SUMS.txt`: `bda41da27c95fb8f2a81e4fafbaaf9e3aea233f88adc91d81b26068fb78b4a85`

**Scope:** This is byte-integrity verification, not a repeat of Muse's mathematical audit. The ZIP binary is NOT included in this commit; the source ZIP remains the user-provided attachment. Muse's actual audit scripts are NOT included in this ZIP, which consists of the audit request, verifier sources, references, evidence, and sample. The report previously archived in this branch is an organized transcript, not a verbatim complete report with appendices.

Next archival step: commit the original ZIP binary to this branch without changing its bytes.
