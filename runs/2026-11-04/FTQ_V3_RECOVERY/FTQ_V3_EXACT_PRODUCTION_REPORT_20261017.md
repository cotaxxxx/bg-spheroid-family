# FT_q V3 exact production — μ16 / P-only

2026-10-17 JST / chat independent recomputation requested

**Verdict: FT_q SIGNED CERTIFICATE CANDIDATE V3**

本報告は Judge の2026-10-17 μ16実行契約による local production の結果。P1 normalization・幾何学的 joint constraints・boundary extension は監査済み architecture の条件として継承する。FT_q の DISCHARGED / CLOSED / CERTIFIED は宣言しない。

## Completeness

|項目|結果|
|---|---:|
|Physical boxes|2048|
|Mandatory branches / P LPs|4096|
|Complete certificates|4096|
|Incomplete|0|
|CHECK_ERROR|0|
|RESOURCE_LIMIT|0|
|Float seed, exact accepted|3913|
|Exact simplex fallback completed|183|
|Independent implementation checker|PASS|

## Exact result

Exact argmin parameter cell(s): `[[0, 0]]`.

厳密な表示用包囲：`295346256371/1000000000000 <= m0 < 295346256372/1000000000000`。

参考小数：`0.295346256371202`。小数を証明入力には使用していない。

m0 と16個の S_ia の reduced exact fractions は `result.json` と独立再構成された `checker_result.json` に全文保存している。両者は文字列化前の exact rational として一致確認した。

|Parameter cell (τ,λ)|参考小数（証明は exact fraction）|
|---|---:|
|(0, 0)|0.295346256371202|
|(0, 1)|0.305997959161509|
|(0, 2)|0.313687650614681|
|(0, 3)|0.319204894184659|
|(1, 0)|0.301123595004194|
|(1, 1)|0.311787930488218|
|(1, 2)|0.319437910740175|
|(1, 3)|0.324840666879289|
|(2, 0)|0.306085956586502|
|(2, 1)|0.316846324999853|
|(2, 2)|0.324604754979948|
|(2, 3)|0.32994568188004|
|(3, 0)|0.310127693950045|
|(3, 1)|0.321001316518424|
|(3, 2)|0.32885207396006|
|(3, 3)|0.334237790529795|

Canonical reduced fraction: `EXACT_M0.txt` (identical to `result.json` / `checker_result.json`).

## Certificate contract

Active variables: `(t,gamma,k,n)`。全枝に同じ8 joint constraints。Multiplier degree `(0,2,2,1)`、residual degree `(4,4,6,2)`。525 rows、144 multiplier variables、145 nonslack variables。

各 branch で `N_P - ell D_P = sum b_i beta_i + sum sigma_q Q_q`、全 multiplier/residual coefficients 非負、positive denominator、dual feasible、primal/dual objective equality を exact rational arithmetic で確認。Float LP は基底候補取得にのみ使用した。

証明書の保存形式は sparse multiplier / dual と exact residual reconstruction。省略項は exact zero。525残差係数は `b=n-ell*d-Ha` として再構成し、checker が全項の非負性を検証する。hash一致だけでは受理しない。

## Independent checker

Checker は frozen producer algebra / enclosure / joint-spec を import せず、別の区間実装、別の sparse polynomial 実装、affine substitution と power→Bernstein の別段階変換、独立 convolution により再構成した。全枝の cover / endpoints、root witnesses、constraints、coefficients、denominator、primal/dual、identity、aggregation を検査。

これは同一assistant・同一runtime内の別実装による検査であり、外部 chat による独立再計算を代替しない。

## Normalization and statistics

μ幅=1/8、t幅=1/4、folded arcsine masses=1/6,1/3。Paired contributions は `(ell+ + ell-)/192` と `/96`。τ,λ は積分せず、16 parameter sums の minimum を採用。

Certificate lower-bound signs: positive=2230, zero=0, negative=1866。これは物理 integrand の sign classification ではない。

Pivot statistics: `{'total': 130906, 'maximum': 7251}`。最大 solution rational bit-size: `8279`。

Ell0 / z / ell の全枝分布は `branch_distribution.jsonl.gz`。z は固定 certificate cone での gain。物理最小値との差ではない。

## Provenance

New μ16 partition SHA-256: `16988a142142bf9708fbf475e5ade8304a13f0dc6414879893635e1f06528455`。旧 partition hash を使用していない。

Astra original document SHA-256: `e6660d52caf482837961962d4df5bf53b335fa4d8529849a6303b142cfcec62b`。

Chat-received document SHA-256: `e6660d52caf482837961962d4df5bf53b335fa4d8529849a6303b142cfcec62b`。

|Frozen source|SHA-256|
|---|---|
|ftq_v3_joint_constraint_spec.py|`d17cd115ee1da13a1470cf5afb17414db158b0f1cf447847dbc27ec0054b153a`|
|ftq_v3_architecture_checks.py|`68c96f1c5c35bd4e7e8c541190a57cebc98d43d538dfc092d18d841996770c08`|
|ftq_algebra.py|`e24ff38dae62d7457aedc65ab46e528c8a737c5887e3ff037b098c4fdb6ed30b`|
|ftq_v2_fixed_enclosure.py|`c83709482525da48fe7fb28fdd15d5dd7f999909a51be855e808847d6f1f1b1f`|

Runtime versions: `{'highspy': '1.15.1', 'python-flint': '0.9.0', 'scipy': '1.17.0', 'numpy': '2.3.5'}`; Python `3.12.14`。

All artifact hashes: `SHA256SUMS.json`。Archive hash は外部表示値であり archive自身を内部hashに含めない。

## Execution continuity

セッション中断後、保存済み 2974 件を保持して再開した。4件の frozen source hash を再照合し、未保存の LP のみ同じ初期基底・同じ固定方針から再実行した。

再開環境で不足していた python-flint を前回と同じ0.9.0へ復元し、highspy 1.15.1を使用した。復元前の起動失敗は LP 実行前の dependency error であり、certificate CHECK_ERROR / RESOURCE_LIMIT には数えていない。詳細は `resume_1.json` と再開ログに保存。

## Governance

Partition・enclosure・constraints・degrees・solver policy に結果依存の変更はない。Optional B/W LP は実行していない。数値積分、sampled positivity、B⁺−B⁻、追加細分化は使用していない。Git commit/push は行っていない。D5 へアクセスしていない。

**FT_q: PARTIAL / whole-face m0: UNPROVED pending external chat and Judge / L3: FREEZE HOLD / L1: PAUSED / D-P2: NOT_CERTIFIED.**

次工程：chat independent recomputation → Judge。
