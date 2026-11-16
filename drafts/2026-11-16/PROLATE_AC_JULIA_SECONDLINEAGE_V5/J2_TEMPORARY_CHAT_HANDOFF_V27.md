# V27 K2｜clean-room一時チャットの立ち上げ・受領記録

2026-11-16 / 監査側手順書 / **SESSION_NOT_STARTED・I1_NOT_STARTED**

## 目的

既存のChatGPTセッションは第一系統の証拠と監査記録を見ているため、clean-room I1導出に使用しない。
ユーザーが**新しいChatGPT一時チャット**を開き、入力pack V2だけを添付して導出を依頼する。

一時チャットはメモリを使わない状態で開始し、**GitHub・研究用PCの接続を使わず、追加ファイルやリンクを読ませない**。
この状態が確保できない場合、独立性をPASSと扱わず隔離方式を見直す。

## 最初に渡す唯一の添付ファイル

- **ファイル名：** `ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md`
- **SHA-256：** `a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd`
- **元の登録：** family draft commit `750cc2c2ecd14e83ebdcc535918cbf5b51002cc9`。
- **V27での判定：** pack V2 I0 PASS。内容を変更しない。

**最初に渡してはならないもの：** chat V26/V27の監査記録、契約V2/V2.1、第一系統のコードや導出式・JSON・原稿、GitHubのリポジトリURL、研究用PC上のファイル。
一時チャットにGitHub・研究用PCの接続を有効にしない。

## 一時チャット最初の依頼文（コピー用）

> 添付の ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md だけを数学的入力として使用してください。
> 定義から Q、Q′、H₄、Q_z を独立に導出し、積分表現と正則性・微分交換の根拠を示してください。
> 第一系統の資料、既存の式、GitHub、外部接続、以前の会話、メモリーを参照しないでください。
> 一次元積分の形を強制せず、原始的な境界積分から導いてください。
> 導出式を一つの独立した文書に固定し、その文書の正確なSHA-256と受領したpackのSHA-256を記載してください。
> 実装、Juliaによる数値計算、証明認証の本走は行わないでください。
> 数式の封印後、その文書を私が別のchat監査側に提出します。

## 必須の受領ログ（ユーザーまたは新セッションが記録）

```text
CLEANROOM_J2_RECEIPT
NEW_TEMPORARY_CHAT: YES
SESSION_ID: <新チャットの識別子。取得できなければ未取得と明記>
SESSION_STARTED_AT: <記録できる開始時刻>
MEMORY_USED: NO
GITHUB_CONNECTED_OR_USED: NO
RESEARCH_PC_CONNECTED_OR_USED: NO
INITIAL_INPUT_COUNT: 1
INITIAL_INPUT_FILE: ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md
INITIAL_INPUT_SHA256: a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd
FIRST_LINEAGE_MATERIAL_USED: NO
V26_OR_V27_AUDIT_RECORD_USED: NO
DERIVED_FORMULAS_DOCUMENT_SHA256: <封印後に記録>
I1_STAGE: DERIVATION_AND_SEAL_ONLY
```

一時チャットの内部状態まで完全に証明できるとは主張しない。**実際に講じた隔離措置**を記録し、
導出結果の独立性はchat I2の第一系統との記号的照合で補強する。

## 封印の後（最初の入力として渡さない）

1. 導出式の文書を受領し、そのSHA-256をchat監査側へ提出。
2. chat側が封印済み式と第一系統を**I2記号照合**。その結果（第一系統の式・値）を実装者には渡さない。
3. 同じ一時チャットで、**導出式封印のあと**にのみ、監査済みの契約V2.1を渡す。実装はJulia専用環境だけで行い、第一系統repoに触れない。
4. I1/I2/I3の監査とJudgeの別FREEZE・明示実行許可が出るまでは、数値認証本走はしない。

**この文書の登録は一時チャットの実際の開設、導出、SHA封印、Judge承認を意味しない。**
