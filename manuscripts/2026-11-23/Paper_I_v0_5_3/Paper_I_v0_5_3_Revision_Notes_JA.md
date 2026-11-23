# 第一論文 v0.5.3｜公開前の監査指摘への対応（差分監査候補）

**作成日：2026年11月23日**  
**作成：Dig（ChatGPT）**  
**状態：Editorial revision candidate / Zenodo未公開 / 数学的証拠等級は不変**

## 根拠

- 前版：`Paper_I_v0_5_2_Manuscript_and_Verification.zip`（SHA-256 `c76656b02e01f12facbffc84e74d0cdee0e4f5d6f48220d23b4626fdb6d8fc4a`）。
- Claudeのv0.5.2差分監査PASS：`experimental-mathematics-ai-collaboration` の `docs/CHAT_AUDIT_PAPER_I_V0_5_2_DIFF_20261123.md`、commit `8c56cf8`。ユーザーが伝えた追加指摘（独立監査の範囲、一次記録の保全、改訂記録の表示説明、PDFメタデータ・言語表示）に限定して対応。
- V24一次原本：`cotaxxxx/bg-spheroid-family` commit `127be52046e9498d1306fe3d35c3e02e91c636de`、`runs/2026-11-16/D_OB_GLOBAL_CLOSED_V24/JUDGE_RULING_D_OB_GLOBAL_CLOSED_20261116.md`（Git blob `07d30eff3db759abd0e6aab1ef07563cf77049a2`、SHA-256 `89435cf9457f1245c337d4433ad074258dea1c954a3bec90613f03cd2f092c3c`）。

## 変更した本文（v0.5.2 → v0.5.3）

1. **第1ページの監査説明：** `independent audit of the supporting computations` を、**プロジェクト内の別AIが行った論証の組み立て・計算記録参照の照合**と説明。全計算の独立再実行ではないことを明記。
2. **第3節末尾：** 同じ監査の射程を数学的組み立て・出典照合と表現し、数値計算の独立な再実行ではないことを明記。
3. **第10節：** 上記監査の実態を正確化。V24一次記録が**日本語の作業記録**であることを追記し、原本をZIP内 `provenance/V24/` にバイト単位で保存していることを明記。
4. **第10節の `Use of AI tools`：** ChatGPTに加えてClaudeによるプロジェクト内監査と原稿差分監査の役割を開示。外部の人間による査読とは区別。
5. **PDFメタデータ：** タイトル、著者、主題、キーワードを明示。
6. **第10節の印字パスについての旧改訂記録との差異：** v0.5.2の改訂記録には「相対パスを本文で示す」と記されていたが、PDF本文に印字されたのはファイルのベース名と完全コミットSHAで、相対パスはリンク注記のみである。本版は**改訂記録側の説明を訂正**する。ZIP内 `provenance/V24/PROVENANCE.md` に完全な相対パスを可視テキストで明記した。PDF本文上での長い相対パス表示は増やしていない。

**版間の本文変更は、上記の監査表現とAI開示だけ。定理3.1、表1・表2、C1〜C6、すべての数値・球の§4.2の証明、要旨、その他の研究本文には変更を加えない。**

## 内容の不変条件

- 全族分類の定理は C1〜C6 を仮定した条件付きの主張のまま。
- 扁平側の別途検証範囲は \(\lambda\in[2/5,33/50]\) に限る。球 \(\lambda=1\) の解析証明は不変。
- 検証コード、数値結果、図、参考文献、計算補足PDFはv0.5.2とバイト単位で一致する。
- 数学的証拠等級・Judgeの裁定・Zenodo公開状況を変更しない。
- V24の原本の内容は原文どおりで、内部用語を現代化・翻訳していない。

## 引渡し

`Paper_I_v0_5_3_Integrated_EN.pdf`、`Paper_I_v0_5_3_Manuscript_and_Verification.zip`、`SOURCE_DIFF_v0_4_to_v0_5_3.patch`、`Paper_I_v0_5_3_ARTIFACT_SHA256SUMS.txt`。数学的な差分監査前の改訂候補であり、著者による公開承認やZenodo投稿を主張しない。
