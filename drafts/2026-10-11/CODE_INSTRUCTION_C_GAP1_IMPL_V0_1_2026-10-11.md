# Code 宛 指示書 — C 空白① 実装 v0.1（2026-10-11）

発行：Judge。起草：chat。根拠は次の3つです。
- 実装指示書 v2（`48204988`）
- 発出メモ（`51a167c7`）
- chat 差分監査 §7 の Judge 裁定（`audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_2026-10-11.md`）

作業の範囲は v2 と同じです。数値の実行、commit、push、既存ファイルの変更、FREEZE はしないでください。

## 1. 基準
- **出発点：** v0 提出物 `C_GAP1_IMPL_V0_SUBMISSION_2026-10-11.tar.gz`（`d4ddd33d…56d6e8`）の新しい7本。
- **変えないもの：** baseline の7本（`85eca228`）と import 17本。
- **守る規則：** DIFF-A/B/C/D/E/K の allowlist と、保護対象の本体。
- **差分の取り方：** v0.1 の diff は、baseline → v0.1 の全文で作ってください。v0 → v0.1 の差分も、別に添えてください。

## 2. 直すこと（Judge 裁定）
1. **F1（DIFF-B）：X の負値ブロックは直接の g_box だけで閉じる。**
   - 対象は [5/8, 31/32]。各箱で、直接の `g_box` の上界が < 0 であることを示します。
   - 初期分割は E0 の 24 × 8、パネルは 1024→2048→4096 で、E_BOX_CAP を守ります。
   - X では **mono 閉包を呼ばない**でください。閉じられなかった箱は `CERTIFICATE_INCONCLUSIVE` になります。
   - L の mono 閉包はそのまま残します（数値契約 v1 §4 が MONO_WORK_CAP を挙げているため）。
   - 「X から mono 閉包に到達できない」ことを確かめる静的 control を追加してください。
   - baseline の `exterior_cover` と `eval_exterior` は変更しないでください。X 専用の経路は、新しい関数として DIFF-B に置きます。
2. **F2：X の根の数を正しく記録する。**
   - `ROOT_FREE_REGION` は **L だけ**に使います。
   - X には、「根がない」という意味にならないラベルを付けます。例：`ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR`。
   - X の根の数は、g(1/2,λ) の符号で決まります。その符号は C1a の receipt と gate D で与えられます。このことを ledger schema に書いてください。
   - λ_x の近似値で分岐する処理は追加しないでください。
   - checker の ACCEPT 判定とスキーマの文書も、このラベルに合わせて直してください。
3. **F3：上限で止まったことを機械で読める形で残す。**
   - 上限（global work、accepted work、MAX_ACCEPTED、MAX_ATTEMPTED）に達して ABORT した場合は、`failure_class=RESOURCE_CAP` と、どの上限に達したかを記録します。
   - 試行の reason が `PASS` のまま ABORT と並ぶ矛盾をなくしてください。
   - producer、checker、resume、replay のどれでも、同じ分類が再現されるようにします。
   - checker が上限で止まる場合も、同じ形で記録してください。
4. **Q10・Q11：** `analysis/c1b_cross_lineage_compare.py`（`85eca228` での blob は `33cdd3290bfa09c88cd8936e1f4557af491f0bc2`）を、driver の照合対象の一覧に加えてください。読むだけのファイルとして pin します。
5. **Q15（DIFF-K）：** L、X、端点のそれぞれについて、`g_box`／`gt_box` を合成スタブに差し替える preflight control を追加してください。
   - 端点では少なくとも次の2つを入れます。
     - seed=−1、U_j=+1 で PASS になる場合
     - seed=−1/64、U_j=+1 で FAIL になる場合
   - 書くだけで、**実行はしないでください**。
6. **そのまま受理：** Q2、Q4、Q5、Q6 は v0 の実装のままです。Q1（pin manifest）は、実行準備の段階で扱います。

## 3. 提出
- 提出の形式は v0 と同じです。tar.gz を1つにまとめ、中に `MANIFEST.sha256` を入れ、**ファイル本体を添付**で渡してください。tar.gz と MANIFEST の SHA-256 も報告してください。
- 次のものを入れてください。
  - v0.1 の新しい7本
  - baseline → v0.1 の全文の diff と hunk の分類表
  - v0 → v0.1 の diff
  - 静的 control（追加分を含む）のスクリプト、実行前に記録した SHA、出力
  - 更新した `LEDGER_AND_REPLAY_SCHEMA` と `OPEN_QUESTIONS`
- 最後の1行は `IMPLEMENTATION_READY_FOR_CHAT_DIFF_AUDIT` または `BLOCKED:<reason>` にしてください。
