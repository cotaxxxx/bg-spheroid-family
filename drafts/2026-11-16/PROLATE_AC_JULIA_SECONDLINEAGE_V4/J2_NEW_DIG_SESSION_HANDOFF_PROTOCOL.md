# J2｜新しいDig clean-roomセッションへの入力pack受け渡し手順

2026-11-16 / 監査側の引渡し記録案 / **SESSION_NOT_STARTED**

## 状態
- chat V26：入力pack V1 I0 PASS、環境PASS。
- V2（J1・J2追記）はchat差分監査待ち。
- **実装者は、この監査・編集チャットではなく、新規のDigチャット（新しいセッション）**とする。
- **新規セッションはまだ作成していない。** 初回受領ログも未作成。
- Q、Q′、H₄、Q_zの導出コード・証明計算は未実施。

## 清浄な引渡し物（1ファイルのみ）

- ファイル：`ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md`
- SHA-256：`a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd`
- 数学内容：元の幾何定義、参照体正規化、導関数の定義と範囲、J1の座標倍率、J2のプロトコル。
- **初回に渡してはならないもの：** V26監査記録、第一系統のソースやJSON・原稿、比較値、v3/v3.1統治事前宣言、第二系統の検証付き積分契約。
- **初回の受領ログを監査側に残すまで、導出に着手しない。** チャットの新規作成と初回ログはJudgeまたはDig実装者が行う。
- 実装者側では、以前の会話・メモリー・接続済みGitHubやRemote Desktopを通じて第一系統の式や出力が入らないよう、最初の導出は**添付pack1件以外の資料参照を禁止**する。外部ソースや既往会話の実質的な隔離が確認できない場合、clean-room独立性をPASSと判定せず**INDEPENDENCE_OPEN**にする。

## 新規セッションの最初の記録（テンプレート・まだ提出していない）

```text
CLEANROOM_J2_RECEIPT
SESSION_ID: <new Dig session ID>
SESSION_START_UTC: <ISO8601>
IMPL_PERSONA: Dig (new isolated session)
INPUT_FILES_COUNT: 1
INPUT_FILE: ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md
INPUT_SHA256: a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd
OTHER_MATH_INPUTS: NONE
FIRST_LINEAGE_CODE_OR_RESULTS_SEEN: NO
AUDIT_RECORD_SEEN: NO
CURRENT_STAGE: I1_SYMBOLIC_DERIVATION_ONLY
```

実装者は原始Eから独立に積分式を導出し、その式・コードのSHAを先に封印する。**封印したあとに**、監査済みの積分契約V2を別途与えて実装する。chatによるI2記号照合に進むまでは、第一系統の数式・数値を一切実装者へ開示しない。

本書は記録側の手順書であって、**新しいセッションを作成した証拠ではない**。
