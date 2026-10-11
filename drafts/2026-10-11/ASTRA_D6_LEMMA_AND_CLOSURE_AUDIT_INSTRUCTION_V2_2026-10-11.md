# Astra 宛 指示書 v2 — D6：端点補題・C2 補題と GAP closure record の別系統監査（2026-10-11）

発行：Judge（ユーザー）。起草・監査：chat。
基準：bg-spheroid-family main `09d44320efa10282bb347b4a341ac09abe0bd007`（STATE v1.18）。
**置き換え：** 旧指示書 `drafts/2026-10-10/ASTRA_D6_LEMMA_AUDIT_INSTRUCTION_2026-10-10.md`（`c61f4c69`。handoff `2b194a72` の Part III にも同じ内容が入っています）は、この v2 に置き換わります。旧指示書は使わないでください。D4 の指示（handoff の Part I・II）は、そのまま有効です。
作業区分：READ-ONLY・紙上の監査。**証明書の生成、数値探索、既存ファイルの変更、commit、push はしないでください。**

## 1. 目的と、いまの位置づけ

第一論文の扁平側の空白①②は、次の2つの補題に依存しています。

D6 は Judge の裁定（10/11）によって、**FREEZE の前提としてはすでに満たしています**（CROSS_LINEAGE_AI_AUDIT_PASS）。根拠は次の2段階の監査です。
- 補題：ChatGPT と Code（Claude 系統）が監査しました。
- GAP closure record：ChatGPT が起草し、chat と Code が監査しました。

今回の監査は、**論文で定理を CLOSED と書くための条件**の1つです。Astra は、これまでの監査者（ChatGPT と、Claude 系統の chat・Code）とは別の系統の監査者として加わります。人間の数学者による外部監査も、条件として残ります。

| 対象 | 場所 | Git blob |
|---|---|---|
| EL：OBLATE_ENDPOINT_C1_LEMMA（109行） | bg-oblate-spheroid `design/d-ob-p2` @ `bbcfe662`、`analysis/OBLATE_ENDPOINT_C1_LEMMA.md` | `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6` |
| C2：MONOTONE_TUBE_C2_INTERCHANGE_LEMMA（250行） | 同上、`analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md` | `7cb9b8091596510203d74e09387bc1e8188b8b47` |
| GAP closure record v0（423行） | bg-spheroid-family main、`drafts/2026-10-11/D6_GAP_CLOSURE_RECORD_V0.md` | `d793bfedc815ac2dd6563003bacbe5e6b842b311`（SHA-256 `d7a8d28c…c401a`） |
| （任意）G0/E1 v3 | bg-spheroid-family main、`drafts/2026-10-10/G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md` | `2e83941eb9108997db99b647bbd8df354d2f8979` |

読む前に、`git rev-parse <ref>:<path>` で blob が一致することを確かめてください。リポジトリを読めない場合は、ファイルを Judge に依頼し、受け取ったファイルの `git hash-object` が表の値と一致することを確かめてください。

## 2. 手順（順番を守ってください）

### 段階 A：補題2本の盲検監査
closure record と既存の監査記録は、まだ読まないでください。

**EL（5afa815f）**
1. §1 の定義：μ = 1 − s² への変数変換、F = sAα²、F_t の式、係数 1/2（3Vol = 4πλ から来るもの）。
2. Lemma 1：N = −s²H、q > 0、0 < γ ≤ 1（1 − γ² の恒等式を含む）。**Lemma 1 が成り立つ t の範囲**も確かめてください。
3. Lemma 2：支配関数 M(s) の各定数。北側の z/(1+z²)^{3/2} ≤ 2/(3√3)、南側の d ≥ 1/2 と q ≥ λ₋²/4 を含みます。
4. Lemma 3：微分と積分の交換。γ = 1 での扱いと、**t = 1/2 での微分が両側か片側か**を確かめてください。
5. Lemma 4、Lemma 5（t → 1⁻ の極限と、[1/2,1] での連続性）、Lemma 6。
6. §7「主張しないこと」が本文と整合しているか。

**C2（7cb9b809）**
1. §2：R_γ、N_t、γ_tt、G_t の導出。**R と R_γ が γ = 1 で定義されているか**も確かめてください。
2. §3：ρ²(2−s²) + λ²φ² = 1、Â = (2−s²)sρ − (1−s²)φ、G_t = T1 + T2 + T3。
3. §4：北側の上界。|H| ≤ 4 と −1 ≤ R_γ ≤ 0 が証明されているか、「compact」という語がどの集合を指しているかも確かめてください。
4. §5：南側。コンパクト性の論証が成り立つ前提を確かめてください。
5. §6：微分の交換、t = 1 での片側極限、微積分学の基本定理を使う前提。
6. 2補題のつながり。C2 は EL の Lemma 3 と Lemma 5 を前提にしています。

ここまでの判定を書き終えたら、**本文を確定**してください（以後は書き換えず、段階 B・C は追記として書きます）。

### 段階 B：closure record の監査
段階 A を確定したあとに読んでください。

closure record（d7a8d28c）は、Code が挙げた GAP 10件と ChatGPT の注記1件を、合わせて11項目として閉じようとする文書です。各項目について、次の3点を判定してください。
- (a) 引用している行番号が、上の blob と一致しているか。
- (b) 示している読み方が正しいか。
- (c) 証明が正しいか。

判定は **CLOSED / NOTE / OPEN / FAIL** のいずれかです。段階 A で Astra が見つけた点のうち、closure record が扱っていないものは、別に一覧にしてください。

### 段階 C：照合（任意）
段階 B を確定したあとであれば、次の記録を読んで、相違点を追記してかまいません。
- `audits/CHAT_AUDIT_D6_GAP_CLOSURE_RECORD_V0_2026-10-11.md`（拘束読み B1・B2 と、Code の K1・K2 を含む）
- `drafts/2026-10-11/CODE_D6_LEMMA_AUDIT_REPORT_V0.md` と、その照合後の追記
- `drafts/2026-10-11/CODE_AUDIT_D6_GAP_CLOSURE_RECORD_V0.md`
- `drafts/2026-10-11/CHATGPT_D6_LEMMA_AUDIT_REPORT_V0.md`

### 任意：G0/E1 v3
G0/E1 v3 は、C2 の方法を λ ∈ [2/5, 5/8]、t ∈ [1/2, 1] に広げたものです。①の X 領域で使う「∂_t g = ∫G_t」はこの補題に依存しているので、余力があれば §2〜§4 の不等式と、t = 1/2 での片側性の扱いを見てください。

## 3. 独立性と計算
- 段階 A を確定するまでは、`audits/` 配下と、`drafts/2026-10-11/` にある D6 関連の報告・closure record を開かないでください。開いてしまった場合は、その事実を報告に書いてください。
- 厳密な記号計算（SymPy など、浮動小数点を使わないもの）は使ってかまいません。その場合は、実行前にスクリプトの SHA-256 と合否の条件を記録し、出力も保存してください。数値による標本化は証拠になりません。

## 4. 提出物
`ASTRA_D6_AUDIT_REPORT_V0.md` を1本提出してください。SHA-256 と行数も報告してください。報告には次の4点を入れてください。
- 段階 A：blob の照合結果、項目ごとの判定（PASS / FAIL / GAP）、FAIL と GAP の該当箇所・内容・修正案、全体判定（`AI_AUDIT_PASS` / `AI_AUDIT_CONDITIONAL` / `AI_AUDIT_FAIL`）。
- 段階 B：11項目の表（CLOSED / NOTE / OPEN / FAIL）と、closure record が扱っていない指摘の一覧。
- 段階 C（行った場合）：既存の監査との相違点。
- 開いたファイルの一覧（独立性の開示のため）。

提出後、chat がこの報告を監査記録として受理するかどうかを判定します。補題 v1.1 にどう反映するかは、Judge が決めます。
