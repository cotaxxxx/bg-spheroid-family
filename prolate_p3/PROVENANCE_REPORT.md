# Item 0c 元 ZIP の来歴調査

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## 結果と範囲

指定リポジトリ `cotaxxxx/basepoint-geometry` の取得時点の 87 ブランチ
（83 個の異なる先端 commit）、17 タグ、リリース一覧、および既定ブランチの
`CERTIFICATES/prolate/item0c_center` の変更履歴を調べた。
**この検索範囲では、0c の元証拠 ZIP は見つからなかった。**
元 ZIP の SHA-256 を推定・再構成していない。

全先端について recursive Git tree を取得し、全て `truncated=false` を確認。
ZIP・圧縮アーカイブ候補と 0c のパスを調べた。
リリース一覧は `[]`（0 件）。タグは GET `git/matching-refs/tags/` で取得。
ページ長 100 に対しブランチは 87、リリースは 0 であり、次ページはない。

## 0c README と履歴

`CERTIFICATES/prolate/item0c_center/README.md` は Git blob
`e1304d7186e295c216c3e5e3a9db80fe663a08a9`。
元の機械パッケージは先行走行で作られたが、0d を入庫した時点には
バイナリ添付がなく、元の ZIP・manifest を再構成せずコピーする必要がある、と記す。
同文書が指す “Prolate item 0 — 0c/0d Arb certificate package, Stage 2” は
今回指定された branch/release 調査の外にある資料への手掛かりであり、取得した原本とは扱わない。

既定ブランチの当該パス履歴は 1 commit：
`e11e30948fafdbb899b403c4cb4198c1a2628adc`。
その tree も確認した。ZIP 本体の追加は見つからない。
この README に記載された採用状態を今回再検収したという意味ではない。

## 見つかった ZIP の実体確認

先端とタグの ZIP 候補の異なる Git blob は次の 3 個。
いずれも取得し、実バイトの SHA-256 と ZIP メンバー一覧を確認した。
0c の元証拠は含まれていない。

| パス | SHA-256 | 内容 |
|---|---|---|
| `01_KAKURON_I/1_楕円体系列/1-1_球体/Kakuron_I_1_1_Sphere_Source_and_PDF.zip` | `6fcd9d4ead4ee56605ebf93f24ec1c716355be6a7b73ff3139cc0ecc5e530fdb` | 球の PDF・TeX |
| `CERTIFICATES/prolate/item0d_interior/item0d_certified.zip` | `db1c68e4bbf43fcb49bd5f27de5d45a36b44f1f8e77141477832ce16ae68df2a` | 0d の JSON と runner 8 ファイル |
| `CERTIFICATES/prolate/item2_circle/b_tube_v2_1/dependencies/blocal-stage1-boundary-entry.zip` | `ab7112ae7ae570555d1add5c48adb72100562c71aff6b74c94883f58da0f495b` | Item 2 境界入口の 9 ファイル |

Git blob と SHA-256 は別物。メンバー一覧は `outputs/PROVENANCE_ARCHIVES.json`、
全 branch/tag の tree 要約は `outputs/PROVENANCE_SEARCH.json`。

さらに `.b64`・`base64`・ZIP 部品・Stage 2 に関するパスも検索した。
`item0d_certified.zip.parts/` の 10 個の Base64 部品と README が見つかる。
その README（blob `113ff2de622ea5fc9748238cf568753e5b89c10b`）を読み、
復元対象の SHA-256 が上表の 0d ZIP と同じであることを確認した。
0c の部品という記載はない。今回は元 ZIP 本体を取得できているため、
この部品列を再復元して独立照合したとは主張しない。
パスの追加調査記録は `outputs/PROVENANCE_ENCODED_PATHS.json`。

ZIP 以外には、`tools/d_ob_p2/loss_decomposition/runs/LD_v1_20261006/`
下の `B_14_13_0`, `B_9_14_10`, `N_12_15_0`, `P003_r022`, `P003_r030`
の各 `cells.tsv.gz`（扁平 D-OB の台帳）がある。これら 5 個はパスと
Git blob の所在を記録したが、0c ZIP の候補とは扱わず、バイト内容は取得していない。

## 探索した場所の一覧

| Ref | 固定した commit |
|---|---|
| `refs/heads/Basepoint-Geometry` | `190d6dad45979a2b52e7e129598918e7d3104b40` |
| `refs/heads/agent/add-4-minus-pi-research` | `050666ff18e43dc12b03ca6f986965e35ff0fd67` |
| `refs/heads/agent/add-prolate-item0d-certificate` | `7cfb9e9a83b9a41e5ea4070b573c9c986a7215e8` |
| `refs/heads/agent/archive-prolate-item0b` | `81756fa62bb0bd8cac17f75b9c96f0b317c99060` |
| `refs/heads/agent/b-tube-v2-1-selftest` | `0088fb7fd9020cc437f218695864d3b3c031407e` |
| `refs/heads/agent/b-tube-v2-1-selftest-probe` | `67f816f595360e92221e67c2d1d34d45e522a526` |
| `refs/heads/agent/basepoint-geometry-terminology-v2` | `09aa60ac940b93093c3309d553e130c29e755d0d` |
| `refs/heads/agent/basepoint-geometry-terminology-v3` | `e6f1f68a572e143d1720088175a17ede2780027e` |
| `refs/heads/agent/bkernel-internal-nonfinite-diagnostic` | `9f300be11c7d437afe96e3a4bbbc23dce6c7760a` |
| `refs/heads/agent/bkernel-nan-frontier-diagnostic` | `e74d90ff02499dc0dd2b146f6b0cf6ae838b30a0` |
| `refs/heads/agent/bkernel-nan-frontier-main-diagnostic` | `ce6a5924cfd43bc27a5645dfd4141847f27581d1` |
| `refs/heads/agent/blocal-bentry-v2-1-design` | `aa7c5d9a44639645900ddc2d1152da574b89ef9b` |
| `refs/heads/agent/blocal-bentry-v2-1-design-audited` | `7e16c82132ed273ade7b667e3cbb6edbb18d849b` |
| `refs/heads/agent/blocal-bentry-v2-1-phase3-implementation` | `6d48ffb9a9fefdc34900cb7a5147f929b05fdb5a` |
| `refs/heads/agent/blocal-bentry-v2-1-selftest` | `b377b42e87b0206a25d33c86d3cf8fed1348cba5` |
| `refs/heads/agent/blocal-bentry-v2-1-selftest-audited` | `b377b42e87b0206a25d33c86d3cf8fed1348cba5` |
| `refs/heads/agent/blocal-phase3-ma-fix-build` | `449775bdad41e51ca9b36338df29858a6588b289` |
| `refs/heads/agent/blocal-phase3-mb-archive-build` | `88bc18f1ddcd37f4d40ea04d004fe81eb1317f83` |
| `refs/heads/agent/blocal-phase4-clean-rebuild` | `f21704b2cbd2954acb492ec2a58dbb0765773f1f` |
| `refs/heads/agent/blocal-v22-l3-bprime-design` | `a8997d11850dbd5b63e3064560a1c311e5c9c267` |
| `refs/heads/agent/blocal-v22-method-selection-taylor2` | `1b6d61eae275590efc5538fadaa94766b583ab74` |
| `refs/heads/agent/blocal-v22-readiness-design-reset` | `039ce0392c3bcb3499570f6df412583935ea15a4` |
| `refs/heads/agent/blocal-v22-readiness-draft` | `e388f30ced20704396ca308186303dae6c0f6e97` |
| `refs/heads/agent/blocal-v22-timeout-recovery` | `597ac12ca0e0c0becf50fb13ec6f148eeb97f363` |
| `refs/heads/agent/btube-v2-1-adaptive-tube-design` | `e6502072d52f4ea414465d3d96656fbc3609651d` |
| `refs/heads/agent/btube-v2-1-calibration-build` | `238e356d37a9720785c07815275796571b734f90` |
| `refs/heads/agent/btube-v2-1-calibration-design` | `b38afd9a40909d09528a3d83eeb00d62d7405597` |
| `refs/heads/agent/btube-v2-1-calibration-implementation` | `22c7553374bc2f1b989fa8f84c4278bc461eee18` |
| `refs/heads/agent/btube-v2-1-calibration-pinned` | `9fdc08c832dfdaf8aa76fd461f256db2db6c4f6c` |
| `refs/heads/agent/btube-v2-1-routed-evaluator-design` | `cae2bcb08afc49be63002ae26f9b00e14bbcacf2` |
| `refs/heads/agent/btube-v2-1-routed-evaluator-implementation` | `c6a45866bf673c01e22c1519e4b87e75bea01c39` |
| `refs/heads/agent/document-prolate-item4-gap` | `7134aca0089f01ebc02a9e16794f369274c38f23` |
| `refs/heads/agent/fix-btube-selftest-audit` | `dbff78474399c47011906631de9cde75992b6d25` |
| `refs/heads/agent/item3-cgtube-r4-precision` | `1e0f671c91798b9c044c04c7a4224a21e1e67830` |
| `refs/heads/agent/item3-lambda-sweep-phase2-selftest` | `10c478a2f360bf65a47c77676aa5386ad263fa02` |
| `refs/heads/agent/item3-lambda-sweep-phase3-implementation` | `70af0de152fe93256dd243770181addb250ca7c2` |
| `refs/heads/agent/item3-lambda-sweep-phase4-workflow` | `21756fbba0aa974df4ebddfd7d40a7816250dcdc` |
| `refs/heads/agent/item3-lambda-sweep-production-config-draft` | `6f557931320ed4018cb4dba29ac9b93bdd38c87c` |
| `refs/heads/agent/item3-lambda-sweep-production-implementation` | `de11615aa6e7fff088ba2ae606248c218ff47c1d` |
| `refs/heads/agent/item3-lambda-sweep-v8-1-design` | `e82324fdcc5db331cc5d3e5a2fd3958773a7fbe1` |
| `refs/heads/agent/item3-sweep-f1-f3` | `269b71d5b08eb2c6e4c1a81fb1525581b8427786` |
| `refs/heads/agent/item3-sweep-v9-kernel-prototype` | `a515ead02ccd87b6504a7ec718f1ef28d54b7e56` |
| `refs/heads/agent/item3-sweep-v9-mean-value` | `b82c00f2f154f131e02e122efdb156592fa98070` |
| `refs/heads/agent/item3-v9-analytic-proof` | `33245390a70c948e688a5a82bbf394fe196bdb6c` |
| `refs/heads/agent/item7-audit-template-v2-correction` | `4ef99567375d530cb61d2efe2c17f8ddc9d96d96` |
| `refs/heads/agent/master-item4-gap-note` | `489d0854a374453660c5635a4eafbee014a24cab` |
| `refs/heads/agent/organize-solid-papers` | `53e71e79ba2ec821a652eb3f1d7792aab3e8e09c` |
| `refs/heads/agent/prolate-item2-bkernel-recovery` | `59da8c11a7ac70d1129f026c8b552994f54b6873` |
| `refs/heads/agent/prolate-item2-circle` | `92c46e5de1a56d90ccf707154f535bbc2a8db76d` |
| `refs/heads/agent/prolate-item3-centered-calibration` | `a9aae9eb2859f686f13a72e0f9ce93c6ec2e6bf9` |
| `refs/heads/agent/prolate-item3-cgtube-hybrid-audit-r2` | `5b352a7b9152873802d6c3aa7d58018e80674b34` |
| `refs/heads/agent/prolate-item3-cgtube-source-candidate` | `3a025346da89818273dc22616e6c7995478f25bb` |
| `refs/heads/agent/prolate-item3-cgtube-spot18-diagnostic` | `38830178ec457950b8c9f7b13a04d883937e10c9` |
| `refs/heads/agent/prolate-item5-maxwell` | `a9ef2d0fe1d8613fa07da2be3076ff8bc5eb5942` |
| `refs/heads/agent/prolate-item6-axis` | `6905a795066f7d475d9caf0013d87b9c97192eb0` |
| `refs/heads/agent/register-experimental-mathematics-canonical` | `62cd4d93d651ac51dc4f3e21d48bc5c1b0e689a4` |
| `refs/heads/audit/btube-census-pass1-v002` | `e472b2d6fac8b078e9f3f019cf99dcb8cbb6fc16` |
| `refs/heads/audit/btube-pre-shard-diagnostics-v001` | `7a7d980a2eadae546f980ed38f46d069ca7eabf6` |
| `refs/heads/audit/paper1-definition-canon-20260822` | `3b4035611375385c8f1e3667defca211462e1fea` |
| `refs/heads/audit-helper` | `3392ba40b630c89d611b3ddabe1dadebcfbb1d21` |
| `refs/heads/btube-route-consistency-depth14` | `891a7ff9a91be7103965a8f8ce6c4463caa15936` |
| `refs/heads/btube-v2-1-uniform24-prepartition` | `52b98b6bd93382a47ed4cf5cbc7067edb0cebe45` |
| `refs/heads/btube-v2-3-native-flambda` | `98dda39e50a1422db23ac12d868b2d4dfd8ce9f3` |
| `refs/heads/candidate/d2-o2-r2-p2b-predeclare-20261014` | `eb337e760a84aecd4b8b3aa485c84525e349b46a` |
| `refs/heads/candidate/dob-p2-closure-erratum` | `cecfb2bd9c906f8ad21337c18a70b441e8cd840e` |
| `refs/heads/candidate/dob-p2-comparison-d1-d4` | `ab683fc33543dcb2cd3f5e0a0eeee7ef2c7031e0` |
| `refs/heads/candidate/dob-p2-phase0-postaudit-artifacts` | `15fff0199e38a707b5c727117bbccb62ed78586d` |
| `refs/heads/canon/basepoint-geometry-2026-08-20` | `b56906add3b9f80c6201e679623802ff0442b9ea` |
| `refs/heads/chatgpt/btube-v2-1-local-audit-helper-20260822` | `aad6f2bf8167f3082ab0113e7dd525d8cfdce53a` |
| `refs/heads/chatgpt/d-p2-o1-predeclare-v1-20261009` | `fbadfc4d3424b0b4d08ac401bfc9ca6c8015098a` |
| `refs/heads/claude/d-ob-p2-resumable-i8dgpn` | `020a4b80a5fe8f65b3b94f3d1b8945f506aeb8a8` |
| `refs/heads/claude/github-write-permission-check-q7qgs3` | `6b6fa7c5f7b1d255b389c06e28a0556d2446c947` |
| `refs/heads/claude/new-session-3uwmo4` | `664e3e3375af982ecf4296ed403b95a69b15b6a1` |
| `refs/heads/claude/new-session-p5haiv` | `dffd874839551a034b767511942eba28a41adf1f` |
| `refs/heads/claude/peer-review-evaluation-scores-zfm9t9` | `f50b12a2718802ce771856798fee7232676d734d` |
| `refs/heads/claude/prolate-item2-boundary-entry-me1kau` | `b0582728d3f8fd3508ba8574a898017212a28caa` |
| `refs/heads/claude/remote-control-7fnz71` | `92c46e5de1a56d90ccf707154f535bbc2a8db76d` |
| `refs/heads/codex/l43-independent-audit-20261009` | `fcbfdaa6007706a65a168fc8a8f5012036c148e4` |
| `refs/heads/controls/btube-v2-1-verification` | `7a7d980a2eadae546f980ed38f46d069ca7eabf6` |
| `refs/heads/design/btube-exact-lambda-addendum-v2` | `9063da8747d29dd172e742943d80af7ec0a9edd6` |
| `refs/heads/item3-cgtube-r3-serialization-fix` | `c05affd36a2bbef4d9e6bea2cbe594e493887a76` |
| `refs/heads/item3-sweep-receipts` | `21756fbba0aa974df4ebddfd7d40a7816250dcdc` |
| `refs/heads/main` | `abf704b8701f3da8eb41d8a99408570a413b2214` |
| `refs/heads/paper1-certchain-202609` | `7cc5726d62f063803b6d83cb9ba5fda5fd91f72c` |
| `refs/heads/tmp-hu-v12-producer-rerun` | `0e3d8954ccd97adf1522088233e65c9729030b4f` |
| `refs/heads/tmp-hu-v12-raw-evidence` | `1a24b0d2a676d5c1ac2192a62c104c912a27b618` |
| `refs/heads/tmp-hu-v12-release-checker` | `6d705c6fbf37ae77d35232a40842692a3e92713e` |
| `refs/tags/blocal-v2.1-run-e86c130d18f69e9d9944a2f35a5af2f37f399881` | `e86c130d18f69e9d9944a2f35a5af2f37f399881` |
| `refs/tags/blocal-v2.2-run-15dd8f56e95920f958db3ecf9091b30f9c39b97f` | `15dd8f56e95920f958db3ecf9091b30f9c39b97f` |
| `refs/tags/blocal-v2.2-run-1b6d61eae275590efc5538fadaa94766b583ab74` | `1b6d61eae275590efc5538fadaa94766b583ab74` |
| `refs/tags/blocal-v2.2-run-597ac12ca0e0c0becf50fb13ec6f148eeb97f363` | `597ac12ca0e0c0becf50fb13ec6f148eeb97f363` |
| `refs/tags/blocal-v2.2-run-a8997d11850dbd5b63e3064560a1c311e5c9c267` | `a8997d11850dbd5b63e3064560a1c311e5c9c267` |
| `refs/tags/blocal-v2.2-run-d827a13ed866f2913f34bf763a7a4b77e812af5e` | `d827a13ed866f2913f34bf763a7a4b77e812af5e` |
| `refs/tags/blocal-v2.2-run-f286d42ac9daac19bc26f1f215f0a2438c004e6b` | `f286d42ac9daac19bc26f1f215f0a2438c004e6b` |
| `refs/tags/btube-v2-1-calibration-approved-021d821daa070f14369fd8a73c52bd33f870caa0` | `021d821daa070f14369fd8a73c52bd33f870caa0` |
| `refs/tags/btube-v2-1-calibration-approved-891a7ff9a91be7103965a8f8ce6c4463caa15936` | `891a7ff9a91be7103965a8f8ce6c4463caa15936` |
| `refs/tags/btube-v2-1-calibration-approved-9fdc08c832dfdaf8aa76fd461f256db2db6c4f6c` | `9fdc08c832dfdaf8aa76fd461f256db2db6c4f6c` |
| `refs/tags/btube-v2-1-calibration-approved-cf49e4199beaa926bbb63a346113cd285ff459bb` | `cf49e4199beaa926bbb63a346113cd285ff459bb` |
| `refs/tags/btube-v2-1-calibration-approved-f15c466dab1d530aec209881069f75cc3857c45b` | `f15c466dab1d530aec209881069f75cc3857c45b` |
| `refs/tags/hu-domain-v1.2` | `6d705c6fbf37ae77d35232a40842692a3e92713e` |
| `refs/tags/item3-sweep-run-269b71d5b08eb2c6e4c1a81fb1525581b8427786` | `269b71d5b08eb2c6e4c1a81fb1525581b8427786` |
| `refs/tags/item3-sweep-run-602ab61f4908f5700ed672f6208f616b583731fa` | `602ab61f4908f5700ed672f6208f616b583731fa` |
| `refs/tags/item3-sweep-run-de11615aa6e7fff088ba2ae606248c218ff47c1d` | `de11615aa6e7fff088ba2ae606248c218ff47c1d` |
| `refs/tags/item3-sweep-run-eb1006718ea720af90cccacab415cc6f6b9c85c7` | `eb1006718ea720af90cccacab415cc6f6b9c85c7` |
| `path_history:item0c_center` | `e11e30948fafdbb899b403c4cb4198c1a2628adc` |

## 未検索の範囲

すべての過去 commit の全 tree、削除された branch、到達不能 Git object、
外部ストレージ、別リポジトリ、元チャットの添付、Actions の全過去 artifact は
網羅していない。従ってリポジトリの全歴史に存在しないとは断言しない。
この調査で 0c を再生成したり、別の ZIP を原本と認定したりしていない。

