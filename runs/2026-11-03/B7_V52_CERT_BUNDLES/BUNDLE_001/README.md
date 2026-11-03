# B7 V5.2 — PASS証明書バッチ001（追加待ち）

2026-11-03 JST

**状態：PARTIAL / 監査用の先行公開。B7正式件数は8/40 PASSのまま。**

現在は `L0_T3_D1` の1箱を収録しています。後続のPASSを同じバッチ系列へ追加するため、このバッチはまだ完結として扱いません。

## 収録物

- `L0_T3_D1_full.json` — 本番V5.2の結果（producer status PASS）
- `L0_T3_D1_full.leaves.json.zst` — 全63,593葉の証明書。圧縮前のファイル名は `L0_T3_D1_full.leaves.json`
- `L0_T3_D1_chat_v52_local_audit.txt` — PC上でのローカル監査（全項目PASS）。独立監査の代替ではない。
- `MANIFEST.json` — ファイル別SHA、圧縮前SHA、V5.2指紋、厳密最終下界。

圧縮前の全葉ファイル SHA-256：
`3f80a336eded8e020d4a12f81a163e2677b68b3f0a5794fecb27bbacc90e79d6`

圧縮ファイル SHA-256：
`cc2de40c0ab5c634015d0bbf70e4dd13b480c6a6ea91c6836e554e0296273efa`

最終下界（参考小数）：`+0.0003786913227644102`

## 取得・再現

GitHubで本ディレクトリのファイルを取得し、以下で展開してください。

```bash
zstd -d -c L0_T3_D1_full.leaves.json.zst > L0_T3_D1_full.leaves.json
sha256sum L0_T3_D1_full.leaves.json
python3 -I chat_b7_pass_audit_v5.py L0_T3_D1_full.json --version v52 --no-float
```

監査ソースには監査済み `ea4540296cffae727d5ff526c8c719750ef02c976aa998778e2a14b18332b245` を使用します。
検証対象のV5.2ソースはブランチ `b7-v52-dig-20261103`、commit `37c75b3bf4f4f1cf5673f1a1172b9885248fff7b` です。

**葉の完全性・被覆・集計・本番核再計算は、受領後にchat側で独立再監査すること。**
