# D-PRO C21 R63_T63 polar cap — PLAN_R63_T63_CAP_BEFORE_RUN
2026-11-19 / Judge instruction / Dig execution via chat
**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — preregistered before first 128-box run.
## Source and isolation
ZIP original: /home/daybreak/ダウンロード/ASTRA_D_PRO_LAMBDA0_GAP_RESEARCH_20261119.zip
expected SHA256: 09473aac223553c17a8c0646555a18e05c4839167fdb3211d8d9ac6766f2c303.
Frozen extracted source: frozen/ASTRA_D_PRO_LAMBDA0_GAP_RESEARCH_20261119/cap_interval.py.
Execute copied BYTE-IDENTICAL cap_interval.py from run/ in SEPARATE folder; original archive is never executed or rewritten.
Heavy slab main process PID1581407 must remain running. Main STATE, SUMMARY, repo main and frozen H evaluator must not be touched.

## Geometry — exact inequalities to check pre-run
Heavy board: R ∈ [63/64,1], τ ∈ [63/64,1], λ ∈ [79/16,5].
Equator chart: ρ=R(1−τ²)/(1+τ²), z=R·2τ/(1+τ²); physical p=(ρ,λz).
z ≥ 7938/8065 >0. ρ²+z²=R²≤1.
χ=1−z²≤2032381/65044225. 25χ≤50809525/65044225<1.
Therefore w=λ√χ ∈[0,1] and u=ρ/√χ∈[0,1]. At χ=0 take u by continuity; on physical box it is well-defined except pole.
Scope of G9/G1 parameter box includes all of R63_T63 for entire λ slab.

## Run settings — frozen
ε=1/λ ∈[1/5,16/79]. Uniform ε subdivisions 2, w subdivisions 8, u subdivisions 8. Total 128 outer boxes.
Geometry mesh 96 θ ×48 φ, precision Arb128 bit; original bound()/geometry()/record() from cap_interval.py unmodified.
Bound valid only if analytical inequality G9 and its denominator premises correct. Use exactly cap_interval.record no code modifications.
Decision: rational lower_exact >0 for E_z>0; also record stricter >1/4.
Use max TWO Python workers, no override of 12-worker heavy slab.
No fallback lower-bound fabrication; preserve any error.
Outcome will be EXPLICIT PROPOSAL only: R63_T63 needs no H sign if E_z>0, but true stationarity exclusion conditional on independent mathematical audit. Do not modify ledger; boundary |q|=1 is trace only, condition B remains separate.
## Repro and receipt
Write geometry Fraction certificate, full JSONL 128 records, summary, checker record and timings.
SHA256SUMS covers plan, scripts and outputs; ZIP and its SHA256. Prerun plan sha256 is recorded in PLAN_FREEZE_SHA256.txt.
