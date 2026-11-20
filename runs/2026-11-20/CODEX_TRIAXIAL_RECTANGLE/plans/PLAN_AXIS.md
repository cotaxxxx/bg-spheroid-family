# PLAN AXIS 1

2026-11-20 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

Purpose: give explicit parameter neighborhoods and certified interval inclusions for selected simple axial roots. This is not an exhaustive classification of the rectangle.

Input: TRIAXIAL_FIRST_ATLAS.md SHA-256 7ba516b708e033ffc51c3bb5232130986306b1a1cabd5fe22e52c3d71060f534. The existing noninterval atlas supplies candidate brackets only.

Parameter denominator: 65536.
A: s in [81919,81921]/65536, t in [196607,196609]/65536.
B: s in [134348,134350]/65536, t in [196607,196609]/65536.

Candidates fixed before new interval evaluation:
A axis 1: r in [3/8,1/2]; expected Hessian diagonal signs (-,+,+).
A axis 2: r in [27/32,29/32]; expected signs (-,-,+).
B axis 2: r in [7/8,15/16]; expected signs (-,-,+).
At the two centers: A expected (+,+,+), B expected (-,+,+).

For each root: enclose the axis gradient at both bracket endpoints; show positive left and negative right. Enclose the diagonal Hessian and U_prime=(r H_ii-g_i)/(2 r^3) on every subinterval of the bracket. Use 8 then 16 then 32 then 64 equal dyadic r panels if needed. Each panel starts with nmu=128 and nw=nmu/2, then doubles through 2048. If all required signs hold, stop refining that panel. Endpoint gradient grids start at 256 and double through 8192. Center grids start at 128 and double through 2048. Save all stages, including inconclusive stages. The final result requires a complete cover of the bracket by accepted panels; larger-number refinements replace coverage logically but never erase records.

Kernel: equation (1) of the source, in surface-area variables mu=xi_i and w=tan(phi/2), folded into the orthogonal-coordinate quadrant. Each angular rectangle is evaluated by outward interval arithmetic; the probability measure is (dmu/2)*4 dw/[pi(1+w^2)]. No point quadrature is promoted to a bound. Gradient and Hessian are algebraically simplified to preserve positive projection terms and the factor 1-mu^2. pi is bounded by the alternating rational Machin series. P,F,Q use positive power series in z=(1-gamma)/2 with terms 0 through 54 and explicit positive tails, then a monotone gamma table of 65536 intervals.

Arithmetic: binary64 nearest-even IEEE 754 primitive operations, gradual underflow and correctly rounded square root, with every primitive result enlarged by nextafter. Exact dyadic endpoints. Python integer ratios rounded and enclosed by neighboring floats. Balanced sums are widened at each addition.

Validation: check formulas against the source axis values as an independent numerical sanity comparison, and exact constant kernels P(1)=2, Q(1)=10/3, F(1)=0. None of those comparisons substitutes for an interval proof. Record input and source hashes, runtime, timings, all bounds and reasons.

Limitations to record: no exclusion outside the three radius brackets, no control of center/boundary collars, no full-rectangle root count, no extension from pointwise numerics. If the declared finite grids do not settle a sign, report unresolved; any new scheme needs a separately dated plan before execution.

CPU use: at most two processes. No research PC and no GitHub mutations.
