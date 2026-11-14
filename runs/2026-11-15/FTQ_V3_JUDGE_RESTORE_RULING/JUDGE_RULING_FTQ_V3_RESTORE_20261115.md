# Judge 裁定：FT_q V3 の条件付き DISCHARGED の復元

2026-11-15 / Judge（ユーザー）／ 記録: chat

## 裁定

**「復元する」**（ボタンによる選択）。

1. 2026-10-17 の裁定「FT_q：DISCHARGED（条件付き）」を復元する。条件は当時と同じ4件：P1 の正規化、対の密度の解釈、境界の延長、端点の NP-T との接続。
2. 正典値は当時と同じ：whole-face m₀ ≥ 295346256371/10¹²（Astra の厳密な m₀、`FTQ_V3_EXACT_M0_20261017.txt`、SHA `207b9617…`）。chat の独立の証明書による下界は m₀ ≥ 3691828199/12500000000 ＝ 0.29534625592。
3. 根拠：chat 独立再計算の原本 V11（`CHAT_ORIGINALS_V11_FTQ_V3_RECOMPUTE_20261115.zip`、SHA `c283666fde05d89b847bf0e857b06ade1de54f16c58ac5f772b00945eab7b359`）。10-17 の会話から復元したスクリプト `bc18df18…` が、10-17 の記録とバイト単位で同一の結果 `79043fa6…` を再現した。Dig の照合も PASS。所在：`cotaxxxx/bg-spheroid-family` `audit/ftq-v3-recovery-20261104` `runs/2026-11-15/FTQ_V3_CHAT_RECOMPUTE_RESTORE/`（commit `88f76fa`）。
4. 2026-10-31（STATE v1.32、`37013af`）の格下げは、計算の失敗ではなく原本の所在不明によるものだった。その理由は解消した。
5. FT_q V4 の認証し直しは行わない。
6. Astra の 4096 枝の束（ChatGPT の Library、修復版）は補助の証拠とする。採用の根拠は chat の独立の証明書であり、Astra の束の独立検証は条件ではない。
7. Dig は STATE の D1 欄と、L3 の継承条件 (4)（FT_q V3 の下界 M の原本欠落）を、この裁定に合わせて直してよい。D5 全体の OPEN、P1 前提の扱いは変えない。
