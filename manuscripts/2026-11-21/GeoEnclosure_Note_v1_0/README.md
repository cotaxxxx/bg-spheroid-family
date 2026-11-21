# GeoEnclosure 研究ノート v1.0（日本語）

GeoEnclosure の方法論、適用条件、限界、検証の枠組みを述べる研究ノートと、その中の集計を再実行するための検査スクリプトです。

> **状態：Zenodo 公開前の原稿。** 補足資料 A.4（著者による最終確認の日付と範囲）は未記入です。ここに置いたことは、数学的な採否や著者の最終確認を意味しません。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `GeoEnclosure_Note_v1_0_JA.md` | 研究ノート本文 |
| `check_n3_cover.py` | 台帳 N3 の被覆、二等分、終端条件、内訳 39・62・85 の整数検査（対応表 G07、G16） |
| `rerun_186_rules.py` | 元の計算核で 186 箱を再評価し、規則 A・B の集計を出力（対応表 G08、G18） |
| `SHA256SUMS` | 上の三つのファイルの SHA-256 |

## 再実行の手順

入力は、本リポジトリのコミット `a5ab9b5016c8df9b7f94cbfd7cd0e82aeba8dd28`（ブランチ `codex/paper-i-v0.4-20261120`）にある
`manuscripts/2026-11-20/Paper_I_v0_4/Paper_I_v0_4_Manuscript_and_Verification.zip`
（SHA-256 `57ee540bb8f3679e1b5abfaf043d6c961d934a981bddfb9d0dba0bd32a4c4d91`）です。これを `X` に展開したとします。

```sh
python3 check_n3_cover.py X/audit/snapshots/ledgers/N3
```

```sh
g++ -std=c++20 -O3 -frounding-math -ffp-contract=off -fno-fast-math X/audit/snapshots/kernel.cpp -o kernel
```

```sh
python3 rerun_186_rules.py X/audit/snapshots/ledgers/N3 ./kernel
```

2026-11-21 の実行（Linux x86_64、g++ 13.3.0、Python 3）では、次の結果になりました。

- 12 個の初期箱が `[2,5]×[0,1]` を敷き詰める。分割は ρ 方向 161 回、λ 方向 13 回。終端箱 186 個、面積の合計 3。
- 台帳に記録された包囲 186 件（E 方式 101 件、T 方式 85 件）が、すべて整数値で一致。
- 規則 A：除外 56、未判定 130。規則 B：H>0 が 56、曲率 67、四階微分 63。
- 元台帳の四階微分 85 箱は、17（H>0）・5（曲率）・63（四階微分）に再分類。

これは元の計算核による再現であり、独立した核による再計算ではありません。計算核のソースには `DIAGNOSTIC_ONLY / NOT_EVIDENCE` の注記があります。位置づけは本文 §6.6 を参照してください。
