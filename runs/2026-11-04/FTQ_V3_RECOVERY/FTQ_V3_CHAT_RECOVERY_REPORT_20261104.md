# FT_q V3 — 過去のチャット・成果物回収報告

基準日：2026-11-04 JST。対象：2026-10-16〜17のFT_q V3 exact production（μ16、P-only、4096枝）。
本資料は回収とファイル整合性の監査であり、証明書の数式を独立再検算した報告ではない。Judge裁定／STATEを自己変更しない。

## 所在
- 2026-10-16 23:32 UTC 頃の過去チャットで生成した `FTQ_V3_EXACT_PRODUCTION_AUDIT_BUNDLE_20261017.zip` は、現在ChatGPTのLibraryで回収可能。
- 原ファイルの保存版は70,026,521 bytes、SHA-256 `a633c6009938ca89a5c0280c41a4ba302964a56dc40ab3184f8d3f0515bb7527`。通常ZIPの中央ディレクトリが存在せず、完結していない。L3報告が記載する当時の「既存V3 audit bundle」のSHA-256 `abd1202ca69e815eddc83919cee3797d67875a3020635735dc312818eca60f93` と一致しないため、当時の完全版そのものの回収ではない。
- Libraryの `L3_V0_2_AUDIT_BUNDLE_20261017.zip` に `sources/SHA256SUMS.json`（8220件、SHA-256 `5c2c2d9af95dd89b4865007606b770a48c7a9a5f21bbe0b84e165d93b57d120e`）と `sources/partition_manifest.json`（SHA-256 `16988a142142bf9708fbf475e5ade8304a13f0dc6414879893635e1f06528455`）が残存。

## バイト単位の回収結果
- 元の不完全ZIPのローカルファイルヘッダー7803件を解析。ファイル内容はすべて正常に伸長でき、CRC32検査が7803/7803一致。
- L3別ZIPの正典SHA台帳（8220件）に対して、回収済み7803ファイルのSHA-256は7803/7803一致（不一致0件）。
- 4096枝の証明書 `ftq_v3_production/certificates/0000.json.gz`〜`4095.json.gz` が全件存在。4096ファイルすべてgzip伸長・JSON parse成功。
- checkerの個別出力 `ftq_v3_production/checked/0000.json`〜`3697.json` は3698件存在。残り3698〜4095の398件は欠落。
- 元ZIPに含まれない別の19 productionファイルには `producer.py`, `checker.py`, `checker_math.py`, `checker_stream.py`, `result.json`, `checker_result.json`, `partition_manifest.json` とログ、manifest等が含まれる。そのうち `partition_manifest.json` はL3別ZIPから原本SHA一致で回収できた。`SHA256SUMS.json` も別ZIPにある。

## 主要な同一性確認
- V3 architecture原本文書：`e6660d52caf482837961962d4df5bf53b335fa4d8529849a6303b142cfcec62b`（MATCH）。
- 実行報告書：`6b9e51e5a13d7dcef09fa04c96b0510bd22e552fa477903e32bd5058cb282d6d`（MATCH）。
- exact m₀：`207b9617d61645e2c89f125debac2e40576f11f790feb09f81471564a1fd7d17`（MATCH）。
- partition manifest：`16988a142142bf9708fbf475e5ade8304a13f0dc6414879893635e1f06528455`（MATCH）。
- 7803件のファイルのハッシュが正典台帳と一致することは、出所と同一性について強い証拠になる。一方、4096枝の数学的証明書の検証を自動的に意味しない。

## 正常に開ける修復版
- `FTQ_V3_RECOVERED_PARTIAL_BUNDLE_20261104.zip` — 中央ディレクトリを新規生成した回収版。7803件。元ZIP内のメンバーを改変せず、元ZIPの末尾にZIP索引を追加したもの。
- 修復版SHA-256：`f36e020d3819ca3ffaca0f82cc1b9760f2229612ddab01220bae7520ab48a102`。
- この修復版は当時の正典ZIPではない。証明書の保存と新たな独立監査のための `RECOVERED / PARTIAL` artifactである。

## 判定
FT_q V3: PARTIAL EVIDENCE RECOVERY（4096 certificates FILE INTEGRITY PASS）。全productionソース、checkerの全出力、result/checker_result、chat独立再計算の結果原本は未回収。数学的証明書検証はOPEN。Judgeが正式に証拠連鎖を再裁定するまでは、STATEのNOT_EVIDENCE等を自動的に変更しない。V4再認証と並行して、この復旧したV3に独立checkerを適用する価値がある。
