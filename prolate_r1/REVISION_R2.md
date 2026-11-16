# D-PRO R1 修正版 R2 — 2026-11-17
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## 入力と版の分離
R1原本：cotaxxxx/bg-spheroid-family、commit
`4b7f1f73421f2765d347e4d2ffc9ab004393695c`。
原本ZIP SHA-256:
`4810f975b31d2da43903f66e28545c2f62db0f63917948738567bc1be6565664`。

Dig動作検査：commit `1917e1ab3c22191852385cf8cd3df5f6d9958fb8`、
`runs/2026-11-17/D_PRO_R1_COROTATION_DIG_RUN1/RUN_RECEIPT.md`。
quick 2/2、box13 pilot成功、axis_g(1/2,3)失敗、
fullは480.13秒の外部タイムアウトで6件のPASS表示まで。23件完了ではない。

R2はこの証拠commitを親とする新規ブランチに登録する。
R1のZIP、そのハッシュ、既存ブランチ、Digの実行証拠は変更しない。
新版ZIPの名前は D_PRO_R1_COROTATION_R2_20261117.zip とする。

## 1. 正の分母を保った逆数
旧軸核は `term / w / D**3` を評価した。
Arbの中心・半径による積は、真の D>0 であっても D³ の包囲に0を含め得る。
この包囲を反転すると非有限になる。

幾何から D²>=ds>0、D<=lambda上端*(1+max|t|)。
ds=(1-t*)²+2t*q下界を、既存の距離下界関数で求める。
正の有理数 d下界を Arb(sqrt(ds)).lower() から取り、
Dの値係数と [d下界,d上界] を有理端点で交差する。

交差端点を l,u とすれば、逆数の定数係数は
[1/u,1/l] を外向きに丸めた ball である。
多重Taylor係数 a_alpha に対する逆数係数 b_alpha は
b_0=1/a_0、
b_alpha=-b_0 Σ_(0<nu<=alpha) a_nu b_(alpha-nu)。
厳密な係数恒等式を区間演算で帰納評価する。
上・下界は値だけに適用し、これらの定数を微分する操作はしない。

`Jet.reciprocal_positive(lower,upper)` を追加し、
invD、invwを先に作り、軸核の分数項は
`term * invw * invD * invD * invD` とした。
D³、wD³、逆数の積のいずれも、積を作ったあとに反転しない。
正の下界がない、交差が空、入力・出力係数が非有限なら明示的に停止する。
lambda>=1より 1<=w<=lambda上端 を利用する。
新たな積分点や結果依存の細分は加えていない。


問題セルの独立した有理検算：y∈[3/4,7/8] なら
mu∈[-17/32,-1/8]。
t=1/2, lambda=3 で D²=8mu²-9mu+13/4 となり、
その微分16mu-9<0から D²∈[9/2,1317/128]。
したがって真のDの正値性に疑いはなく、対処対象は包囲の反転順序である。

これは真の積分核・導関数を変更せず、包囲の評価順序と値域の利用を変更する修正である。
独立数学監査と新版のArb実行結果は未了。

## 2. full検査の逐次保存と再開
元の full 23ケースの名前、順序、標本、精度、次数、格子、差分刻み、判定式を保持。
run_tests.py のテスト関数と _quick_axis の本文はR1とバイト単位で同一。
case_list()への列挙移動と main()の実行管理だけを変更した。
R2の回帰検査は test_revision_r2.py に分離する。

出力 foo.json に対し、foo.json.cases/ に以下を保存する。

- plan.json：ソースSHA、Python/python-flint版、精度、環境変数、固定ケース一覧。
- 各ケースの各試行の started.json：実行前に保存。
- result.json：完了・失敗・中断を保存。失敗時は完全なPython tracebackを含む。
- stdout.log、stderr.log：試行ごとに別ファイル。
- foo.json：実行開始時と各ケース開始・終了時に、全体の状態を更新。

JSONは同じディレクトリの一時ファイルへ書き、flush、fsync、os.replace、
POSIXのディレクトリfsyncを行う。
完了したcaseのresultを先に保存し、次に全体snapshotを更新する。
snapshotの更新途中に停止しても、resumeはcase記録から全体を再構成する。
OSロックで同じ出力への同時実行を拒否する。強制終了時にロックはOSが解放する。

--resumeはソース・環境・固定ケースの一致を要求する。
PASSとFAILの完了記録を保持し、未完了・中断ケースをそのケースの最初から再実行する。
失敗を再試行する場合だけ --retry-failed を明示する。前の失敗記録は残る。
元のR1 stdoutの6行を、新版の成功記録へ自動転記しない。

SIGINT/SIGTERMをPythonが処理できた場合は、中断時のスタックとINTERRUPTEDを保存。
SIGKILL、電源断、Pythonが信号を処理する前の強制終了では、スタックの取得を保証できない。
その場合はstartedだけの記録を次のresumeでINTERRUPTEDとして保存し直す。
取得できなかったtracebackを作らない。
ケース内部の積分セル単位の再開は今回の範囲外。

終了コード：
0=全固定ケース完了かつ全件PASS、1=全件完了だがFAILあり、
2=選択ケース・max-cases等による未完了、130=SIGINT、143=SIGTERM。
実行前のI/O・識別情報エラー等は別の非ゼロ終了になり得る。
未完了の終了コード2をテスト失敗や全件成功へ読み替えない。

## 3. 変更しないものと残る確認
四つのAPIの契約、角度・中心・球冠処理、平均値形式、
求積次数、固定27箱、fullの数値的判定式を保持。
full総実行時間を短縮したという主張はしない。
--max-casesと--caseは同じ固定検査を分けて実行するための指定である。
一つのケースが外部タイムアウトより長ければ、そのケースには十分な実行時間が必要。

Codexの実行環境は今回も利用できず、新版のPython/Arb動作と回帰検査は未実行。
R1で確認済みの結果をR2の結果として報告しない。
Digは新版のハッシュ照合、R2回帰検査、quick、分割したfullを行う。
条件 A・Z・C の数学的認証や大域符号の判定は行わない。
