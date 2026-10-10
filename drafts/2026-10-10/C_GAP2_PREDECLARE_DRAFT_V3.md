C 空白② C1b 上側 strip — 事前宣言 DRAFT v3
基準：bg-spheroid-family main 32218d7855e3e6218dddbe315eacb38cd2dd8295、STATE.md v1.12。監査：CHAT_AUDIT_THREE_PREDECLARE_DRAFTS_V2_2026-10-10.md（SHA-256 43f3d811f62ad50de041e2a234c64f7bb9e9c1d9b2103a141c696f1d54ea10dd、原典照合済み）。
状態：DRAFT v3 / NOT FROZEN / EXECUTION PROHIBITED。 数値上限は設計案であり、成功実績ではない。原典未 pin、評価式未確定、誤差評価未完成の項目は FREEZE blocker。計算・インストール・commit は許可しない。
1. 集合と接続
封印済み accepted slab ledger に含まれる unclamped slab Λ について、t_+(Λ)<1、t_*(Λ)=max(31/32,t_+(Λ)) とし、U₂=⋃_{Λ unclamped} Λ×(t_*(Λ),1)。Λ は連続した λ 区間とは仮定しない。ledger の端点所有規則を使い、共有 λ 辺を必ず被覆する。λ=9/20,31/32<t<1 は②の責任。t=1 は B_ob 既存 receipt による照合辺（U₂ には含めない）。下端 t=t_* は既存 tube/exterior との接続辺で U₂ には含めない。clamped slab は ledger の t_plus=1 と B_ob 右壁の整合性のみを確認し、C1b を再証明しない。
2. 封印 ledger L0（v3：完全 SHA pin）
権威は bg-oblate-spheroid の analysis/GLOBAL_AXIAL_C1B_MACHINE_RECEIPT.md §1.1（blob bdcafce7）。封印ディレクトリの親の絶対パスは未確認であり、L0 最初の読み取り専用 ls で確定する。名前・SHA は L0 より前に次のように固定する。
オブジェクト	固定ファイル名／seal	SHA-256（全64桁）
producer ledger	phase1_v212s_seal_20260918T222551Z/ledger.jsonl	1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f
checker ledger	phase2_v212s_seal_20260920T140743Z/ledger.jsonl	09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38
replay plan	Phase 1 seal 内 checker_replay_exact.jsonl	c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69
抽出表	/home/daybreak/basepoint-geometry-artifacts/C1b/c1b_receipt_extract.json	8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b


L0 の順序は、(a) 研究用 PC で ls により seal の親パスを読み取り専用で同定、(b) 4ファイルの SHA-256 を全桁照合、(c) producer/checker ledger の slab ID、λ の閉開端点、accepted 159、clamped 35、t_plus、replay plan、抽出表を照合、(d) 固定仕様への適合性を報告する。親パスが見つからない、複数候補がある、SHA 不一致、schema 不一致はそれぞれ SEAL_PATH_OPEN／LEDGER_MISMATCH として停止する。ledger を読んだ結果を用いて方式・分割上限・符号条件を変更しない。
clamped slab は t_plus=1 の ledger 一貫性と B_ob 右壁を照合するだけであり、C1b の再証明ではない。
3. 固定証明方式
各 unclamped Λ について閉箱 Λ×[t_*,1] で g<0 を独立に認証する。右端は既存の B_ob<0 on [9/20,5/8] を照合する。未被覆の開 strip は閉箱証明から従う。t_* が厳密有理数でない場合は事前定義した有理外包と包含証明が必要であり、なければ停止。下端の閉箱評価が厳密負にならない場合は勝手に下端をずらさず CERTIFICATE_FAILED。
共通端点契約 E1（空白①②で同一）
g(t,λ) の t<1 における原典積分表示と、B_ob(λ)=g(1,λ) の端点表示を 異なるチャート として扱う。端点に接する閉箱 [t_e,1]×Λ では、(a) 内部表示から導く一様有界の差 g(t,λ)-B_ob(λ)、(b) B_ob の厳密上界、(c) t→1 の一様連続延長を合わせ、全箱で sup g<0 を示す。差の評価には |g(t,λ)-B_ob(λ)|≤C_Λ(1-t)^α（C_Λ 有理上界、α>0 固定有理数）という目標形式を用いるが、現段階でその成立は未証明。必要なら二チャートの原典積分核から別の明示評価式を v3 で確定する。C_Λ,α,t_e、支配関数、丸め誤差、積分と極限の交換を証明・pin するまで E1_FORMULA_OPEN。非有限な端点式をそのまま区間評価しない。実行中の端点法変更は禁止。
4. 数値契約（暫定）
λ は ledger slab のまま使用し、再編成しない。各 slab 内 λ 二分深度≤10、t 二分深度≤12、総セル≤1048576。符号不確定セルで λ→t を交互二分。厳密有理演算、超越包囲精度候補 256→512→1024 bits。E1 の二チャート明示式、近似次数、剰余誤差、端点評価の実装仕様は未完成：E1_FORMULA_OPEN／APPROX_DEGREE_OPEN。producer は全閉箱の厳密上界と ledger ID を出力し、独立 checker が ledger の両系統、被覆、符号、端点と①との接続を再計算。CPU 48 core-hours、RAM32 GiB、出力10 GiB。見積りは上限であり成功予測ではない。
資源・D5 排他契約
時間単位は CPU core-hours（1コアを1時間使用＝1 core-hour）。wall-clock は別に測定・記録する。現時点の上限は実行許可ではない。候補機は研究用 PC（12コア）だが、D5 は契約再裁定待ちであり優先順位は未裁定。D5 と本件の同時占有は禁止。順序は Judge が D5 の再裁定後に明示的に決定する。選択肢は「D5先行→本件」「本件先行→D5」「別マシンで完全分離」のみとし、無裁定なら SCHEDULING_HOLD。実行前にマシン ID、OS、利用コア数、メモリ上限、コア時間と wall-clock の換算見積り、停止・再開規則を pin する。
5. FAIL-CLOSED
SEAL_PATH_OPEN, LEDGER_MISMATCH, DOMAIN_MISMATCH, E1_FORMULA_OPEN, APPROX_DEGREE_OPEN, CERTIFICATE_FAILED, RESOURCE_CAP, SCHEDULING_HOLD, MATHEMATICAL_CONTRADICTION を区別。λ=9/20 と各共有端点を落とした場合は COVERAGE_FAILED。C1b 全体の再証明、軸外、全 census は対象外。
6. v3 固有の未解決・次工程
L0 の seal 親パス確認が未完了。共通 E1 の具体的評価式と厳密剰余、近似次数は E1_FORMULA_OPEN／APPROX_DEGREE_OPEN のまま。①との接続は λ=9/20 上の 31/32<t<1 を②が受け持ち、t=1 は既存 B_ob の照合辺とする。48 core-hours は CPU 上限案で実行許可ではない。