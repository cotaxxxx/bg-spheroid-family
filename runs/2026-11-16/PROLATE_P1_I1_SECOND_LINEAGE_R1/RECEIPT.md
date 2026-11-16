# 第二系統 I1 独立導出原本の受領・保全

- 日付：2026-11-16
- 状態：**EVIDENCE ARCHIVE / FORMULA I2 AUDIT PENDING / NOT_CERTIFIED / NOT_FROZEN**
- 元版：`SECOND_LINEAGE_INDEPENDENT_DERIVATION_20261116.md`（6,113 bytes、SHA-256 `4f954c68bc0521eaa250b5ed2961b369bec0151f4396fbebf4f692fa691d3ea4`）。第1節の面積要素と外向き法線の正規化に不一致があり、元版のI2記号照合はFAIL。
- 差戻し対応版：`SECOND_LINEAGE_INDEPENDENT_DERIVATION_20261116_R1.md`（8,151 bytes、SHA-256 `1e53f74e2ba09bd9cf7207ed0ef153dd9e3a63b252185191153be75cea212241`）。第1節の余分な `n` を削除した版。
- **元版・R1とも原本バイト列を変更しない。** GitHubへ保全する目的は、監査者が両版の実体と差分を追えるようにすること。
- R1 §1 の法線・面積要素・体積による正規化はchat確認済みとのJudge報告。**R1 §2以降のQ、Q′、H₄、Q_z積分核は正式I2記号照合待ち**であり、本レシートは採用判定を意味しない。
- J2正式clean-room隔離の認証、Julia実装、数値検算、Judge FREEZEはいずれも本登録の対象外。
- 原本の出所：ユーザーのファイルライブラリに保存された同名Markdownファイル。登録時に各ファイルのバイト数とSHA-256を確認した。
- 正本の `STATE.md` と第一系統は変更しない。

## 検収

`sha256sum -c SHA256SUMS.txt` で両版のSHA-256照合を実施する。コード実行と数学的正しさの検査は別工程。
