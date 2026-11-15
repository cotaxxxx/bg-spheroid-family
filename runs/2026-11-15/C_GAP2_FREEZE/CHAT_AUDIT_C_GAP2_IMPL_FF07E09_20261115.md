# chat 監査記録：C 空白② 実装の修正 `ff07e09`（直親 `45617d0`）

2026-11-15 / chat / 差分と静的な監査（実行なし、封印入力は読んでいない）

## 対象

`cotaxxxx/bg-oblate-spheroid`、branch `implement/c-gap2-v4-r2-20261115`、commit `ff07e097c098ace4051b04b76d410713fb59490a`。直親が `45617d0` の単一 commit であることを確かめた。変更は5ファイル（+657/−122 行）：`endpoint_driver.py`（改修）、`README`（改修）、`lineage_compare.py`・`runtime_identity.py`・`synthetic_preflight.py`（新規）。kernel と gating は `45617d0` から変わっていない。

## 判定

**F1〜F6 の対応は方向として正しい。ただし、駆動部に本走の最初の1区画で必ず止まる不具合が1つある。直してから回帰に進むこと（必須2点）。**

## 1. 必須の直し

**G1. 駆動部の t_e の照合が、型の違いで必ず失敗する。** `endpoint_driver.py` 158行の `if ev["endpoint_seed_t"] != parent.t_e:` が問題である。

- `ev` は `gap2_endpoint_record` が `_gap1_value()` を通した記録で、`endpoint_seed_t` は `rational_text()` の文字列（"p/q"）になっている。
- `parent.t_e` は `Fraction` である。

したがって、この比較はいつも「不一致」になる。本走は最初の区画の門を計算した直後に `CHILD_SEED_INHERITANCE_FAIL` で止まる。fail-closed なので誤った証明は出ないが、FREEZE を1回むだにする。`45617d0` では文字列と Fraction の両方と比べていたので通っていた。今回の書き換えで壊れた。

- 直し方：`Fraction(ev["endpoint_seed_t"]) != parent.t_e`（`persistence.fraction_from_text` を使ってもよい）。

**G2. 駆動部を本物の経路で端から端まで通す対照がない。** 今回の不具合は、静的な検査でも、合成区画の対照（kernel を直接呼ぶ）でも、比較器の模擬124区画（手で組んだ記録）でも見つからない。C1d の駆動部のとき（`7a583d75`、C4 の test が本物の記録を通らず、本走の最初の評価で止まった）と同じ型の穴である。次を加えること。

- `full_run` を「封印入力の読み込み（L0(c)）」と「親の一覧から門を回して台帳を書く部分」に分ける。後者を、合成の親2つ（例：λ ∈ [1/2, 1/2 ＋ 1/1600] と、それに隣接する区画、t_e ∈ {993/1024, 63/64}）で、本物の kernel・gating・Ledger・manifest・runtime_identity を通して実行する対照を作る。結果は NOT_EVIDENCE。
- その出力2系統に `lineage_compare` をかけて、比較器も本物の出力で通ることを確かめる（親の数は引数で受け取れるようにする）。
- 失敗の経路も1つ通す。たとえば、深さの上限に届く合成の親で ABORT、segment_end、manifest の ABORT_NOT_EVIDENCE まで書けることを確かめる。

## 2. 直したほうがよいもの

- **G3. 系統ごとに違う import が、系統間の一致の検査を誤って落とす恐れ。** `runtime_identity()` は、閉包の外で import されたファイルを `blobs` に足し、それを `current_blobs_and_sha256` として返している。`lineage_compare` はこの辞書が producer と checker で同じことを要求する。系統ごとに import が違えば、正しい実行でも `LINEAGE_RUNTIME_MISMATCH` で止まる。pin した集合（変更分と run4 の25）の blob と、実際の import の閉包を別の辞書に分け、系統間では前者だけを比べるとよい。同じ理由で、実行の途中で遅れて import されるモジュールがあると、前後の同一性も崩れる。G2 の対照で前後の一致を実際に確かめること。
- **G4. 比較器で門の算術を独立に確かめる。** 今の比較器は記録の seed と累積の上界の符号を見るだけである。ACCEPT の葉ごとに次を加えるとよい。
  - `endpoint_gt_boxes` の t 区間が一般の式（N ＝ ⌈512(1 − t_e)⌉、等幅）の分割と一致すること。
  - 厳密な分数で seed_upper ＋ Δt・Σ max(0, upper_j) を計算し直し、それが負で、記録の累積上界以下であること。
- **G5. `Ledger.append` の副作用。** header と segment_end の直後に `lscpu_raw_trace` の記録が自動で足されることがある（`_LAST_LSCPU_TRACE` が設定されているとき）。比較器は「header、slab_record の列、segment_end」以外を拒むので、もし足されると正しい実行でも落ちる。gap2 では設定されないはずだが、比較器でこの記録の扱いを明記するとよい。
- **F7（前回から）。** 抽出表 `c1b_receipt_extract.json` の件数照合はまだ入っていない。

## 3. PASS の部分

- **F1（比較器）：** 両系統の manifest と ledger の SHA、ハッシュの連鎖、header と manifest の親の一覧・入力 pin・Judge pin の一致、木の再構成（右の子が先、深さ ≤3、REFINE と ACCEPT の区別、ABORT の拒否）、葉の和が親の区間にちょうど一致すること、ACCEPT は seed < 0 かつ累積 < 0 かつ `endpoint_pass`、両系統の親と t_e の一致、全体の最悪値の表を検査している。正しい。
- **F2（実行時の同一性）：** HEAD・直親・凍結の祖父、clean、変更ファイルと run4 の25 blob の照合、import の閉包、Python・flint・mpmath・platform の記録、前後の一致。方向は正しい（G3 を除く）。
- **F3(a)：** `_static_check` で、一般の式を 31/32 に当てはめると run4 の16箱と一致すること、993/1024・63/64・1023/1024 で kernel の分割が一般の式と一致することを assert している。足りる。
- **F3(b)：** `synthetic_preflight.py` は、新しい分岐（t_e ≠ 31/32）を両系統で本物の kernel で実行し、門の記録の上界を `gt_box` の再計算と照合し、producer と checker の区間が重なること、判定が一致することを確かめる。足りる。
- **F4：** `persistence.Ledger` の追記（1記録ごとに fsync、ハッシュの連鎖）に変わった。header と segment_end もある。
- **F5：** 資源の検査は台帳のバイト数を見る形に変わった。
- **F6：** λ の深さの意味を header に明記した。

## 次の工程

G1・G2（と、できれば G3〜G5、F7）を直した新しい単一 commit（直親 `ff07e09`）→ chat の差分監査 → 回帰の preflight 一式（run4 回帰、合成区画の対照、G2 の端から端までの対照、すべて NOT_EVIDENCE）の実行 → chat の検収 → Judge FREEZE・実行許可 → L0(c)(d) → 本走。

なお `runtime_identity` は直親を `45617d0` に固定しているので、次の commit ではこの定数も更新が要る（`ff07e09` を直親にする場合）。
