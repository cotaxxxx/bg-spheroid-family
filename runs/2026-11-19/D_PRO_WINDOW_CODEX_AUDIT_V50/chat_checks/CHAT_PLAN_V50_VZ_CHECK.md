# chat V50 V/Z leaf check plan (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Purpose: chat's own independent Arb enclosure of E_z (V leaves) and E_zz (Z leaves) on sampled leaves of Codex's
window package (ZIP sha256 66a71b7c...), with a DIFFERENT kernel from Codex's (2)/(3):
- E_z = (1/2pi) int_{-1}^{1} int_0^pi I dphi dmu,  I = mu(F + g F') - k g F' w/d^2   (V43 (G4); general rho)
- E_zz = (1/2pi) int int d_z I,  d_z I = [mu Q - V(F' + g F'')] eps(-mu+V)/(sqrt(B) d) - g F' (-mu w/d^2 - k/d^2 + 2 k w^2/d^4)
  (V46/V47 form with d^2 = w^2 + eps^2 A, A = s^2 + rho^2 - 2 rho s cos phi; V = k w/d^2), reference z.
- F via arb acos; F', F'' via the positive h-series (h=(1-g)/2, 24 terms) with geometric tail bounds; Q = 2F' + gF''.
- Cells: mu in [-1,1] 256 equal cells, phi in [0,pi] 48 cells; lower bound = sum of interval lower ends x cell measure.
- Sample: the 3 weakest V and 3 weakest Z leaves (by Codex's stored lower end), plus 10 V and 6 Z leaves drawn uniformly
  (Python random, seed 50) from the positive leaves.
- If a leaf's lower bound is <= 0: bisect the leaf (largest of dl, 4 dr, 4 dz), depth <= 4. Confirmed iff all children > 0.
- A leaf left unconfirmed is reported as "undecided by chat's method" (not a counterexample) together with a
  non-interval mpmath value of E_z or E_zz at its centre.

## Amendment 1 (before the sampled run; recorded after two pre-run test evaluations on the weakest V and Z leaf)
The pre-run test returned "no positive denominator" for the weakest V leaf (A = s^2 + rho^2 - 2 rho s cos phi loses its
positivity under interval wrapping) and a lower bound -6.89 for the weakest Z leaf (cells too coarse near mu = z).
Changes: A = (s - rho)^2 + 2 rho s (1 - cos phi); mu-cells within 1/8 of the leaf's z-range are split 16-fold
(cell measure carried exactly). Sample, seed, bisection rule and criterion are unchanged.
