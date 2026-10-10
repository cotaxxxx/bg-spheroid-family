# CHAT AUDIT — ① contract v7, the consolidated binding text (2026-10-11)

Baseline: bg-spheroid-family main `8bc2c00508727f6e6455b21fa75a27b11f165f47` (STATE v1.15). No computation was run for this audit.

**Verdict: PASS as consolidated contract text.** Two notes follow, and one identity issue must be settled before FREEZE.

## Checked
- **All 8 documents the text incorporates match their SHA-256 on `8bc2c005`.** Re-read on GitHub just now:
  - design v2 `0a407d1b`;
  - addendum v2 `7471800d`;
  - numeric contract v1 `be67046f`;
  - G0/E1 v3 `8bf8f5d8`;
  - E3 ruling `43f3d811`;
  - Code review `a1437832`;
  - list of 27 amendments `f8a1f954`;
  - Code audit `0d882b53`.
- **Code's accepted findings are all in place:**
  - K1(a): E3 is cited, and the C1a receipt is not edited;
  - K1(b): gate D is used together with the two signs;
  - K2: continuity cites Lemma 5 with I = [2/5, 9/20];
  - K3: the continuation centre is the midpoint of the right neighbour's T_*, with right child first;
  - K4: P2's authority is the executed kernels, and v2.3 / v2.3.1 stay NOT_BINDING;
  - K5: the two roles of ROOT_TARGET are stated;
  - K10: CERTIFICATE_INCONCLUSIVE is the umbrella term for the *_INCONCLUSIVE codes;
  - K11: what to compare at 699/1600 and 281/640 is defined.
- **Logic:**
  - L gives 0 roots.
  - X is split into three cases (g(1/2) < 0, > 0, = 0); the case analysis is complete.
  - In R, gate D together with F_x(281/640) > 0 gives g(1/2, ·) > 0.
  - The endpoint rule is exactly the cumulative mean-value form, with B_ob as a consequence.
  - The FREEZE conditions include D6 PASS. Execution needs separate authorization after FREEZE.

## Notes (not blockers; can be fixed when the file is saved)
1. **R root count.** §6 does not state the conclusion. Add one line: "R: exactly one root in U₁, simple (C1b tube: left exterior g > 0, ∂_t g < 0 in the tube, right exterior g < 0 up to 31/32, then the endpoint gate)."
2. **Scope of 6fba6e4f.** v6 listed lemma 6fba6e4f as a dependency, because transversality at (1/2, λ_x) was argued through it. In v7 the X box certifies ∂_t g < 0 directly on [1/2, 5/8], so **①'s conclusions in U₁ no longer depend on 6fba6e4f**. It stays a dependency of the lower-half (t ≤ 1/2) parts of the C cover. State this explicitly so that it is not read as an omission.

## Identity issue (must be settled before FREEZE)
- ChatGPT states that the v7 file has SHA-256 `a49148180fdeb33272e7358028caa55ec1dc06e5d4f526cd23eca50ff65c2a37`.
- **The text relayed to chat has SHA-256 `255eb630a1b98a03d89371a4fdf4b703222c1f135a27714fd66b9d4bf17668a7`.** The relay presumably changed the formatting (line endings or markdown).
- **The object that gets frozen must be the exact file `a4914818…`, saved in the repository.** Before FREEZE: save that file, confirm its SHA on GitHub, and chat confirms that its content equals the audited text. The same applies to the Astra hand-off file (`2b194a72…`), which chat has not seen.
