# ChatGPT 独立差分監査 — C 空白① 実装 v0.1（2026-10-11）

監査者：ChatGPT  
作業区分：READ-ONLY / STATIC DIFF AUDIT  
対象：`C_GAP1_IMPL_V0_1_SUBMISSION_2026-10-11.tar.gz`  
対象 SHA-256：`df2a691585e0aebf7558f0e9cf0de1dfd2b55949fcff41c586173e172fb70077`

**全体判定：`DIFF_AUDIT_FAIL`**

理由は、数値本体や F1–F3 の主要修正ではなく、machine-readable ledger の意味に2件の不整合が残るためである（F4, F5）。数値実行・import・証明書生成は行っていない。

## 0. 独立性と方法

chat の v0.1 差分監査本文ファイルは参照していない。Code 同梱の diff / static-control 出力は結論の根拠にせず、次を独立に行った。

1. tar.gz と `MANIFEST.sha256` を照合。
2. 新7本に Code 同梱の baseline→v0.1 patch を逆適用し、復元された7本の Git blob が baseline `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b` の指定 blob と一致することを確認。
3. 復元 baseline と新7本から自前の unified diff を再生成（62 hunks）。
4. 研究用PCの baseline commit に対して import 17本と `analysis/c1b_cross_lineage_compare.py` の Git blob を実測。
5. `GAP1_AUTHORITY_SHA256` の11件を `bg-spheroid-family` main 上の実ファイル SHA-256 と照合。
6. 提出コードは import / execute せず、テキスト・AST・diff の静的読解だけを行った。

## 1. SHA / pin — PASS

- tar.gz：`df2a691585e0aebf7558f0e9cf0de1dfd2b55949fcff41c586173e172fb70077` — 一致。
- `MANIFEST.sha256`：`acdf7cfd037044b0affa1a0015177324cef12ba8971df25a3f1b0b4cc152a691` — 一致。40 entries すべて一致。
- baseline 7本：逆適用後の Git blob は7/7一致。
- import closure 17本：17/17一致。
- read-only pin `analysis/c1b_cross_lineage_compare.py`：`33cdd3290bfa09c88cd8936e1f4557af491f0bc2` — 一致。
- `GAP1_AUTHORITY_SHA256`：v0.1で追加された2件を含む11/11一致。監査指示書の「9件」は v0 時点の記述であり、v0.1 指示で追加された `CODE_INSTRUCTION...` と `CHAT_DIFF_AUDIT...V0` の2件を含む現在実装を正と解した。

## 2. hunk 分類 / 保護対象 — PASS（静的）

自前 diff は62 hunks。変更箇所を関数・定数・制御フロー単位で分類すると、DIFF-A/B/C/D/E/K の範囲外に出る変更は認めなかった。

特に、baseline の次の数値本体は本文一致を確認した。

- `g_box`, `gt_box`
- `root_localize`
- `predictor_accept`
- `mono_closure_box`, `eval_exterior`, `exterior_cover`
- baseline の tube / root interval arithmetic 本体
- P1/P2 の既存本体

既存共通関数のうち実質変更されたものは、U1 queue / preflight / header / run-loop / replay 配線など、許可された領域に限られる。

## 3. L / X — PASS（計算経路）

### L

- predictor / root localization を呼ばない。
- `[1/2,31/32]` は `attempt_l -> exterior_cover`。
- Judge の v0.1 裁定どおり、L では baseline の mono closure を残している。
- endpoint は共通 endpoint gate へ進む。
- L 失敗時に root search へ逃げる経路はない。

### X

- `[1/2,5/8]` は固定 Gt<0 path。
- `[5/8,31/32]` は新設 `x_negative_cover` で direct `g_box` のみ。
- `x_negative_eval` は `g_box` 以外で負値を閉じない。
- X から `mono_closure_box` / `eval_exterior` / `exterior_cover` を成功経路として呼ぶ配線はない。
- predictor / root localization へ fallback しない。

したがって旧 F1 の主要修正は静的に成立している。

## 4. R — PASS（静的）

- coarse queue は high-λ → low-λ。
- REFINE は `right child` を先に queue へ戻す。
- continuation は `previous_root` の midpoint、初回は `9/16`。
- `previous_root` 更新は ACCEPT 時だけ。
- P2 選択は `abs(continuation-scan_mid) <= ROOT_TARGET` で、等号を continuation 側に含む。
- R の right-clamp 成功は `R_RIGHT_CLAMP_FORBIDDEN` として拒否される。

P1/P2・root-localize の protected body 自体には変更を認めなかった。

## 5. endpoint gate — PASS（静的）

- seed は `t=31/32` の direct `g_box` 1回。
- 16個の幅 `1/512` の t-box で `gt_box` を評価。
- 各寄与は `max(0,U_j)`。
- 成功条件は cumulative upper `<0`。
- `(31/32,1)` 内部で direct `g_box` を呼ばない。
- endpoint gate 内で runtime `C_Lambda(1-t)`、B_ob rescue、t 再分割を使用しない。

arb upper と正寄与を用いる形で outward upper-bound の構造も維持されている。

## 6. checker independence — PASS（静的）

- checker は `gap1_producer.*` を import しない。
- checker kernel は `checker.*` baseline 数値 lineage を使用。
- producer から渡される replay は exact rational labels / decisions / R の `t_c` 等に制限され、producer の interval enclosure を直接信用する配線はない。
- 共有 `gap1_analysis/c1b_resumable_driver.py` は schema / persistence / replay bookkeeping 側で、数値 enclosure の共有には使われない。

## 7. 共有辺 / exact union — PASS（静的）

- `699/1600`：X owner / L overlap。
- `281/640`：R owner / X overlap。R `T_star` と `(1/2,5/8)` の交差を要求。
- `9/20`：boundary consistency only。
- accepted slabs の exact union は rational endpoint の完全連結と `[2/5,9/20]` の両端を照合する。

## 8. v0 Q1–Q6 への意見

- **Q1（pin manifest 未作成）**：差分監査段階では延期を受理。実行許可前には実物 pin manifest の生成・照合が必要。
- **Q2（`__init__.py` なし）**：静的設計として受理。ただし namespace/import 解決は実行前 preflight で別途確認が必要。
- **Q3（X mono closure）**：旧案は不採用で正しい。v0.1 の direct `g_box` only を受理。
- **Q4（R right clamp 拒否）**：受理。
- **Q5（160 slabs 全体を降順 / right-child-first）**：受理。
- **Q6（baseline 定数を残し GAP1_* を追加）**：受理。

## 9. F1–F3 の再監査

- **F1：PASS。** X negative block は direct `g_box` only。
- **F2：PASS（主要修正）。** X label は `ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR`。`root_count` は null で、C1a sign + gate D による規則を明記。λ_x 近似分岐なし。
- **F3：PARTIAL PASS。** `reason` / `failure_class` / `abort_cause` / `resource_cap` の resource-cap 分類は修正されている。ただし accepted counters と machine-readable semantics に F5 が残るため、F3 全体を最終 PASS にはできない。

## 10. 新規 FAIL finding

### F4 — L の `root_count.rule` が実際の証明経路を偽っている

**判定：FAIL / machine-readable ledger semantics**

`gap1_* / global_axial_c1b_gating.py` の `gap1_root_count_record()` は L について常に

`g<0 on [1/2,31/32] by direct certificate; endpoint gate on [31/32,1]`

と記録する。

しかし L の実装は `attempt_l -> exterior_cover -> eval_exterior` を通り、direct `g_box` で閉じなかった box を `mono_closure_box` で閉じることが Judge 裁定により許可されている。したがって mono closure が実際に使われた ACCEPT でも `rule` は「direct certificate」と記録し、台帳の machine-readable 説明が事実と一致しない。

該当箇所（producer；checker も同型）：

- gating `gap1_root_count_record`：L rule の固定文字列。
- kernel `attempt_l`：`exterior_cover(slab,T_LO,T_LO)`。
- kernel `eval_exterior`：未解決 box に対して `mono_closure_box` を使用。

**修正案：** L rule を、例えば `g<0 on [1/2,31/32] by direct g_box and permitted mono closure; endpoint gate ...` のように実装と一致させる。より厳密には `direct_boxes` / `mono_closed_boxes` 等の既存 guard 情報から、実際に使用した方法を machine-readable field で記録する。

### F5 — producer の cap-ABORT で `accepted=false` と `accepted_count/accepted_work` が矛盾する

**判定：FAIL / ledger-resume semantic consistency**

producer の success path は、まず

- `accepted_count += 1`
- `accepted_work += attempt_work`
- `previous_root = root`

を行い、その後 `MAX_ACCEPTED` / `ACCEPTED_WORK_CEILING` を検査する。超過時は最終 `decision` を `ABORT` に変更する。

その後 `gap1_mark_decision()` は `root_count.accepted = (decision == "ACCEPT")` とするため、この slab は `accepted=false` になる。一方、同じ slab_record の `accepted_count` / `accepted_work` にはその slab を加えた値が保存される。

さらに shared driver の `resume_state()` は `decision == "ACCEPT"` の slab だけを accepted / accepted_work に加えるため、同じ terminal ABORT record を ledger から再構成した accepted counters と、slab_record に保存された accepted counters が一致しない。

現在は `gap1_terminal_abort()` が terminal ABORT を見つけると再開前に停止するため、その不一致が次の数値 slab を誤って実行させる経路は確認していない。しかし、v0.1 監査指示で要求された「machine-readable field の意味」と「producer / checker / resume / replay で同じ分類」の観点では不整合である。

**修正案：** cap 判定用に `candidate_accepted_count` / `candidate_accepted_work` を別変数で計算し、cap を検出する。最終 decision が ABORT なら committed `accepted_count` / `accepted_work` / `previous_root` は更新しない。必要なら cap 判定に使った candidate 値を別 field として記録する。こうすれば `root_count.accepted=false`、`decision=ABORT`、resume_state の accepted counters が一致する。

checker の B2 方針（plan の `decision` と checker 自身の `checker_decision` を分離）は、それ自体は受理可能だが、`accepted_count` が plan acceptance を数えるのか checker acceptance を数えるのかを schema 上で明示する必要がある。

## 11. B1–B7 への意見

- **B1：受理。** `MAX_DEPTH_EXHAUSTED` は certificate closure failure / traversal ceiling であり、v0.1 指示で列挙した4 resource caps と同一視しない方が意味が明確。
- **B2：受理（schema 明記を条件）。** `decision`=producer plan、`checker_decision`=checker status の分離は合理的。両者を読む必要を schema で固定する。
- **B3：受理。** resume 開始時に4 cap を先に検査するのは fail-closed 側。
- **B4：考え方は受理、現実装は F5 のため未受理。** `certified` と `accepted` の分離は正しいが、accepted=false の slab を producer の `accepted_count/accepted_work` に含めるのは整合しない。
- **B5：受理。** process exit string より ledger の `abort_cause` を machine authority とするなら静的には問題なし。
- **B6：受理。** `append_segment_end` が RESOURCE_CAP 時に `SystemExit` する副作用はコメントで明示されており、fail-closed。
- **B7：受理（実行前条件）。** 11 stub controls を preflight 毎に実行する設計は妥当。今回の監査では提出コードを実行していないため、実際の PASS は NOT_VERIFIED。将来の実行許可では preflight 実行を必須条件として明記すべき。

## 12. NOT_VERIFIED

静的監査のため次は未検証。

- namespace package / dynamic import の実行時解決。
- preflight 11 stub controls の実行結果。
- L/X/R の数値証明書が実際に閉じること。
- producer / checker が本走で同じ tree を再現すること。
- interval arithmetic の実行時 rounding behaviour（protected body の不変性は確認済み）。

## 13. 結論

主要な数値経路については v0.1 で F1・F2・F3 の大部分が修正されており、protected numerical body と diff allowlist に重大な逸脱は見つからなかった。

しかし、v0.1 監査指示が特に要求した machine-readable ledger の意味に F4 と F5 が残る。したがって現版は

`DIFF_AUDIT_FAIL`

とする。

FREEZE 審査へ進む前に、F4 と F5 を修正した次版を作り、ChatGPT / chat の独立差分監査を再実施することを推奨する。
