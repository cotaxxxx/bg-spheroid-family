# Judge 裁定：FT_q（関門4）と L3 V0.2 の条件を外す

2026-11-15 / Judge（ユーザー）／ 記録: chat

## 裁定

**「条件を外す」**（ボタンによる選択。chat の推奨どおり）。

1. FT_q（関門4）を **DISCHARGED** とする。2026-10-17 の裁定（V12 で復元）に付いていた継承4条件は、次の chat 監査ですべて解消した。
   - P1 の正規化：V14
   - 対の密度：V14（L3 が使うのは P1 §8.2 の K_H ではなく、積分として同値な E_yy の表示。その同値性を確かめた）
   - 境界の延長：V13（Lemma V(c)・Lemma 6.1）を V14 の鎖で使用
   - 端点の NP-T との接続：V15（NP-T の証明 PASS。極で NP-T の核と FT_q V3 の縮約が同じ値を与えることを10桁で照合。m₀ を出すのに NP-T は前提として要らない）
2. L3 V0.2 の数学的な前提（FT_q の下界 M と QM の連続度 ω_E）は閉じた。QM-1・QM は V15 で PASS（QM-1 は Muse の 10-31 の独立監査とも一致）。L3 V0.2 の結論 H(p) > 273790294597/7000000000000（δ₀ ＝ 3/10⁸ の閉境界層）は条件なしで成り立つ。
3. 正典値は変えない：whole-face m₀ ≥ 295346256371/10¹²（Astra の厳密な m₀、SHA `207b9617…`）。chat の独立の下界は m₀ ≥ 3691828199/12500000000。
4. 換算係数は 1（V14）。後掛けの λ/2、1/2、2、π はない。
5. Muse は使わなかった。見解は割れていない。
6. Dig は STATE の D1 欄（FT_q）と L3 の欄から「条件付き」と継承条件を外してよい。L1、D4/D5 全体の P1 前提の扱い、D5 全体の OPEN、D-OB global の状態は、この裁定では変えない。

## 根拠の原本

| 原本 | SHA-256 | 内容 |
|---|---|---|
| `CHAT_ORIGINALS_V13_P1_NOTE_AUDIT_20261115.zip` | `a634cf78c258cef9e9713da489a714f0356194ddb4e168c231e947b87e72fe8e` | P1 設計ノートの監査（PASS） |
| `CHAT_ORIGINALS_V14_FTQ_SIGNED_REDUCTION_AUDIT_20261115.zip` | `88347233b5c50b8ee42731ee1ac245ddba826f47b15ee58dd48eeb44c271d67d` | FT_q の符号付きの縮約の監査（PASS、換算係数 1） |
| `CHAT_ORIGINALS_V15_NPT_L2_QM_AUDIT_20261115.zip` | `9ad8bfb2ae211d1f67dde966516ce7d9db4aebe92e69f8f666a7611d44fc3c1a` | NP-T・L2・QM-1・QM の監査（4件 PASS） |

所在：`cotaxxxx/bg-spheroid-family`、branch `audit/ftq-v3-recovery-20261104`、`runs/2026-11-15/` の下。
