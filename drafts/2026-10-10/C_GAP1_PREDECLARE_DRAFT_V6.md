C 空白① 事前宣言 DRAFT v6
基準：STATE.md v1.12 / bg-spheroid-family 32218d7855e3e6218dddbe315eacb38cd2dd8295。監査原典 SHA-256 c2e63b3ae2a247291c3e554c136683ac1d27df2b1243e86d8ec7f9dd82aca629。\n状態：DRAFT / NOT FROZEN / EXECUTION PROHIBITED。
1. 対象・主張
対象 U1: 1/2<t≤1, 2/5≤λ<9/20。λ_x の厳密符号入力は C1a receipt e494e789 の F_x(699/1600)<0, F_x(281/640)>0 の2点のみ。点推定は NON_GATING。λ≤λ_x で根0個、λ>λ_x で単純根1個という主張は G0/E1 および既存の外部監査待ち依存関係を条件とする。
2. 領域別の固定ゲート
L λ∈[2/5,699/1600]: 各閉 slab の [1/2,1] 上で g<0 を認証。単調性も根予測も要求しない。
X λ∈[699/1600,281/640]: 根予測・root target・P0/P1/P2 を適用しない。固定 [1/2,5/8] で ∂_t g<0、[5/8,1] で g<0 を認証。C1a の g(1/2,λ) の負・正・零に応じ、内部根0・1・0個。正の場合は連続性（端点補題 Lemma 3）、負の場合は単調性と右領域の負値、零の場合は t=1/2 が U1 に含まれないことによる。固定 tube を実行中に変更しない。
R λ∈[281/640,9/20]: g(1/2,λ)>0 を先に認証。右端 λ=9/20 から左向きに進む。最初の continuation 中心 t_cont=9/16、以降は右隣 slab の認証済み根包囲を引き継ぐ。P0 の進行方向だけ変更し、P1 の格子符号転換探索は c785ceda に従う。P2 は旧 |t_cont−t_scan|≤1/64 を使用禁止とし、v2.3 5326e2b5 と supersession v2.3.1 4a493191 の |continuation−scan_mid|≤ROOT_TARGET を唯一の選択規則とする。ROOT_TARGET = 1/128（確定）。v2.3 5326e2b5 46行目および producer kernel 34行目・checker kernel 35行目と一致。|continuation−scan_mid|≤1/128 なら continuation、厳密に超えれば relocated scan を採用する（等号は continuation）。scan_mid・continuation の具体的データ配線は実装差分監査の対象。旧規則が producer または checker に残れば FAIL-CLOSED。左 exterior g>0、tube ∂_t g<0、右 exterior g<0 を認証。半幅 W0=1/16、予測中心の受理距離 PRED_ACCEPT=1/64、選択閾値 ROOT_TARGET=1/128 は producer/checker 双方の kernel による確定値。
境界 λ=699/1600 と 281/640 は閉箱の重複照合を行う。λ=9/20 の U1 側は境界照合のみ、空白② v3 との責任分担を維持する。t=1 は統合 G0/E1 の端点評価を使用。
3. 実行済みコードを権威とする継承
C1b machine receipt §1.2（implementation head 85eca228）の7コード blobを継承仕様の基準とする。
系統	役割	implementation head 85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b の相対パス	Git blob ID（40桁）
producer	kernel	producer/global_axial_c1b_kernel.py	67dda838369302010ef3d589937b834b96ede4d8
producer	gating	producer/global_axial_c1b_gating.py	a93ca173ae0bededcd5a0248aa07ac3348f9a243
producer	producer	producer/global_axial_c1b_producer.py	0616fbd7c9c85f77c8e80b61a5b3b536b45012a8
producer	driver	analysis/c1b_resumable_driver.py	5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d
checker	kernel	checker/global_axial_c1b_kernel.py	4eaca55ddf79b437fc756d666294372e5d1a6ba4
checker	gating	checker/global_axial_c1b_gating.py	03df262012bfbebcf4d2ea173933186c70abafbf
checker	checker	checker/global_axial_c1b_checker.py	0760764ef7592be1ddd4ffec3966e9c6ec930a5b


27件の C1b 改訂文書は説明資料として blob 固定する。少なくとも P2 の拘束文書 5326e2b5 と 4a493191 を明示し、旧 c785ceda の P2 が失効したことを記録する。27文書の逐語的な再裁定は行わず、実行コード7本の path・full blob ID の receipt 照合（上表は研究 PC の Git オブジェクト解決により取得済み）、および v5 実装と7本の行単位・意味単位の差分監査を FREEZE 前に行う。許容される振る舞いの差分は (a) P0 の左向き進行、(b) X の固定 tube、(c) L の負値ゲート、(d) 統合 G0/E1 に基づく端点処理、(e) それらに必須の入力配線のみ。P2 の復旧は差分として許可しない。独立 checker にも同じ差分監査を行う。
4. 計算方式と停止
有理 slab と interval enclosure、厳密剰余評価、独立 checker を使用。近似次数・誤差配分・根包囲の計算規則は未確定。ROOT_TARGET とコード7本の Git blob ID は確定済み。これらを FREEZE 前に固定する。失敗・非有限値・上限到達・仕様不一致はそれぞれ CERTIFICATE_INCONCLUSIVE、NONFINITE、RESOURCE_CAP、CONTRACT_MISMATCH とし、数学的反例と混同しない。
96 CPU core-hours は上限案であり実行許可ではない。研究用 PC 12コアの D5 と同時実行しない。順序は Judge の再裁定待ち。計算、commit、push は禁止。
5. FREEZE 阻止条件
新実装と7本の実行コードの行単位・意味単位の差分監査、統合 G0/E1 の数学的証明・外部監査、近似次数と誤差上界、必要な B_ob 符号ゲート、既存 C1a 依存補題の外部監査が未完了。これらを未解決のまま FREEZE しない。旧 v3 全文の再掲はしない（監査連鎖を参照）。
6. v6 pin 監査の境界
7本の40桁 ID は研究用 PC の git rev-parse で解決し、実装 head のファイル一覧からパスを同定した。7本の実行済みファイルを「これから①に移植した」とは主張しない。新しい①の実装は未作成であり、差分監査は NOT_STARTED。v6 は契約文面の pin 更新のみである。