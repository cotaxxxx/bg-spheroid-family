# chat 監査記録：C 空白② v4-r2 の実装 `45617d0`（直親 `26d81e1`）

2026-11-15 / chat / 差分と静的な監査（実行なし、封印入力は読んでいない）

## 対象

`cotaxxxx/bg-oblate-spheroid`、branch `implement/c-gap2-v4-r2-20261115`、commit `45617d0`。直親は `26d81e1049340d44ef7f08ae8e17d0692983395b`（空白① run4）の単一 commit であることを確かめた。変更は13ファイル（既存4、新規9、+638/−16 行）。

## 判定

**kernel と gating の差分、封印入力の読み込みは PASS。駆動部と回帰の対照は、FREEZE の前に直しが要る（必須3点）。**

## 1. kernel（両系統）の差分：PASS

- `endpoint_partition(t_e)`：t_e ＝ 31/32 なら run4 と同じ行をそのまま通る（16 箱、幅 1/512、同じ partition ID）。それ以外は N ＝ ⌈512(1 − t_e)⌉、Δt ＝ (1 − t_e)/N を厳密な分数で作り、終点 ＝ 1、等幅、1 ≤ N ≤ 16 を検査する。範囲外は `ENDPOINT_PARTITION_MISMATCH`。
- `endpoint_gate(slab, t_e)`：変わったのは seed の位置（`g_box(t_e, t_e, …)`）と、累積の重み `dt ＝ base._point(Δt)` だけ。`g_box`、`gt_box`、panel、精度、chart の判定、成功条件（seed_upper < 0 かつ cumulative < 0）は変わっていない。
- **2進で表せない t_e と Δt の扱いも正しい。** `_point(Fraction)` は `arb(分子)/分母` で、有理数を含む球を返す。`_box(左, 右)` の `arb(中点, 半径)` は中点の球の半径を保つ（python-flint で確かめた）。累積は球の和の上端で判定するので、丸めで上界が小さくなることはない。
- λ の範囲の制限はない（`L_LO, L_HI ＝ 9/20, 5/8` は C1b の範囲）。G0/E1 v3 の範囲 [2/5, 5/8] の内側である。
- t_e ＝ 31/32 の記録は run4 と同じキーだけを持つ。新しいキー（`endpoint_n_boxes`、`endpoint_delta_t`）は t_e ≠ 31/32 のときだけ付く。

## 2. gating（両系統）の追加：PASS

`gap2_endpoint_record` は門を1回呼ぶだけの入口である。t_e の範囲、親の ID、記録の t_e と作業量の一致を検査している。

## 3. 封印入力の読み込み `sealed_contract.py`：PASS（スキーマは chat が原本のコードと照合した）

封印台帳を書いた C1b のコード（receipt §1.2 の blob）と静的に照合した。

| 読み方 | 照合先 | 結果 |
|---|---|---|
| ハッシュの連鎖（`Ledger`） | 封印を書いた `analysis/c1b_resumable_driver.py` `5fd308bb` と、gap1 の写し `f381ae68` の差分 | 連鎖の検査の計算は同じ。違いは pin の一覧と `checker_decision` が ABORT の記録を受理しない点だけで、厳しくなる方向である |
| 区画の鍵（`coarse_index`、`refinement_depth`、`lambda_lo/hi`）、`result.t_plus`、`result.right_clamp` | producer の gating `a93ca173` と checker の gating `03df2620` の `slab_payload` と記録関数 | 一致 |
| 右の外側の箱（`exterior_guards` の `kind` が "R" か "R_MONO"、`truth`、`t_lo/t_hi`、`lambda_lo/hi`） | `_serialize_guard`、C1b kernel `67dda838` の `exterior_seed`（R は [t₊, 31/32]）と `eval_exterior`（R と R_MONO。R_MONO は Gt < 0 かつ左端の g < 0 のときだけ真） | 一致 |
| replay の行（`decision`、`t_plus`） | `REPLAY_KEYS`（`a93ca173`） | 一致 |
| phase1 ＝ producer、phase2 ＝ checker | C1b receipt §1.1 | 一致 |

被覆の検査（`_verify_right_cover`）は、真の閉じた箱の端点で格子を作り、すべての格子の小区画がどれかの箱に入ることを確かめる。箱の辺はすべて格子線の上にあるので、これで閉じた長方形 [t₊, 31/32] × Λ の被覆として正しい。真でない箱（後で細分された親など）は数えない。

## 4. 要修正（FREEZE の前に必須）

**F1. 系統間の比較と最終判定の道具がない。** 駆動部は producer と checker がそれぞれ自分の木を作って書き出すだけで、両者を突き合わせる段がない。v4-r2 §6 の 4・5（全区画の合否表、両系統の一致）を満たすために、比較の道具を加えること。中身は次のとおり。

- 両方の manifest と ledger の SHA を照合する。
- 124 の親ごとに、両系統で t_e が一致し、ACCEPT の葉の λ 区間の和が親の区間にちょうど一致し、ABORT がない。
- 最悪の seed 上界と累積上界の表を出す。
- 片側だけの PASS は FAIL とする。

**F2. 実行時の同一性の記録がない。** run4 と C1d の契約 §10 と同じく、実行の前と後に次を manifest に記録し、食い違えば NOT_EVIDENCE とすること。

- commit、作業木が clean であること。
- 変更・新規の13ファイルと、run4 の閉包の blob。
- import の閉包（`sys.modules` の中の repo 内のファイル）。
- Python と python-flint の版。

**F3. 回帰の対照が、変えていない行しか通らない。** `run4_regression.py` は t_e ＝ 31/32 で呼ぶので、kernel の「RUN4-IDENTICAL」の分岐（元のコードそのまま）だけを通る。新しい分岐（t_e ≠ 31/32）は一度も実行されない。次の2つを加えること。

- (a) 静的な対照：一般の式（N ＝ ⌈512(1 − t_e)⌉、Δt ＝ (1 − t_e)/N）を t_e ＝ 31/32 に当てはめると run4 の16箱と一致することを assert する。分岐の書き方を「一般の式で作り、31/32 のときは run4 の行と等しいことを確かめる」形に変えれば一番よい。
- (b) 数値の対照（NOT_EVIDENCE）：封印台帳を使わない合成の区画（例：λ ∈ [1/2, 1/2 ＋ 1/1600]）で、t_e ∈ {993/1024, 63/64} の門を両系統で実行する。値が有限であること、判定が一致すること、producer と checker の上界が整合することを確かめる。実行の権限は run4 の回帰と同じ preflight の枠に入れる。

## 5. 直したほうがよいもの

- **F4. 台帳の書き方。** 今は最後に1回だけ書くので、途中で止まると全部失われ、改ざんの検出もできない。run4 と同じ `persistence.Ledger` の追記（ハッシュの連鎖、1記録ごとの書き込み）にするとよい。再開を許すかどうかは FREEZE で決める。
- **F5. 資源の検査。** `_resource_guard` が毎回 `canonical(entries)` 全体を作り直すので、記録が増えるほど時間がかかる。書いた量を足していく形にするとよい。
- **F6. 深さの意味。** 子の深さは C1b の親の深さではなく 0 から数え直している（最大3、親の 1/8 幅まで）。README に一文書くこと。
- **F7. 抽出表の検査。** `c1b_receipt_extract.json` は「空でない辞書」しか見ていない。抽出表の件数（accepted 159、clamped 35）とも照合するとよい。

## 次の工程

F1〜F3（と、できれば F4〜F7）を直した新しい単一 commit（直親は `45617d0` か `26d81e1`）→ chat の差分監査 → run4 回帰と合成区画の対照の実行（preflight、NOT_EVIDENCE）→ chat の検収 → Judge FREEZE・実行許可 → L0(c)(d) → 本走。
