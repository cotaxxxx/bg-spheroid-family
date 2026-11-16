# DIAGNOSTIC_ONLY / NOT_EVIDENCE — 実行状況

この登録物は **実行未検証の実装草稿** であり、依頼された動作検査済み成果物の代わりにはなりません。

固定資料を取得し、前半の実装作業を進めた後、Codex の実行環境に接続できなくなりました。
再接続を試しましたが、`No usable execution environment is available` が返されました。
前の作業ディレクトリを回収できないため、固定 GitHub 資料と作業記録から、このソース一式を再構成しています。
この再構成版について Python 構文検査、import、Arb の実行、テスト、1箱試走は **いずれも未実行** です。
以前の版での環境構築や途中作業を、この版のテスト結果として扱っていません。

- `outputs/CODEX_TEST_STATUS.json`：未実行の理由。テスト出力ではありません。
- `outputs/CODEX_PILOT_STATUS.json`：未実行の理由。幅・時間の実測値はありません。
- `tests/run_tests.py`：実行した各検査について PASS/FAIL と、失敗時の traceback を出します。
- `run_diagnostics.py`：固定した1箱試走と全27箱の幅・時間を、Dig が実行するための道具です。
- `SHA256SUMS` と原本ZIPの SHA-256 は、Python 実行とは別の JavaScript 実行環境で計算しました。

実行に必要な依存は python-flint==0.8.0 だけです。検査結果が出るまで実用性・速度・幅は未確認です。
数学的包囲は ANALYSIS.md の導出を監査対象として提示します。API、微分係数、
球冠定数、中心剰余を含め、chat の独立監査は未了です。
不成立や資源上限に達した場合は例外で止まり、無限区間や成功表示で埋めません。

この制約を隠してテストを成功扱いにすることはしていません。
