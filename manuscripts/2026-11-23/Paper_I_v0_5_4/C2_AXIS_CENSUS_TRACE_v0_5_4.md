# C2 axial census — trace of the ten disjoint parameter cases (v0.5.4)

**Original:** `cotaxxxx/bg-spheroid-family@2c084bc05e5dd0b0d7deeb9f9c293deeb1d5e40a`, `drafts/2026-11-16/C_AXIS_GLOBAL_COVER_ASSEMBLY_V1/C_AXIAL_GLOBAL_COVER_ASSEMBLY_DRAFT_V1.md`, §§0–8, specifically its §2 10-case table and §§3–4 frozen sign gates. This English map is editorial and does not replace the pinned Japanese primary record or assert a new numerical evaluation.

Conventions: `t∈(0,1)` is the reference axial coordinate; center `t=0` and pole `t=1` are not counted. The old axis family is related to the volume-preserving family by a positive scale, and the derivative rescaling is positive; this does not change the root positions or signs. `g(t,λ)` is the axial first derivative; `Φ(t²,λ)=g(t,λ)/t`. The paper assumes C2(3), so this table shows **which frozen sign gates would imply it**, not a new proof that each frozen gate was correctly computed.

The source explicitly bounds `2/5 < c_o < 83/200 < 699/1600 < λ_x < 281/640 < 703/1600 < 9/20 < 5/8 < b_o < 33/50`; `λ_x` is the unique zero of `g(1/2,λ)`.

| Case | λ interval, owner | Lower half and boundary signs | Upper half, uniqueness/exclusion, shared endpoints | Count N+ |
|---|---|---|---|---|
| 1 | `[2/5,c_o)` | `Φ(0)=H<0`, `∂_(t²)Φ<0` (C0a+Cor.18) | Gap1 L: `g<0` for `1/2<t≤1` | 0 |
| 2 | `{c_o}` | `H=0`, strict `∂_(t²)Φ<0` for `t>0` | Gap1 L: `g<0` | 0 |
| 3 | `(c_o,83/200]` | `H>0`, `Φ(1/4)<0`, strictly decreasing ⇒ unique lower-half root | Gap1 L: no upper root; C0b | 1 |
| 4 | `(83/200,λ_x)` | `H>0>Φ(1/4)`, C1a A + A1 transfer gives unique lower root | Gap1 X: excludes `(1/2,1]` | 1 |
| 5 | `{λ_x}` | `Φ(1/4)=0`; lower `g>0` before `t=1/2` | Gap1 X: excludes `t>1/2`; root `t=1/2` counted once | 1 |
| 6 | `(λ_x,9/20)` | `Φ(1/4)>0`, strict decrease ⇒ no lower root | Gap1 X up to `703/1600` or R afterward: one upper tube, `g_t<0`, negative exterior | 1 |
| 7 | `[9/20,5/8]` | C1c & C1b positive anchor: `g>0` on `(0,1/2]` | C1b: 159 intervals (124 unclamped / 35 clamped); 124 outer-right exclusions include Gap2 | 1 |
| 8 | `(5/8,b_o)` | C1d: `g>0` on `(0,31/32]` | Band `g_t<0`, `g(31/32)>0>B_o`; one `t∈(31/32,1)` | 1 |
| 9 | `{b_o}` | C1d positivity through `31/32` | Band negative derivative and `B_o=0`; only pole `t=1` is zero | 0 |
| 10 | `(b_o,33/50]` | C1d positivity through `31/32` | Band monotone, `B_o>0`; no root | 0 |

**Open/closed boundary ownership (from primary §2–4):** 83/200 belongs to case 3 for root counts, but the Gap1 frozen slab owner there is X and the L gate is a consistency check; 703/1600 is an X/R shared boundary of the same root; 9/20 belongs to C1b; 5/8 belongs to case 7, with band providing a second verification of that **same** root; `t=31/32` is a bookkeeping cut. A positive root at exactly `t=1/2` at λ_x is counted once, while a root at `t=1` at b_o is excluded from the **interior** count.

**C2 source gate inventory:** Gap1 L48/X78/R34 parameter slabs (160 total); C1b 159 accepted parameter intervals, 124 unclamped and 35 clamped tubes; Gap2 checks the remaining outer-right intervals for all 124 parents; upper band `[5/8,33/50]×[31/32,1]` supplies `g_t<0`, left positive anchor, polar trace. The exact technical origins and proof/ledger limitations are listed in primary §7: CENTER, C0, C1a, A1, C1b, C1c, C1d, band, B_ob, GAP1, GAP2, D6, V22. A single public English self-contained machine-checkable C2 proof archive has **not** been produced by this editorial map. The conditional theorem's premises are unchanged.
