# Code 宛 指示書 — C 空白① 実装 v0.3（2026-10-11）

発行：Judge。起草と監査：chat（体制の記録 `audits/CHAT_RECORD_AUDIT_ROLES_2026-10-11.md` による）。
根拠：`audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_2_2026-10-11.md` の Judge 裁定。

作業の範囲と禁止事項は v0.2 と同じです。数値の実行、commit、push、既存ファイルの変更、FREEZE はしないでください。

## 1. 基準
- **出発点：** v0.2 の提出物 `C_GAP1_IMPL_V0_2_SUBMISSION_2026-10-11.tar.gz`（`eb5f6e86…ed2b`）。
- **変えないもの：** baseline の7本、import 17本、読むだけの pin 1本、allowlist、保護対象の本体。
- **差分：** v0.2 → v0.3 の全文と、baseline → v0.3 の全文の両方を提出してください。

## 2. 直すこと
1. **A1（DIFF-K）：根拠文書の pin を追加する。**
   - 両 kernel の `GAP1_AUTHORITY_SHA256` に、次の6件を加えてください。
     - `CODE_INSTRUCTION_C_GAP1_IMPL_V0_2_2026-10-11.md`
     - `CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_1_2026-10-11.md`
     - `CHAT_RECORD_AUDIT_ROLES_2026-10-11.md`
     - `CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_2_2026-10-11.md`
     - `CODE_INSTRUCTION_C_GAP1_IMPL_V0_3_2026-10-11.md`
     - `C_GAP1_IMPL_V0_2_SUBMISSION_2026-10-11.tar.gz`（提出物そのもの）
   - SHA-256 は、bg-spheroid-family main の実ファイルから**実測**してください。記憶や報告からの転記は禁止です。
   - 新しい main は、この指示書が保存されたコミットです。
2. **A7（DIFF-E）：checker の通し番号を plan の番号と分ける。**
   - checker の slab_record に `plan_attempt_sequence = item["attempt_sequence"]` を加えてください。
   - checker の `replay_state` と resume が plan と照合するときは、この項目を使ってください。
   - checker 自身の `attempt_sequence` は、checker の試行の通し番号という意味のまま残します。
   - 次の2つの場合に、照合がずれないことをソースから示してください。
     - producer が中断していた場合
     - checker 自身が中断した場合

## 3. 静的 control の追加
- 新しい pin（6件）が、実測した値と一致すること。
- `plan_attempt_sequence` と plan の item が一対一に対応すること。ソースを読んで確かめてください。
- 既存の C0〜C17 が引き続き PASS すること。

## 4. 提出
- 形式は v0.2 と同じです。tar.gz を1つにまとめ、中に `MANIFEST.sha256` を入れ、**ファイル本体を添付**で渡してください。
- 最後の1行は `IMPLEMENTATION_READY_FOR_CHAT_DIFF_AUDIT` または `BLOCKED:<reason>` にしてください。
