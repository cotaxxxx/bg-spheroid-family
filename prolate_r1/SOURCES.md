# DIAGNOSTIC_ONLY / NOT_EVIDENCE — 固定入力・来歴

Repository: `cotaxxxx/bg-spheroid-family`。

- **report**: commit `9d100927cface0161337d4c0c0ddf6c2ac02362a`、[runs/2026-11-17/D_PRO_COROTATION_R0_V30/ASTRA_D_PRO_COROTATION_REPORT_20261117.txt](https://github.com/cotaxxxx/bg-spheroid-family/blob/9d100927cface0161337d4c0c0ddf6c2ac02362a/runs/2026-11-17/D_PRO_COROTATION_R0_V30/ASTRA_D_PRO_COROTATION_REPORT_20261117.txt)、Git blob SHA `da83668e909ec2c8fa9849ebd643b1fb739030ae`。
- **r0_audit**: commit `9d100927cface0161337d4c0c0ddf6c2ac02362a`、[runs/2026-11-17/D_PRO_COROTATION_R0_V30/CHAT_AUDIT_AND_RULING_D_PRO_COROTATION_20261117.md](https://github.com/cotaxxxx/bg-spheroid-family/blob/9d100927cface0161337d4c0c0ddf6c2ac02362a/runs/2026-11-17/D_PRO_COROTATION_R0_V30/CHAT_AUDIT_AND_RULING_D_PRO_COROTATION_20261117.md)、Git blob SHA `dd46e32ecce20cabcef8d145b31b82d08fb52874`。
- **r0_checks**: commit `9d100927cface0161337d4c0c0ddf6c2ac02362a`、[runs/2026-11-17/D_PRO_COROTATION_R0_V30/chat_r0_corotation_checks.py](https://github.com/cotaxxxx/bg-spheroid-family/blob/9d100927cface0161337d4c0c0ddf6c2ac02362a/runs/2026-11-17/D_PRO_COROTATION_R0_V30/chat_r0_corotation_checks.py)、Git blob SHA `830a1c065dd43c553451676f8678a1e7201dcad4`。
- **r0_split**: commit `9d100927cface0161337d4c0c0ddf6c2ac02362a`、[runs/2026-11-17/D_PRO_COROTATION_R0_V30/chat_w1_split.log](https://github.com/cotaxxxx/bg-spheroid-family/blob/9d100927cface0161337d4c0c0ddf6c2ac02362a/runs/2026-11-17/D_PRO_COROTATION_R0_V30/chat_w1_split.log)、Git blob SHA `31f1d5354435050caa5b86005329e9523f8e2244`。
- **old_kernel**: commit `556997ac2387933138296939b9c58eda32d7cdec`、[prolate_p3/kernel.py](https://github.com/cotaxxxx/bg-spheroid-family/blob/556997ac2387933138296939b9c58eda32d7cdec/prolate_p3/kernel.py)、Git blob SHA `d69504ea11cb1d5674845ed01ef3e1c6704cd168`。
- **old_w1**: commit `b2fc41d4a247c68201238f4ed036d8193359af30`、[prolate_p3/kernel_w1.py](https://github.com/cotaxxxx/bg-spheroid-family/blob/b2fc41d4a247c68201238f4ed036d8193359af30/prolate_p3/kernel_w1.py)、Git blob SHA `9107f6d778b6a8f7d26b041a91506c8354fa5eff`。
- **old_audit**: commit `ce2aa83c5373bb5cedc19e50beedf5c87e84f5a3`、[runs/2026-11-16/CODEX_P3_KERNEL_AUDIT_V29/CHAT_AUDIT_CODEX_P3_KERNEL_20261116.md](https://github.com/cotaxxxx/bg-spheroid-family/blob/ce2aa83c5373bb5cedc19e50beedf5c87e84f5a3/runs/2026-11-16/CODEX_P3_KERNEL_AUDIT_V29/CHAT_AUDIT_CODEX_P3_KERNEL_20261116.md)、Git blob SHA `8c030196a467fa5ce1c2c178eb1e19b2e2b3d32d`。
- **boxes**: commit `556997ac2387933138296939b9c58eda32d7cdec`、[prolate_p3/boxes.json](https://github.com/cotaxxxx/bg-spheroid-family/blob/556997ac2387933138296939b9c58eda32d7cdec/prolate_p3/boxes.json)、Git blob SHA `3c75b6b9a84e70ea3652f8fe680417c70115431e`。

[R0] = report §§3–5,6.4,9、式(3)–(11),(13)–(15),(17)–(20)。
[K0] = old_kernel、[W1] = old_w1。旧監査は old_audit §3 W1/W2。

vendor の2ファイルは原文と同一です。級数・剰余・求積方法の再利用を明記し、clean-room とは呼びません。
chat の19/19は R0の式の監査であり、このR1ソースの検査結果ではありません。


## R2 の追加入力
- 修正元R1: commit `4b7f1f73421f2765d347e4d2ffc9ab004393695c`、
  `prolate_r1/density.py` の axial、
  `prolate_r1/jets.py` の Jet、
  `prolate_r1/tests/run_tests.py` の main と固定テスト。
- Dig RUN1: commit `1917e1ab3c22191852385cf8cd3df5f6d9958fb8`、
  `runs/2026-11-17/D_PRO_R1_COROTATION_DIG_RUN1/RUN_RECEIPT.md`
  の Reproduced axis_g error / Full suite timeout。
  同 `logs/axis_stage_diagnosis.stdout`、`axis_cell_diagnosis.stdout`、
  `axis_default.stderr`、`full.stdout`、`full.time`。
R1の動作証拠とR2の未実行状態を区別する。

## R3の追加入力
- 修正元R2：`bc70e1badbd9a89449cae6707ef37f5e69757a11`、
  branch `codex/d-pro-r1-corotation-r2-20261117`、`prolate_r1/`。
  読取時にR2のSHA256SUMS全29項目が一致した。
- V31：`47a4558a9adecea65ddcab038186cc3130bcb849`、
  branch `evidence/c-gap2-freeze-20261115`、
  `runs/2026-11-17/D_PRO_R1_R2_MATH_AUDIT_V31/CHAT_AUDIT_D_PRO_R1_R2_KERNELS_V31.md`。
  R2の動作検査11/11・23/23はこの監査が参照するDigの記録であり、R3の結果ではない。
- 依頼にある同ディレクトリの`CODEX_INSTRUCTION_D_PRO_R1_COROTATION_20261117.md`は
  このcommitでは404で、再帰treeにも存在しなかった。
  本会話の元R1依頼全文とV31本文を照合し、平均値・距離セル・接触座標・普遍量を維持した。
- R3仕様・参照値：Judgeの2026-11-17依頼（この会話）。固定化は
  `PLAN_R3_BEFORE_RUN.md`、`tests/width_r3.py`。
  参照値はchatの非区間の総当たり診断であり、包囲の証明入力ではない。
