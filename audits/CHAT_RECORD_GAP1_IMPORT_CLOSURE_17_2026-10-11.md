# CHAT RECORD — gap① import closure is 17 modules, not 15; Code review of the implementation instruction draft v1 (2026-10-11)

## 1. Trigger
Code ran read-only checks on the gap① implementation instruction "INSTRUCTION DRAFT v1 / JUDGE REVIEW REQUIRED". It did not start implementing, because the draft has not been issued. Code reported three points, B1–B3. Its script for the closure has SHA-256 `825eb415…`; Code relayed the report only, not the file. chat re-derived B1 and checked B2 and B3 on its own.

## 2. B1 — the static import closure has 17 modules (confirmed by chat)

**Method.** `audits/importclosure/static_import_closure.py` walks the import graph with the AST only, without executing anything. It starts from the 7 baseline files at bg-oblate-spheroid `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b` and keeps only modules inside the repository. The outputs are `closure_85eca228.txt` and `closure_85eca228_blobs.txt`.

**Result.** The closure has 17 modules. 15 of them are exactly the list in design v2 §4 (from pack `0bfc5c4e`), with matching blobs. The other two are:

| path | blob | imported by |
|---|---|---|
| `producer/c0a_four_group_v2.py` | `2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4` | `producer/global_axial_c1b_kernel.py` L20 (`from producer import c0a_four_group_v2 as grouped`), and the producer c0 v2 module |
| `checker/c0a_four_group_v2.py` | `18e66b6450cd2a379bbb869a99e4e5ce6999f6e5` | checker kernel, and the checker c0 v2 module |

The baseline kernel's own self-pin `C1B_NUMERIC_IMPORT_CLOSURE` (producer kernel L60–61) already lists `producer/c0a_four_group_v2.py` with blob `2bb556ab…`. So the omission is in design v2 §4 and v7 §8.3 / §14, not in the code.

**This is chat's own error (CHAT-IMPORT-001).** In the design v0 audit (Q4), chat accepted "the 15 modules in pack `0bfc5c4e`" without computing the closure. The same count went unchecked in the design v2 audit, in the v7 audit (`b177c450`) and in the v7 identity record.

**Judge ruling (2026-10-11): "記録で17本に拘束" — bind 17 modules by record.**
- v7 (`a4914818`) and design v2 (`0a407d1b`) stay unchanged.
- Wherever they say "15-module import closure" (v7 §8.3 L438, §14 L623; design v2 §4), read **the 17-module closure**: the 15 listed blobs plus the two above, all byte-identical at their pinned blobs.
- `IMPORT_BLOB_MISMATCH` and the diff audit cover all 17.
- This makes the requirement strictly stronger. It is the same mechanism as the clarifications bound in `541f3025`.

## 3. B2 — producer/checker imports that cross lineages (checked; chat's position)

The baseline already crosses lineages in its imports:
- `producer/endpoint_interval_producer.py` L21 and L26 import `checker.endpoint_local_controls` and `checker.oblate_axis_prototype`.
- Both gating modules import `analysis.c1b_resumable_driver`, which v7 §8.1 classifies as producer/driver.

v7 §13 is about **data flow**: the checker recomputes independently, and only exact replay labels, box endpoints and decision labels may pass from producer to checker. v7 §13 does not ban imports.

**chat's position, for the instruction draft v2:**
- The import ban applies to **new ① code only**.
- Baseline imports inside the 7 files plus the 17-module closure are accepted as pinned.
- Any ledger/replay wiring shared by both lineages must reuse the baseline `analysis/c1b_resumable_driver.py`, or a ① copy of it that is changed only under DIFF-E. It may carry only what §13 allows. No new module may give the checker access to producer numerics.

## 4. B3 — the gating import is resolved by package name (checked; chat's position)

Both kernels call `importlib.import_module(lineage + ".global_axial_c1b_gating")` (producer kernel L1723, checker kernel L1709). If the new ① files sit inside `producer/` or `checker/` under new names, that self-test silently loads the **baseline** gating.

**chat's position:**
- The ① files go in **separate packages, with the baseline module names** (for example `gap1_producer/global_axial_c1b_gating.py`). Then `from producer import …` still resolves to the pinned 17, and the gating lookup resolves to ①'s own gating.
- The instruction draft v2 must state these paths. It must also add a static control: every dynamic `import_module` in the new files must resolve inside the ① package.

## 5. Status
- C gap ① is **not frozen**.
- The implementation instruction must go to v2, with B1 per the ruling and B2 and B3 as above. chat audits it, and the Judge issues it.
- chat has not yet seen the text of instruction draft v1. It is needed for the v2 audit.
