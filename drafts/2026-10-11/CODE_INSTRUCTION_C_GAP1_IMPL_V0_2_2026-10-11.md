# Code 宛 指示書 — C 空白① 実装 v0.2（2026-10-11）

発行：Judge。起草：chat。根拠は次のとおりです。
- 実装指示書 v2（`48204988`）と発出メモ（`51a167c7`）
- v0.1 の指示書（`f8f436f3`）
- `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_1_2026-10-11.md` §8 の Judge 裁定
- ChatGPT の監査（`f1ffe1f8`）の F4・F5

作業の範囲と禁止事項は v0.1 と同じです。数値の実行、commit、push、既存ファイルの変更、FREEZE はしないでください。

## 1. 基準
- **出発点：** v0.1 の提出物 `C_GAP1_IMPL_V0_1_SUBMISSION_2026-10-11.tar.gz`（`df2a6915…0077`）。
- **変えないもの：** baseline の7本（`85eca228`）、import 17本、読むだけの pin 1本、allowlist、保護対象の本体。
- **差分：** 次の3つを提出してください。
  - baseline → v0.2 の全文
  - v0.1 → v0.2
  - hunk の分類表

## 2. 直すこと
1. **F4：L の記録を、実際に使った証明の方法と一致させる。**
   - L の slab_record に、どの方法で閉じたかを機械で読める形で残します。直接の g_box で閉じた箱の数と、mono 閉包で閉じた箱の数を、段（E0/E1/E2）ごとに記録してください。
   - 元の情報は、baseline の exterior が出す guard と mono の記録から取ってください。baseline の関数は変更しないでください。
   - `root_count.rule` は、実際に mono 閉包を使ったかどうかで文言を変えます。少なくとも次の2つを区別してください。
     - direct g_box のみ
     - direct g_box と mono 閉包（G0/E1 v3 による）
   - X は v0.1 のとおり direct のみで、変えません。
2. **F5：受け入れの件数を、ABORT した slab で増やさない。**
   - producer の成功した経路では、上限の判定を**候補の値**（`accepted_count + 1`、`accepted_work + attempt_work`）で行います。
   - 最終的に ABORT になった場合は、確定した `accepted_count`、`accepted_work`、`previous_root` を**更新しないでください**。
   - 判定に使った候補の値は、別のフィールドとして記録してかまいません。例：`cap_test_accepted_count`。
   - checker も同じ方式にそろえてください。
   - resume と replay（`resume_state`、`gap1_terminal_abort`）が台帳から組み立て直す件数・work と、slab_record に保存した値が、すべての経路で一致するようにします。
   - schema には、それぞれの系統で `accepted_count` が何を数えているかを書いてください（producer と checker）。
3. **B2：** schema に、`decision` は plan の決定、`checker_decision` は checker 自身の状態を表すことを、読み方の規則として固定してください。

## 3. 静的 control の追加
- **同じ record の中の整合：**
  - `accepted` と、件数・work の関係
  - `rule` と、実際に使った guard の関係
  - `reason`、`failure_class`、`abort_cause`、`resource_cap` の組み合わせ
- **台帳と組み立て直した結果の整合：** slab_record に保存した件数・work と、`resume_state` が組み立て直す値が等しいこと。ソースを読んで分かる範囲で確かめてください。

## 4. 提出
- 形式は v0.1 と同じです。tar.gz を1つにまとめ、中に `MANIFEST.sha256` を入れ、**ファイル本体を添付**で渡してください。
- 最後の1行は `IMPLEMENTATION_READY_FOR_CHAT_DIFF_AUDIT` または `BLOCKED:<reason>` にしてください。
