# V26対応提出物｜扁長P1 a_c Julia第二系統（pack V2／積分契約V2）

2026-11-16 / Dig／**CHAT_DELTA_AUDIT_PENDING・NOT_FROZEN・NO_CERTIFICATION_RUN**

## 監査根拠

- chat V26：family `evidence/c-gap2-freeze-20261115`、commit `12bb2d183ef9f7367233a0aa9740aa046a36fa43`。
- V26監査記録SHA-256：`5056f9a9a3d17fe46cf99f1fbcb1fa51ef52a9f46c4ed05c6b65a098f73d7fa6`。
- 改訂前：family `draft/prolate-ac-julia-stage-v3-20261116`、commit `9b22b107be758252d242225d43e41fe86f1b499b`。
- V26裁定の状況：**I0原pack V1 PASS／Julia環境PASS／積分契約V1はV2改稿要**。

## 今回の成果物

| ファイル | 用途 | 判定 |
|---|---|---|
| `ORIGINAL_DEFINITIONS_INPUT_PACK_V2.md` | J1参照体の係数／J2受領手順。実装者へ唯一最初に渡す数学入力 | **V2差分chat監査待ち** |
| `J2_NEW_DIG_SESSION_HANDOFF_PROTOCOL.md` | 新セッションと受領ログを管理する監査側手順 | **SESSION_NOT_STARTED** |
| `VERIFIED_QUADRATURE_CONTRACT_DRAFT_V2.md` | J3〜J6を追記した積分契約 | **chat監査待ち** |
| `PROLATE_AC_JULIA_SECONDLINEAGE_PREDECLARE_DRAFT_V3_1.md` | 統治上の事前宣言整合 | **NOT_FROZEN** |
| `J4_INTERVAL_OUTWARD_SMOKE.jl`／`.stdout` | sqrt(2)・acos(0)の有理括弧とisguaranteedの軽量試験 | **PASS・NOT_EVIDENCE** |
| `julia_env/Project.toml`、`Manifest.toml` | 初版から依存追加なし。Julia／IA版をpin | **V26環境PASSを維持** |

## 修正の対応表

**J1:** Q、Q_z、H4、Q′は参照体 `K_λ` での係数。相似に伴う二階・四階係数のスケールとQ′の区別を追加。

**J2:** 新しい独立Digセッションでpack V2だけを渡し、最初の会話にセッションID・pack SHA・単独入力の受領記録を残す。**まだセッションは作成していない**。

**J3:** `Interval{BigFloat}` で有限次Taylor jetを自前実装する方式(b)。TaylorSeries.jl依存なし。独立解析・jet・剰余のchat監査が前提。

**J4:** `Rational{BigInt}` を入口とし、Float64リテラル・暗黙変換を拒否。`isguaranteed`の最終門、sqrt・acosで有理括弧と外向き丸めの実証を追加。

**J5:** checkerは台帳の有理端点からセル被覆・係数の積分・Taylor剰余・πの上下界・累積和・門を厳密に再計算。被積分関数の再計算は要求せず、その包囲の妥当性はI3 chat監査が担保。

**J6:** I0およびI2の担当を**chat**に変更。第一系統にアクセスできるのはchat側であり、実装者へ第一系統の導出式や数値を渡さない。

## 依存性・運用

- `Julia 1.10.13`＋`IntervalArithmetic.jl 1.0.10`。
- Project SHA-256：`3b14e1942ba3d9c63b7be31f52934ce285cffbf8ce92f69d9327c1356933aee8`。
- Manifest SHA-256：`f1de48582bdef170b152b5a785490b3f176bc9c70fc0594e6589449c1d4d7350`。
- **V1/V2修正のchat差分監査 → J2独立セッション受領ログ → I1導出 → I2記号監査 → I3実装監査 → Judge FREEZE → 本走 → chat検収 → Judge採否**。
- RSS上限（24GiB候補）とcore-hour予算は**FREEZEでJudgeが裁定**。現在は確定していない。

**今回の登録は新しい認証結果やI3 PASSを意味しない。**
