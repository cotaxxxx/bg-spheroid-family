# Research Status

## Repository status

**ASSEMBLY / NOT_BINDING**

`bg-spheroid-family` is the integration layer for the volume-preserving prolate–sphere–oblate manuscript. It does not issue certificates.

## Claim classes

Use the following labels consistently in notes, tables, and manuscript drafts.

### CERTIFIED_UPSTREAM

A statement proved or interval-certified by immutable upstream evidence and referenced through a verified entry in `UPSTREAM_PINS.md`.

### EXACT_ANALYTIC

A statement established analytically in the manuscript or a cited mathematical source and not dependent on numerical certification.

### HIGH_PRECISION_CANDIDATE

A numerical value or structural observation supported by high-precision computation but not yet covered by binding certification.

### DIAGNOSTIC_ONLY

A computation, plot, exploratory script, cross-check, or repository state that is useful for research but is not evidence for a theorem.

### OPEN

A claim or global exclusion statement not yet established at the required level.

## Current synthesis target

Construct a single phase diagram for the stationary-point structure of the basepoint functional along the constant-volume family

`prolate -> sphere -> oblate`.

The synthesis should distinguish:

- local bifurcation statements from global completeness statements;
- exact analytic results from interval-certified results;
- certified upstream evidence from diagnostic calculations;
- the sphere's enhanced symmetry from the two nonspherical regimes.

## Promotion discipline

No claim may be marked `CERTIFIED_UPSTREAM` until its upstream evidence has been entered and verified in `UPSTREAM_PINS.md`.

No result is promoted merely because the same numerical value appears in multiple repositories or manuscript drafts.
