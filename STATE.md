# STATE — 工程管理（最初に読む1枚）

版：v1.29（2026-10-13、chat 起草。v1.28→v1.29 の変更：C 空白① v0.5 run4 両系統 PASS、Judge CONDITIONAL_CLOSED。経緯は git 履歴）。運用：**書き換え式**（追記しない。古い行は削除し、経緯は git 履歴に任せる）。上限 150 行。
更新：chat が起草 → ユーザーが commit。他の AI は書き換えない。新しいセッションの AI は、まずこの1枚だけを読む。

## 1. 道標
形の数学的研究とは、ものが持つ要素を削ぎ落とした「形（shape）」そのものを見ること。
迷ったら問う：**その作業は、削ぎ落とした形の構造を見ることにつながっているか。**

## 2. 目標と期限
| 項目 | 内容 |
|---|---|
| 第一論文 | 体積保存回転楕円体族、扁平→球→扁長、**両側とも大域定理（必須）** |
| 投稿 | Experimental Mathematics、**2027年1月**（目標 1/31） |
| 出願 | 京都芸術大学 通信制大学院（学際デザイン研究領域・早川ゼミ）。2027年度募集要項 p.3・p.11 で確定：Web 出願 2027-01-14〜02-18、提出後の差替え不可、合格発表 03-10。指定提出物＝志望理由 800字程度・研究計画 1,200字程度・活動実績の概要 1,200字程度（要項の2を選択）・参考資料 PDF1点。初稿は Docs「研究計画書 骨子案」の「出願書類 初稿」タブ。数学は「数学的見方（レンズ）」として扱い、論文は活動実績の概要で示す。第一論文の投稿（1/31）は出願期間内 |
| 三部作 | 第二論文＝体積保存3軸楕円体族（三角形）、第三論文＝体積保存楕円体族（地形・勾配場）。第二論文の着手は第一論文の投稿後。Θ_K(p,x) 生データ探索（9/22 表 No.37–44）は第三論文への入力として第一論文の投稿後に開始 |

## 3. 今有効な決定（置き換えられたものは載せない）
- 扁平の主定理の窓：λ ∈ [2/5, 33/50]（λ_c^ob と λ_∂^ob の両事件を含む最小窓）。
- 扁長の主定理の窓：**λ ∈ [2, 5]**（Judge 2026-10-10）。λ_∂^pro ∈ [2.06538, 2.06539]（Item 0 Stage 1）と a_c ∈ (4.72438340452113340672, …673)（局所証明書）を含み、左端は Item 0 の認証範囲（1≤λ≤2.06539）内、右端は a_c から 0.28 離れて非退化。tail λ→1⁺・λ→∞ は扱わない。
- 予想で代替しない。すべての主張は証明書に基づく（closed world）。
- λ 規約：a₁=a₂=λ^(−1/3)、a₃=λ^(2/3)。λ<1 扁平、λ=1 球、λ>1 扁長。回転軸は z。
- 論文の主役は停留構造。分岐はその λ 変化、認証は方法。
- D-OB の内部（L1）は Form II（一様下界）を目標とする。ROUTE は δ_L1 確定まで UNDETERMINED。
- 統治：事前宣言 → 監査 → FREEZE → 実行許可。診断は証拠にしない。版上げのみ。fail-closed。
- 監査役は chat（一系統）。ChatGPT は Dig（調査・起草・実装、研究用 PC と GitHub に直接アクセスし main へ push）、Code・Astra は Judge が必要時に使う（`audits/CHAT_RECORD_AUDIT_ROLES_2026-10-11.md`）。
- 効率規則（Judge 10/11、`audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_3_2026-10-11.md` 末尾）：数学的指摘は慎重に止めて Judge 裁定（数学的結果を誤記する台帳欄を含む）。手順上の指摘（pin・ラベル・文言・resume 配管）は次版にまとめ、追加の監査往復やボタンを作らない。ファイルは ChatGPT→GitHub→chat で流し、Judge の中継を求めない。正の台帳はこの STATE.md と `UPSTREAM_PINS.md`。

## 4. 部品表
### 扁平（D-OB）
| # | 部品 | 状態 | 根拠（1行） | 次の関門 | 担当 |
|---|---|---|---|---|---|
| C | 軸上 C 系列（C0, C1a–d, 帯） | ① U_check＝v0.5 run4 PASS（160/160 両系統、`26d81e1`／family `40e83b5c`）→ Judge 10/13 条件付き CLOSED（D6 束・G0/E1 v3 条件、receipt `audits/C_GAP1_JUDGE_RECEIPT_2026-10-13.md`）。残＝空白②と global cover assembly。 | 文面は監査済み（`drafts/2026-10-10/`）：① 事前宣言 v6、② v3、実装設計 v1（v2 へ文面修正のみ）、端点追補 v2、数値契約 v1。方式：①は λ を 1/3200 刻み 160 slab（L・X・R の3群）、R は 9/20 から左へ C1b の予測規則（P2＝ROOT_TARGET 1/128）、端点は t_e からの累積平均値形（g は t_e の1点、[t_e,1] は幅 ≤1/512 の Gt 箱、粗い定数 C_Λ は使わない）、B_ob は帰結（receipt は照合のみ）。統合補題 G0/E1 v3 PASS（C2 恒等式の記号検算・機械 Gt のソース一致を含む） | FREEZE 前：① 契約 v7 は FREEZE 対象として確定（`drafts/2026-10-11/C_GAP1_CONTRACT_DRAFT_V7.md`、a4914818、文面 PASS、補足2点は記録で拘束、監査文面との同一性確認済み `audits/CHAT_RECORD_V7_EXACT_FILE_IDENTITY_2026-10-11.md`）。D6＝**充足**（Judge 10/11）：5afa815f・7cb9b809 は CROSS_LINEAGE_AI_AUDIT_PASS（補題監査 ChatGPT・Code、closure record `drafts/2026-10-11/D6_GAP_CLOSURE_RECORD_V0.md` d7a8d28c を chat・Code が監査、拘束読み B1・B2・K1・K2 は `audits/CHAT_AUDIT_D6_GAP_CLOSURE_RECORD_V0_2026-10-11.md` §3・§5）。論文で CLOSED と書く条件：補題 v1.1（closure 11 項目と B1・B2・K1・K2 を反映）とその監査、Astra（指示書 v2 `drafts/2026-10-11/ASTRA_D6_LEMMA_AND_CLOSURE_AUDIT_INSTRUCTION_V2_2026-10-11.md`）、人間の外部監査。残る FREEZE 前の関門：① の実装は **v0.3 PASS（static）**（`submissions/2026-10-11/C_GAP1_IMPL_V0_3_SUBMISSION_2026-10-11.tar.gz` 2ec6e70f、監査 `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_3_2026-10-11.md`。import 17本 `audits/CHAT_RECORD_GAP1_IMPORT_CLOSURE_17_2026-10-11.md`、F1–F5・A1・A7 解消、B1–B12 受理）。**v7 run2 STOP**（10/12、`runs/2026-10-12/C_GAP1_V0_3_RUN2_STOP/`：slab 126〜159 は ACCEPT、slab 125 [5621/12800,11243/25600] で TUBE 不成立、根 T* が t=1/2 へ近づくことによる R 方式の劣化で、反例ではない）。Judge 10/12：**契約 v8＝R/X 境界を 703/1600 へ**（X 8・R 34、gating 点 281/640 は不変）、実装 v0.4 → chat 監査 → X 診断（NOT_EVIDENCE）→ run3（`drafts/2026-10-12/C_GAP1_CONTRACT_V8_DELTA_AND_IMPL_V0_4_INSTRUCTION_2026-10-12.md`）。 **run3 STOP**（10/12 10:56、slab 117 [11183/25600,699/1600] で L 未解決、λ_x 左側の同じ構造）。Judge 10/12：**契約 v9＝L/X 境界 λ_b を左へ**（slab 117→109 の範囲で X・L 診断により決定、C1a 点 699/1600 は不変）→ 実装 v0.5 → chat 監査 → run4（`drafts/2026-10-12/C_GAP1_CONTRACT_V9_DELTA_AND_IMPL_V0_5_INSTRUCTION_2026-10-12.md`）。 **v9 診断 STOP**（14:23、L は λ_x から 0.004 離れても壁 g(1/2) を数値で負にできない）。Judge 10/12：**v9.1＝λ_b=83/200 に固定**（L 48・X 78・R 34。X は gate D で g(1/2)<0 を解析的に得る）、X・L 並列診断（NOT_EVIDENCE）→ v0.5 → chat 監査 → run4（`drafts/2026-10-12/C_GAP1_CONTRACT_V9_1_DELTA_2026-10-12.md`）。実行順は C 空白①→D5（同時占有禁止）。② の封印ディレクトリは確認済み | ChatGPT |
| D1 | 極 corner 境界面 FT_q | DISCHARGED（P1 監査条件付き）。南側 39′ は readback 済みで CLOSED（P1 条件付き） | 南側 39′ は `UPSTREAM_PINS.md` V1（`bbcfe662`、照合済み・再実行一致）、C45/C43、22″ v1.2 `d445b302` | 残りの構成部品の pin 昇格 | chat |
| D2 | 極 corner 内部 L1 | O1 CLOSED（P1 条件付き）。O2：v1・v1.1-r1（O2-A3）FROZEN、P0–P1 ADOPTED。R1＝FAIL-CLOSED（項ごとの絶対値上界が成功条件の約 3×10⁶ 倍）。**R2 枠組み FROZEN**（Judge 2026-10-10、v0＋v0-r1 差分）：M_+ を (λ,τ,r) の閉箱（r=1・τ=1 を含む）ごとに符号付き積分下界・有理包囲・Bernstein で直接認証、全箱共通の h_*>0（P 単位）。補題 R2-L1：D²≥(a−|ξ|)²+(λμ−z)²。t 積分の許容方式 R2-T1（τ≤τ₁、正確な割線）／R2-T2（τ≥τ₁、ξ=0 展開、g⁽⁴⁾ が必要）。10/31 CLOSED は保証なし | pin：basepoint-geometry `chatgpt/d-p2-o1-predeclare-v1-20261009` commit `fbadfc4d`（R2 v0 `764c1860…e8be`、v0-r1 差分 `957b7d00…6aa`、v1.1-r1 `7dcbd6d6…12c5`、P2 v1-r1 `3f0fcdb3…6b5d`、chat が GitHub 上で照合済み） | P2-b（R2 の実行事前宣言：箱・セル数・近似次数・誤差予算・τ₁・g の包み・工数見積り）→ 監査 → FREEZE → 実行 → 独立検証 → O3 → O4–O6 | ChatGPT |
| D3 | L3–L1 接続 | UNDETERMINED | 仕様 v1 `ecd31446` | D2 に従う | — |
| D4 | 中心帯（`0,0,3` 系の 3584 箱、r∈[1/64,1/8]、τ∈[0,1/8]、λ∈[119/200,33/50]、z/λ≤2/65。所在＝`full_terminal_map.tsv` `0584…26f8`、DIAGNOSTIC） | Astra が原典調査に着手。補遺 v2 で D4-0 を「中心での H の挙動」に訂正（λ_∂^ob との関連は撤回、CHAT-D4-K4-001） | — | 指示書全文と補遺 v2 の送付 → 原典調査・方式比較（10/17）→ 監査 → Judge 方式裁定 | Astra |
| D5 | 一般域（区間認証本走） | 未実施。概算 150〜170 h（256 箱 / 12 並列、9/22 見積り・保証値ではない） | SPEC/contract V2、resume `c0f099f9`、smoke #4 | 契約再裁定 → 外部 backup（SHA 照合）→ 環境固定 → 本走 → machine receipt → 成果物保全 → Judge | Code |
| D6 | 外部監査（P1 Lemma V、C 側 5 件） | 未送付 | — | 監査一式の送付、または付録に全証明 | ユーザー |

### 扁長（D-PRO）
| # | 部品 | 状態 | 根拠（1行） | 次の関門 | 担当 |
|---|---|---|---|---|---|
| P0 | 扁長側の主張範囲 | **裁定済み**：窓 [2, 5]（2026-10-10） | basepoint-geometry main `abf704b8`：CERTIFICATES/prolate（Item 0、local_bifurcation） | — | — |
| P1 | a_c の局所分岐 | 認証済み（未昇格）。`68bc9828` は後続 commit に置き換えられ、昇格は FAIL-CLOSED。後継 `abf704b8`（12 objects、manifest 一致、再実行一致） | basepoint-geometry main `abf704b8`（SHA256SUMS `3b6fc57d…c11d`） | 第二系統の事前宣言 v2（DRAFT、枠組み PASS）。段階制（Judge 10/10）：必須＝Q_z≥1/100・5桁括弧・Q′<0・H4<0、追加＝20桁括弧・Q_z≥0.0885587746621582。Julia＋IntervalArithmetic.jl、clean-room（入力は原始定義のみ）。FREEZE 前：入力一式・精度保証付き積分の契約 → 監査 → 実行 → PASS 後に登録。Julia 導入は Judge 承認が必要 | ChatGPT/Code/Astra |
| P2 | 停留円の接続枝 λ_∂^pro→a_c（item2_circle を含む） | pilot 単一スライスのみ | basepoint-geometry Actions receipt | C1b 契約の移植設計 | Code/ChatGPT |
| P3 | 有界域の子午面排除 | 未着手 | D-OB の道具を雛形に | 設計 | ChatGPT |
| P4 | 窓の端での境界処理（窓外へ枝が出ないこと） | 未着手 | — | 設計 | ChatGPT |

### 原稿
| 項目 | 状態 | 根拠 |
|---|---|---|
| 骨格 | v0.2 | `MANUSCRIPT_SKELETON.md` |
| pin 登録簿 | 昇格済み 1 件（V1 南側 39′） | `UPSTREAM_PINS.md` |
| 球の定理（§6） | 出典未特定 | 要調査 |

## 5. 次の関門（日付順）
| 期限 | 関門 |
|---|---|
| 10/17 | D5 契約再裁定（本走開始は契約再裁定と研究用 PC の準備の完了後）／D4 方式決定（Astra）／G0/E1 v3 整理／扁長第二系統の入力一式と積分契約／原稿 §1–3 の起草（確定結果と未認証の主張を分ける） |
| 10/31 | D2 O2 CLOSED／D4 証明書／P3 設計凍結 |
| 11/07 | チェックポイント1：両側の残量を数値化し、投稿月を確定 |
| 11/30 | 扁平側の大域 CLOSED |
| 12/25 | 扁長側の大域 CLOSED |
| 1/15 | 全体統合・付録 A を pin から生成・最終監査 |
| 1/31 | 投稿 |

## 6. 判断待ち（Judge）
1. D6：外部監査を投稿前に終えるか、付録の全証明で査読に委ねるか。
2. 22:47 以降の ChatGPT ブランチの run1/run2：O1 の Judge CLOSED として扱い済み（記録の整合のみ残る）。
