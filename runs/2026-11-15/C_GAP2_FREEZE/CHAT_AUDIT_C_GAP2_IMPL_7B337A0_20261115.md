# chat 監査記録：C 空白② 実装の最終修正 `7b337a0`（直親 `3bd5113`）

2026-11-15 / chat / 差分と静的な監査（実行なし、封印入力は読んでいない）

## 対象

`cotaxxxx/bg-oblate-spheroid`、branch `implement/c-gap2-v4-r2-20261115`、commit `7b337a01950ae37dd568e3370198c9ce4f26a805`。直親が `3bd5113` の単一 commit であることを確かめた。変更は4ファイル（+145/−12 行）：`lineage_compare.py`、`runtime_identity.py`、`sealed_contract.py`、README。

## 判定

**H1 は PASS。F7 は、書き方を変える必要がある（本走の入口で誤って止まる恐れ）。直しは小さいので、もう1回の単一 commit で済ませ、その commit で preflight を流すこと。**

## 1. H1：PASS

SEALED の比較で、次を必須にした。

- 両系統の `input_sha256` が `sealed_contract.PINNED`（封印4ファイルの完全な SHA）と完全に一致すること。
- 引数 `--judge-ruling-sha256`（64桁の小文字 hex）があり、両系統の manifest の Judge の SHA と一致すること。

合成モードで Judge の SHA を渡すことは禁止されている。SEALED のときに引数がなければ実行を拒む。正しい。

## 2. F7：直しが要る

`_receipt_count_candidates` は、抽出表のどの深さの辞書でも、`accepted`、`accepted_count`、`right_clamp` などの名前のキーを全部拾い、そのすべてが 159 と 35 に等しいことを要求する。抽出表の実際の構造はまだ誰も見ていない。

その中に、別の意味で同じ名前のキーがあると、正しい入力でも `RECEIPT_EXTRACT_COUNT_MISMATCH` で止まる。たとえば、根の局所化や外側の段ごとの「受理した箱」の数、非有限の記録の数などである。止まる場所は FREEZE の後の L0(c) なので、そこで止まると commit・監査・FREEZE をやり直すことになる。

主な証拠である件数（accepted 159、clamped 35、unclamped 124）は、両系統のハッシュ連鎖台帳と replay から厳密に数えている。抽出表の照合は補助なので、推測したキー名で本走を止めるべきではない。

直し方（推奨）：

- `verify_receipt_extract_counts` を**止めない記録**にする。見つかった候補の経路と値を、照合結果（一致・不一致・見つからない）とともに manifest の `receipt_counts` に書くだけにする。
- 抽出表の件数と receipt の文書の値との照合は、本走の後に chat の検収で行う。抽出表の SHA はすでに pin されている。

## 3. `runtime_identity` の親の鎖（今後の手戻りを減らすため）

修正の commit を作るたびに `BASE_NEW` などの定数を書き換え、それまでの preflight の同一性が使えなくなる。これを避けるために、次の形にするとよい。

- 途中の commit を固定する代わりに、`git merge-base --is-ancestor 26d81e1 HEAD` で run4 の凍結 commit が祖先であることを確かめる。
- `26d81e1..HEAD` で変わったファイルの集合が、宣言した集合（13 ＋ 新規5）とちょうど一致することを確かめる。
- HEAD の完全な SHA を記録する。

本走で使う commit は Judge の FREEZE 裁定に HEAD の SHA として書くので、固定はそこで行われる。preflight の記録と本走の記録の HEAD が一致することは、chat が検収で確かめる。

## 次の工程

F7 の書き換えと、親の鎖の検査の一般化（任意）を入れた単一 commit（直親 `7b337a0`）→ chat の差分監査（小さい差分）→ PASS なら、その commit で preflight 一式を流す（Judge の裁定で許可済み。すべて NOT_EVIDENCE、封印入力は読まない）→ chat の検収 → Judge FREEZE（裁定に HEAD の SHA を書く）。
