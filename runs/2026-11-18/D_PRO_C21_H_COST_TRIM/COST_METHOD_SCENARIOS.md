# D-PRO C21 H post-run method-specific COST SCENARIOS
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Pure arithmetic extrapolation, NOT a H covering or an upper bound.
Assumptions: 12 workers, mix 75% general/25% axis,
all boxes take four-probe median cost of the listed method,
and each depth has hypothetical fraction f of boxes splitting.
All lambda plate widths are unverified away from measured local boxes.
No W work included. Combining enlarged R-tau initial boxes with
coarse Hessian is a counterfactual combination NOT measured together.

| Mode | Initial grid | split f | lambda plates | assumed H jobs | 12-worker hours |
|---|---:|---:|---:|---:|---:|
| original_second_order_1_256_HESS16x32n4 | 64² | 0.5 | 768 | 15,728,640 | 238,427.8 |
| thick_1_8_HESS16x32n4 | 64² | 0.5 | 24 | 491,520 | 7,244.2 |
| hessian_only_8x16n4 | 16² | 0.25 | 24 | 12,264 | 73.2 |
| hessian_only_8x16n2 | 16² | 0.25 | 24 | 12,264 | 54.7 |
| hessian_only_8x16n4 | 16² | 0.25 | 1040 | 531,440 | 3,173.7 |
| hessian_only_8x16n2 | 16² | 0.25 | 1040 | 531,440 | 2,369.4 |

The conditional low-lambda 1/1024 width [2,3] is an independently
assumed high-resolution policy. The λ≈2 pilot never establishes this
thickness nor that the entire λ∈[2,5] signs can be covered.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
