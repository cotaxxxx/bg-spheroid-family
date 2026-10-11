# C 空白① FREEZE 審査書 兼 実行指示書 v1（chat、2026-10-11）

- **宛先：** ChatGPT（研究用 PC と GitHub で実行・push する）。
- **監査：** chat が GitHub の正本で行う。
- **効力：** 本書末尾の Judge 裁定で発効する。裁定前は、§2 以降のどの手順も実行しない。

## 0. 前提となる裁定と監査
- **実行順（Judge 10/11）：** C 空白① → D5。研究用 PC を同時に占有することは禁止。
- **実装 v0.3 は PASS（static）：**
  - 監査役は chat 一系統（`audits/CHAT_RECORD_AUDIT_ROLES_2026-10-11.md`）。
  - 監査記録は `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_3_2026-10-11.md`。
  - v0.3 には独立監査を別に立てない。役割裁定により、chat の監査がその役を兼ねる。
- **B7：** preflight の中で stub controls（L 3件、X 3件、端点 5件、計 11件）が実行される。本書の裁定はその実行を明示的に含む。

## 1. FREEZE 対象（この値以外では実行しない）

### 1.1 数学契約
`drafts/2026-10-11/C_GAP1_CONTRACT_DRAFT_V7.md`

SHA-256 `a49148180fdeb33272e7358028caa55ec1dc06e5d4f526cd23eca50ff65c2a37`

拘束読みは次の記録で固定する：
- `audits/CHAT_RECORD_V7_EXACT_FILE_IDENTITY_2026-10-11.md`
- D6 の B1・B2・K1・K2

### 1.2 実装
`submissions/2026-10-11/C_GAP1_IMPL_V0_3_SUBMISSION_2026-10-11.tar.gz`

SHA-256 `2ec6e70f…`（main `f0f3bcbb` の値）

### 1.3 実行ブランチ
- bg-oblate-spheroid に新しいブランチ `run/c-gap1-v0-3` を作る。
- 起点は `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`。
- 追加してよいのは次の8ファイルだけ。既存ファイルは1バイトも変えない。
  - tar の `new_files/` にある7本（byte-identical）
  - `gap1_analysis/GAP1_RESUMABLE_PINS.json`
- ブランチ先頭の commit を **RUN_COMMIT** と呼ぶ。

### 1.4 25本の git blob
`REQUIRED_C1B_BLOB_PATHS` の25本の git blob を、chat が事前に計算した。RUN_COMMIT ではすべてがこの値に一致しなければならない。

**新規7本（v0.3）**

| path | git blob |
|---|---|
| gap1_analysis/c1b_resumable_driver.py | f381ae6849670f02f2c1b4d86442e3df6c6a299d |
| gap1_producer/global_axial_c1b_gating.py | 7a96afdc42e3de4422888c2c23d47f1976c004ef |
| gap1_checker/global_axial_c1b_gating.py | 4fb03151d7a519b11f6fce2836c2c2a49024803b |
| gap1_producer/global_axial_c1b_kernel.py | bf196ba2fae4add025b17eb054a8a4627f6e6999 |
| gap1_checker/global_axial_c1b_kernel.py | 0a51fb32d8f5ec303d9ad15932fd00f3b587ec8a |
| gap1_producer/global_axial_c1b_producer.py | 34ef3758382de5993116c49d511b5b68e4e87bfa |
| gap1_checker/global_axial_c1b_checker.py | 5b526ddc4f48dc01d3f95eafb44f3d638e2e35ed |

**baseline 18本（85eca228。import 17本と read-only pin 1本）**

| path | git blob |
|---|---|
| producer/monotone_tube_refinement_producer.py | c2fee40053ab055ce352e93e1c6d1fc43e46310a |
| checker/monotone_tube_refinement_checker.py | 15d660265552fc2f2c83ffe897ed5efab8514da2 |
| checker/monotone_tube_interval_checker.py | f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77 |
| producer/global_axial_c1b_endpoint_r.py | 29d441a578f10fe7f4beb38476d3699f3648a3b1 |
| checker/global_axial_c1b_endpoint_r.py | 1a953b22c12a89afc06790b28d6b0dea9680dc43 |
| producer/endpoint_interval_producer.py | 51060fea01cb9ff661518b7c52146f71187846ff |
| producer/monotone_tube_interval_producer.py | b6d96df223c0e423e804d96f4892a8e818c05827 |
| producer/global_axial_c0_producer.py | c4c8d6b59d3829e1843d149b7857eda5800287aa |
| checker/global_axial_c0_checker.py | 85978625e029b01c8ae40fa8234566f10eea251c |
| checker/endpoint_local_controls.py | c913c47d228e51a15f56957f5df9196efa1b22c3 |
| checker/oblate_axis_prototype.py | df402583c320c459ff4f72dc5294558f14f44d31 |
| checker/endpoint_interval_checker.py | 4cb16f8a975e5a3be601a7926af695ad5be57790 |
| checker/endpoint_local_checker.py | 2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc |
| producer/global_axial_c0_producer_v2.py | cdbdf51f8656c1fcae97666cc1846461b250a591 |
| checker/global_axial_c0_checker_v2.py | fbec890588d2d390ea67bc90116b80bb37ebf9cc |
| producer/c0a_four_group_v2.py | 2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4 |
| checker/c0a_four_group_v2.py | 18e66b6450cd2a379bbb869a99e4e5ce6999f6e5 |
| analysis/c1b_cross_lineage_compare.py | 33cdd3290bfa09c88cd8936e1f4557af491f0bc2 |

### 1.5 pin ファイル `GAP1_RESUMABLE_PINS.json`（Q1 の pin manifest）
- **形式：** baseline の `analysis/GLOBAL_AXIAL_C1B_RESUMABLE_PINS.json` と同じ形にする。キーは `producer` と `checker` の2つ。
- **内容：**
  - `ref` = `run/c-gap1-v0-3`
  - `blob_paths` = 上の25本
  - `expected_blobs` = 上の表の値
  - `expected_environment`：研究用 PC で `environment_snapshot` を使って実測した値
  - `wheel_dir`、`wheel_sha256`、`requirements_sha256`：同じく実測した値
- **禁止：** 手書きの推測値、HEAD の自己参照 pin。
- **Python 環境：** baseline の C1b 本走と同じ環境（mpmath と python-flint の版）を使う。違う場合は §2 の手順 1 で止めて報告する。

## 2. 手順（すべて fail-closed。STOP 条件に当たったら、その場で止めて push・報告する）

作業ディレクトリは bg-oblate-spheroid のルートとする。run dir は repo の外に置く（`clean_status` を空に保つため）。

| # | 手順 | 合格条件 | STOP |
|---|---|---|---|
| 0 | 研究用 PC で D5 などほかの本走が動いていないことを確認する | 占有なし | 占有あり |
| 1 | ブランチを作り、8ファイルを入れて commit する（RUN_COMMIT）。25本の blob を照合する | 25/25 一致、working tree clean | 1本でも不一致 |
| 2 | **import-only test**（非数値）：`importlib.util.find_spec` で `gap1_*` 7本と import 17本の origin を出力する | すべて RUN_COMMIT の作業木内のパス | 外部パス、解決失敗 |
| 3 | **preflight**：`python3 -m gap1_producer.global_axial_c1b_producer --ledger-only` と `python3 -m gap1_checker.global_axial_c1b_checker --ledger-only` | 両系統で `GAP1_STUB_CONTROL … PASS` が11行、read-only pin PASS、`C1B_PREFLIGHT_ESTIMATES` を記録 | FAIL が1件でもある |
| 4 | **producer 本走**：`python3 -m gap1_producer.global_axial_c1b_producer --run-dir <RUN>/producer` | ledger 完走、`checker_replay_exact.jsonl` が出る | 下の判定 |
| 5 | **checker 本走**：`python3 -m gap1_checker.global_axial_c1b_checker --run-dir <RUN>/checker --replay-plan <RUN>/producer/checker_replay_exact.jsonl --producer-ledger <RUN>/producer/ledger.jsonl` | `GAP1_PLAN_ORDER_AUDIT PASS`、全 slab REPLAYED | 下の判定 |
| 6 | **保存**：bg-spheroid-family に `runs/2026-10-1x/C_GAP1_V0_3/` として ledger 2本、replay plan、stdout、手順 2〜3 の出力、SHA-256 一覧を push する。RUN_COMMIT と pin ファイルは bg-oblate-spheroid に push する | push 完了 | — |

**手順 4・5 の判定**
- 中断（停電や SIGTERM）は resume で続けてよい（A7 修正済み）。
- それ以外の停止はすべて **その時点で終了** とし、ledger をそのまま保存して報告する：ABORT、RESOURCE_CAP、`CONTRACT_MISMATCH`、`PIN_IDENTITY_FAIL`、`CHECKER_REPLAY_UNRESOLVED`。
- 再実行、パラメータの変更、コードの修正はしない。これらは数学的な判断にあたるので、Judge 裁定を必要とする。

## 3. 禁止事項
- コード、契約、パラメータを変更すること。
- 部分的な結果を証拠として扱うこと（途中経過は NOT_EVIDENCE）。
- D5 と同時に実行すること。
- STOP の後に自分の判断で再実行すること。

## 4. 結果の扱い
- chat が GitHub の正本で監査する。照合するもの：ledger の連鎖、件数、L/X/R のラベル、`negative_block_closure`、端点の U_cum<0、両系統の一致。
- 監査が PASS の後、Judge が C 空白① の CLOSED を裁定する。
- 論文で CLOSED と書く条件は、D6 の残り（補題 v1.1、Astra、人間の外部監査）と共通である。

## Judge 裁定（2026-10-11）
- 実行順：**「C空白①→D5」**。
- 本書：**「FREEZE＋実行許可」**。§1 の対象を FREEZE し、§2 の手順 0〜6 を一括で許可する。preflight の stub controls 11件の実行を含む。STOP 条件に当たった場合はその時点で終了し、再実行は別の裁定による。
