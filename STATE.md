# STATE — 工程管理（最初に読む1枚）

版：v1.44（2026-11-09。Museの現行検収版（添付SHA256 53ce8d43b4d6b1b7defe553a85448e52f58b8a5a5c62eb44e3585cf8254bbaf2）でchat本来のchat_box_check.py SHA256 3fd3a81fbe78ea6b7878f4c3a3c2144c5a726637e10fbe9cc506f8e216fbf67e を確認し、T2/T3両箱の本来手順4項目全PASSが報告された。旧Muse再実装方式の留保を解消。Judge 11/08既承認3条件の下でT3正式採用、B7 V5.4公式28/40・D3=4/8・残12箱。D5 Plan Bは診断のみ・全域OPEN）。運用：**書き換え式**（追記しない。古い行は削除し、経緯は git 履歴に任せる）。上限 150 行。
更新：ChatGPT 起草・push → chat が GitHub で照合。他の AI は書き換えない。新しいセッションの AI は、まずこの1枚だけを読む。

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
- B7：**V5.3はFROZEN（Judge 2026-11-07、再開禁止、workers=0）**。V5.4 `L0_T0_D3` は Judge 2026-11-08 正式PASS（最悪 r=8、H下界≈+0.378777491488）。**`L0_T1_D3` はchat独立box checkの4項目PASSを経てJudge 2026-11-08正式採用**（H下界≈+0.4083351194、J≈+1.6037617983、最悪 r=8、mid/far 20,549セル・near 19,100葉、20セル×16小箱の再計算不一致0、最悪rの近帯全葉照合PASS）。**公式28/40**（D0・D1・D2各8/8、D3=4/8、D4=0/8、残12箱）。T0証拠：`cotaxxxx/bg-oblate-spheroid` `design/d-ob-p2` `analysis/B7_V54_D3_L0_T0_20261108/`（commit `291d09bb73d5f8585373e5a8ecfe84af763c140a`）。T1証拠・chat検収記録：同branch `analysis/B7_V54_L0_T1_D3_20261108/`、候補ZIP SHA-256 `4d6f27a82815d8c4d8a784a648a8372268a25db4a251da265bafda01d819deaa`（検収記録は2026-11-09転記登録）。**以後のJudge事前承認3条件（2026-11-08）：(1) Muse監査済みchat verifier一式 SHA-256 `68747f031bb89c1237c45322ad6c6b6f645458e6da923e3b9237056526dd7ec9` を無変更使用、(2) chat `chat_box_check.py` の4照合〔被覆、分数合計とH再計算、20セル×16小箱の再計算、最悪小箱の近帯全葉再計算〕すべてPASS、(3) 厳密下界H>0。**3条件充足で箱ごとのJudge操作不要。変更・不足ならJudgeに伺う。証拠ZIPの複数箱一括登録と正本STATEの即時事実訂正は別。**L0_T2_D3 は2026-11-09採用登録済み（27/40時点）、後着のMuse現行版で指定chat_box_check.pyによる4/4 PASSが追認され、代行方式の留保は解消**（H下界≈+0.446123294402、J≈+1.752155614608、最悪 r=8、mid/far 20,549セル41,097ノード、near 18,633葉37,265ノード、抽出20セル×16小箱320件不一致0、r=8のnear全18,633葉を再計算し分数・採用方式内訳まで一致：MIDPOINT 10,049 / ZEROTH 4,062 / ASTRA3 4,522）。T2結果ZIP SHA-256 `8b35ee40849d9fc3e68a556d2cb89a521c01be86fdd9ac37efbb2a91cf4d82cc`（証拠：`cotaxxxx/bg-oblate-spheroid` `design/d-ob-p2` `analysis/B7_V54_L0_T2_T3_CANDIDATES_20261109/`、commit `e89bed6c8545cba69ee318e2cb67db942fe4dabc`。ZIP内のREADMEは当時未採用時点の引渡し原本であり、本STATEの後続採用記録が優先）。**L0_T3_D3 は2026-11-09 Muse現行版の指定chat_box_check.pyによる4/4 PASSによりJudge既承認3条件が成立し正式採用**（r=8、H≈+0.486601930308、J≈+1.911114846188、mid/far 20,549セル41,097ノード、near 17,839葉35,677ノード、抽出320件不一致0、最悪rの近帯17,839葉の分数再計算PASS、MIDPOINT 11,050 / ZEROTH 2,991 / ASTRA3 3,798）。代行検収原本：`cotaxxxx/bg-oblate-spheroid` `design/d-ob-p2` `analysis/B7_V54_L0_T2_T3_CANDIDATES_20261109/MUSE_PROXY_ACCEPTANCE_B7_V54_T2_T3_20261109.md`（commit `9ba503c54e73522db339d395c38416d16fcbc9be`）。Muse代行の初期検収は `my_box_check.py` 再実装だったため旧検収原本では手順留保としたが、2026-11-09後着現行版により、Museが指定 `chat_box_check.py` SHA-256 `3fd3a81fbe78ea6b7878f4c3a3c2144c5a726637e10fbe9cc506f8e216fbf67e` を照合のうえ元の抽出基準（最悪セル優先＋種20261108）で両箱にBOX CHECK PASSを得たとの追加報告を受領。**T2・T3とも条件(2)を充足、T3を公式28/40へ登録**。代行時点の旧原本は `analysis/B7_V54_L0_T2_T3_ACCEPTANCE_20261109/MUSE_PROXY_ACCEPTANCE_20261109.md` （SHA256 `51d2da5a631f342723941223e8a1953c8ff292dbc90eb77951fd4ab415dc8b0e`）に保存。**後着現行版の同一原本**：proof repository `design/d-ob-p2` `analysis/B7_V54_L0_T2_T3_ACCEPTANCE_20261109/MUSE_ACCEPTANCE_CURRENT_20261109.md` SHA-256 `53ce8d43b4d6b1b7defe553a85448e52f58b8a5a5c62eb44e3585cf8254bbaf2`、commit `e3f2c4974aa222bc076d706be885a346fca8f581`。Dig自身によるchat原スクリプトの独立再実行は主張しない。残り12箱も未採用。Muse §8 の「23/40」は作成当時の正しい公式値。その後の L0_T0_D2 採用で24/40、L0_T0_D3 採用で25/40、L0_T1_D3 採用で26/40、さらに L0_T2_D3 採用で27/40、L0_T3_D3 採用で28/40になった（当時の原文は変更しない）。B7-D4帯OPENと工程D4 B_003の条件付きCLOSEDは別。D5全体はOPEN。
- λ 規約：a₁=a₂=λ^(−1/3)、a₃=λ^(2/3)。λ<1 扁平、λ=1 球、λ>1 扁長。回転軸は z。
- 論文の主役は停留構造。分岐はその λ 変化、認証は方法。
- D-OB の内部（L1）は Form II（一様下界）を目標とする。ROUTE は δ_L1 確定まで UNDETERMINED。
- 統治：事前宣言 → 監査 → FREEZE → 実行許可。診断は証拠にしない。版上げのみ。fail-closed。
- 役割：Dig＝ChatGPT（Astra）／監査＝Claude（chat）／独立監査＝Muse。Judge の裁定権限は別。ChatGPT は調査・起草・実装・GitHub 登録を担当する。
- 効率規則（Judge 10/11、`audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_3_2026-10-11.md` 末尾）：数学的指摘は慎重に止めて Judge 裁定（数学的結果を誤記する台帳欄を含む）。手順上の指摘（pin・ラベル・文言・resume 配管）は次版にまとめ、追加の監査往復やボタンを作らない。ファイルは ChatGPT→GitHub→chat で流し、Judge の中継を求めない。正の台帳はこの STATE.md と `UPSTREAM_PINS.md`。

## 4. 部品表
### 扁平（D-OB）
| # | 部品 | 状態 | 根拠（1行） | 次の関門 | 担当 |
|---|---|---|---|---|---|
| C | 軸上 C 系列（C0, C1a–d, 帯） | ① U_check＝v0.5 run4 PASS（160/160 両系統、`26d81e1`／family `40e83b5c`）→ Judge 10/13 条件付き CLOSED（D6 束・G0/E1 v3 条件、receipt `audits/C_GAP1_JUDGE_RECEIPT_2026-10-13.md`）。残＝空白②と global cover assembly。 | 文面は監査済み（`drafts/2026-10-10/`）：① 事前宣言 v6、② v3、実装設計 v1（v2 へ文面修正のみ）、端点追補 v2、数値契約 v1。方式：①は λ を 1/3200 刻み 160 slab（L・X・R の3群）、R は 9/20 から左へ C1b の予測規則（P2＝ROOT_TARGET 1/128）、端点は t_e からの累積平均値形（g は t_e の1点、[t_e,1] は幅 ≤1/512 の Gt 箱、粗い定数 C_Λ は使わない）、B_ob は帰結（receipt は照合のみ）。統合補題 G0/E1 v3 PASS（C2 恒等式の記号検算・機械 Gt のソース一致を含む） | FREEZE 前：① 契約 v7 は FREEZE 対象として確定（`drafts/2026-10-11/C_GAP1_CONTRACT_DRAFT_V7.md`、a4914818、文面 PASS、補足2点は記録で拘束、監査文面との同一性確認済み `audits/CHAT_RECORD_V7_EXACT_FILE_IDENTITY_2026-10-11.md`）。D6＝**充足**（Judge 10/11）：5afa815f・7cb9b809 は CROSS_LINEAGE_AI_AUDIT_PASS（補題監査 ChatGPT・Code、closure record `drafts/2026-10-11/D6_GAP_CLOSURE_RECORD_V0.md` d7a8d28c を chat・Code が監査、拘束読み B1・B2・K1・K2 は `audits/CHAT_AUDIT_D6_GAP_CLOSURE_RECORD_V0_2026-10-11.md` §3・§5）。論文で CLOSED と書く条件：補題 v1.1（closure 11 項目と B1・B2・K1・K2 を反映）とその監査、Astra（指示書 v2 `drafts/2026-10-11/ASTRA_D6_LEMMA_AND_CLOSURE_AUDIT_INSTRUCTION_V2_2026-10-11.md`）、人間の外部監査。残る FREEZE 前の関門：① の実装は **v0.3 PASS（static）**（`submissions/2026-10-11/C_GAP1_IMPL_V0_3_SUBMISSION_2026-10-11.tar.gz` 2ec6e70f、監査 `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_3_2026-10-11.md`。import 17本 `audits/CHAT_RECORD_GAP1_IMPORT_CLOSURE_17_2026-10-11.md`、F1–F5・A1・A7 解消、B1–B12 受理）。**v7 run2 STOP**（10/12、`runs/2026-10-12/C_GAP1_V0_3_RUN2_STOP/`：slab 126〜159 は ACCEPT、slab 125 [5621/12800,11243/25600] で TUBE 不成立、根 T* が t=1/2 へ近づくことによる R 方式の劣化で、反例ではない）。Judge 10/12：**契約 v8＝R/X 境界を 703/1600 へ**（X 8・R 34、gating 点 281/640 は不変）、実装 v0.4 → chat 監査 → X 診断（NOT_EVIDENCE）→ run3（`drafts/2026-10-12/C_GAP1_CONTRACT_V8_DELTA_AND_IMPL_V0_4_INSTRUCTION_2026-10-12.md`）。 **run3 STOP**（10/12 10:56、slab 117 [11183/25600,699/1600] で L 未解決、λ_x 左側の同じ構造）。Judge 10/12：**契約 v9＝L/X 境界 λ_b を左へ**（slab 117→109 の範囲で X・L 診断により決定、C1a 点 699/1600 は不変）→ 実装 v0.5 → chat 監査 → run4（`drafts/2026-10-12/C_GAP1_CONTRACT_V9_DELTA_AND_IMPL_V0_5_INSTRUCTION_2026-10-12.md`）。 **v9 診断 STOP**（14:23、L は λ_x から 0.004 離れても壁 g(1/2) を数値で負にできない）。Judge 10/12：**v9.1＝λ_b=83/200 に固定**（L 48・X 78・R 34。X は gate D で g(1/2)<0 を解析的に得る）、X・L 並列診断（NOT_EVIDENCE）→ v0.5 → chat 監査 → run4（`drafts/2026-10-12/C_GAP1_CONTRACT_V9_1_DELTA_2026-10-12.md`）。実行順は C 空白①→D5（同時占有禁止）。② の封印ディレクトリは確認済み | ChatGPT |
| D1 | 極 corner 境界面 FT_q | FT_q V3＝採用記録のみ・原本欠落（再現不能）。仕様・producer・checker・4096 枝証明書・m_V3 厳密値原本・chat 独立再計算 artifact はいずれも未発見（欠落台帳 `d481d79`）。2026-11-03 まで探索し、揃わなければ NOT_EVIDENCE として FT_q V4 再認証の事前宣言へ移行。L3 は 10/17 に継承条件付き FREEZE（δ₀ = 3/10^8、H > 273790294597/(7·10^12)）。**L3 継承条件 (4)：第6段で使用する FT_q V3 下界 M の原本欠落（`d481d79`）。この入力の再認証までは L3 の証拠連鎖は未充足。**pin：`1b65c7c`。南側 39′ は readback 済みで CLOSED（P1 条件付き） | 南側 39′ は `UPSTREAM_PINS.md` V1（`bbcfe662`、照合済み・再実行一致）、C45/C43、22″ v1.2 `d445b302` | 残りの構成部品の pin 昇格 | chat |
| QM | QM-1 三階微分上界 | 適用範囲 DISCHARGED（`ec5e121`）。QM-1 は Muse 独立監査 PASS（`f30ca10`、非阻害的指摘3件）、chat 照合済み。元の chat 監査記録は所在不明。Judge 10/31 確定（QM-1 Muse 独立監査 PASS）。残る条件は P1／Lemma V 束（No.15a）のみ。全体の無条件 CLOSED ではない。 | `bg-oblate-spheroid` `design/d-ob-p2` `analysis/MUSE_INDEPENDENT_AUDIT_QM1_2026-10-31.md`（commit `f30ca10f09f3bc568ad9f1dcb1c19f01cd4f5d0d`、原本 SHA-256 `6382f3e8a80151845c2c892cd98ddbe5911648c594681eb3f4fdd89848e185c7`） | P1／Lemma V 束の外部監査、Judge 裁定 | chat / Judge |
| D2 | 極 corner 内部 L1 | O1 CLOSED（P1 条件付き）。O2：v1・v1.1-r1（O2-A3）FROZEN、P0–P1 ADOPTED。R1＝FAIL-CLOSED（項ごとの絶対値上界が成功条件の約 3×10⁶ 倍）。**R2 枠組み FROZEN**（Judge 2026-10-10、v0＋v0-r1 差分）：M_+ を (λ,τ,r) の閉箱（r=1・τ=1 を含む）ごとに符号付き積分下界・有理包囲・Bernstein で直接認証、全箱共通の h_*>0（P 単位）。補題 R2-L1：D²≥(a−|ξ|)²+(λμ−z)²。t 積分の許容方式 R2-T1（τ≤τ₁、正確な割線）／R2-T2（τ≥τ₁、ξ=0 展開、g⁽⁴⁾ が必要）。L1 は Route K／Route B の二経路比較（10/17 Judge、`bd041c0`）。10/24 期限の比較報告は未提出。10/31 CLOSED は保証なし | pin：basepoint-geometry `chatgpt/d-p2-o1-predeclare-v1-20261009` commit `fbadfc4d`（R2 v0 `764c1860…e8be`、v0-r1 差分 `957b7d00…6aa`、v1.1-r1 `7dcbd6d6…12c5`、P2 v1-r1 `3f0fcdb3…6b5d`、chat が GitHub 上で照合済み） | P2-b（R2 の実行事前宣言：箱・セル数・近似次数・誤差予算・τ₁・g の包み・工数見積り）→ 監査 → FREEZE → 実行 → 独立検証 → O3 → O4–O6 | ChatGPT |
| D3 | L3–L1 接続 | UNDETERMINED | 仕様 v1 `ecd31446` | D2 に従う | — |
| D4 | D5 V3委譲の閉箱 B_003＝(0,0,3)、r,τ∈[0,1/8]、λ∈[119/200,33/50]（r=0・端点を含む）。旧3,584 unresolvedは歴史的診断サブセット | **B_003全域の被覆はCLOSED（P1前提つき）**：chat独立監査PASS・Judge条件付きCLOSED（監査原本登録済み）。高λ帯中心列（r≤1/8、τ∈[0,1]、λ∈[119/200,33/50]）はB_003を完全に含み、ρ²+(z/λ)²=r²≤1/64。**D4工程全体の無条件CLOSEDは宣言しない。**監査原本SHA-256 `7eae9f035cac17f806cbdef372f49c68d372918d469d6ec769fa6756459249c4` は実ファイルから一致確認済み | `cotaxxxx/bg-oblate-spheroid` `design/d-ob-p2`：原本 `analysis/D5_CENTER_HILAM_20261106/CHAT_AUDIT_D5_CENTER_HILAM_20261106.md`（commit `24c6c8b5c4b59573fea29033eac6bc237b53ab0d`、blob `d0b3cb6ba322e1aeb70dbfb96565d5bdec9ff5e8`）、同README／D5 SPEC V3 §0。Dig受領記録は歴史資料 | 監査原本のbyte-level登録とchat被覆照合は完了。P1継承・D4工程の統合記録を確認。B_003被覆をD4全体閉鎖と取り違えない | Dig / chat / Judge |
| D5 | 一般域（区間認証本走） | **B′ v2 外側境界面 r=1 は CLOSED（Judge 2026-11-07、面の定理 H≥1/5、m_∂=1/5、τ∈[0,1]、λ∈[2/5,33/50]）。** 832/832 両系統・Muse監査PASS・chat再計算20/20分数一致。最小値は verifier +0.3204609366、producer +0.2642053359。**外側薄層 r∈[59999/60000,1] は2026-11-08 JudgeによりP1条件付きCLOSED（H≥607/6000）。厚いカラーの残り r<59999/60000 と一般域はOPEN、D5全体はOPEN、FT_q V4との照合はOPEN。** **中心列 r≤1/8、τ∈[0,1]、λ∈[2/5,33/50]：chat監査PASS・Judge条件付きCLOSED（P1前提、原本登録済み）**。一般域V3はABORTED / NOT_EVIDENCE（10/18）・V4再設計中、254箱の完走ではない。43,654 unresolvedは診断資料 | **薄層カラー採用証拠**：cotaxxxx/bg-oblate-spheroid `design/d-ob-p2` `analysis/D5_COLLAR_LEMMA_20261108/`（commit `7522ec057ff5e0c1639a3437d63f1ee56a1e46e9`、chat ACCEPT・Muse PASS、P1条件付き）。**Plan B格子C較正（いずれも診断のみ／NOT_CERTIFIED）：第2回（11/08、最深d∈[1/32,1/16]、負帯2倍・β=1）E=−0.572962576、M=−12.178898060。第3回（11/09、同最深、方式(c)：β=2・i=3..8を4倍・負帯2倍、重複帯は8倍）は最悪子箱で E=+0.0540726069、M=+0.2271157309。境界d∈[1/64,1/32]は第3回β=1・負帯2倍ではE=−0.2076933752、M=−5.0402948880であったが、11/09 07:54完了のβ=2自動細分では2子箱の最小でE=+0.0525925164、M=+0.2019890255。正値は代表E/Mの対象親箱のみ。全9,984箱の本走・独立verifier・大域CERTは未実施／OPEN。第3回のGitHub証拠：`analysis/D5_PLANB_ROUND3_20261109/` commit `20ce0adf7fdc4f454e7b91c0f066a31857c8e0a2`。境界β=2の原本JSONは外部PC `D5_PLANB_BOUNDARY_AUTOSPLIT_20261109/`に保存。** **B′ v2採用証拠**：cotaxxxx/bg-oblate-spheroid の design/d-ob-p2、analysis/D5_BPRIME_V2_20261107/（commit 8da3174f847fd4e9fd58ceaf1cd613b66b72fde4。chat検収 SHA-256 f0b11a64925089142a713bba0ab96181415d6a6bfa06b446d2d9d30ac35a480c、Muse原本 SHA-256 7e5997a059abfc92061514c6d4d90bfa3a93365ee5b3e5286c10ad5d85dbb033、証拠ZIP SHA-256 027f42f0140144bfaf90eec958d05b7e5b8ac24f81e995ef316bec2fe8a99b81）。 `cotaxxxx/bg-oblate-spheroid` `design/d-ob-p2`：監査原本 `analysis/D5_CENTER_HILAM_20261106/CHAT_AUDIT_D5_CENTER_HILAM_20261106.md`（commit `24c6c8b5c4b59573fea29033eac6bc237b53ab0d`）・README（Dig受領記録は歴史資料）、旧V3停止記録 `analysis/D5_V3_RUN_ABORT_RECORD_2026-10-18.md`。正規化被覆SHA-256（登録済みchat監査原本の記載）M40′ `8bd4725fe89408f35796607db6d3cb4c1ca384a61e1567327d946e93b780be07`／M22′ `8886d04376b60172df71502ce4c2cbabc7c2cd498f15e1c1b4a4aeda2c55446a`。監査原本SHA-256 `7eae9f035cac17f806cbdef372f49c68d372918d469d6ec769fa6756459249c4`（実ファイル照合済み） | 外側薄層は条件付き採用済み。厚いカラーPlan Bと一般域は未認証であり、V4の内側到達半径も未認証。監査原本・完全SHA登録照合済み。一般域境界A9/B2・V4事前宣言→chat監査→Judge。V3 resumeおよび全域本走は未承認 | Dig / Code / Astra / chat |
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
