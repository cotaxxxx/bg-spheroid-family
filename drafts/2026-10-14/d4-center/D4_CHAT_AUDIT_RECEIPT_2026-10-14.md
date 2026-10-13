# D4 chat audit receipt — 2026-10-14

Status: USER-RELAYED CHAT AUDIT PASS for phase-A Appendices A/B.
This receipt records the user's audit report supplied in this conversation at
2026-10-14 05:53:57 JST. It is not a Codex-local SymPy execution receipt.
No raw execution log or environment/version manifest was supplied.

## Audited objects

- D4_PHASE_A_INDEPENDENT_DERIVATION.md, SHA-256
  5271d5d89626f1db18939b3d3dae5547cbc12d35168ad26fb4765211aaaa55d1.
- d4_phase_a_independent.py, SHA-256
  4b8fe0c9a7368ad758be70aa79a6e86a1a91960b3fc79939d3019f266e300653.
- These are Appendices A/B of D4_PLAN_A_DERIVATION_AND_AUDIT_ADDENDUM_V0.md,
  SHA-256 1ec1ad9779041228ee0f440c9adf25e49a2cd3fd23420220a70f9959c5ae71e9.

## Checks reported PASS by chat

1. The d1–d4 homogeneous terms agree with the direct t expansion, difference zero.
2. The F[4] decomposition agrees with direct expansion of h G(gamma), difference zero.
3. C4=166496/105; 16 C4<25600; the distance/normalization bound;
   z<=264 r/1625<r/6; loss 325/1152; margin 5629/155520;
   L(119/200)=610465550029/1200000000000.
4. Integral bounds |R''|<=32/15 and |R'''|<=192/35.
5. Separate evenness, two second-order Taylor remainders, and the s integral give
   H>=H0-M40 rho^2/6-M22 z^2/2.
6. The fourth-order polarization identity and degree-four homogeneity justify
   M22=25600 from the directional bound.
7. Affinity of h, Leibniz, Legendre bounds, and chain-rule coefficients
   16/128/240/96 agree with an independent derivation.
8. gamma>=0 follows from h>0 in the interior (Lemma 3.1), so the R-integral
   denominator lower bound applies.

## Adopted conditional paper lemma

Conditional on the P1 Lemma V bundle and the prior proof D>=833/1600,

    H >= 5629/155520 > 0

on the full closed patch r in [0,1/128], tau in [0,1/8],
lambda in [119/200,33/50]. This is a paper lemma; no B_003 discharge is declared.
The centre itself is stationary by symmetry. H0>0 is transverse curvature,
not exclusion of the central stationary point. For r>0 in this box, rho>0 and
E_rho=rho H>0 excludes a meridional stationary point.

## Correction and provenance

The instruction to use L>=0.509 is withdrawn. Use the exact fraction above,
or the downward rational 127/250. Do not use 509/1000 as a lower bound.
Claude Code's original L expression remains unavailable for comparison.

The user clarified that 07db380e and 74f0608e are prefixes of hashes of files
inside a Claude Code session, not Git commits. Their full hashes and contents
are not available here. No further Git commit lookup is needed for those IDs.
They are not pinned evidence and no fourth-order cross-comparison is claimed.
Historical independent derivation remains SELF-REPORTED.
Committing a file now records its current archival submission; by itself it
cannot retroactively prove that the old derivation preceded access to another
document. That would require the historical ordering record as well.

## Scope boundary

The new centre coefficient bound (23,18), its algebra script, and its analytic
mu-integral majorants were developed after this chat audit and are NOT covered
by this PASS. They require a separate chat audit.

