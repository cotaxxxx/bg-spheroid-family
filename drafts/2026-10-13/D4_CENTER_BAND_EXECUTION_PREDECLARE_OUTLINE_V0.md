# D4 CENTER BAND EXECUTION PREDECLARE OUTLINE V0

2026-10-13。
**DRAFT / NOT FROZEN / EXECUTION PROHIBITED。METHOD_UNDETERMINED。**

これは将来の事前宣言の骨子。METHOD_SELECTED、Judge method ruling、FREEZE、実装監査、実行許可のいずれも発行しない。現時点で機械的に実行可能な契約ではない。

## 1. Claim

閉箱B_003の全パラメータ点に対し、正則化Hに厳密下界を与えることを第一候補とする。直接必要な排除主張はr>0でH>0。r=0は同じ量の連続延長として扱い、中心値の補題H0≥1547/4860をchat監査にかける。中心自身の停留点を排除したとは主張しない。

一様下界が得られない場合も、Hの符号反例か単に包囲不能かを区別する。H>0と異なる局所排除を採用するならJudgeによる方法・claimの再裁定が必要。

## 2. Domain

\[
B_{003}=[0,1/8]\times[0,1/8]\times[119/200,33/50]
\]
（r,τ,λの順）。source pinはsource audit V0 §2に記載。SPEC V3 @111c3169…、SHA-256 511d2f371784a07359c2b691abfb224ef772cddf298f2890b5596a5dc2309330を担当単位の正典とする。

D5と共有する面はr=1/8、τ=1/8、λ=119/200。D4はこれらを含めた全閉箱を担当。D-AN-1 Σとの交わりはない。担当の縮小・拡張は本骨子では行わない。

## 3. Mathematical representation

P1のF=h arccos²γと
\[
H=\int_0^1E_{\rho\rho}(s\rho,z)ds
=\frac1{4\pi\lambda}\int K_H\,d\mu d\phi
\]
を基準とする。φ半区間を使う場合はI=2J、H=J/(2πλ)の係数を固定し、JとHのmarginを混同しない。

中心H0の1D公式、別々の偶性、D≥833/1600を紙上証明。採用候補：符号付きTaylor下界＋定量剰余。外側は正則なpaired/平均積分。Rと導関数のγ=1延長、有限級数tailまたは別の厳密包囲を事前に指定する。

## 4. Center treatment

中心の全τ-fiberを一つのH0(λ)で処理。H0≥m_*は監査対象の補題案。r→0は一様Taylor剰余で接続し、0/0を評価しない。

ρ,zの符号反転で偶性を確認し、一次補正を除去する。高階微分は内部コンパクト集合上でのみ必要。境界までのC4/C6を仮定しない。

## 5. Domain partition

B単独が成立すればB_003全域を一つの解析patchで覆う。

Cを採用する場合は、有理δ>0を証明済みMから決定し、[0,δ]と[δ,1/8]を採用。δ、λ分割、積分分割規則はFREEZE前にexact rationalで固定。今回のδはUNSET。診断値から事後に境界を調整しない。

境界r=δは両patchで覆う。r=0とλ両端を落とさない。必要ならu,vの多角形を扱うが、元r,τ箱とのexact包含証明を必須にする。

## 6. Rational enclosures

係数定義、πの包囲、R系列とtail、導関数の剰余式、正分母の下界、丸め規則を固定する。比較は厳密な下端>0で行う。丸められた正の小数、midpoint符号、samplingからの推定は不可。

M40/M22またはM60/M42/M24を使うなら、そのsupを覆う領域を定義し、明示的な有理上界を証明する。boundが粗い場合の次数増加・分割変更は新しい監査対象とする。

## 7. Producer structure

将来、独立したD4出力ディレクトリに限定して実装する。D5のrepo/worktree/run/ledgerには依存・アクセスしない。

入力：authority pins、数式version、領域、分割、精度、次数、予算。
出力：analytic lemma manifest、exact parameter/cell partition、各認証不等式のラベル、診断と正式証拠の分類、実行identity。

producerは有限の事前宣言された探索規則内でのみpartitionを作る。成功値はcheckerに信用させない。既存D5や旧smokeの結果を書き換えない。

## 8. Independent checker

producerのmoduleをimportしない。原始定義と監査済み表示から、別系統の区間実装で各評価を再計算する。exact rationalな被覆、重複許容、共有面、中心fiber、kernel同一性を独立に確認。

producerの近似値・margin・cell分類は参考情報。parser/schema違反、pin不一致、未被覆、非有限値、未証明tailはfail-closed。

独立性の範囲（実装・丸め・分割・数学的導出）を別々に開示し、同じ数式を使うことだけでclean-roomを称さない。

## 9. theorem-to-D-P2 handoff

将来のD4 handoff artifactには次を含める。

1. source SPEC V3、B_003 exact endpoints、採用座標とHの同一性。
2. 全解析補題と条件付き依存の一覧。
3. 閉箱を覆うpatchのexact union証明。
4. r>0でE_ρ=ρH>0となる排除の帰結。
5. r=0の連続延長と中心係数。軸上の停留点分類は別担当である旨。
6. r=1/8、τ=1/8、λ=119/200の共有面の重複被覆。
7. λ=33/50・r=0面のうちP′に残らない部分もD4が覆うこと。
8. 独立checker receiptと外部handoff監査結果。
9. P′、B_770、B_003のassemblyに必要な他担当のreceiptを未解消依存として列挙。

proof→box dischargeは別の監査対象。D5 ledgerからB_003を削除する操作は本契約に含めない。旧3,584箱一覧は歴史資料であり、現在claimの母集団ではない。

## 10. Success conditions

中心補題受理、必要な全パラメータの厳密正値性、全tail/剰余の検証、exact cover、独立checker、handoff audit、Judge裁定。いずれかを省略してCLOSEDとしない。

## 11. FAIL-CLOSED conditions

- 必須原典・実装pin・数学的量の同一性が未確認。
- 正下界が得られない、非有限、tail不成立、資源上限到達。
- 中心や共有面の欠落、λ端点の開区間扱い。
- 箱やmethodを結果に応じ無断変更。
- H≤0の厳密証明が得られた場合は一様H>0 routeを停止してJudgeへ。これは自動的な停留点反例ではない。
- 0を含む区間だけならINCONCLUSIVE。数値認証不能と数学的偽を混同しない。

## 12. Resource bound

現時点：UNSET。実行禁止の理由であり、省略可能な欄ではない。

FREEZE前にMAX_PARAMETER_BOXES、MAX_PARAMETER_DEPTH、MAX_INTEGRATION_CELLS、MAX_INTEGRATION_DEPTH、補助s積分上限、固定precision、series/Taylor次数、総work、メモリ、wall-clock上限、並列度、checkpoint/abort規則を確定する。

設計工数はBが数学HIGH・実装LOW〜MEDIUM、Cが数学MEDIUM〜HIGH・実装MEDIUM。run/checkerの実時間はUNVERIFIED。D5との計算資源調整は別のJudge工程であり、今回D5を調査・停止しない。

## 13. 10/31までの工程案（保証ではない）

| 期間 | 必要成果・gate |
|---|---|
| 10/13〜10/17 | source audit、中心補題のchat監査、剰余方式比較、handoff設計、METHOD_SELECTEDまたはMETHOD_UNDETERMINEDのJudge提出 |
| 10/18〜10/21 | 方法裁定後に明示定数・partition・resource boundを埋める。事前宣言監査→Judge FREEZE |
| 10/22〜10/25 | FREEZE後に実装→実装監査。未完なら実行へ進まない |
| 10/26〜10/29 | 別途許可と資源確保後、producer→独立checker。所要時間は未測定 |
| 10/30〜10/31 | handoff audit→Judge。未解消義務があれば未完を報告 |

現在この表を自動実行・予約していない。前段が閉じなければ後段は開始しない。

## 提出状態

**D-AN-2 / D4 — READ-ONLY / SOURCE AUDIT + D4-0 + METHOD DESIGN / CHAT AUDIT REQUESTED**
