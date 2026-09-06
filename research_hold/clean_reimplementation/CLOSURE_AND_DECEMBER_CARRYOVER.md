# Triaxial diagnostic closure and December carryover

- status: DIAGNOSTIC_ONLY / NOT_BINDING / NOT_CERTIFIED
- branch: hold/triaxial-december-cleanreimpl
- scope: operational note only

## Closure

The current triaxial diagnostic thread is closed until December 2026.

Priority remains:

1. C1b
2. C1d / D
3. manuscript

No further triaxial design, certification architecture, or manuscript claim is to be advanced before December unless this hold is explicitly changed.

## Current treatment of the splitting numbers

The existing repository-side values `+1.18 / -1.29` are left unchanged for now and are to be interpreted only as finite one-sided secant values, not as the derivative at `delta = 0`.

The clean re-implementation and its JSON diagnostic receipt record the symmetry relation

`Q1(delta) = Q2(-delta)`

under the `a1 <-> a2` exchange. Therefore, at `delta = 0`, the true derivatives are exactly antisymmetric:

`dQ1/ddelta = -dQ2/ddelta`.

The central-difference diagnostic value retained for December is approximately

`(+1.2345, -1.2345)`.

The unequal one-sided values arise from finite-step curvature contamination and do not change the qualitative conclusion about the order of the two principal-axis absorptions.

## Single December carryover item

At the first triaxial commit in December, include both of the following in the same change:

- an explicit note that the historical `+1.18 / -1.29` numbers are one-sided secant values;
- the central-difference diagnostic value `+/-1.2345` together with the exact antisymmetry statement from `a1 <-> a2` symmetry.

Until that commit, do not rewrite the historical repository values.

## Evidence location

The numerical basis for this correction is the clean re-implementation JSON and script stored in this branch under `research_hold/clean_reimplementation/`.

This note is not theorem evidence, not a certification receipt, and not a manuscript claim.
