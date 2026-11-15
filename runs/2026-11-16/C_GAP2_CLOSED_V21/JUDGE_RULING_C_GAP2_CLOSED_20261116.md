# Judge 裁定：C 空白② の採用（CLOSED）

2026-11-16 / Judge（ユーザー）／ 記録: chat

## 裁定

**「採用（比較器の再実行は記録の補完）」**（ボタンによる選択。chat の推奨どおり）。

C 空白② U₂ ＝ Λ × (t_e, 1) を **CLOSED** とする。U₂ は、打ち切っていない C1b の区画 124 の上側の帯で、t_e ＝ max(31/32, t₊) である。ここで g < 0 であることは、右の外側 [t₊, 31/32] を C1b v2.4 から取り込むことも含めて、凍結した手順のとおりに両系統で証明された。

## 根拠

| 項目 | 値 |
|---|---|
| FREEZE 裁定 | `JUDGE_RULING_C_GAP2_FREEZE_AND_RUN_20261115.md`、SHA-256 `f737fa582652b87f8d3ebbb87e1a0ef81709d22df8b55fa206b800b90e116e6f` |
| 実装 | `cotaxxxx/bg-oblate-spheroid` の HEAD `0d32ac2a0325f41998adebf922a57ed50cf3ba59`。実行の前と後で同一性が一致し、作業木は clean |
| 本走の証拠 | `bg-spheroid-family` branch `evidence/c-gap2-run-0d32ac2-20261115` commit `4ecb713`、zip SHA-256 `598ed0c3c9574beec4f4def31b384b3ee4507a00370a564d38da419fbdbe5580` |
| 結果 | producer と checker の両方で、親 124 のすべてを深さ 0 で受理（細分 0、ABORT 0）。最小の余裕 −U_cum は 0.009169 |
| chat の検収 | `CHAT_ACCEPTANCE_C_GAP2_FORMAL_RUN_0D32AC2_20261115.md`：封印入力と右の外側の照合が 22/22 PASS、本走の検収が 29/29 PASS、凍結した比較器が `COMPARE_PASS_NOT_JUDGE_CLOSED`（出力 SHA-256 `6fb9d29238cd73c023c96f87f202255c743e968c7b39a32853ff25c8df3b975b`） |
| 解析の前提 | G0/E1 v3、C1 補題 `5afa815f`、C2 補題 `7cb9b809` と `f66ffe5a`（V19 で chat 監査 PASS） |

## 研究用PC の比較器

研究用PC での比較器の停止（`ModuleNotFoundError`、0.00 秒）は、監視スクリプトが作業ディレクトリを指定していなかったことによる。これは FREEZE 裁定 §3 の起動の段階の誤りにあたる。

記録を補うために、Dig は次の手順で比較器だけを流し直す。数値本走はやり直さない。

1. 実装リポジトリ（HEAD `0d32ac2`、clean）の中で実行する。
2. 実行する前に、HEAD と `git status --porcelain` をログに残す。
3. `python -m gap2_analysis.lineage_compare --producer-run <producer> --checker-run <checker> --judge-ruling-sha256 f737fa58… --output <新しいJSON>` を流す。
4. 出力 JSON の SHA-256 が chat の `6fb9d292…` と一致することを確かめる。
5. stdout、stderr、所要時間とあわせて、証拠ブランチに登録する。

SHA が一致しなかった場合は、その差分を chat に回す。この裁定の効力は、その場合も変わらない。差分が数学の結果に関わるものであれば、Judge が改めて判断する。

## 次の工程

C 系列の大域の軸被覆の組み立てに入る。構成は次のとおりである。

- C0
- C1a〜C1d
- 帯 [31/32, 1]
- 空白①
- 空白②（右の外側の取り込みを含む）

組み立ての後、STATE の 判断待ち1（D6 の外部監査）を整理し、D-OB の大域の CLOSED に向かう。
