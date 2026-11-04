# 独立監査報告 — B7 独立 verifier（chat 実装）のコード監査

2026-11-04 / 監査人: Muse（独立監査、単発依頼）  
対象: `MUSE_PACKAGE_B7_VERIFIER_20261104.zip`  
報告記載の SHA-256: `bda22ab559753a4b883a4bb96f7b2d487aa0af7e8e999c503a58cfdf4159dfd6`

> 保存注記：本ファイルは2026-11-04にチャットで受領したMuse監査報告の本文内容を整理して登録したもの。付録§6の長大なスクリプト本文・出力はこのファイルには転記していない。パッケージZIPの実物は本操作では受領・ハッシュ再計算していない。原報告に記載された検査結果とSHAはMuseの報告事項であり、登録担当による独立再検証結果ではない。

## 1. 総合判定

**verifier の PASS は、B7 の独立検証として採用できる。** 区間演算層（誤差なし変換による方向付き丸め）、2-jet、カーネル転記、4種のリーフ下界、tiling 検査、最終組み立てについて、原典の再導出・厳密有理数との照合・独立実装との突き合わせで確認し、偽の PASS を生みうる欠陥は見つからなかった。致命的欠陥なし。修復可能な欠落1件（`slabs` の縮退δでのassert、fail-closed）、表記上の指摘1件。

- 区間演算：subnormalから1e308近傍まで、厳密有理数照合16,782件、違反0。積の境界探索300,000件、違反0。逆数・平方根掃引60,000件、違反0。
- clamp：dv=1−s、L²+J²=1、|V|²=1−(1−λ²)ω_z²∈[λ²,1]を解析的に確認。V2,w²∈[4/25,1]、B̂≥4/25。
- H=λ(2/π)∫Σ_ε K：独立P1実装で3点確認。高解像度の1点で相対差1.1e−9。
- ASTRA3のρ第3経路：r·v=λĤの数値残差は4.4e−16以下。
- runner：例外、NaN、件数不一致、tiling失敗はPASSにならない。synthetic_8で実行確認。

L_chat=9.54e−3、L_Dig=3.79e−4 の差は主にΔβ⁺上界の緻密化による。Muse報告にはMIDPOINTの共通部分・ASTRA3のスラブminもproducerより締まる経路と記述があるが、Judge/chatの補正では**producerもMIDPOINTの共通部分を使用する**ため、その差をこの点に帰属させない。採用判定に影響しない。

## 2. 項目別判定

| ID | 判定 | 監査内容と根拠 |
|---|---|---|
| V1a | PASS | TwoSum、Veltkamp分割、Dekker TwoProduct、誤差符号による方向付き丸め。厳密有理数照合16,782件、違反0。subnormal×大数300,000件で反例なし。 |
| V1b | PASS | EFT適用外はok=False、nextafterで外側に倒れる。overflowの下界処理、0×有限、0×infのNaN伝播を確認。 |
| V1c | PASS | 逆数と平方根の誤差符号、Sterbenzの条件、最小桁の符号保存を確認。対数一様掃引60,000件、違反0。 |
| V1d | PASS | sqの零跨ぎ、invの零包含、sqrt負下端のNaN、下流でのNaN検出を実行確認。 |
| V1e | PASS | meetの全呼出箇所を列挙。同じ量の正当な包囲の共通部分であることを確認。 |
| V2a | PASS | 積、二乗、逆数、平方根の2階連鎖律を再導出。mpmath40桁の微分値と12桁一致。 |
| V2b | PASS | withvは値のみを証明済み範囲に狭め、微分の包囲を保持する。 |
| V3a | PASS | jacとFの転記を原典と照合。P1独立実装で確認。κ形とη形は代数的に同一、数値的に1.8e−15まで一致。 |
| V3b | PASS | dv=1−sから回転恒等式、V2・w²・B̂の3 clampを解析的に証明。CL<4/25も確認。 |
| V3c | PASS | F·jacとW·jac·num/denの包囲の共通部分が正当。 |
| V4a | PASS | 反復中点則の剰余は各変数の2階微分のみで包囲でき、混合微分不要。中心形式と直接形式の包囲を確認。 |
| V4b | PASS | ZEROTH=vol×inf K。delta_boxes×rem_partsの分割min、非有限値の保守的処理を確認。 |
| V4c | PASS | Δβ⁺=2(t_b−t_a)/(1+t_a t_b)の厳密有理上界。mpmath照合300件、違反0。K_FLOORの導出を確認。 |
| V4d | PASS | ρの3経路、b₃上限、NaNフォールバック、δスラブの方向を確認。無作為300点で違反0。 |
| V4e | PASS | 正当な4候補のmax、delta_boxesのλ・τ一致とδ tiling検査を確認。 |
| V5a | PASS | ギロチン再帰のtiling健全性を不変条件で確認。重複、隙間、領域外等の敵対的ケースはFAIL。非ギロチンtilingの棄却は保守的。 |
| V5b | PASS | final_lowerの端点選択、2/πの厳密有理包囲、接触帯損失の係数と向きを確認。 |
| V5c | PASS | 件数照合、float→Fractionの厳密変換、例外伝播、NaN処理、selftest停止、keyごとのPASS証明書選択、SHA記録を確認。 |
| V6 | PASS | selftest全PASS。synthetic_8はTILING FAILでNOT PASS。証拠ファイルL0_T3_D1の63,593リーフ、127,185ノード、最終下界9.542343e−3と一致。 |

### V4d の補足

- ρ=(λĤ/T)²、ρ≥λ²cp²、ρ=1−|r×v|²/T²。
- b₃≤2W/λ³≤275/4。NaN時はρ=0、b₃=275/4へ保守的に倒れる。
- ASTRA3の恒等式r·v=λĤは数値的に4.4e−16まで確認。

## 3. 欠陥一覧

**致命的欠陥：なし。**

1. **修復可能・軽微：** `b7iv_vleaf.py` の `slabs` は、δが点区間または相対幅約1e−15以下で幾何中点の近似有理数が端点に一致すると、`assert e[-1] < q < hi`で停止。実運用では到達せず、到達してもfail-closed。次版で`lo == hi`なら`[(lo,hi)]`を返す分岐を検討。**現行監査済みソースは変更しない。**
2. **表記：** `b7iv_ia.py` のdocstringはnextafter主体の旧説明。実装はEFT主体でnextafterはフォールバック。次版で説明更新。**現行監査済みソースは変更しない。**

欠陥としない事項：subnormal領域のVeltkamp分割への懸念（反例なし）、P1初期求積の相対差1.31e−4（高解像度で1.1e−9に解消）、非ギロチンtilingの保守的棄却。

## 4. 受領ファイルのSHA-256照合表（Muse報告値）

| ファイル | SHA-256 |
|---|---|
| src/b7iv_ia.py | b2d26146647903e9656413548b354113efcc818a75cd73d02f043e6ceb56f7e4 |
| src/b7iv_vk.py | f2d6c4a91f30e672a8eb5014c30900604b2c455b44ddce55d1e7256e93bbe524 |
| src/b7iv_vleaf.py | 1c1ee3b48d06b5468eef5d934e97c7039b55ee053af9ff3c2adb3f8f526bb897 |
| src/b7iv_run.py | 31505ba7e4cefc179e86a9076ca8992bc6f4361799057eca3ee0c0c965f0c8d6 |
| src/b7iv_all.py | 0694d95895bae3fb188c8765526b695fc91b2d7347d0ec88926b7fa0e2807341 |
| src/b7iv_selftest.py | efc52d8bc1744852e7c57042e66246caf9bd6de4dabb073750f9f701ae1b8c9b |
| src/README_B7IV.md | 21eca5eef4989aa388bc586b2677ad9ec7feb202f3850c37b57800dc55f97f83 |
| ref/v0_repr_check.py | efe5cf6586d359ea1fe4d9f321c285ab6c0e80469d71e08d70781f48754a9861 |
| ref/ASTRA_FLOOR_LEMMA_V5_20261103.md | b7b188275230cd50d324c7c753a5d911e3ecf5b1ec32368713b7868f14664fc5 |
| ref/CHAT_VERIFY_ASTRA_FLOOR_20261103.md | edf8be22fa081e52a0ad146d5a86dacc2500a19a2ca98e36b1b3e108b34a9869 |
| evidence/selftest_20261104.txt | 00f4befa45e8e2058d350812559731bce1defdc3ab9134875b002c07940a06e2 |
| evidence/L0_T3_D1_chat_iv_run.txt | f34d3c57ba72eefc194a25a7a6209f8cded4172c395d301846969d8cc18d38f5 |
| sample/synthetic_8_L0_T3_D1.leaves.json | fced5da8385e6e8c118038843b7328a59ce4b9dd292617d612cf7d7f3ec1ed19 |

Muse報告によれば全項目が一致。

## 5. 監査範囲と方法

- 前提となる表示およびAstra補題1・2は再監査の対象外。ただし実装がそれらをどう使うかは監査対象。
- daybreak-worksの15箱実行結果には依拠せず、Muse自身がselftest、synthetic_8、証拠ファイルのL0_T3_D1との数値照合を実施。全箱の再実行はしていない。
- 数値プローブは反例探索であり、判定は導出と厳密照合に基づく。

## 6. 付録の取扱い

ユーザーがチャットで提示した報告には、`audit_b7iv_checks.py` の長大な本文が続く。本登録ファイルは付録の完全保存ではなく、**§1–5の監査内容を整理した転記**である。付録スクリプトの原本と出力、および`MUSE_PACKAGE_B7_VERIFIER_20261104.zip`のバイナリは別途保存・照合が必要。

## 7. B7工程への適用（Judge共有情報）

daybreak-worksでの独立verifierは15/15 PASS。B7全体は15/40 PASS、25箱OPEN。ソースdigest `48d7b03813dc530d2ca013c47e56b369f4131322a8d5aff4668bf6adc827e411` が不変なら、今後の追加箱にも今回のコード監査を継承可能。ただし証明書ごとの再計算、B7全40箱のCLOSED、T1組み立ては別工程。
