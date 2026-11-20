# 再現手順と検査範囲

2026-11-20　DIAGNOSTIC_ONLY / NOT_EVIDENCE

1. ZIP を空のディレクトリに展開し、D_TRI_RECTANGLE_INTERVAL に移動する。`sha256sum --quiet -c MANIFEST.sha256` を実行する。
2. `./reproduce.sh --check` は Python 標準ライブラリのみで動く。全域・辺・組み合わせ図・移送・五点帯・明示帯の台帳の矩形分割、中心の符号、区間からの Krawczyk 再構成、精密交点、両右端点を再検査する。全ファイルの区間積分は次の手順で再計算する。
3. `JOBS=7 ./reproduce.sh` は一時ディレクトリへソースと必要入力だけをコピーする。コンパイラは GCC/G++ 14.2.0 (x86-64)。Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8。新規コンパイルして空の out/ から再生成し、22個の科学出力をバイト比較する。さらに独立な非区間検算 spot.csv と図も再生成・比較する。図のバイト比較には同じ Matplotlib・フォント環境を使う。コンパイラ・数値ライブラリの違いによるバイト差は、単独では数学的な矛盾を意味しない。
4. 計時を含む *_time.csv は初回走行の CPU 秒でありバイト比較から外す。任意の段階の出力が欠けている場合には終了コードが非零になる。日付や生成時刻で科学出力を選別する処理はない。

固定計画とコードはルートの各 .sha256 に記録した。`for f in *.sha256; do sha256sum --quiet -c "$f"; done` で展開後に照合できる。 `MANIFEST.sha256` は自己参照を含まない。ZIP 外側の SHA-256 は、ZIP、報告書、図、証明付録に対して独立に照合する。

## 台帳の読み方

- axis_cover、bfinish、central、topology の s0,s1,t0,t1 は分母5242880の整数分子。positive/negative は値域の片側符号、down は値が零になり得る箱の方向導関数が負という意味。topology の parent_* を使うと旧箱ごとの細分化が復元できる。
- cal の stage=0 は元の形状箱、1 は中央の微小箱、2 は選択した未決定箱の再評価。mode=1 は勾配比、2 はせん断比、3 は H33。整数位置は列 q10 から q31 まで。
- central は h_i の最終台帳。nodes、polycoef、poly_errors は構成要素。cross と endpoints は形の分母1000000。cross_refined は列 denominator を使う。
- disk は tau2 が半径二階、tau が値。hb は mode=0 が四階、1 が規格化した傾き。substrip は同じ2モードの主量と副量に応じて判定を記録する。bridge は四階への切替半径を広げた補充台帳。
- transfer は inputs/v50 の原本行 path を参照し、共通分母が2^20の形・半径箱ごとに edge_margin − error = remaining を有理数で記録する。これが主報告の全明示帯の軸上根数を支える。旧ZIP全体の出所は証明付録 B4 に記した。
- `PROOF_NUMERICS.md` は単体平均・境界端点・形パラメータの微分、角度および形の解析剰余の設計、閉球への移送の証明をまとめた。V55 の図用データは既存 ZIP（SHA-256 259f721216b2c0b4348f1ccd3351f06b4500ff98903767875798ff778d85b89f）の out/sections.csv と out/special.csv を使用する。

長軸の追加検査を含む最終版の入口は同じ `./reproduce.sh`。中核の22出力・別実装31点・図の後で、第2の空ディレクトリで長軸用 C++ をビルドし `long_end.csv`、`long_axis.csv` を全行再計算する。`--check` でもこれらの形状・半径被覆と証明付録 C の有理定数を調べる。全域で決まる長軸の外側と、内側の未決定行を併せて保存した。Matplotlib は図の再生成だけに使われる。
