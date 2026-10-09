# 今後の研究工程管理表 — 2026-10-10 改訂版

前版：2026-09-22「実績反映・訂正版」（46工程＋7a・15a）。番号は前版を保持し、10/9 版の 22a–22j を引き継ぎ、新設は 22k・33a・47 とする。
現在状態の正本は `STATE.md`（bg-spheroid-family）。本表はその工程番号付きの詳細版で、食い違う場合は STATE.md を優先する。

## 0. 10/10 の主要決定（9/22 版からの変更点）
| 項目 | 9/22 版 | 10/10 版 |
|---|---|---|
| 道標 | — | 形の数学的研究＝要素を削ぎ落とした「形（shape）」を見ること |
| 第一論文の範囲 | 扁平の大域＋扁長は局所（D-PS 未決） | **扁平・扁長とも大域（必須）**。扁長の窓＝λ_∂^pro と a_c を含む最小窓 |
| 投稿 | 11/30 | **2027年1月（目標 1/31）**、Experimental Mathematics |
| D-OB の主線 | P2 区間認証の本走のみ | 一般域＝本走（D5）、未解決 7,662 点＝解析ルート（極 corner＝D-AN-1、中心帯＝D-AN-2） |
| 台帳 | 二系統（ChatGPT 側／chat 側） | 一本化。正本＝STATE.md と UPSTREAM_PINS.md、監査役＝chat |

## 1. 工程管理表

### A. 軸上 C 系統（No.1–14）
| No. | 工程 | 状態（10/10） | 次工程・完了条件 |
|---|---|---|---|
| 1 | C1b Phase 1 producer | COMPLETED / SEALED | — |
| 2 | C1b Phase 2 checker replay | COMPLETED / SEALED | — |
| 3 | C1b cross-lineage | PASS | — |
| 4 | C1b machine evidence | MACHINE CLOSED | 解析 assembly へ接続 |
| 5 | C1c machine | JUDGE PASS | — |
| 6 | C1c analytic assembly | CONDITIONAL PASS | lemma 6fba6e4f 外部監査 |
| 7 | C0（C0a・C0b） | JUDGE PASS / CONDITIONAL | 6fba6e4f＋963b03be 外部監査 |
| 7a | C1a | CLOSED（receipt 7f34c95d） | 被覆図に含める |
| 8 | C1d | MACHINE PASS / CONDITIONAL | lemma 35656381 外部監査 |
| 9 | band [31/32,1] | JUDGE PASS / CONDITIONAL | aefa8ed2・f66ffe5a 外部監査 |
| 10 | 軸上 C 各部品 | 部品は条件付き CLOSED／global cover 未検証 | No.13 |
| 11 | C artifacts 外部保全 | COMPLETED | — |
| 12 | C 側 lemma 5 件の外部監査 | PENDING | No.15a と同じ監査束（STATE D6） |
| 13 | C global cover diagram | PENDING・**10/17 関門** | 最初に U_check={1/2<t≤1, 2/5≤λ<9/20} の receipt 照合。推測で埋めない |
| 14 | C global assembly | PENDING | cover＋5 lemma 監査＋assembly 文書で C CLOSED |

### B. D-OB（扁平の子午面排除）
| No. | 工程 | 状態（10/10） | 次工程・完了条件 |
|---|---|---|---|
| 15 | D-OB P1 Design | COMPLETED / SEALED | — |
| 15a | P1 Lemma V 外部監査（Lemma 3.1–3.4・6.1 を含む） | PENDING | 監査束の送付、または論文付録に全証明（判断待ち） |
| 16 | P1 diagnostic | COMPLETED / SEALED（Q1 YES(+)、Q2 NO） | — |
| 17–20 | SPEC V2・contract V2・producer・checker | SEALED / AUDITED（D5 で再利用） | No.25 の再裁定に従う |
| 21 | smoke #1 | FAILED / PRESERVED | — |
| 22 | smoke #1 後の実装修正 | COMPLETED / RE-AUDITED | — |
| 22a | FT_q 境界一様下界 | **DISCHARGED（P1 条件付き）**、m₀=540861826035521/336806928254720000 | 構成部品＝22k・Contract 45/43・22″ v1.2・R-G・c_FT・BPL v1。pin 昇格 |
| 22b | QM | AUDIT PASS | — |
| 22c | L3-MRA | PASS | — |
| 22d | L0・L2・NP-T | CLOSED | — |
| 22e | δ_L1 仕様 v1 | FROZEN（ecd31446） | — |
| 22f | L3–L1 接続 | UNDETERMINED。**Form II を目標**（10/10） | 22h–22i の結果に従う |
| 22g | L1 O1 内部表示 | CLOSED（P1 条件付き） | — |
| 22h | L1 O2 内部正質量 | 事前宣言 v1 FROZEN（7fb2bfb8）、P0–P1 紙導出 CHAT AUDIT PASS（0456c1ef）、**Judge 採否待ち** | P2（推奨：境界面の値＋r_rad 方向 Lipschitz）→ CLOSED |
| 22i | L1 O3–O6 | NOT STARTED（O3 が最難所） | O2 の後 |
| 22j | D-AN-2 中心帯（λ≈0.6–0.66、未解決 3,584 点） | NOT STARTED | **10/17 方式決定** |
| 22k | 南側 39′（Lemma A・B・C、S″_lb） | **CLOSED**（canonical bbcfe662、18 ファイル照合済み） | pin 昇格の第1号 |
| 23 | smoke 履歴 | #2 後続確定／#3 中断／#4 完走・gate FAIL（未解決 7,662＝極 corner 4,078＋中心帯 3,584） | 履歴保存。証拠ではない |
| 24 | raw audit・監査史 | HISTORY PRESERVED。SPEC V3 候補比較は 10/05 CLOSED（採用ゼロ） | — |
| 25 | runtime・resume 裁定 | resume c0f099f9 ACCEPT。24h 規則は旧経路の事前宣言として保存 | **D5 用に契約を再裁定（10/17）** |
| 26 | 本走前の外部 backup | PENDING | SHA 一致で完了 |
| 27 | 本走環境準備 | PENDING | 自動更新・スリープ停止、12 並列専用化 |
| 28 | 一般域の本走（D5） | NOT RUN。概算 150〜170 h（保証値ではない） | identity_before → producer → checker → identity_after |
| 29 | machine receipt | NOT RUN | receipt PASS は CERTIFIED と呼ばない |
| 30 | run artifacts 外部保全 | NOT RUN | SHA 照合 |
| 31 | D-OB P2 Judge | PENDING | 22a・22g–22k・28 を含む証拠鎖の判定 |
| 32 | D-OB closure | NOT CLOSED | 31 PASS＋15a＋C（No.14）。**目標 11/30** |

### C. D-PS（扁長の大域）・論文・探索
| No. | 工程 | 状態（10/10） | 次工程・完了条件 |
|---|---|---|---|
| 33 | D-PS 採否 | **GO（10/10）**。範囲＝λ_∂^pro≈2.0654 と a_c≈4.7244 を含む最小窓。tail は扱わない | 窓の端点確定（10/17） |
| 33a | 扁長 a_c の局所分岐 | 認証済み（basepoint-geometry 68bc9828、9/05 投稿一式） | pin 昇格 |
| 34 | D-PS Certification | 設計開始前 | 停留円の接続枝（C1b 契約の移植）・有界域の子午面排除・窓端の処理。**目標 12/25** |
| 35 | Paper I 統合 | **着手**：bg-spheroid-family に骨格 v0.2（v0.3 で窓を反映）、STATE.md | 定理と証明書の1対1対応、付録 A を pin から生成 |
| 36 | Paper I 最終監査・投稿 | NOT STARTED | **1/15 統合・最終監査、1/31 投稿** |
| 37–44 | Θ_K(p,x) 生データ探索 | 第一論文投稿後に開始 | 第三論文（地形・勾配場）への入力 |
| 45 | Paper II（体積保存3軸楕円体族・三角形） | 第一論文投稿後に着手 | — |
| 46 | Paper III（体積保存楕円体族・地形・勾配場） | 三部作として構成確定（10/10） | Paper II の後 |
| 47 | 京都芸術大学 通信制大学院 出願 | 2027 年度募集要項の確認待ち | 投稿・preprint 公開を出願締切の 2〜3 週間前までに |

## 2. 関門（日付順）
| 期限 | 関門 |
|---|---|
| 10/17 | 扁長の窓の端点確定／No.25 再裁定・No.28 本走開始／22j 方式決定／No.13 U_check 照合／pin 昇格の第1号（22k・33a）／原稿 §1–3・扁長局所の起草 |
| 10/31 | 22h O2 CLOSED／22j 証明書／No.34 設計凍結 |
| 11/07 | チェックポイント：両側の残量を数値化し、投稿月を確定 |
| 11/30 | No.32 D-OB closure（扁平の大域） |
| 12/25 | No.34 扁長の大域 |
| 1/15 | No.35 統合・最終監査 |
| 1/31 | No.36 投稿 |

## 3. 判断待ち（Judge）
1. 扁長の窓の端点（chat が認証値から案を起草）。
2. 22h：O2 P0–P1 の採否と P2 の道筋。
3. 15a・12：外部監査を投稿前に終えるか、付録の全証明で査読に委ねるか。
