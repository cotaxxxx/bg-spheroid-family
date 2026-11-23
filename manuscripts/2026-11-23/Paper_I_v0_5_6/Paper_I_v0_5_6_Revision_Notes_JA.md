# Paper I v0.5.6｜変更記録・監査引渡し

- 作成日：2026-11-23／担当：Dig（ChatGPT）
- 編集の親版：v0.5.4（PDF SHA-256 `6fa3a41e1ea1f5e79a65e4f5b1f805d67827bbd583c7c6b9ef023b0e5de722bb`）
- v0.5.5 は編集元に使わない。先行研究不足のため採用しない。
- 対象指示：`DIG_SESSION_HANDOFF_20261123.md`（`a61e43a`）、通常監査 `2af6b07`、Judge承認済み先行研究5項目。
- 公開可否・採否：Digは判断しない。Claude通常監査とJudge裁定待ち。

## 変更箇所

1. `main.tex`：所属を `DAYBREAK (independent research)`、版表示v0.5.6、監査範囲について「独立再計算した標本箱・整数被覆の確認／C1–C6の全実行なし」を区別。
2. `sections/core.tex`：§1のGeoEnclosureから DOI を引用。§3に監査範囲を正確に記述。
3. `sections/numerical_discussion.tex`：§10の監査範囲・AI利用（ChatGPT、Codex、GPT-6.2 Astra、Claude、Claude Code、Muse）を修正。**最後の `Author verification ... is pending.` は変更していない。**
4. `sections/related_work.tex`：O’Haraの境界積分表示と重みの共通性、Sakataの平面円環例、Böröczkyほかの放射ガウス写像、Bertrandの式(6)の角度費用、Johanssonの区間積分、作者旧稿（球・扁長局所分岐）と本稿の大域的貢献を記載。未確認のO’Hara定理・式番号は付けず、Sakataの例番号も付けていない。
5. `references_additions.bib`：上記5件（3論文、GeoEnclosure DOI、作者球旧稿）を追加。O’Hara・Sakata・扁長局所分岐の従来文献は保持。
6. 新規 `LICENSE`：著者作成の論文・文章・資料は CC BY 4.0、著者作成プログラムソースは MIT。第三者の権利は別。

## 非変更保証と再現可能性

- 定理、分類表、C1–C6、数学的証明、数値、計算資料は編集対象外。`sections/computational_evidence.tex`、`sections/prolate_tail.tex`、`sections/radial_experiment.tex` を含む全非対象既存ファイルは原本とバイト一致。
- `main.tex` と `sections/core.tex` の差分は表紙・§1・§3の文章だけ。
- 数値本走・研究PC操作は実施していない。出典別の再計算範囲は v0.5.4 以来の `CURRENT_REPRODUCTION_v0_5_4.md` を維持。
- 原本からのpatchは `SOURCE_DIFF_v0_5_4_to_v0_5_6.patch`。基準ファイルへの適用再試験と全変更バイト比較はPASS。
- BibTeX: `/usr/bin/bibtex.original` + pdflatex、本文39ページ。未解決引用・参照なし。
- 旧版の原本ハッシュ一覧は ZIP 内 `provenance/SHA256SUMS_v0_5_4_Original.txt` に保存。今回のZIP内部 `SHA256SUMS` は今回の全ファイル（自身を除く）を列挙する。

## 今後の工程

- chat（Claude）が v0.5.4 → v0.5.6 の差分だけを通常監査。Dig作成物は `CHAT_` を名乗らない。
- 著者自身の37ページ原本通読と承認に関して、§10最終文はJudgeの指示があるまで「pending」を保持。
- Zenodoへの公開はこの束の作成で自動的に承認されたものではない。
