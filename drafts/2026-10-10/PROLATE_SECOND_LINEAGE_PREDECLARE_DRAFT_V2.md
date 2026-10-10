扁長局所 a_c — 第二系統検証 事前宣言 DRAFT v2
基準：bg-spheroid-family main 32218d7855e3e6218dddbe315eacb38cd2dd8295、STATE.md v1.12。監査：CHAT_AUDIT_THREE_PREDECLARE_DRAFTS_V1_2026-10-10.md（ユーザー訂正 SHA-256 66f2461d…aa4b。全桁の照合は未完了）。
状態：DRAFT v2 / NOT FROZEN / EXECUTION PROHIBITED。 数値上限は設計案であり、成功実績ではない。原典未 pin、評価式未確定、誤差評価未完成の項目は FREEZE blocker。計算・インストール・commit は許可しない。
1. 証拠 pin と独立性の対象
第一系統の比較対象は basepoint-geometry main abf704b8701f3da8eb41d8a99408570a413b2214、CERTIFICATES/prolate/local_bifurcation/、manifest SHA-256 3b6fc57de63c6154165bb22ea96905cc669e8be89680175aadb0b36a9f05c11d（12 objects）。旧 68bc9828 は superseded。原稿 R3 は branch paper1-certchain-202609、commit 7cc5726d62f063803b6d83cb9ba5fda5fd91f72c、01_KAKURON_I/1_楕円体系列/1-2_長球/submission_experimental_mathematics/manuscript.tex、SHA-256 4b30c2b2ed4dbbc6eb9439c74eb0d30ef95187df8ff70c9c9820bf886c74a257。
重要：R3 原稿全体は clean-room 入力として渡さない。 R3 に含まれる h の微分連鎖、₀F₁ の微分公式、Q・H₄・Q_z の被積分関数は第一系統の導出を含むため、これらを第二系統に転記しない。
2. Clean-room 入力と関門
担当案：Code が新規 Julia 実装、Astra が先行数式監査、chat が統治監査。第一系統の repo clone・コード・JSON・原稿全文を sandbox に置かない。入力 pack は原始的定義（楕円体、測度、角度汎関数、パラメータ規約、定義域、導関数が表す幾何学的量）だけを抽出し、SHA-256 と項目一覧を固定する。第一系統で導いた積分核・特殊関数微分公式・Q/H4/Qz の展開式は除外。pack の具体的 bytes/SHA は INPUT_PACK_OPEN として FREEZE blocker。
Gate I0：Astra が pack の原典との整合性と、派生式の混入がないことを監査。Gate I1：Code が pack だけから Q、Q′、H₄、Q_z を独立導出し、微分交換・端点正則性を証明。Gate I2（比較前必須）：Astra が第二系統の導出式と R3 の記載式を、第一系統の数値出力を見せずに記号的に照合し、導出差・同値変形・前提を記録する。I2 が PASS するまで数値結果を比較しない。Gate I3：独立の検証付き求積仕様を CHAT AUDIT。Gate I4：別途 Judge FREEZE／実行許可。各関門の attestation に署名者、pack SHA、アクセス可能なパス一覧、式の SHA を含める。単なる既存コードの他言語移植は禁止。
3. 算術ライブラリと共有の境界
第二系統候補：Julia + IntervalArithmetic.jl（version、Manifest.toml、丸め mode、精度 pin 必須）。Arb/FLINT/python-flint/Sage RBF を算術 core として使わない。 GMP/MPFR の共有は許容する（高精度整数・浮動小数の基盤であり、第一系統の Arb/FLINT 区間演算・積分実装の共有とは区別する）。Julia の依存関係が Arb/FLINT を使用していないことを環境 manifest と実行時検査で示す。Julia の導入はJudge の別承認があるまで禁止。
4. Judge の段階制ゲート
Tier A（必須）：A1 Q_z(a)≥q₂=1/100>0 for all a∈[47/10,19/4]（設計閾値・未認証）。A2 Q(4.72438)>0, Q(4.72439)<0、よって 4.72438<a_c<4.72439。A3 Q′(a)<0 全域。A4 H₄(a)<0 全域。A5 Q(4.7)>0, Q(4.75)<0 を独立 enclosure として保存。
Tier B（追加、個別判定）：B1 4.72438340452113340672<a_c<4.72438340452113340673。B2 Q_z(a)≥0.0885587746621582 全域。Tier B の EXTRA_INCONCLUSIVE は Tier A PASS を取り消さない。真の反対符号が厳密に得られた場合は Tier を問わず MATHEMATICAL_CONTRADICTION とし両系統の監査へ戻す。Paper I には両系統で PASS した数値だけを採用する。
5. 検証付き積分の未完成契約
積分区間 [0,π/2]、パラメータ [47/10,19/4]。積分変数の端点を含む区間分割と、各セルの Taylor あるいは高次求積の厳密剰余を証明し、導関数の有界包囲、π の有理外包、パラメータ微分交換、区間演算の外向き丸めを独立 checker が検証する。求積次数、分割規則、誤差予算の gate 別割当、微分の支配関数、端点特異性の処理は QUADRATURE_CONTRACT_INCOMPLETE で FREEZE blocker。特に B1 は約 10^-22 の絶対誤差を目指す必要があり、工数見積りにその開発・監査時間を含める。
候補精度 256→512→1024 bits、最大2048 bits、パラメータ二分深度≤16、積分セル≤262144、総箱≤1048576。CPU Tier A 120 core-hours、Tier B 追加 240 core-hours、RAM32 GiB、出力20 GiB。合計 360 core-hours。数値上限は予測ではなく予算案。求積法の実装・別 checker・Astra 監査の開発工数は別途人時として見積り、CPU時間に混ぜない。
資源・D5 排他契約
時間単位は CPU core-hours（1コアを1時間使用＝1 core-hour）。wall-clock は別に測定・記録する。現時点の上限は実行許可ではない。候補機は研究用 PC（12コア）だが、D5 は契約再裁定待ちであり優先順位は未裁定。D5 と本件の同時占有は禁止。順序は Judge が D5 の再裁定後に明示的に決定する。選択肢は「D5先行→本件」「本件先行→D5」「別マシンで完全分離」のみとし、無裁定なら SCHEDULING_HOLD。実行前にマシン ID、OS、利用コア数、メモリ上限、コア時間と wall-clock の換算見積り、停止・再開規則を pin する。
6. FAIL-CLOSED
INPUT_PACK_OPEN, INDEPENDENCE_FAILED, SOURCE_MISMATCH, QUADRATURE_CONTRACT_INCOMPLETE, CERTIFICATE_FAILED, RESOURCE_CAP, SCHEDULING_HOLD, MATHEMATICAL_CONTRADICTION を区別。Tier A 不成立は REQUIRED_INCONCLUSIVE、Tier B だけ不成立は EXTRA_INCONCLUSIVE。本件の成功だけで pin 昇格や原稿 CERTIFIED を宣言しない。