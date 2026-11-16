# Judge 裁定：扁長 P1（a_c の局所分岐）の第二系統に Julia を使うことを承認する

2026-11-16 / Judge（ユーザー）／記録：chat

## 裁定

**「承認：Julia で第二系統」**（ボタンによる選択。chat の推奨どおり）。

研究用 PC（daybreak-works）に、Julia と IntervalArithmetic.jl を導入することを承認する。

扁長 P1（a_c の局所分岐）の第二系統は、事前宣言 v2 の段階制（Judge 2026-10-10）に従い、clean-room で実装する。入力は元の定義だけとする。

| 区分 | 条件 |
|---|---|
| 必須 | Q_z ≥ 1/100、5 桁の括弧、Q′ < 0、H4 < 0 |
| 追加 | 20 桁の括弧、Q_z ≥ 0.0885587746621582 |

対象の第一系統は、`cotaxxxx/basepoint-geometry` main `abf704b8701f3da8eb41d8a99408570a413b2214` の `CERTIFICATES/prolate/local_bifurcation/` である。

## 条件

- **版の固定：** Julia と IntervalArithmetic.jl の版は、具体的な番号で固定する。Manifest.toml は事前宣言に pin する。
- **導入する場所：** 研究用 PC の既存の Python 環境とは別の場所に入れる。D-PRO の本走や較正と、同時に重い計算をしない。
- **進め方：** 事前宣言の入力一式と、精度保証つき積分の契約を作る。chat がそれを監査する。そのあと FREEZE、実行、chat の検収、Judge の採否の順に進める。
- **扱い：** 第二系統の結果は、PASS したあとに登録するまで、候補（CANDIDATE）として扱う。

## 記録上の区別

このファイルは、2026-11-16のJudgeメッセージにある裁定本文の保存である。添付のV25 `JUDGE_RULING_D_PRO_DESIGN_ADOPTED_20261116.md` は別の裁定（Astra D-PRO設計の採用）であり、Julia第二系統の実行FREEZEを含まない。
