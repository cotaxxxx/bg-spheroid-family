# CHAT AUDIT — Astra's first D4 response, and a corrected addendum v2 (2026-10-10)

Input: Astra's reply (relayed 23:38). Astra received the **addendum only**, not the full D4 instruction.
This audit checked Astra's claims by reading `full_terminal_map.tsv` and counting its rows exactly. No certificate or numerical evaluation was run. The file is DIAGNOSTIC / NOT_EVIDENCE; it is used here only to locate boxes.

## 1. Astra's claims — independently confirmed

- basepoint-geometry `ab683fc33543dcb2cd3f5e0a0eeee7ef2c7031e0`:`tools/d_ob_p2/full_terminal_map.tsv`, SHA-256 `0584110495c9d3b98a96d88e3d9fbe717bde326f2b76dcc465db784ad3bd26f8`. ✓ The header reads "DIAGNOSTIC / NOT_EVIDENCE", with source smoke_20260923T121918Z `producer_ledger.jsonl` on the research PC.
- There are 7662 unresolved boxes, all in column `near`.
  - **Center band = the boxes with prefix `0,0,`: 3584**, all distinct. Their exact union is r ∈ [1/64, 1/8], τ ∈ [0, 1/8], λ ∈ [119/200, 33/50]. ✓
  - The remaining **4078** (the pole corner) have union r, τ ∈ [7/8, 1] and λ ∈ [2/5, 93/200].
- On the center boxes, m = 2τ/(1 + τ²) ≤ 16/65 and z/λ = r·m ≤ 2/65. ✓ The boundary entry of the axial root is at t = z/λ ∈ [31/32, 1]. **The two are far apart in space.**

## 2. chat's deviations (accepted)

- **CHAT-D4-K4-001.** Audit `1001a038`, K4 and addendum item 3, linked the thin margin of the center band to λ_∂^ob, **because the λ-ranges overlap**. That is not a valid reason. λ_∂^ob is an event at the boundary (t → 1), and the center band lies near the center (z/λ ≤ 2/65). The *question* "structural degeneracy or method artefact" stays valid, but it must be asked about the center itself. Corrected in addendum v2 §B.
- **CHAT-D4-CITE-001.** "帯 receipt `d6b0a787` §6" was a wrong citation. `d6b0a787` is the receipt's blob prefix, and the receipt has no §6. The consequences are in §6 of the **Judge request** (`LOCAL_ENTRY_BAND_JUDGE_REQUEST.md`). The receipt's status is JUDGE_PASS / CONDITIONAL_ON_TWO_LEMMAS / EXTERNAL_AUDIT_PENDING.

Astra's other points are sound and consistent with the ledger:
- L43 exists in an original version and an addendum version, which must not be mixed.
- The QM reverse-feasibility conclusion is UNDETERMINED, not "FT_q improvement required", and must not be carried over to the center band.
- D-P2 stays NOT_CERTIFIED, and no METHOD_SELECTED is declared.

## 3. Addendum v2 for Astra (replaces addendum v1 items 2–3; can be sent as is)

> **D4 補遺 v2（2026-10-10、Judge 発行・chat 監査、v1 の項目2・3 を置き換え）**
> A. 基準は STATE v1.14、bg-spheroid-family main `d707e6ef3e583616fa3f24409351ea01b6d4be58` とする。D4 指示書の全文を別途送る。方式 A〜D の定義と作業許可の範囲は全文のとおり。
> B. 中心帯の正確な範囲は Astra の特定どおりとする（`full_terminal_map.tsv` `0584…26f8`、DIAGNOSTIC）：3584 箱、r∈[1/64,1/8]、τ∈[0,1/8]、λ∈[119/200,33/50]、z/λ≤2/65。補遺 v1 の「λ_∂^ob との関連」は撤回する（chat の誤り CHAT-D4-K4-001）。D4-0 は次の形に改める：**中心 (ρ,z)=(0,0) とその近傍での H の値と挙動**（H(0,0;λ)=E_ρρ(0,0;λ)、および小さい r での展開の主要項）が、λ∈[119/200,33/50]、とくに右端 33/50 の近くで 0 に近づくかどうかを、原典から調べること。主張が正しいか誤っているかを前提にしない。
> C. 引用の訂正：帯の帰結は `LOCAL_ENTRY_BAND_JUDGE_REQUEST.md` の §6 にある（receipt `d6b0a787` は条件付き Judge PASS）。
> D. 補遺 v1 の項目4（定理から D-P2 への引き渡し）と項目5（箱の一覧）は維持する。一覧は Astra が特定した `full_terminal_map.tsv` で足りるが、箱を消去するには、元の ledger との対応を確かめる段階が別途必要である。
