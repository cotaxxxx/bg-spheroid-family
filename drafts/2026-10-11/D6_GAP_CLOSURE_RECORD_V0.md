# D6 GAP CLOSURE RECORD V0

**Date:** 2026-10-11  
**Status:** `DRAFT / SUBMITTED FOR CHAT+CODE AUDIT / D6 REMAINS CONDITIONAL`  
**Objects:**
- EL = `analysis/OBLATE_ENDPOINT_C1_LEMMA.md`, blob `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`, 109 lines.
- C2 = `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md`, blob `7cb9b8091596510203d74e09387bc1e8188b8b47`, 250 lines.
- Both source blobs are in `bg-oblate-spheroid`, `design/d-ob-p2` at `bbcfe662` and are **not modified** by this record.

**Precondition checked before drafting.** The Judge-confirmed save is on `bg-spheroid-family` main at `e63fd68e76a5737904d39f665c4af6d900c6803b`, containing STATE v1.17 (`45841924…2f09`), ruling record `97860a25…87f5`, chat review `a2804dae…cc41`, Code report `6d83cba5…fe9e`, and Code addendum `587e617c…b076`.

**Authority for the item list.** `audits/CHAT_REVIEW_CODE_D6_REPORT_AND_ADDENDUM_2026-10-11.md`, SHA-256 `a2804dae0a9951a8d761159318c33656788b3044943d34188121845c702acc41`, §3.

This is a closure **record**, not an edit of EL or C2. Wherever a source line is too broad or omits an endpoint convention, the subsection below states the exact reading that is to accompany that line if this record passes audit. No computation, certificate generation, producer/checker run, or source-file change was performed.

---

## 1. E-G1 — value of `R` at `gamma = 1`

### (a) Source lines
EL L13–17 defines `gamma`, `alpha`, and `R = alpha/sin(alpha)`. EL L42 uses `1 <= R <= pi/2`; EL L52 differentiates through the `gamma = 1` locus; EL L93 again uses `R` in the endpoint limit.

### (b) Reading
For `0 <= u <= 1`, define

\[
\Psi(u)=\frac{\arcsin\sqrt u}{\sqrt u}\quad(u>0),\qquad \Psi(0)=1.
\]

On the branch `0 <= gamma <= 1`, read

\[
R:=\Psi(1-\gamma^2).
\]

For `gamma < 1` this equals `alpha/sin(alpha)`; at `gamma = 1` it gives the continuous value `R=1`.

### (c) Proof
Put `u=1-gamma^2`. For `0 <= gamma < 1`, `alpha=arccos(gamma)=arcsin(sqrt(u))` and `sin(alpha)=sqrt(u)`, hence

\[
\frac{\alpha}{\sin\alpha}=\frac{\arcsin\sqrt u}{\sqrt u}=\Psi(u).
\]

The standard Taylor expansion `arcsin x = x + x^3/6 + O(x^5)` gives `Psi(u)=1+u/6+O(u^2)`, so `Psi(u)->1` as `u->0+`. Thus the removable singularity at `gamma=1` is filled by `R(1)=1`. This also justifies every EL use of `R` across `gamma=1`.

**Closure:** CLOSED, subject to audit of this record.

---

## 2. E-G2 — range of EL Lemma 1

### (a) Source lines
EL L31 states Lemma 1 as `For t < 1`; EL L33 proves `A>0` and `gamma>0`. The dependent majorant is explicitly scoped to `t in [1/2,1)` at EL L35–46; Lemma 3 is scoped to the same interval at EL L50–54.

### (b) Reading
EL Lemma 1 is to be read on

\[
t\in[0,1),
\]

and in every actual use in EL/C2 it is used only on the smaller ranges `t in [1/2,1)` or `t in [63/64,1)`.

### (c) Proof
With `mu in [-1,1]`,

\[
A=1-t\mu.
\]

If `0 <= t < 1`, then `A >= 1-t > 0`. Equivalently, with `delta=1-t` and `s^2=1-mu`,

\[
A=\delta+t s^2,
\]

where `delta>0` and `t s^2>=0`. The original phrase `t<1` is too broad: for example `t=-1`, `mu=-1` gives `A=0`, so the proof of strict positivity does not hold on all of that stated range.

All uses are nevertheless inside the corrected range: EL Lemma 2 is `[1/2,1)` (L35), EL Lemma 3 is `[1/2,1)` (L50), and C2's near-boundary tube is `[63/64,1)` (C2 L104–110, L203–212). Thus narrowing Lemma 1 to `[0,1)` changes no downstream conclusion used by ① or ②.

**Closure:** CLOSED, subject to audit of this record.

---

## 3. E-G3 — endpoint `t = 1/2` is one-sided

### (a) Source lines
EL L35 gives the common majorant only for `t in [1/2,1)`. EL L50 states `g_axis_ob(t,lambda)=partial_t E_lambda(t)=integral F_t ds` on `[1/2,1)`, and EL L52 proves it by dominated differentiation.

### (b) Reading
At `t=1/2`, the proof in EL establishes the **right derivative**

\[
\partial_t^+E_\lambda(1/2)=\int_0^{\sqrt2}F_t(s,1/2,\lambda)\,ds.
\]

For `1/2<t<1`, `partial_t E_lambda(t)` is the ordinary two-sided derivative.

### (c) Proof and exhaustive check of uses in ①/②
Dominated differentiation on a half-interval gives the derivative in directions that remain in that half-interval; therefore at its left endpoint the conclusion is one-sided unless an additional left-neighbourhood majorant is supplied.

The uses in ① and ② are as follows.

1. **①, X region.** The only explicit monotonicity interval whose left endpoint is `t=1/2` is the X step `partial_t g < 0 on [1/2,5/8]` (the same point is recorded in the pinned chat review `a2804dae`, L20). To conclude that `g` is strictly decreasing on the closed interval, one needs `g` continuous on `[1/2,5/8]` and `partial_t g<0` only for interior points `t in (1/2,5/8)`. The mean-value theorem is applied between two points `a<b`; its derivative point lies in `(a,b)`, never at `a=1/2`. Thus no two-sided derivative at `1/2` is required.
2. **①, L region.** The L path certifies `g<0`; it does not use a derivative at `t=1/2`.
3. **①, R region.** `g(1/2,lambda)>0` is a sign input. The tube condition `partial_t g<0` is used for uniqueness/monotonicity of an interior root in `t>1/2`. If a closed enclosure box touches `t=1/2`, the theorem still uses the derivative only on its open interior; the endpoint contributes only the value/continuity of `g`.
4. **①, endpoint strip.** The cumulative endpoint argument begins at `t=31/32`, so it does not use `t=1/2`.
5. **②.** For every unclamped slab, `t_*=max(31/32,t_+)`, so every derivative/endpoint box lies at `t>=31/32`. There is no use of `partial_t g` at `t=1/2`.

Therefore the one-sided reading at `t=1/2` is sufficient for every ①/② use.

**Closure:** CLOSED, subject to audit of this record.

---

## 4. E-G4 — continuity of `g` on `[1/2,1)`

### (a) Source lines
EL L50–52 gives `g=integral F_t ds` and the integrable majorant; EL L91–93 asserts continuity on `[1/2,1]` after adjoining the endpoint value but spells out only the limit at `t=1`.

### (b) Reading
For each fixed `lambda in I`, `g_axis_ob(·,lambda)` is continuous on `[1/2,1)` by dominated convergence, and EL Lemma 5 then extends that continuity to `t=1`.

### (c) Proof
Fix `t_0 in [1/2,1)`. For each fixed `s>0`, the quantities `A,q,gamma,gamma_t` are continuous in `t` near `t_0`; `q>0` there. At `gamma=1`, Item 1 supplies the continuous `Psi` reading of `R`, so `F_t(s,t,lambda)` is continuous in `t`. The exceptional point `s=0` is null for the integral and in fact the outer factor `s` gives the natural continuous value there.

EL Lemma 2 supplies a single integrable function `M(s)` such that

\[
|F_t(s,t,\lambda)|\le M(s)
\]

for every `t in [1/2,1)`. Hence for any sequence `t_n -> t_0` from within the interval, dominated convergence gives

\[
g(t_n,\lambda)=\int F_t(s,t_n,\lambda)\,ds
   \longrightarrow
\int F_t(s,t_0,\lambda)\,ds=g(t_0,\lambda).
\]

At `t_0=1/2` this is right continuity; at interior points it is ordinary continuity. EL Lemma 5 separately gives the limit at `t=1`.

**Closure:** CLOSED, subject to audit of this record.

---

## 5. C-G1 — pin the premise of C2 L50

### (a) Source lines
C2 L50 says `g_axis_ob(t,lambda)=integral F_t ds` by an "already established C1-level differentiation argument" without a pin. C2 L221 later uses endpoint continuity. EL L50–54 is Lemma 3; EL L91–93 is Lemma 5; EL L103 explicitly records that these are the premises invoked by C2.

### (b) Reading
The exact premise is:

- `OBLATE_ENDPOINT_C1_LEMMA`, blob `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`, **Lemma 3**, EL L50–54, for the interior representation; and
- the same blob, **Lemma 5**, EL L91–93, for continuity at `t=1`.

For C2, take `I=[5/8,33/50]`, which is allowed by EL L5 because `33/50 < 1/sqrt(2)`.

### (c) Proof of range compatibility
C2 needs the representation only on `t in [63/64,1)`, which is contained in EL Lemma 3's `[1/2,1)`. It needs endpoint continuity on the same lambda interval, exactly supplied by EL Lemma 5. Therefore the pinned premises cover the entire C2 use without extending either lemma beyond its stated scope.

**Closure:** CLOSED, subject to audit of this record.

---

## 6. C-G2 — continuous definition of `R_gamma`

### (a) Source lines
C2 L57 writes `R_gamma=(gamma R-1)/(1-gamma^2)`; C2 L92 uses `R_gamma` in `T2`; C2 L140–146 bounds it; C2 L191–199 mentions the `Psi/Psi_prime` continuous extension only later in §5.

### (b) Reading
Throughout C2 §§2–4, define

\[
R_\gamma:=-2\gamma\,\Psi'(1-\gamma^2),
\]

with `Psi` as in Item 1. For `gamma<1` this equals the quotient in C2 L57. At `gamma=1`, define

\[
R_\gamma(1)=-\frac13.
\]

### (c) Proof
Since `R(gamma)=Psi(1-gamma^2)`, the chain rule gives

\[
\frac{dR}{d\gamma}=-2\gamma\Psi'(1-\gamma^2).
\]

For `gamma<1`, differentiating `R=alpha/sin(alpha)` with `gamma=cos(alpha)` gives the algebraically equivalent formula

\[
R_\gamma=\frac{\gamma R-1}{1-\gamma^2}.
\]

From `arcsin x=x+x^3/6+O(x^5)`,

\[
\Psi(u)=1+\frac{u}{6}+O(u^2),\qquad \Psi'(0)=\frac16.
\]

Hence at `gamma=1`,

\[
R_\gamma(1)=-2\cdot1\cdot\frac16=-\frac13.
\]

Thus `R_gamma` has a continuous value at every `gamma=1` locus used in §§2–4.

**Closure:** CLOSED, subject to audit of this record.

---

## 7. C-G3 — proof of `|H| <= 4`

### (a) Source lines
C2 L46–47 defines `H`; C2 L128–132 invokes `|H|<=4` as a previously established bound without a source.

### (b) Reading
For `s in [0,1]`, put `x=s^2`. For `delta in [0,1]` and `lambda<=lambda_+<1`,

\[
|H|\le 2+2\lambda_+^2<4.
\]

### (c) Proof
C2 L46–47 can be rewritten as

\[
H=(1-x)(2-x)+\lambda^2(2-x)(x-\delta),
\]

because `2x-2delta-x^2+delta x=(2-x)(x-delta)`. On `x,delta in [0,1]`,

\[
|(1-x)(2-x)|\le 2,
\qquad
|(2-x)(x-\delta)|\le 2\cdot1=2.
\]

Therefore

\[
|H|\le 2+2\lambda^2\le 2+2\lambda_+^2<4,
\]

since `lambda_+=33/50<1` in C2 §4.

**Closure:** CLOSED, subject to audit of this record.

---

## 8. C-G4 — proof of `-1 <= R_gamma <= 0`

### (a) Source lines
C2 L57 defines the quotient formula for `R_gamma`; C2 L140–146 uses `-1 <= R_gamma <= 0` without proof.

### (b) Reading
For `0<=gamma<=1`, with the continuous extension at `gamma=1` from Item 6,

\[
-1\le R_\gamma\le0.
\]

### (c) Proof
First take `0<=gamma<1` and set `gamma=cos(alpha)`, `alpha in (0,pi/2]`, `R=alpha/sin(alpha)`.

For the lower bound,

\[
R_\gamma+1
=\frac{\gamma R-1+1-\gamma^2}{1-\gamma^2}
=\frac{\gamma(R-\gamma)}{1-\gamma^2}.
\]

Here `gamma>=0`, while `R>=1` because `sin(alpha)<=alpha`, and `gamma<=1`; hence `R-gamma>=0`, so `R_gamma>=-1`.

For the upper bound, `R_gamma<=0` is equivalent to `gamma R<=1`, or

\[
\alpha\cos\alpha\le\sin\alpha.
\]

Let `f(alpha)=sin(alpha)-alpha cos(alpha)`. Then

\[
f(0)=0,
\qquad
f'(alpha)=alpha\sin(alpha)\ge0
\]

on `[0,pi/2]`. Thus `f(alpha)>=0`, proving `R_gamma<=0`.

At `gamma=1`, Item 6 gives `R_gamma=-1/3`, which lies in `[-1,0]`; continuity closes the endpoint.

**Closure:** CLOSED, subject to audit of this record.

---

## 9. C-G6 — continuity of `partial_t g` before the fundamental theorem of calculus

### (a) Source lines
C2 L203–212 obtains `partial_t g = integral G_t ds` on `[63/64,1)`; C2 L214–219 gives its finite limit as `t->1-`; C2 L221–236 invokes the fundamental theorem of calculus to identify the one-sided derivative at `t=1`.

### (b) Reading
For each fixed `lambda in [5/8,33/50]`, `partial_t g_axis_ob(·,lambda)` is continuous on `[63/64,1)`. Hence the fundamental theorem of calculus applies on every compact interval `[a,b]` with `63/64<=a<b<1`, and the passage `b->1-` is justified by the endpoint continuity of `g` and the finite limit of `partial_t g`.

### (c) Proof
For fixed `s` and `t<1`, `q>0`. The algebraic factors in `G_t` are continuous in `t`; Items 1 and 6 make `R` and `R_gamma` continuous through every `gamma=1` locus. Thus `G_t(s,t,lambda)` is continuous in `t` for each fixed `s`.

C2 §§4–5 provide an integrable majorant independent of `t` on the whole near-boundary interval. Therefore, if `t_n->t_0<1`, dominated convergence gives

\[
\partial_tg(t_n,\lambda)
 =\int G_t(s,t_n,\lambda)\,ds
 \longrightarrow
 \int G_t(s,t_0,\lambda)\,ds
 =\partial_tg(t_0,\lambda).
\]

So `partial_t g` is continuous on `[63/64,1)`. For `a<b<1`, the ordinary fundamental theorem gives

\[
g(b,\lambda)-g(a,\lambda)=\int_a^b\partial_tg(u,\lambda)\,du.
\]

Now let `b->1-`. EL Lemma 5 supplies `g(b,lambda)->g(1,lambda)`, while C2 L214–219 supplies a finite limit `L(lambda)` for `partial_t g`. Hence

\[
g(1,\lambda)-g(a,\lambda)=\int_a^1\partial_tg(u,\lambda)\,du,
\]

and averaging over `[a,1]` and sending `a->1-` gives the limit `L(lambda)`, exactly as asserted in C2 L223–233.

**Closure:** CLOSED, subject to audit of this record.

---

## 10. C-G5 — note: no explicit positive lower bound on `gamma` is required

### (a) Source lines
C2 L191–199 treats the south set `s in [1,sqrt(2)]`, `t in [63/64,1]`, `lambda in [5/8,33/50]` and invokes continuity through the internal `gamma=1` locus.

### (b) Reading
No separately derived numerical lower bound for `gamma` is needed. On the south compact set, `gamma` is continuous and takes values in `(0,1]`; `R` and `R_gamma` are continuous on `(-1,1]`. Consequently their restrictions to the image of that compact set are bounded.

### (c) Proof / note
On `s>=1`, `mu=1-s^2<=0`, and for `t in [63/64,1]`,

\[
A=1-t\mu\ge1>0.
\]

C2 L185–188 gives `q>0`, and `w>0`, `lambda>0`; hence

\[
\gamma=\frac{\lambda A}{w\sqrt q}>0.
\]

The identity `1-gamma^2>=0` gives `gamma<=1`. Thus the continuous map `gamma` sends the compact south set into `(0,1]` (indeed into a compact subset of it).

For `-1<gamma<1`, `R(gamma)=arccos(gamma)/sqrt(1-gamma^2)` is analytic. Items 1 and 6 give the continuous extensions `R(1)=1` and `R_gamma(1)=-1/3`. Therefore both `R` and `R_gamma` are continuous on `(-1,1]`, in particular on the south image. Boundedness follows without an explicit lower-bound constant for `gamma`.

This item is retained for traceability but, per the Code post-collation self-correction accepted by chat, it is a **NOTE**, not a remaining mathematical GAP.

**Closure:** NOTE.

---

## 11. ChatGPT note 2 — the north set is half-open at the corner `(s,t)=(0,1)`

### (a) Source lines
C2 L148 calls the domain a "compact north rectangle"; C2 L151–175 then gives uniform bounds on `s in [0,1]`, `t in [63/64,1)`, `lambda in [5/8,33/50]`. At `(s,t)=(0,1)`, the formula in C2 L28 has `q=0`, so the scaled variables of C2 L72–78 are not defined there.

### (b) Reading
The north majorant argument is on

\[
s\in[0,1],\qquad t\in[63/64,1),\qquad
\lambda\in[5/8,33/50],
\]

not on a closed rectangle including `(s,t)=(0,1)`. The point `(0,1)` is excluded. All bounds are **uniform for `t<1`** and therefore remain valid as `t->1-`.

### (c) Proof
If `t<1`, then `delta=1-t>0`. At `s=0`,

\[
q=\lambda^2\delta^2>0,
\]

so the scaled variables are defined. For `s>0`, the first term `s^2(2-s^2)` is positive on the north half, so again `q>0`. Thus the scaled identity is valid at every point actually used in §4.

The estimates `0<=rho<=1`, `|phi|<=1/lambda_-`, `|Ahat|<=2+1/lambda_-`, `w>=lambda_-`, `|H|<4`, `-1<=R_gamma<=0`, and `q<=2` have constants independent of `t`; none requires a positive lower bound on `1-t`. Hence the resulting `M_N` is uniform as `t->1-`. At the single excluded corner `q=0`, no value of the scaled variables is needed; the endpoint is reached later by pointwise limits for `s>0` and dominated convergence in C2 §6.

The word "compact" in C2 L148 should therefore be read as shorthand for this uniformly controlled half-open north tube, not as inclusion of the singular corner.

**Closure:** CLOSED, subject to audit of this record.

---

## Final closure table

| # | Item | Proposed status in this record |
|---:|---|---|
| 1 | E-G1 | CLOSED |
| 2 | E-G2 | CLOSED |
| 3 | E-G3 | CLOSED |
| 4 | E-G4 | CLOSED |
| 5 | C-G1 | CLOSED |
| 6 | C-G2 | CLOSED |
| 7 | C-G3 | CLOSED |
| 8 | C-G4 | CLOSED |
| 9 | C-G6 | CLOSED |
| 10 | C-G5 | NOTE |
| 11 | ChatGPT note 2 | CLOSED |

No item is marked OPEN in this draft. This table does **not** itself promote D6: until chat and Code audit this record and the Judge accepts that audit, the project state remains `D6 = CONDITIONAL / GAP-CLOSURE PENDING`.

C2 §7 item 5 / G0/E1 §5 (machine producer/checker enclosing the same `G_t`, record `50ca0315`) is intentionally untouched and remains outside the scope of this closure record.
