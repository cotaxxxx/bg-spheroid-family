# CHAT REVIEW — Code's independent audit of ① contract v6 (2026-10-10)

Input: Code's audit report (received text SHA-256 `0d882b5313cbb26cf41a9ec22cb8524b6e2b78525de3154c58f36bb07c82da3b`). Code read the sources only, against `d707e6ef` and bg-oblate-spheroid `85eca228`. By design it did not read the chat audit records. This review classifies each finding. No computation was run for this review.

| Finding | chat assessment |
|---|---|
| K1(a) the bracket signs are upgraded from report-only to gate input without a declaration | **Already ruled.** Judge ruling E3, appended to `audits/CHAT_AUDIT_THREE_PREDECLARE_DRAFTS_V2_2026-10-10.md` (`43f3d811`): only the two certified endpoint signs are gating inputs, and λ_x stays NON_GATING. Code could not see it because of the independence rule. v7 must **cite the ruling**. |
| K1(b) the root count also depends on C1a gate D (∂_λF_x > 0) | **Accepted (correction).** v6 says "2点のみ", but the sign of g(1/2, ·) across X needs gate D (C1a L45). v7 states both. |
| K2 continuity should cite Lemma 5, with I = [2/5, 9/20] stated | **Accepted.** chat's own v4 audit also cited "Lemma 3" for continuity. Lemma 3 gives the representation on [1/2, 1); continuity on the closed [1/2, 1] is stated in Lemma 5. Recorded as a citation slip (CHAT-CITE-002). |
| K3 continuation takes the midpoint of the right neighbour's T_*; child order | **Accepted.** The midpoint is made explicit. Child order is already in design v1 §6 and numeric contract v1. |
| K4 the v2.3 / v2.3.1 headers read NOT_BINDING; where the authority of P2 comes from | **Accepted; important.** This matches chat audit J2 (the executed code is the authority). v7 wording: "P2 の権威は C1b 実行コード（receipt §1.2 の kernel 2本）が実装した規則。v2.3／v2.3.1 は説明資料（ヘッダは NOT_BINDING）。本契約の FREEZE で採用する。" |
| K5 ROOT_TARGET has a dual role | Accepted (note). |
| K6–K9 | Already superseded by later documents, as Code itself found. |
| K10 no mapping from v6 failure codes to the numeric-contract codes | **Accepted (correction, numeric-contract side).** |
| K11 what is compared at the λ boundaries 699/1600 and 281/640 | **Accepted.** Compare root counts on both sides. At 281/640, check that R's T_* meets (1/2, 5/8). A mismatch is CONTRACT_MISMATCH. |
| K12 the responsibility split at λ = 9/20 | Confirmed (note). |
| K13 the ancestry of `85eca228` | Confirmed after the deeper fetch; Code retracted its earlier wrong result. |
| K14 design v2 is not in the repository; the list of 27 amendments is not found | **Not a defect of the chain.** Design v2 had been received and audited (`67584fea`) but not yet saved; it is in the next save. The list of 27 blobs is in `audits/CHAT_AUDIT_C_GAP1_V4_AND_G0_V0_2026-10-10.md` (`f8a1f954`, J2), which Code did not read by design. v7 should reproduce or cite the list. |

**Code's structural finding is accepted:** v6 alone is no longer a binding source. Its §3–§5 are superseded by design v2, addendum v2 and numeric contract v1.

**Recommendation:** before any FREEZE, ChatGPT drafts **① contract v7 as one consolidated binding text**. It should:
- state the claim and the gating inputs (E3 cited, gate D included);
- cite design v2, addendum v2, numeric contract v1 and G0/E1 v3 by SHA, without restating them;
- include K1(b), K2, K3, K4, K10 and K11;
- cite the list of 27 blobs.
Freezing a fragmented chain invites exactly the kind of misreading Code found.
