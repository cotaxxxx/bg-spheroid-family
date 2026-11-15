# Judge 裁定：軸上 C 系列の大域を CLOSED とする

2026-11-16 / Judge（ユーザー）／ 記録: chat

## 裁定

**「採用：C 系列の大域を CLOSED」**（ボタンによる選択。chat の推奨どおり）。

扁球 λ ∈ [2/5, 33/50] について、定理 C-AXIS-V1 を採用する。

> 正の軸上の内部の根の数 N₊(λ) ＝ #{t ∈ (0, 1)：g(t, λ) ＝ 0} は、次のとおりである。
>
> - 2/5 ≤ λ ≤ λ_c で 0
> - λ_c < λ < λ_∂ で 1
> - λ_∂ ≤ λ ≤ 33/50 で 0
>
> 特別な点では次のようになる。
>
> - λ ＝ λ_c：中心 t ＝ 0 の零点が退化し、三次の項は c₃ < 0 である。
> - λ ＝ λ_x：ただ一つの正の根がちょうど t ＝ 1/2 にあり、単純根である。
> - λ ＝ λ_∂：根は境界 t ＝ 1 に達し、内部の根ではない。
>
> 負の側の根は、奇性により正の側の根と対になる。

λ の位置関係は 2/5 < λ_c < 83/200 < λ_x < 9/20 < 5/8 < λ_∂ < 33/50 である。

## 根拠

| 項目 | 値 |
|---|---|
| 組み立て | `bg-spheroid-family` の `drafts/2026-11-16/C_AXIS_GLOBAL_COVER_ASSEMBLY_V1/C_AXIAL_GLOBAL_COVER_ASSEMBLY_DRAFT_V1.md`（commit `aab1d06`、SHA-256 `aeb435fc30c352d85b875f6268a69d48c58950aff4f09607b01929cd4dda6c35`） |
| A1 移送 | `bg-oblate-spheroid` の `analysis/OBLATE_AXIAL_LOWER_HALF_LEMMA_C1A_TRANSFER.md`（commit `473d7022`、blob `b8370d649bac0bbe943186eb003b6b0e837a3dd6`） |
| chat 監査 | V22（v0 の監査と、C1b の内側の被覆の独立検算）。V23 `CHAT_AUDIT_C1A_TRANSFER_AND_ASSEMBLY_V1_20261116.md`（A1 PASS、v1 PASS） |
| 部品 | 次の表のとおり |

| 部品 | 内容 |
|---|---|
| 機械と受領書 | CENTER、C0（C0a・C0b）、C1a、C1b（B_ob の部分門を含む）、C1c、C1d、帯 Claims 1〜3、B_ob の再認証 |
| 空白 | 空白①（run4、条件付き CLOSED）、空白②（V21 CLOSED） |
| 解析補題（chat 監査 PASS） | V13、V19（C1 `5afa815f`、C2 `7cb9b809`・`f66ffe5a`、G0/E1 v3）、V20（下半分 `6fba6e4f`、C0 移送 `963b03be`、C1d `35656381`）、V23（C1a 移送 `b8370d64`） |

各受領書に「EXTERNAL_AUDIT_PENDING」と付いている条件は、chat の監査が PASS したことにより、この裁定で外す。外部の人間による解析補題の監査は、論文と投稿の段階で別に扱う。CLOSED の条件にはしない。

## 付記

- **v1.1：** v1.1 で文言の直し B1〜B3（V23 §3）を入れる。chat は差分だけを確かめ、数学の内容は変えない。差分に数学の変更が含まれていた場合は、Judge に戻す。
- **D-OB の大域：** この裁定は D-OB の大域を CLOSED とするものではない。次の工程で、Dig が C と D をつなぐ短い組み立てを作る。対象は、軸上の根の構造（C）と、横断の D 系列（V18 CLOSED）による軸の外の停留点の除外である。chat がそれを監査したあと、Judge が別に裁定する。
