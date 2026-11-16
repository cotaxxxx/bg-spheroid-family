# 取得・移植台帳

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## 設計と解析

- 設計：`cotaxxxx/bg-spheroid-family`, commit
  `7756bc51684cbb327835c4820864c3007cc97603`,
  `drafts/2026-11-16/D_PRO_GLOBAL_DESIGN_ASTRA/D_PRO_GLOBAL_DESIGN_ASTRA_20261116.md`。
  Git blob `84b06abab1083a9c19e7e21f0df4bfb674c31ba8`。
- 扁平 P1：`cotaxxxx/bg-oblate-spheroid`, branch `design/d-ob-p2`,
  `analysis/D_OB_P1_DESIGN_NOTE.md`。取得時 Git blob
  `f81e120e44a866d206117d4fab5fac627f26ccd1`。§2–§6 と面積評価を参照。
- 核の座標・量・範囲は今回のユーザー指示書を優先。
  設計の主推奨である相殺差商を、今回の要求された箱経路に置き換えた。

## 取得して読んだ移植元 ZIP

`cotaxxxx/bg-oblate-spheroid`, branch `evidence/d5-planb-run1-20261112`,
`analysis/D5_PLANB_ROUND3_20261109/DIG_D5_PLANB_ROUND3_EVIDENCE_20261109.zip`。

- Git blob: `50e3b53cb0833e058d155a68396316f4d65d0d1d`
- ZIP SHA-256: `477e2b3e88f75a12fe4944f44365db128b70eb7bafeecb825fd977d5d7e5d935`

| ZIP 内のファイル | SHA-256 |
|---|---|
| `sources/chat_m22iv.py` | `b4ea57e134150e57be8ced020eafa4cfd6c740af75d27939b108e23de38d6a89` |
| `sources/chat_m40iv.py` | `d39be478485cb1faaf804ddbf970ce1c790b0d7a5d0bf7f2fb400561c2cdad1b` |
| `sources/chat_bprime_iv.py` | `93b9431dffee9931675b9adf937f99118981b7128f0e6c89699b8158a452d098` |

移したもの：外向き丸め、二次 Taylor 係数の意味、連鎖律、
`chat_m40iv.J` の一変数二次部分、`chat_bprime_iv` の逐次中点線求積。
変更したもの：有理端点独自区間型から Arb、球面の θ/π・φ/π 座標、
扁長の E/E_z/E_zz 核、今回の q=1−γ の級数と片側尾部、箱の V 経路。
元コードにある float による打切り選択、扁平用の定数・符号・範囲は移さない。

もう一つの候補 `evidence/d5-v4-run1-20261111` の ZIP は今回の移植に
使用していない。Plan B ZIP を正本の移植元として取得・照合した。
元の証拠の認証状態を、この新実装へ継承するものではない。

## 来歴調査

`PROVENANCE_REPORT.md`、`outputs/PROVENANCE_SEARCH.json`、
`outputs/PROVENANCE_ARCHIVES.json` を参照。
