# C系列の大域軸被覆｜組み立て台帳 v0

2026-11-16 / Dig draft / **GLOBAL ASSEMBLY OPEN — NOT A PROOF OR JUDGE RULING**

## 0. 目的と正本の状態

対象は扁平窓 λ∈[2/5,33/50]、軸 t∈[-1,1]。まず正の半軸 0<t≤1 について、既存のC0・C1a〜d・帯 [31/32,1]・空白①・空白②の証拠を接続し、後で奇性を使って負の半軸と中央 t=0 を扱う。本書は証明そのものではなく、証拠の領域の被覆と論理接続をchatが監査するための設計台帳である。**軸C全体・D-OB globalをCLOSEDと宣言しない。**

2026-11-16正本STATE v1.60（family main 3519926）では、空白②はJudge V21でCLOSED、空白①は条件付きCLOSED、D系列はJudge V18でCLOSED。軸C大域の組み立てはOPEN。

## 1. 領域の七つの部品

| 番号 | λの範囲 | tの範囲（正の半軸） | 入力する証拠の種類 | 利用可能な帰結と限界 |
|---|---|---|---|---|
| L0 | [2/5,83/200] | (0,1/2] | C0a・C0b、C0解析移送 | gの三階微分符号・右壁符号と中心分岐の符号構造。C0 Judge receiptは二つの補題を条件としていた |
| L1 | [83/200,9/20] | (0,1/2] | C1a機械とlower-half lemma | F_x=2g(1/2,λ) が厳密単調、λ_x∈(83/200,9/20)。根数・中心H符号との接続は組み立てで検証する |
| L2 | [9/20,5/8] | (0,1/2] | C1c + C1bの正の1/2アンカー | g>0、非零根なし（C1c解析組み立て、条件付き根拠） |
| L3 | [5/8,33/50] | (0,31/32] | C1d三階微分＋31/32正のアンカー＋解析補題 | g>0、非零根なし（C1d解析組み立て） |
| U1 | [2/5,9/20) | (1/2,1] | 空白① v9.1、run4 | 160/160両系統PASS、Judge条件付きCLOSED。端点λ=9/20は隣のC1bで接続 |
| U2 | [9/20,5/8] | (1/2,1] | C1bの左外側・TUBE・右外側と空白②Judge V21 | C1bの159受理区画、unclamped124の上側、clamped35。右の外側R/R_MONOの閉被覆を含む |
| U3 | [5/8,33/50] | [31/32,1] | 局所境界侵入band Judge receipt | g(31/32)>0、∂tg<0で単調減少。B_obの符号・零点との接続は条件付き根拠 |

L0〜L3とU1〜U3の合併が正の半軸全体を覆うという**有理端点だけの組合せ**は、同梱の exact_tile_check.py で検査する。組合せPASSは各領域の数学的符号や独立監査の代用ではない。

## 2. 接続（数値の再実行なし）

1. **λ=83/200**：C0とC1aの下側の閉端点で、Φとg(1/2,λ)の符号構造が一致すること。C0の局所分岐結論とC1aの横断を接続するためのH_axis(λ)の既認証情報を明示する。
2. **λ=9/20**：空白①の形式上のλ上端は開区間。C1bの左端は閉区間であり、未被覆点がない。根の同一枝としての接続は単なる被覆の一致とは別の主張として、必要なら連続性・一意性で証明する。
3. **λ=5/8**：C1cの右端、C1dの左端、C1bの右端、境界bandの左端が一致。t=31/32でC1dの正のアンカーとbandのClaim 3を照合する。C1bのroot tubeがこの境界を横切る場合も根数の重複を避ける。
4. **t=1/2**：C0b負、C1aのF_x符号横断、C1b/C1cの正のアンカーがλの各領域の境界と整合すること。空白①は1/2より上だけで、下の領域の閉境界に接する。
5. **t=31/32**：C1dとbandは閉境界で接する。C1bには31/32のbookkeeping cutがあるが、真のTUBE端点t₊はそれとは別。C1bのunclamped親124についてt_e=max(31/32,t₊)、うち106親はt_e=31/32、18親はt_e>31/32。後者の中間区間を空白と誤認しないこと。
6. **t=1**：C1b clamped35はt₊=1、unclamped124はJudge V21上側門が端点に到達。U1は端点門を含む。bandは片側微分とB_ob同定による端点接続。
7. **t=0 と負の半軸**：各D6解析補題で奇性とt=0での延長が証明される範囲を明示し、正の半軸の議論を符号反転して移す。中心t=0での分岐はC0および関連する軸Hの符号構造を利用する。

## 3. 根数を述べる前に必要な区別

- 有理長方形の被覆は「空白領域がない」ことしか保証しない。gの符号・三階微分・端点の上下界はそれぞれ凍結した個別証拠に由来する。**被覆証明だけで根数は言えない。**
- C1aが定めるλ_x、C0が定めるλ_c^ob、bandが定めるλ_∂^obの相対配置と根数の切替条件を、それぞれの機械・解析証拠に照合する。端点λ_x、λ_c^ob、λ_∂^ob自体の扱いも分離する。
- C1bの機械検収済み範囲と空白②のJudge CLOSEDを部品として用いるが、それだけでC1dやbandの証明範囲を代替したとは扱わない。
- 右の外側[ t₊,31/32 ]を取り込むunclamped106親について、閉被覆とR/R_MONOの全真をchat V21で確認済み。U₂の残り18親はt_e>31/32で、全124親が深さ0ACCEPT、REFINE/ABORT=0。
- bandについては∂t g<0 on [31/32,1]、g(31/32)>0とB_obの境界符号から、λ<λ_∂^obで上側1根、λ=λ_∂^obでt=1、λ>λ_∂^obで上側0根という**条件付き結論**がJudge receipt §6に記される。B_ob零点の一意性と定義域を最終組み立てで再照合する。
- D-OB横断D系列のCLOSEDと軸Cの大域CLOSEDを混同しない。D-OB globalの裁定はchatによる本稿の検収後の別工程である。

## 4. 根拠原本（証拠の格付けを混ぜない）

- C0: bg-oblate-spheroid analysis/GLOBAL_AXIAL_C0_JUDGE_RECEIPT.md（C0a/C0b Judge PASS、解析補題は条件付き）。
- C1a: analysis/GLOBAL_AXIAL_C1A_MACHINE_RECEIPT.md（F_x単調、λ_x∈(83/200,9/20)）。
- C1b: analysis/GLOBAL_AXIAL_C1B_MACHINE_RECEIPT.md（159区画の厳密被覆とTUBE）。
- C1c: analysis/GLOBAL_AXIAL_C1C_ANALYTIC_ASSEMBLY.md（[9/20,5/8]のlower half）。
- C1d: analysis/GLOBAL_AXIAL_C1D_ANALYTIC_ASSEMBLY.md（[5/8,33/50]の0<t≤31/32）。
- band: analysis/LOCAL_ENTRY_BAND_JUDGE_REQUEST.mdとLOCAL_ENTRY_BAND_JUDGE_RECEIPT.md（Claims 1–3、条件付き）。
- 空白①: family audits/C_GAP1_JUDGE_RECEIPT_2026-10-13.md、run4凍結commit 26d81e1049340d44ef7f08ae8e17d0692983395b。
- 空白②: family evidence/c-gap2-freeze-20261115 commit 151d3c5（Judge V21 CLOSED）、本走原本4ecb713、比較器補完a2255fa、実装0d32ac2。JSON SHA256 6fb9d29238cd73c023c96f87f202255c743e968c7b39a32853ff25c8df3b975b。
- D6: V13/V19/V20 chat監査PASS。V20証拠fc9e48e、C1c blob6fba6e4f、C0 transfer963b03be、C1d blob35656381。**外部人間監査の有無とJudgeの最終global裁定は別件**。
- 調査時のoblate証拠クローンHEAD: 59aed60305fca61fd63551f49fe9667ff1acfad4。各歴史的machine receiptの状態文（EXTERNAL_AUDIT_PENDING等）は、2026-11-16のV20監査やJudge V21を上書きする文書ではない。

## 5. chat独立監査へ依頼する項目

A. 4本のλ境界とt=1/2,31/32,1での被覆・開閉区間、奇性から負側へ戻す射程。

B. C0・C1aのλ_c〜λ_x間でH_axis符号とΦ単調性から根数を正確に導くための正本ピンと論理鎖。

C. C1bの159区画（35 clamped/124 unclamped）、空白②の124親、106親のR/R_MONO、端点符号の接続。

D. λ=5/8でのC1b root tube・C1dの正アンカー・band rootの一意性に矛盾や二重計上がないこと。

E. 根数分類がそろったあとに、λ_c・λ_x・λ_∂の零点での扱いと大域結論を別の本文として立証すること。

**このv0を採用すると宣言しない。数学的グルーのchat監査が必要で、C-axis globalはOPENのままである。**
