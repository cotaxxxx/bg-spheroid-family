# ChatGPT 宛 指示書 — C 空白① 実装提出 v0.1 の独立差分監査（2026-10-11）

発行：Judge。起草：chat。作業区分：**READ-ONLY・静的監査**。提出されたコードの import・実行、数値計算、commit、push、既存ファイルの変更はしないでください。

## 1. 対象と根拠
- **対象：** Code の提出物 `C_GAP1_IMPL_V0_1_SUBMISSION_2026-10-11.tar.gz`
  - SHA-256 `df2a691585e0aebf7558f0e9cf0de1dfd2b55949fcff41c586173e172fb70077`、271,429 バイト
  - 中の `MANIFEST.sha256` は `acdf7cfd037044b0affa1a0015177324cef12ba8971df25a3f1b0b4cc152a691`（40 項目）
  - 研究用 PC の `~/ダウンロード` にあります。保存後は bg-spheroid-family main の `submissions/2026-10-11/` にも入ります。
- **baseline：** bg-oblate-spheroid `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b` の7本と、import 17本。
- **根拠文書**（bg-spheroid-family main `e34f6a09` 以降）：
  - 実装指示書 v2（`48204988`）と発出メモ（`51a167c7`）
  - 契約 v7（`a4914818`）
  - 数値契約 v1（`be67046f`）
  - 端点追補 v2（`7471800d`）
  - G0/E1 v3（`8bf8f5d8`）
  - import 閉包17本の記録（`b48887c1`）
  - v7 の拘束補足（`541f3025`）

## 2. 独立性
- chat の差分監査はすでに書き終えていますが、まだ保存していません。今の時点で公開しているのは SHA-256 だけです。
- **ChatGPT は、自分の結論を確定させるまで chat の監査を見ないでください。**
- Code が tar.gz に入れた diff や静的検査の結果は、参考資料として扱ってください。差分は、baseline と新しい7本から**自分で作り直して**ください。

## 3. 確認してほしい点（発出メモ N3 で求めた監査）
1. **SHA の照合：** tar・MANIFEST・baseline の7本・import 17本の SHA。加えて、新しい kernel に書き込まれている `GAP1_AUTHORITY_SHA256`（9件）を、main 上のファイルから実測した値と照らしてください。
2. **hunk の分類：** すべての hunk が DIFF-A/B/C/D/E/K のどれか1つに入るか。保護対象の本体（`g_box`/`gt_box`、T1–T3、P1/P2、`root_localize`、`predictor_accept`、exterior の機構、区間演算）が変わっていないか。
3. **L と X：** predictor と root の機構に到達できず、失敗時に別の経路へ逃げる仕組みもないこと。X の下側 Gₜ ブロックと負値ブロック、L の負値ブロックの範囲と符号条件が、v7・数値契約と一致すること。
4. **R：** λ の降順で処理すること、REFINE では右の子を先に処理すること、continuation の中心は右隣の受理済み slab の T_* の中点で、REFINE では更新しないこと、P2 の比較が `<=ROOT_TARGET` で等号のとき continuation になること。右端が t=1 に張り付いた tube が ACCEPT にならないこと。
5. **端点ゲート：** seed は 31/32 での g を1回だけ、Gₜ 箱は 16 個、累積上界 `U_cum<0` だけが成功条件であること。外向きの丸めになっていること。区間の内部での直接の g 評価、C_Λ、B_ob、t の細分化が、どれも使われていないこと。
6. **checker の独立性：** checker が数値を自分で計算し直していること。producer から受け取るのは、許可された replay の label と t_c だけであること。
7. **共有辺：** 699/1600、281/640、9/20 の所有者と overlap の検査、exact union の検査。
8. **Code の Q1〜Q6 への意見**（OPEN_QUESTIONS.md）。とくに Q3（X の負値ブロックで baseline の mono 閉包を使うこと）が健全かどうか。

## 4. 提出物
`CHATGPT_DIFF_AUDIT_C_GAP1_IMPL_V0_1.md` を1本提出してください。SHA-256 と行数も報告し、ファイル本体を研究用 PC の `~/ダウンロード` に置いてください。中身は次の4つです。
- 上の 1〜8 について、PASS / FAIL / NOT_VERIFIED と根拠
- FAIL の箇所と修正案
- Q1〜Q6 への意見
- 全体判定：`DIFF_AUDIT_PASS` / `DIFF_AUDIT_CONDITIONAL` / `DIFF_AUDIT_FAIL`

## 5. v0.1 で追加して確認してほしいこと
- **F1〜F3 の修正：** 指示書 v0.1（`f8f436f3`）と、裁定の記録（`audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_2026-10-11.md` §7）のとおりに直っているか。
  - X の負値ブロックが、直接の g_box だけで閉じること。
  - X に付けるラベルが「根なし」を意味しないこと。
  - 上限による停止が、`RESOURCE_CAP` と上限の名前で記録されること。
- **台帳のフィールド：** 機械で読むフィールドの一つ一つが、契約上の意味と食い違っていないか。とくに `reason`、`failure_class`、`abort_cause`、`resource_cap`、`root_count`、`checker_decision`。
- **v0 → v0.1 の差分：** 指示書 v0.1 の範囲を出ていないか。
- **Code の B1〜B7 への意見**（`OPEN_QUESTIONS_V0_1.md` §B）。
