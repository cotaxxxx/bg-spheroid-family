# V27 K1・K2修正版｜Julia 第二系統・監査用提出束

**2026-11-16 / Dig / DRAFT／CHAT_DELTA_AUDIT_PENDING／NOT_FROZEN／NOT_EVIDENCE**

監査元：family `evidence/c-gap2-freeze-20261115` commit
`2e678b641dda92a8d6f820f6a8dd879d9e5c857e`。
監査原本 `CHAT_AUDIT_PROLATE_AC_JULIA_V4_DIFF_20261116.md`、
SHA-256 `2ba8a922c9574e0f31e5a5b2fdd093d2ff230c97db62f1f8569d7fe29fa0a233`。
元のpack V2・契約V2はchat V27 PASS。今回の差分は**K1の型・精度とK2の一時チャット隔離手順**。

## 成果物

| ファイル | 内容・状態 |
|---|---|
| `ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md` | **バイト変更なし**、SHA `a01407dc9f1addb663a69fdb57d6365c8bdada9de83835942cf305e480459cbd`、chat V27 PASS |
| `VERIFIED_QUADRATURE_CONTRACT_DRAFT_V2_1.md` | Q3cへK1の全区間型・精度確認を追加。**差分chat監査待ち** |
| `J4_INTERVAL_OUTWARD_SMOKE_V2.jl` | `interval(BigFloat,rational)`、型・256ビット・有理幅`≤2^(-240)`・`diam`・`isguaranteed`を検査 |
| `J4_INTERVAL_OUTWARD_SMOKE_V2.stdout` | **7行、全検査PASS、NOT_EVIDENCE** |
| `J4_INTERVAL_OUTWARD_SMOKE_V2.stderr` | 空 |
| `J2_TEMPORARY_CHAT_HANDOFF_V27.md` | 一時チャット、packのみ、接続なし、受領ログ、導出封印後の契約投入を明示 |
| `PROLATE_AC_JULIA_SECONDLINEAGE_PREDECLARE_DRAFT_V3_2.md` | V27の状態とK1/K2を事前宣言のDRAFTへ整合 |
| `julia_env/Project.toml`／`Manifest.toml` | 変更なし。Julia 1.10.13、IA 1.0.10、TaylorSeries.jl不使用 |

## 新しい一時チャットの運用

**ユーザーが新しいChatGPT一時チャットを開く必要がある。**
この監査・編集チャットから別セッションを自動作成したり、接続を解除したり、ファイルを添付したりしたとは主張しない。
メモリなし、GitHubなし、研究用PC接続なしの一時チャットに、**最初はpack V2一件のみ**を添付してI1導出を依頼。
導出した式の文書とSHAを封印し監査側へ渡す。**封印後**に契約V2.1を同じ一時チャットへ渡す。

隔離を完全に証明することはできないので、受領した隔離措置を記録して、後続chat I2の記号照合で独立性を補強する。

## 残る関門

- **今回のK1差分とK2実施手順：chat確認待ち**（pack V2の原定義I0のPASSは維持）。
- I1独立導出・SHA封印、I2記号照合、I3 jet/積分証明監査、Judge FREEZEは未了。
- Julia環境・既存Python・STATE main・第一系統の証拠は変更しない。
- RSS 24 GiB案と計算予算はJudge FREEZE時の裁定へ残す。
