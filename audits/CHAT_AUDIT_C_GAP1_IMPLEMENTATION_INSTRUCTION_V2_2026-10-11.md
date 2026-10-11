# CHAT AUDIT — C gap ① implementation instruction DRAFT v2 (2026-10-11)

**Object.** `drafts/2026-10-11/C_GAP1_CODE_IMPLEMENTATION_INSTRUCTION_DRAFT_V2_2026-10-11.md`, SHA-256 `48204988…f6b9e6f`, 300 lines, on main `0b430ed7`. Drafted by ChatGPT. chat has not seen v1; Code's pre-review of v1 (B1–B3) is in `b48887c1`. chat ran no computation except reading files.

## Checks
- **§1.1 authority SHAs.** These 8 are the same values as in the ledger: v7 `a4914818`, design v2 `0a407d1b`, addendum v2 `7471800d`, numeric contract v1 `be67046f`, G0/E1 v3 `8bf8f5d8`, clarifications `541f3025`, identity `7118070b`, and the v7 audit `b177c450`.
- **§1.2.** The 7 baseline paths and blobs match bg-oblate-spheroid `85eca228`. chat checked this with `git ls-tree`.
- **§1.3–1.4 (B1).** The 15 listed modules plus the 2 added ones are exactly chat's 17-module closure (`audits/importclosure/closure_85eca228_blobs.txt`). The added blobs `2bb556ab` and `18e66b64` are correct.
- **§1.4 B2.** Consistent with v7 §13 (independence is about data flow) and with chat's position in `b48887c1` §3.
- **§1.5 B3.** Correct. Both kernels compute `lineage = __name__.split(".",1)[0]` and call `import_module(lineage + ".global_axial_c1b_gating")`. The `gap1_*` packages that keep the baseline basenames route these calls correctly, while `from producer import …` still resolves to the pinned 17. `Path(__file__)` and the `C1B_NUMERIC_*` hard-coded paths are properly listed for per-site enumeration.
- **§2.** The allowlist A/B/C/D/E/K is identical to v7 §8.2, and the protected bodies are listed.
- **§3–4.** The regions, slab counts and owners match v7 and design v2. The E3 gating inputs and gate D are used correctly. λ_x is NON_GATING. The X dependency on G0/E1 and the g(1/2) vs ∂_t g distinction (D6 B2/K2) are stated correctly. The R rules (P2 `<=`, right-child-first, accepted right-neighbour midpoint) are right.
- **§5.** The cumulative endpoint gate is as ruled (S1): seed at 31/32, 16 boxes of width 1/512, 8192 s-panels. The forbidden routes are listed, and B_ob is non-gating.
- **§6.** Every constant was checked against numeric contract v1 (`be67046f`): caps 1280/2400 and the work ceilings, 160/192 bits, degree 50, T stages, ROOT_*, E0 24/8, the 1024→2048→4096 ladders, X blocks, seed and box panels 8192, budget 96 core-h / 32 GiB / 10 GiB. All match.
- **§7–9.** The ledger, failure codes and static-only controls are consistent with v7 and the addendum.

## Findings (none of them requires changing v2's mathematics)
| ID | Finding | Resolution |
|---|---|---|
| I1 | §1.1 still names base `201d4808`; v2 itself is saved at `0b430ed7` | Re-based by the issue note, N1 |
| I2 | §1.4 and §9 make B1 and B2 "pending Judge acceptance", but both have now been accepted (`b48887c1`) | Recorded as accepted in the issue note, N1 |
| I3 | No delivery format. The deliverables would sit in Code's scratchpad; on 10/11 a scratchpad path was relayed instead of the file | The issue note, N2, requires one tar.gz with a SHA-256 manifest, attached as a file |
| I4 | §10.8 says CHAT diff audit; §11 says ChatGPT | Judge ruling: both audit independently (issue note, N3) |

## Verdict
PASS as an instruction, with the issue note `ISSUE_NOTE_C_GAP1_IMPLEMENTATION_INSTRUCTION_V2_2026-10-11.md`.

**Judge ruling (2026-10-11):**
- "発出メモを付けて発出": v2 is issued with the issue note.
- "ChatGPTとchatの両方": both ChatGPT and chat audit the diff.

Code may now implement in isolation under v2 and the issue note. Nothing is frozen, and no numeric execution is authorized.
