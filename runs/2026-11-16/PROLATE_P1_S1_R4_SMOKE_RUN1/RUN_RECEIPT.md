# 扁長 P1・Julia 第二系統 S1 R4｜研究用PC軽量実行証拠

2026-11-16 / Dig / **SMOKE_FAILED／NOT_CERTIFIED／I3_OPEN／NOT_FROZEN**

## 原本
- 一時チャットからの原本ZIP：`R1_V23_S1_R4.zip`
- サイズ：10,123 bytes
- SHA-256：`72de77a659db01d48fbcefcbf53c8d7f715a629aade0e21240c52ad3b5091155`
- ZIP内部6ファイルは原本のSHA-256に一致。再構成したZIP全体のバイト列も上のSHAと一致。
- 原本のコード・README・UNCERTAINTIES.mdは一切改変していない。

## 実行環境
- 端末：`daybreak-works` / 専用フォルダ：`/home/daybreak/D_PRO_P1_JULIA_SECONDLINEAGE_20261116/runs/S1_R4_SMOKE_20261116/R1_V23_S1_R4`
- Julia 1.10.13、IntervalArithmetic.jl 1.0.10。
- Project.toml SHA-256：`3b14e1942ba3d9c63b7be31f52934ce285cffbf8ce92f69d9327c1356933aee8`
- Manifest.toml SHA-256：`f1de48582bdef170b152b5a785490b3f176bc9c70fc0594e6589449c1d4d7350`
- `JULIA_DEPOT_PATH` は隔離depot、`JULIA_LOAD_PATH=@:@stdlib`、`JULIA_NUM_THREADS=1`、`JULIA_PKG_PRECOMPILE_AUTO=0`。
- すべて `--startup-file=no` を指定。timeoutガード（producer 360秒、checker 180秒）を付け、**自動再試行なし**。

## 実行コマンド

```bash
julia --startup-file=no --project=<専用env> producer.jl 47/10 47/10 s1_ledger.tsv 4 4
julia --startup-file=no --project=<専用env> checker.jl s1_ledger.tsv
```

## 実際の結果

| コマンド | exit | wall秒 | 最大RSS（kB） | stdout | stderr |
|---|---:|---:|---:|---:|---:|
| producer | 2 | 1.80 | 363632 | 0 bytes | 104 bytes |
| checker | 2 | 0.70 | 299248 | 0 bytes | 110 bytes |

**producer stderr（原文）**
```text
MethodError: reducing over an empty collection is not allowed; consider supplying `init` to the reducer
```

**checker stderr（原文）**
```text
SystemError: opening file "s1_ledger.tsv": そのようなファイルやディレクトリはありません
```

- `s1_ledger.tsv` は **未生成**。生成されていないファイルをZIPに捏造していない。
- `LEDGER_NOT_PRODUCED.txt` に未生成と依存エラーを記録。
- 生ログ `producer.stdout` / `producer.stderr` / `checker.stdout` / `checker.stderr`、exitコード、計時生データと `TIMING.json` を保存。
- **第一系統のQ(4.7)・その他の数値への比較は行っていない。第二系統の数値・比較値も実装者に返さない。**
- 計算した値・区間証明書はないため、I2数値追加照合もI3数学監査も開始しない。
- Judge FREEZEおよび認証本走は未実施。

## 次工程

一時チャットへは第一系統資料・監査数値を渡さず、**producerの上記エラーメッセージと、台帳不生成に伴うcheckerのエラーだけ**を返す。実装者は原本を維持して修正版を別SHAで封印し、Digが別フォルダで軽量動作検査を行う。

本証拠ブランチは **失敗した軽量検査の記録**であり、コード採用・認証のPASSとは無関係。
