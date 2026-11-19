# PLAN_TAIL_AXIS_BEFORE_RUN.md — small diagnostic TAILAX_V1

2026-11-19 / Dig (via chat), Judge instruction commit 00024f8e62dafc8ce3bf0f7579f3f7b9ab46d4fb.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. This plan is frozen before any new numerical probe. Mathematical derivation MATH_DERIVATION_BEFORE_PROBE.md was written first.

## Hypothesis to measure — not the goal theorem

Check a fixed **inner-limit kernel at ε=0** after exact subtraction of its 1/|t| tail. This does NOT enclose H at finite ε and does NOT prove a uniform ε or boundary statement. A single compact sample is intended to identify whether the analytic subtraction reduces the *tail magnitude* and signed angular interval width.

Fixed q=(ρ,z)=(1/2,0). Thus S=1, μ=z=0 in the inner limit and
A0=5/4−cosφ, k0=1−(1/2)cosφ, D0²=t²+A0,
γ0=k0/√(D0²), y0=sinφ, B0=1.
K0=(1/D0)[F'(γ0)γ0²((t²+(cosφ−1/2)²)/D0²)
          −Q(γ0)y0²(1−k0/D0²)²].
c0(φ)=−2πsin²φ.
r0=K0−c0(φ)/√(1+t²). Evaluate this as
r0=(1/D0)F'(γ0)γ0²((t²+(cosφ−1/2)²)/D0²)
   + y0²[2π/√(1+t²)−Q(γ0)(1−k0/D0²)²/D0].
This is algebraically the SAME kernel, with y0² correlated.

Use N=20 positive h polynomial bounds:
a_n=4^n(n!)²/(2n+1)!; q_n=a_n(2n²+10n+10)/(2n+3).
Plo=2Σ_{n≤20}a_nh^n ≤ F' ≤ Phi=Plo+4a21h^21.
Qlo=Σ_{n≤20}q_nh^n ≤ Q ≤ Qhi=Qlo+52a21h^21.
h=(1−γ0)/2, γ0∩[0,1], all coefficients rational.
For products containing negative signs use genuine interval arithmetic on the **common factored expression**. Do not turn float approximations into proof. Prove geometric positivity of denominators for every cell: t≥8 and A0≥1/4 imply D0²≥64+1/4, k0∈[1/2,3/2], γ0>0, 0≤y0²≤1.
When a geometry intersection is empty, a denominator is not positive, or a nonfinite interval occurs, STOP with explicit reason.

## Fixed pilot grid and thresholds

- t nodes: **8,16,32,64** exactly (four positive integer points).
- φ quadrature: **256** equal cells on [0,2π] with Arb π bounds.
- python-flint 0.8.0, Arb **192 bit**, 1 worker, nice +15, CPU pin a single CPU after checking load; no overlap with the C21 slab's chosen worker quota and do not signal PID 1581407.
- For each t, integrate K0 and the factored r0 separately using each φ cell's interval **range × positive angular area**, normalized by 1/(2π).
- Output exact rational endpoints for mean K0 and mean r0; also the exact analytic c-mean = −π, and identity check that mean(r0) overlaps mean(K0)+π/√(1+t²).
- Binary questions: (i) does mean(r0) interval contain 0; (ii) is the absolute upper bound on mean(r0) smaller than the absolute lower bound on mean(K0)? Report YES/NO (NO does not disprove the underlying analysis).
- All measured times and interval halfwidths must be recorded. No adaptive subdivision, no extra t points, no changing N/precision or number of cells after result inspection.
- Per-probe wall cap: 120 seconds. Complete run cap: 600 seconds.
- Also include **symbolic exact rational identities** of axis reflection k(−μ,z)=k(μ,−z), d²(−μ,z)=d²(μ,−z), B(−μ)=B(μ) for ε=1/5 and (μ,z)=(1/4,1/2),(3/4,1/2). This is only an algebraic unit check, not interval evidence of E_z/z>0.

## Deliverables, STOP rules, costs

Produce four full Arb intervals with exact rational endpoints for K0 and r0, binary table, stopwatch timings, axis symmetry test, source code, log, SHA256SUMS, report with OPEN conditions. Raw output remains independent of existing C21 records.
No certificate, no CLOSED claim, no extrapolation of point/slice results to all λ, ρ or z. In particular ε=0 and φ average at fixed t is not the same as the full physical E integral.
Before committing, verify the frozen plan SHA-256 and list it in the output. If numerical plan changes, create new plan version; never rewrite this frozen one.
