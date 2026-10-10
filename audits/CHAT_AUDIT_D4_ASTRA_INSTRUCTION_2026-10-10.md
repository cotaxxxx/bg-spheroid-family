# CHAT AUDIT — instruction to Astra, D-AN-2 / D4 center band (2026-10-10)

Object: the instruction to Astra "D-AN-2 / D4 — 扁平中心帯の解析・認証方式設計", as relayed by the user on 2026-10-10.
No computation was run for this audit. Sources were read on GitHub (bg-oblate-spheroid `design/d-ob-p2`).

**Verdict: PASS with corrections K1–K5.** The scope, the permissions and the decision vocabulary are sound. The instruction keeps the order design → audit → Judge, and it says explicitly that a failed interval certificate does not mean the mathematical claim fails. Send it to Astra **with the addendum below attached**; there is no need to redraft it.

## Findings

**K1 (correction) — outdated baseline.** The instruction cites STATE v1.11 / `87cd7181`. The current baseline is STATE v1.12 / `32218d7855e3e6218dddbe315eacb38cd2dd8295`. v1.12 does not change the D4 row, but the instruction must cite the current baseline.

**K2 (correction) — who issued it.** The header says "発行：CHAT / Dig". chat is the auditor and does not issue instructions. The issuer is the Judge (the user); the drafter is ChatGPT; chat audits.

**K3 (major — a source exists for the center band).** `analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md` (blob `931c0cdb`), line 53, says:

> "The `0,0,3` band, with `lambda in [0.595,0.66]` near the upper central endpoint and a distinct thin-margin mechanism, is out of scope for D-AN-1 and explicitly deferred to D-AN-2."

So the band already has a name (`0,0,3`), a range [0.595, 0.66] and a stated mechanism (thin margin). Astra should start from this text rather than from "λ ≈ 0.6–0.66".

**K4 (major — an investigation item the instruction does not mention).**
- The band's range [0.595, 0.66] contains the certified boundary-entry parameter λ_∂^ob ∈ (5/8, 33/50). That is where the axial root reaches t = 1 (band receipt `d6b0a787` §6). Its right end is the end of the main-theorem window, 33/50.
- One question therefore matters before methods A–D are compared: is the small margin of H in this band a **structural degeneracy** tied to λ_∂^ob (failure class E), or only an artefact of the method (classes A–D)?
- If H → 0 at some point, no method can prove a uniform lower bound H > 0 there. The claim itself would have to be restated with a local exclusion handled by bifurcation analysis.
- This is a question to investigate, not a claim. The instruction's rule "区間認証の失敗 ≠ 数学的主張の失敗" also works the other way: the claim must not be assumed true either.

**K5 (major — the handoff is not in scope).**
- The D-problem kick-off draft (`D_OB_P2_D_PROBLEM_TRACK_KICKOFF_DRAFT.md`, line 43) and D-AN-1 v1.2 (line 219) state that removing the 7,662 boxes from D-P2 is "a separate audited stage". An analytic H > 0 does not by itself discharge boxes.
- The method comparison has to state how the chosen method's output becomes a discharge of the 3,584 boxes: the theorem-to-D-P2 handoff. A method that cannot state this cannot be selected.

**K6 (note).** The list of the 3,584 boxes from smoke #4 is probably a run artefact on the research PC, not on GitHub. If Astra cannot reach it, SOURCE_NOT_FOUND is the correct outcome. The user then supplies the file, pinned by SHA-256.

---

## Addendum to attach for Astra (can be sent as it is)

> **補遺（2026-10-10、Judge 発行・chat 監査済み）**
> 1. 基準を STATE.md v1.12、bg-spheroid-family main `32218d7855e3e6218dddbe315eacb38cd2dd8295` に更新する。発行者は Judge、起草は ChatGPT、監査は chat。
> 2. 中心帯の出発点となる原典：bg-oblate-spheroid `design/d-ob-p2`、`analysis/D_OB_P2_D_AN1_PREDECLARE_V1_2.md`（blob `931c0cdb`）53行目。「`0,0,3` band, λ ∈ [0.595, 0.66], near the upper central endpoint, distinct thin-margin mechanism」。D4-1 はここから始めること。
> 3. 追加の調査項目 D4-0：この帯は λ_∂^ob ∈ (5/8, 33/50)（帯 receipt `d6b0a787` §6）と窓の右端 33/50 を含む。H の余裕が小さいのは λ_∂^ob に結びついた構造的な退化（分類 E）なのか、方式の問題（分類 A–D）なのかを、方式比較より先に原典から調べること。H → 0 となる点があり得るなら、そのことを主張の問題として報告すること（一様下界の方式では閉じられない）。主張が真であることも、偽であることも前提にしない。
> 4. 提出物 B には、各方式の結論が D-P2 の未解決箱 3,584 個の消去にどう引き渡されるか（theorem-to-D-P2 handoff。kick-off 43行目、D-AN-1 v1.2 219行目では別段階の監査と定められている）を必ず含めること。引き渡しを記述できない方式は METHOD_SELECTED にしない。
> 5. smoke #4 の未解決箱の一覧に到達できない場合は SOURCE_NOT_FOUND と記録し、ユーザーに SHA 付きでの提供を求めること。
