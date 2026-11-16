# D-PRO R1 共回転の区間積分核
**DIAGNOSTIC_ONLY / NOT_EVIDENCE — 実行未検証の実装草稿**

登録先：cotaxxxx/bg-spheroid-family の
`codex/d-pro-r1-corotation-20261117`。
成果物は `prolate_r1/` のみ。
この版は Codex 実行環境の障害により、テストと1箱試走を実行できていません。
VALIDATION.md と outputs の未実行記録を必ず先に読んでください。
動作確認済み・監査済みの積分核という扱いにはできません。

## API
```python
from flint import fmpq as Q
from prolate_r1 import angular_raw, angular_quotient, axis_g, equatorial_phi_s
raw = angular_raw(Q(1,2), Q(1,2), Q(3), angle_kind="tau")
w = angular_quotient((Q(15,16), Q(1)), Q(1), Q(3), angle_kind="tau")
g = axis_g(Q(1,2), Q(3))
phi = equatorial_phi_s(Q(1,4), Q(3))
print(raw.balls)        # (E, E_beta, E_beta_beta), derivatives w.r.t. beta
print(w.enclosure)     # W = lambda^2 V - H
```

幾何入力は fmpq の点または fmpq 端点対だけ。
デフォルト angle_kind="beta" は有理数のラジアンを受け取ります。
極 beta=pi/2 を正確に指定するときは angle_kind="tau", tau=1 を使います。
tau 入力でも raw の微分は beta 微分です。
lambda=1 は球の対照、通常は lambda∈[2,5]。
R,s∈[0,1]、axis_g は t∈[0,1)。
物理的な軸座標は z=lambda*t です。
全幅、端点は浮動小数の表示値ではなく有理数で出力します。

Result は balls、中心点積分 point_balls、外側補正 correction、
球冠 cap_errors、cells、route を保持します。
チャートを分割した場合、point_balls は子中心の区間の合併です。
幅比較の道具は箱の全体の中心を別途評価するので、この合併を点幅と取り違えません。

## Dig の動作検査用1行
リポジトリのルートで実行してください。出力は新しい dig_* ファイルに書きます。
```sh
python -m pip install -r prolate_r1/requirements.txt && python -m prolate_r1.verify_manifest && python -m prolate_r1.tests.run_tests --full && python -m prolate_r1.run_diagnostics --pilot --fixed27
```

小さな確認だけなら次です。
```sh
python -m prolate_r1.tests.run_tests && python -m prolate_r1.run_diagnostics --pilot
```

full 検査は9内点、9境界箱、3箱×20点等を含むため、小試走とは別です。
同梱した PLAN_BEFORE_DIG_RUN.md の条件を出力を見る前に確認してください。
上限到達や例外は停止として出し、成功扱いにはしません。
この版について所要時間の実測値はありません。

## 構成と範囲
- api.py：四つのAPI、平均値形式、角度と中心の除算処理。
- density.py：設計の (3)-(8),(17),(20) の exact 密度。
- jets.py：Arb の mixed Taylor 係数と符号付き級数剰余。
- quadrature.py：接触距離で決まるセルと2/4/6次の逐次 Taylor 求積。
- tests/：自動 PASS/FAIL の診断。有限差分検査は数学的証明ではありません。
- run_diagnostics.py：1箱と固定27箱の幅・点幅・倍率・時間。符号を判定しません。
- ANALYSIS.md：包囲の根拠・微分次数・上界・未解決点。
- SOURCES.md：固定入力と再利用の来歴。
- SHA256SUMS：ZIP自身を除くソース等のハッシュ。
- artifacts/D_PRO_R1_COROTATION_20261117.zip：このソース原本。
- artifacts/D_PRO_R1_COROTATION_20261117.zip.sha256：原本のハッシュ。

ZIPは prolate_r1/ 以下のソース・文書・未実行記録と SHA256SUMS を含みます。
ZIPとZIP用ハッシュは自己参照を避けるためZIPの中に含みません。
SHA256SUMS も自分自身と artifacts/ を対象外にします。
登録後に Dig の出力が加わっても、元のソースの照合はこの台帳で行えます。

平均値補正は一般に箱幅の一次です。「必ず二次に小さくなる」とはしていません。
中心・端点の包囲幅が十分に狭いかは未測定です。
本実装が存在することは、条件 A・Z・C の符号を示すものではありません。
