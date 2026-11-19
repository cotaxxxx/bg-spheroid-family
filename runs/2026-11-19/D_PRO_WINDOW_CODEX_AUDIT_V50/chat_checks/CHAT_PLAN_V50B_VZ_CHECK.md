# chat V50-B V/Z leaf check (new plan version, fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Plan V50 (G4 kernel with 1/d^2 terms) cannot enclose E_z/E_zz by cell ranges (odd near-singular terms lose their
cancellation; pre-run tests gave NaN and -6.4). Plan B keeps the same sample (seed 50, 3 weakest + 10/6 random)
but uses bounded kernels, implemented by chat from the formulas (validated numerically against chat's E_ref first):
- V: E_z = (1/2pi) int_{-1}^1 int_0^pi [mu J(g) - lam sqrt(B) u_z K(g)] dphi dmu,  J = gP - arccos^2 g, K = g^2 P,
  u_z = lam (mu - z)/D,  D^2 = A + lam^2 (mu-z)^2, A = (s-rho)^2 + 2 rho s (1 - cos phi).
  mu: 256 cells, cells within 1/8 of the z-range split 16-fold; phi: 48 cells.
- Z: E_zz by the chord formula (3)-(4) (i = z), average over m in [0,1], psi in [0,pi]; per-side signed upper/lower and
  the w_+ + w_- = 1 combination (lower bound version); m 512 cells, psi 64 cells.
- P lower/upper from the positive h-series with tail; Q = 2P + gP'' bounds likewise; arccos by arb.
- Bisection depth <= 4 (largest of dl, 4 dr, 4 dz). Confirmed iff all children have lower > 0.

Amendment B1 (implementation only): run 1 produced NaN in V leaves — arb acos of a ball whose radius overshoots 1.
arccos is now evaluated from the clipped endpoints [acos(min(hi,1)), acos(max(lo,0))]. Run 1 output kept
(vz_check_B_run1_acos_nan.jsonl). Sample, grids, rule unchanged.
Amendment B2 (implementation only): one random V leaf (near contact, |q|^2 up to 0.974) returned NaN because the arb
power (s - rho)**2 produced a ball reaching below 0, making D^2's lower end non-positive. (s - rho)^2 is now enclosed
from endpoints (sq()). Only that leaf is rerun with the same rule; the other 21 results stand (the change can only
tighten them).
Amendment B2b: the cause is arb ball (midpoint-radius) squaring of wide balls, not interval squaring; (mu - z)^2 in D^2
is also enclosed from endpoints with sq(). Still a valid (looser-than-needed before) enclosure; only that leaf rerun.
