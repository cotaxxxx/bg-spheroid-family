# DIAGNOSTIC_ONLY / NOT_EVIDENCE — supplementary identity test

The first fixed experiment returned false for Q5 (co-rotation vs laboratory gradient integral at absolute tolerance 2e-5). Its output and script remain unchanged. No numerical residual or failing location is inspected.

This follow-up tests the SAME identity, not any positivity hypothesis, on a new fixed Cartesian sample: lambda=[2,7/2,5], R=[1/8,1/2,15/16,1], tau=[1/16,1/4,1/2,3/4,15/16], 60 points. Use the same panels and quadrature implementation, rules (24,192),(48,384),(72,576), absolute tolerance 2e-5. Record a Boolean for each rule and an additional Boolean over strictly interior R, and record no residuals, worst points or extrema. Also test the ORIGINAL full Q5 sample at the final (72,576) rule, same tolerance. Fixed samples are not certification parameters.

If the finest test still fails, no claim that the discrepancy is resolved may be made. The analytic integration-by-parts identity is independently derived in the report. This diagnostic is not its proof.
