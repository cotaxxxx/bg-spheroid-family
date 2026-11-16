# 扁長 P1 a_c 第二系統｜事前宣言 DRAFT v3.1（V26 J1〜J6反映）

2026-11-16 / Dig（ChatGPT）／**I0 V1・環境 V26 PASS、pack V2・契約V2差分監査待ち／NOT_FROZEN・NO_PROOF_EXECUTION**

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
  `ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md` **だけを新しいDigセッションの最初の数学入力**とする。
  SHA-256 `a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd`。
  ここからQ、Q′、H₄、Q_zを独立に定義・導出する。
  被積分式は現時点で未作成であり、第一系統のソースを第二系統へコピーしない。
- **監査者の契約文**：
  `VERIFIED_QUADRATURE_CONTRACT_DRAFT_V2.md`
  SHA-256 `1f8bbce7e4e3cde55a113d37b874b3931ebf061d600fa8764e3c8be334fdd84d`。
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
| I0：数学入力 | chat | V1原始定義混入なし、J1参照体・J2受領ログ追加 | **V1 PASS（V26）、V2差分監査待ち** |
| I1：独立導出 | 新しいDigセッション | pack V2だけを受領したログ→独立にQ、Q′、H₄、Q_zの式・微分交換・端点正則性を導出し封印 | **J2新セッション未作成／I1未着手** |
| I2：記号同一性 | chat | 封印された導出式と第一系統を記号比較。実装者に第一系統の式・数値を見せない | **未実施** |
| I3：検証付き積分 | chat | 自作Interval{BigFloat} Taylor jet、有理入力、isguaranteed、厳密有理checker、端点剰余を監査 | **V2契約DRAFT／差分未監査** |
| I4：実行裁定 | Judge | I0–I3 PASS、Manifest/実装/資源/SHA/FREEZEに明示承認 | **未許可** |

**I0 V1はV26 chat監査PASS。** ただしpack V2差分のchat PASSと、J2の**新しいDigセッションの実在・初回pack単独受領SHA記録**までは、I1の導出や実装を開始しない。既存の監査・編集セッションはclean-room実装者にならない。

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

導出された一次元または有限次元の積分領域の有理分割、πの有理上下界、
セル別のTaylor積分と厳密剰余を**契約V2**で規定する。1D積分を実装者へ指定しない。
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

- **済み：** Julia/IA隔離インストール、Project/Manifest固定、I0 V1 chat V26 PASS、pack V2（J1/J2）と契約V2（J3〜J6）を作成、算術J4 smokeで有理bracketと保証フラグPASS（**NOT_EVIDENCE**）。
- **未了：** pack V2・契約V2差分chat監査、J2の新規Digセッション受領ログ、I1独立導出・実装、I2記号照合、I3の全使用関数・jet・剰余監査、FREEZE・認証本走。
- **次の一手：** chatへpack V2・契約V2の差分とJ4 smokeを提出。chat V2差分PASS後に新しいDigセッションへpack V2だけを添付し、SHAとSESSION_IDを最初に記録する。その後I1を開始する。

**FREEZEも本走も行っていない。**

## 7. V26 J1〜J6の明示的な採用区分

- **J1：** 参照体`K_λ`でのQ/Q_z/H₄が数値門の基準。体積保存体の二階係数は`λ^(2/3)`倍、四階は`λ^(4/3)`倍。Q′は単純倍率にならない。
- **J2：** 新規Digセッション・pack V2のファイル名／SHA／セッションIDの初回記録。**J2_SESSION_PENDING**。
- **J3：** 自前Taylor jet(b)を選択。TaylorSeries.jlは追加しない、Manifest SHAは不変。jetと剰余はchatの別監査。
- **J4：** `Rational{BigInt}`のみから入力。Float64リテラル禁止。最終門で全区間`isguaranteed=true`。MPFR外包の軽量実証はPASS、P1認証ではない。
- **J5：** checkerは台帳の有理端点から被覆・Taylor剰余・π・区間和・門の符号を再計算。被積分関数の再求積は要しないが、係数包囲の正しさはI3の解析・コード監査で担保。
- **J6：** I0・I2はchatが担当。実装者には第一系統の数式・出力、監査記録を渡さない。外部委託増加なし。

V26監査原本：family `evidence/c-gap2-freeze-20261115` commit `12bb2d183ef9f7367233a0aa9740aa046a36fa43`。
旧v3および旧v2を上書きしない。本書は**DRAFT**で、J2新セッションもJudge FREEZEも未了。
