# 扁長 P1 a_c 第二系統｜事前宣言 DRAFT v3（Julia承認反映）

2026-11-16 / 起草 Dig（ChatGPT）／**NOT_FROZEN・NO_PROOF_EXECUTION・CHAT_AUDIT_PENDING**

旧原本：family `drafts/2026-10-10/PROLATE_SECOND_LINEAGE_PREDECLARE_DRAFT_V2.md`。
Judge 2026-11-16「承認：Juliaで第二系統」により**ソフトウェア導入のみ解禁**された。
他のv2ゲート（clean-room・I0–I4・段階制・FREEZE・二系統検収）は維持する。
別件のJudge V25（Astra D-PRO設計採用）はP1 Julia証明の成功・本走許可を意味しない。

## 1. 固定する二系統と入力のアクセス制限

- **第一系統（比較対象だけ）**：
  `cotaxxxx/basepoint-geometry` main `abf704b8701f3da8eb41d8a99408570a413b2214`、
  `CERTIFICATES/prolate/local_bifurcation/`、
  manifest `SHA256SUMS.txt` の既知の SHA-256
  `3b6fc57de63c6154165bb22ea96905cc669e8be89680175aadb0b36a9f05c11d`。
  このコード・JSON・導出済みの積分核・原稿全文は第二系統の入力環境に置かない。
- **第二系統（実装前）**：
  `ORIGINAL_DEFINITIONS_INPUT_PACK_V1.md` **のみを数学入力**とする。
  SHA-256 `181e0e36b23bc5f37012ef59b2597c998d9f2fd252b4f7d608bd6df29643d63b`。
  ここからQ、Q′、H₄、Q_zを独立に定義・導出する。
  被積分式は現時点で未作成であり、第一系統のソースを第二系統へコピーしない。
- **監査者の契約文**：
  `VERIFIED_QUADRATURE_CONTRACT_DRAFT_V1.md`
  SHA-256 `5993c2c67ece17a644b6c5365c5dd34f755b6b08f95892b5e1facf1bab9ca277`。
  実装の数値積分手順はこの監査後に確定する。

## 2. 固定したJulia環境

研究用PC `daybreak-works`、専用
`/home/daybreak/D_PRO_P1_JULIA_SECONDLINEAGE_20261116`。

| 項目 | 固定値 |
|---|---|
| Julia | **1.10.13**（公式LTS）、公式tarball SHA-256 `f2bfa080db29b50a9bf250f69e9acdcfd8b7c49409dee5e55588f986706fb8bd` |
| IntervalArithmetic.jl | **1.0.10**、Manifest pinned=true、git-tree-sha1 `c3ee408ae340565f41699e3a3fa1053698c7626e` |
| Project.toml SHA-256 | `3b14e1942ba3d9c63b7be31f52934ce285cffbf8ce92f69d9327c1356933aee8` |
| Manifest.toml SHA-256 | `f1de48582bdef170b152b5a785490b3f176bc9c70fc0594e6589449c1d4d7350` |
| Julia depot | 専用`depot/`。既存Pythonのsite-packages、pyenv、FLINTを変更しない |
| 禁止依存 | Arb/FLINT/Arblibを算術coreに用いない（Manifest有効依存に不在） |
| 軽量動作確認 | Julia/IntervalArithmeticの版assertionと区間演算smoke PASS |
| 実行 | P1の数値計算なし、D-PROの本走・較正との同時重負荷なし |

`julia_env/Project.toml` と `julia_env/Manifest.toml` を**この事前宣言と同一コミット**に登録する。以後、監査なしのPkg.update/resolveによる変更を行わない。

## 3. clean-room関門 I0–I4

| Gate | 担当 | 完了条件 | 現在 |
|---|---|---|---|
| I0：数学入力 | Astra + chat | 幾何の元定義のみ、pack SHA固定、派生式混入なし | **提出稿／監査待ち** |
| I1：独立導出 | Dig／Julia側 | Q、Q′、H₄、Q_zの式・微分交換・端点正則性を独立に証明 | **未着手** |
| I2：記号同一性 | Astra | 第一系統の出力数値は見せず、2系統の導出の同値性を記録 | **未実施** |
| I3：検証付き積分 | chat | 有理区間、π外包、Taylor剰余、丸め、端点、独立checkerを監査 | **契約DRAFT／未監査** |
| I4：実行裁定 | Judge | I0–I3 PASS、Manifest/実装/資源/SHA/FREEZEに明示承認 | **未許可** |

**I0の結果が出るまでは、第二系統の派生コードを作り始めない。** 本書と積分契約のレビューは先行してよい。

## 4. 段階制の採否門（Judge 2026-10-10）

**Tier A必須：** `λ∈[47/10,19/4]` において
`Q_z≥1/100`、`Q′<0`、`H₄<0`、
`Q(4.72438)>0>Q(4.72439)`、
端点`Q(4.7)>0>Q(4.75)`も個別保存する。

**Tier B追加：** `Q(4.72438340452113340672)>0>Q(4.72438340452113340673)`、
`Q_z≥0.0885587746621582`。
Tier BのINCONCLUSIVEはTier AのPASSを取り消さない。
数学的に厳密な反対符号が出ればMATHEMATICAL_CONTRADICTIONとして両系統を監査へ戻す。

第二系統の判定は第一系統から**数値を借りない**。
Gate I2を通るまで数値の照合を禁ずる。

## 5. 具体的な精度・計算・停止の提案（まだ許可ではない）

積分`[0,π/2]`の有理化、πの有理上下界、
セル別のTaylor積分＋独立の厳密剰余を契約V1で規定する。
導出済みの核・微分支配・端点延長・実際の外向き区間丸めは
**証明とchat監査が残るFREEZE blocker**。

旧v2の候補は256→512→1024→2048 bits、
λ深度≤16、積分セル≤262144、総箱≤1048576、
Tier A≤120 core-hours、Tier B追加≤240 core-hours。
**これらは数値本走の認可ではない。**
研究用PCの物理RAM約29GiBに対して旧32GiB RSS案は過大である。
安全なRSS上限（案：24GiB）と同時作業停止規則は
FREEZEで新たにJudge確認を受ける。

監査不能・容量超過・正規化不一致・事前宣言違反はFAIL-CLOSED。
未完了記録も保全。自動再計算／自動リトライ禁止。
認証出力はchat独立検収とJudge採否を経て登録し、
それまでは**CANDIDATE**のみ。

## 6. この版が完了した範囲と次の工程

- **済み：** JuliaとIAを別ディレクトリにインストール、版・Manifest固定、軽量smoke、原始入力pack・検証付き積分契約DRAFTを作成。
- **未了：** I0～I3独立監査、第二系統の独立導出・実装、Julia外向き丸めと端点誤差の実証、第一系統の比較、FREEZE。
- **次の一手：** chatへpack・契約・Project/Manifestを提出。監査が済んでから、clean-room実装担当がpackのみを読んで導出する。

**FREEZEも本走も行っていない。**
