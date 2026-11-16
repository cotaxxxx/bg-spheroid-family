# Julia第二系統｜環境導入・隔離レシート（2026-11-16）

**状態：INSTALLATION_PASS／ENVIRONMENT_ONLY／NOT_FROZEN／NO_NUMERICAL_EVIDENCE**

- 許可：Judge 2026-11-16「承認：Juliaで第二系統」。
- 研究用PC：`daybreak-works`、Linux x86_64（Ubuntu）。
- 独立ルート：`/home/daybreak/D_PRO_P1_JULIA_SECONDLINEAGE_20261116/`
- Python、python-flint、既存D-PRO実装から分離。PATHグローバル変更、apt導入、sudo、既存Python環境更新なし。
- Julia公式配布物：`julia-1.10.13-linux-x86_64.tar.gz`、
  `https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.13-linux-x86_64.tar.gz`、
  SHA-256 `f2bfa080db29b50a9bf250f69e9acdcfd8b7c49409dee5e55588f986706fb8bd`。
  Julia公式の `julia-1.10.13.sha256` と照合PASS。
- Juliaのバージョン：**1.10.13**（2026-11-01 LTS）。
- プロジェクト `env/Project.toml` SHA-256：
  `3b14e1942ba3d9c63b7be31f52934ce285cffbf8ce92f69d9327c1356933aee8`
- 依存ロック `env/Manifest.toml` SHA-256：
  `f1de48582bdef170b152b5a785490b3f176bc9c70fc0594e6589449c1d4d7350`
- IntervalArithmetic.jl：**1.0.10**、`pinned = true`、
  Julia package git-tree-sha1 `c3ee408ae340565f41699e3a3fa1053698c7626e`。
- `Project.toml` [compat]：Julia `=1.10.13`、
  IntervalArithmetic `=1.0.10`。
- Julia専用depot：`/home/daybreak/D_PRO_P1_JULIA_SECONDLINEAGE_20261116/depot`。
  Manifestの有効なインストール依存パッケージに
  `Arblib`, `ArbNumerics`, `FLINT`, `Libflint_jll` は存在しない。
  IntervalArithmeticにはweakdepとしてArblibの**名前だけ**があるが、インストール依存ではない。
- `using IntervalArithmetic`、Julia/IAの版assertion、区間 `[1,2]+[1,2]` の最小smoke：PASS。
- 本件ではQ,Q′,H₄,Q_zの数値計算、第一系統との比較、認証の較正、本走は**一切実行していない**。
- 物理RAMは約29GiB（2026-11-16の観測）。事前宣言v2の32GiB RSS候補は、FREEZE前に調整が必要。

## 実行環境の固定指定（将来の監査用）

```bash
ROOT=/home/daybreak/D_PRO_P1_JULIA_SECONDLINEAGE_20261116
export JULIA_DEPOT_PATH="$ROOT/depot"
export JULIA_LOAD_PATH="@:@stdlib"
export JULIA_NUM_THREADS=1
export JULIA_PKG_PRECOMPILE_AUTO=0
"$ROOT/toolchain/julia-1.10.13/bin/julia" \
  --startup-file=no --project="$ROOT/env" --version
```

**注意：** このコマンドは版表示だけを行う。数値認証実行の許可ではない。
実装者へ配る数学入力は`ORIGINAL_DEFINITIONS_INPUT_PACK_V1.md` **のみ**。
本レシートと統治資料は監査者側で管理する。

## 適用前の追加監査

この登録済みManifestから再現可能な環境か、IntervalArithmeticの丸め設定・
MPFR演算と、Julia区間基本関数の外向き包囲が成り立つかを
**chatが契約の一部として確認するまで証明に使用しない**。
公式checksumとの照合はしたが、バイナリのGPG署名は今回別途検証していない。
