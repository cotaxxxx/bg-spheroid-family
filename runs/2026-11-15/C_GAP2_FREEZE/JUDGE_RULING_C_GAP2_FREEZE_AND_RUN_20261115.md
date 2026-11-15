# Judge 裁定：C 空白② の FREEZE と実行許可

2026-11-15 / Judge（ユーザー）／ 記録: chat

## 裁定

**「FREEZE＋実行許可」**（ボタンによる選択。chat の推奨どおり）。

C 空白②（C1b の上側の帯）を事前宣言 v4-r2 と実装 `0d32ac2` で FREEZE し、研究用PCでの本走（L0(c)(d) の封印台帳の読み込みを含む）を許可する。

## 1. 凍結するもの

| 項目 | 値 |
|---|---|
| 事前宣言 | `C_GAP2_PREDECLARE_DRAFT_V4_R2_20261115.md`、SHA-256 `c9b82f2c9aadc722b3f3cdabe06aadb42c96c69a7065660e67d14e8e01ecaccc` |
| 実装 | `cotaxxxx/bg-oblate-spheroid`、branch `implement/c-gap2-v4-r2-20261115`、HEAD `0d32ac2a0325f41998adebf922a57ed50cf3ba59`（run4 の凍結 commit `26d81e1049340d44ef7f08ae8e17d0692983395b` が祖先。変更ファイル17） |
| 数値の引数 | producer 160 bit／checker 192 bit、次数 50、seed と Gt の panel 8192、λ の二分は深さ ≤3（親ごとに 0 から数える、右の子が先）、t の箱は N ＝ ⌈512(1 − t_e)⌉ 個の等幅、t の追加の細分なし、成功条件は seed の上界 < 0 かつ累積の上界 < 0 |
| t_e | 封印台帳の unclamped の親ごとに t_e ＝ max(31/32, t₊)。子は親の t_e を受け継ぐ |
| 封印入力（L0(a)(b) PASS） | `phase1_v212s_seal_20260918T222551Z/ledger.jsonl` `1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f`、`phase2_v212s_seal_20260920T140743Z/ledger.jsonl` `09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38`、phase1 `checker_replay_exact.jsonl` `c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69`、`c1b_receipt_extract.json` `8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b` |
| preflight の証拠 | `bg-spheroid-family` branch `evidence/c-gap2-preflight-0d32ac2-20261115` commit `e20ade6`、zip SHA-256 `9653bdde540ea3db3d10941fa1be95c1a878a7002df9a210c513271be945b637`（13/13 PASS、NOT_EVIDENCE。chat が検収し、run4 回帰を chat の環境で両系統とも分数まで同一に再現） |
| 解析の前提 | G0/E1 v3、C1 補題 `5afa815f`、C2 補題 `7cb9b809`・`f66ffe5a`（V19 で chat 監査 PASS） |

## 2. 実行の手順

1. 研究用PC の bg-oblate-spheroid を HEAD `0d32ac2…` に合わせ、作業木を clean にする。D5 などほかの重い計算と同時に動かさない。
2. 環境変数 `C_GAP2_JUDGE_FREEZE_APPROVED=YES` を設定する。この裁定書のファイルと SHA-256 を `--judge-ruling` と `--judge-ruling-sha256` に渡す。
3. producer：`python -m gap2_producer.driver --execute --sealed-parent /home/daybreak/basepoint-geometry-artifacts/C1b --run-dir <新しいフォルダ> --judge-ruling <この裁定書> --judge-ruling-sha256 <SHA>`
4. checker：同じ形で `gap2_checker.driver` を流す。出力先は別の新しいフォルダにする。producer と checker を並行して2つのプロセスで流してよい。それぞれの上限は CPU 48 core-hours、RAM 32 GiB、出力 10 GiB である。
5. 両方が完了したら比較する：`python -m gap2_analysis.lineage_compare --producer-run … --checker-run … --judge-ruling-sha256 <SHA> --output <新しいJSON>`
6. 各手順の前に HEAD と `git status --porcelain` をログに残す。stdout と stderr は手順ごとのファイルに残す。
7. 次の一式を zip にまとめ、SHA256SUMS を付けて、証拠ブランチに登録する。
   - 両系統の run フォルダ（`ledger.jsonl`、`manifest.json`）
   - 比較の JSON
   - ログ
   - 所要時間
   - 版の情報

## 3. 止まったときの扱い

- 自動の再開はしない。どの停止（L0(c) の不一致、`RIGHT_EXTERIOR_*`、門の失敗による ABORT、資源の上限、同一性の不一致）でも、そこで終了し、台帳と manifest を残して報告する。
- 門の失敗（深さ3でも累積の上界が負にならない親）は反例ではない。方式を変えるには新しい版（v5）と再 FREEZE が要る。
- 止まった原因が起動の段階の誤り（コマンドの打ち間違い、パスの指定違いなど）で、何も計算していないことがログで確かめられる場合に限り、直して最初から流し直してよい。
- 封印フォルダと USB には書き込まない。

## 4. 採否

本走の結果は CANDIDATE であり、証拠ではない。比較が `COMPARE_PASS_NOT_JUDGE_CLOSED` になったら、chat が次を検収する。

- 封印入力との照合
- 右の外側の取り込み
- 両系統の木と葉の被覆
- 門の算術

検収のあと、Judge が C 空白② の採否を裁定する。C 系列の大域の被覆の組み立ては、その後に行う。
