# CHATGPT D6 LEMMA AUDIT REPORT V0 — 2026-10-11

**Auditor:** ChatGPT  
**Audit class:** `CROSS_LINEAGE_AI_AUDIT / NON_BLIND`  
**Mode:** READ-ONLY / paper re-derivation only  
**Numerical computation:** none  
**Symbolic-computation script:** none  
**Implementation / producer / checker execution:** none  
**Commit / push:** none

## 0. Instruction and source pins

Instruction read and SHA-256 checked:

- `drafts/2026-10-11/CHATGPT_D6_LEMMA_AUDIT_INSTRUCTION_2026-10-11.md`
- SHA-256: `d757dfb48084ab2efc8a6eb252c38dbbd2b5135826768f1f3c91255bbb20bf3d`
- `bg-spheroid-family` main: `32060ca5aadbfad5697d89b6c33323cfdc628428` (STATE v1.16)

The target branch was checked read-only at:

- `bg-oblate-spheroid` `origin/design/d-ob-p2` = `bbcfe6628a074d1f7b48e1f818542ee205e88f50`

The two target blobs match exactly:

| target | path | required blob | observed blob | result |
|---|---|---|---|---|
| endpoint lemma | `analysis/OBLATE_ENDPOINT_C1_LEMMA.md` | `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6` | same | MATCH |
| C2 interchange lemma | `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md` | `7cb9b8091596510203d74e09387bc1e8188b8b47` | same | MATCH |

## 1. Independence disclosure

This is a cross-lineage audit, but not a blind audit. Before this audit I had already seen, in this research chain, material including:

- `CHAT_AUDIT_C_GAP1_V4_AND_G0_V0_2026-10-10.md`;
- `CHAT_AUDIT_C_GAP1_IMPL_DESIGN_V2_2026-10-10.md`;
- `CHAT_REVIEW_OF_CODE_AUDIT_C_GAP1_V6_2026-10-10.md`;
- `CHAT_AUDIT_C_GAP1_V7_2026-10-11.md`;
- the existence/result of the earlier `c2id` symbolic identity check;
- my own earlier `G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md` work.

None of those PASS conclusions is used below as a premise. Every PASS below was re-derived from the two target lemma texts themselves, together with elementary algebra/calculus and the geometric definitions explicitly cited by the endpoint lemma. G0/E1 v3 is **not audited here** because I was its drafter.

---

# Part A — OBLATE_ENDPOINT_C1_LEMMA (`5afa815f`)

## A1. §1 definitions, change of variables, and normalization — PASS

**Lines 13–26.**

The definitions are mutually consistent. For the boundary parametrization

`x(mu,theta)=(sqrt(1-mu^2) cos theta, sqrt(1-mu^2) sin theta, lambda mu)`,

one has

- `dA = w dmu dtheta`, with `w^2=lambda^2(1-mu^2)+mu^2`;
- the outward-unit-normal dot product `(x-p).nu = lambda A/w`;
- `3 Vol(K_lambda)=4 pi lambda` because the semiaxes are `(1,1,lambda)`.

Therefore the cone measure is

`dmu_K,p = A/(4 pi) dmu dtheta`,

and integration over `theta in [0,2pi]` gives exactly

`E_lambda(t)=(1/2) integral_{-1}^1 A alpha^2 dmu`.

Under `mu=1-s^2`, `dmu=-2s ds`, the factor `1/2` cancels the Jacobian factor `2`, giving

`F=s A alpha^2` on `s in [0,sqrt 2]`.

Also `A_t=-mu`, `q_t=2 lambda^2 d`, hence

`gamma_t = lambda[-mu q-lambda^2 A d]/(w q^(3/2))`,

and differentiating `alpha^2` gives `-2R gamma_t` with the continuous value at `alpha=0`. Thus the stated `F_t` is correct.

## A2. Lemma 1(i): `N=-s^2 H` — PASS

**Lines 31–33.**

Put `x=s^2`, `mu=1-x`, `d=x-delta`. Directly,

`mu d + A = x(2-x)`.

Therefore

`N=-mu[x(2-x)+lambda^2 d^2]-lambda^2 A d`

`  =-x(2-x)[mu+lambda^2 d]`

`  =-x H`.

The displayed form of `H` is exactly `(2-x)[(1-x)+lambda^2(x-delta)]` expanded. PASS.

## A3. Lemma 1(ii): positivity of `q` — PASS

**Lines 31–33.**

For `0<s<sqrt 2`, `s^2(2-s^2)>0`. At `s=0`, `q=lambda^2 delta^2>0` because `t<1`; at `s=sqrt 2`, `q=lambda^2(2-delta)^2>0`. No zero remains on the stated pre-limit scope.

## A4. Lemma 1(iii): `0<gamma<=1` — PASS

**Lines 31–33.**

`A=delta+(1-delta)s^2>0`, so `gamma>0`. Independently expanding

`w^2 q-lambda^2 A^2`

gives

`(1-mu^2)[mu(1-lambda^2)+lambda^2 t]^2`.

Since the denominator `w^2 q` is positive, this proves the displayed identity for `1-gamma^2` and hence `gamma<=1`.

## A5. Lemma 2, north-half majorant — PASS

**Lines 35–44.**

From `alpha in [0,pi/2]`, one has `alpha^2<=pi^2/4` and, with the continuous value at `alpha=0`, `1<=R<=pi/2`. Thus

`|F_t| <= s(pi^2/4 + pi |A gamma_t|)`.

On `s in [0,1]`:

- `|H| <= 2+2lambda_+^2<4`;
- `q>=s^2+lambda_-^2 d^2`;
- `A<=delta+s^2<=|d|+2s^2`.

With `z=lambda_-|d|/s`,

`s^2|d|/(s^2+lambda_-^2d^2)^(3/2)`

`= z/[lambda_-(1+z^2)^(3/2)]`.

The derivative of `z(1+z^2)^(-3/2)` vanishes at `z=1/sqrt 2`, where its maximum is `2/(3sqrt 3)`. The second term satisfies

`2s^4/(s^2+lambda_-^2d^2)^(3/2)<=2s`.

Combining these with `lambda<=lambda_+`, `w>=lambda_-`, and `|H|<4` gives exactly the north part of `M(s)` in lines 38–39.

## A6. Lemma 2, south-half majorant — PASS

**Lines 35–46.**

For `s in [1,sqrt 2]` and `t>=1/2`, `delta<=1/2`, so `d>=1/2` and

`q>=lambda_-^2/4`.

Moreover

- `|(1-x)(2-x)|<=1/4` on `x in [1,2]`;
- `0<=(2-x)(x-delta)<=(2-x)x<=1`;
- hence `|H|<=1/4+lambda_+^2<1`.

Using `A<=2`, `s^2<=2`, `w>=lambda_-`, `q^(3/2)>=lambda_-^3/8` yields

`|A gamma_t|<=32 lambda_+/lambda_-^4`,

which is exactly the south part of the majorant. The resulting `M` is integrable.

## A7. Lemma 3: differentiation under the integral — PASS

**Lines 48–54.**

The potentially delicate point is `gamma=1`. The identity from Lemma 1 gives

`1-gamma^2 = C(s,t,lambda) L(t)^2`,

where for fixed interior `s`, `L(t)=(1-lambda^2)mu+lambda^2t` is linear. Since

`Phi(u)=(arcsin sqrt u)^2`

has a power series in `u` at `u=0`, `alpha^2=Phi(1-gamma^2)` is smooth through the `gamma=1` locus. Away from that locus, direct differentiation gives `partial_t alpha^2=-2R gamma_t`; continuity extends the identity across it. At `s=sqrt 2`, `gamma=1` identically and both sides are zero.

Lemma 2 supplies an integrable, `t`-independent majorant for both `F` and `F_t`, so dominated differentiation applies. The stated representation of `g_axis_ob` follows.

## A8. §4 endpoint algebra — PASS

**Lines 58–73.**

At `delta=0`, direct substitution gives

- `A=s^2`, `d=s^2`;
- `q=s^2 qhat`, `qhat=2-(1-lambda^2)s^2`;
- `w^2=1-2as^2+as^4`, `a=1-lambda^2`.

The identities in lines 62 and 64 follow by expansion. Substituting `N=-s^2H` into `A gamma_t` and cancelling the `s^3` from `q^(3/2)` gives exactly line 63. The identity for `u=1-gamma^2` then follows from `w^2 qhat-lambda^2s^2`.

Because `gamma>=0`, `alpha=arcsin(sqrt u)` and `R=Psi(u)` on the endpoint branch, so the displayed `F_ob` is exactly the endpoint limit of `F_t`.

## A9. Lemma 4(i): north chart — PASS

**Lines 75–87.**

For `e=s^2 in (0,1]`,

`u/gamma^2 = h(e)/lambda^2`,

`h(e)=(2-e)(1-ae)^2/e`.

Writing `h'=n/e^2`, the numerator is

`n=-(1-ae)[2+2ae(1-e)]<0`.

Hence `h(e)>=h(1)=lambda^4`, so `u>=lambda^2 gamma^2`. Since `u+gamma^2=1`,

`gamma^2<=1/(1+lambda^2)`.

The endpoint `s=0` has the regularized value `gamma=0`. Thus the north chart stays uniformly away from `gamma=1`.

## A10. Lemma 4(ii)–(iii): south chart and bounded lambda derivative — PASS

**Lines 75–87.**

On `s in [1,sqrt 2]`, `w^2<=1`, `qhat<=2`, `s^2>=1`, hence

`gamma^2=lambda^2s^2/(w^2qhat)>=lambda^2/2`,

so `u<=1-lambda^2/2`. This keeps `Phi` and `Psi` a fixed positive distance from their singular endpoint `u=1` on `closure(J)`.

The internal zero of `u` is double because of `(1-as^2)^2`; `Phi` and `Psi` are analytic at `u=0`. The denominators satisfy `w^2>=lambda^2` and `qhat>=2lambda^2`, so both chart formulas and their `lambda` derivatives extend continuously to the closed rectangles. Their values coincide at `s=1`. Compactness therefore gives the required uniform bounds.

## A11. Lemma 5: one-sided limit and continuity — PASS

**Lines 89–93.**

For every fixed `s>0`, all pre-limit factors have the stated endpoint limits, including at the internal `gamma=1` locus because the `Phi/Psi` representations are continuous there. Lemma 2 supplies the common integrable majorant, so dominated convergence gives

`lim_{t->1-} g_axis_ob(t,lambda)=integral F_ob ds`.

Interior continuity of `g_axis_ob` follows from the same dominated-continuity argument applied to `F_t`; adjoining the one-sided limit gives continuity on `[1/2,1]`.

## A12. Lemma 6: lambda differentiation — PASS

**Lines 95–99.**

Lemma 4 gives an open `J` containing `I` on which `partial_lambda F_ob` is bounded on a compact rectangle. Thus the integral defines a `C^1` function on a neighborhood of `I`; restricting to `I` gives the stated formula, including one-sided interpretations at the endpoints of `I`.

## A13. Scope and §7 disclaimer — PASS

**Lines 5, 101–105.**

Every estimate above uses only

`0<lambda_-<=lambda_+<1/sqrt 2`, `t in [1/2,1)`.

Therefore both intended applications

- `I=[2/5,9/20]`, and
- `I=[2/5,5/8]`

fit the proved scope. Section 7 does not claim an integral sign, branch-zero identification, or anything below `t=1/2`; this is consistent with what was proved.

**Endpoint-lemma verdict: PASS.**

---

# Part B — MONOTONE_TUBE_C2_INTERCHANGE_LEMMA (`7cb9b809`)

## B1. §1 inherited pre-limit kernel — PASS

**Lines 19–50.**

The definitions agree with the endpoint lemma. Expanding

`(2-s^2)(1-s^2+lambda^2(s^2-delta))`

gives exactly the displayed `H`. The representation `g_axis_ob=integral F_t ds` is within the endpoint lemma's scope because `[63/64,1)` is contained in `[1/2,1)` and `[5/8,33/50]` satisfies `lambda_+<1/sqrt 2`.

## B2. §2 formal second derivative — PASS

**Lines 52–68.**

For `R=acos(gamma)/sqrt(1-gamma^2)`, direct differentiation gives

`R_gamma=(gamma R-1)/(1-gamma^2)`

with its continuous limit at `gamma=1`.

From

`N=-mu q-A lambda^2d`, `q_t=2lambda^2d`, `A_t=-mu`, `d_t=1`,

one obtains

`N_t=-lambda^2(mu d+A)=-lambda^2s^2(2-s^2)`.

Differentiating `gamma_t=lambda N/(wq^(3/2))` gives

`gamma_tt=lambda^3s^2[3dH-(2-s^2)q]/(wq^(5/2))`.

Finally,

`partial_t[-mu alpha^2]=2mu R gamma_t`,

while differentiating `-2ARgamma_t` supplies a second identical `2mu R gamma_t` plus the two displayed negative terms. Hence the coefficient `4mu` and the entire formula for `G_t` are correct.

## B3. §3 scaled identities — PASS

**Lines 70–100.**

By definition,

`rho^2(2-s^2)+lambda^2phi^2=q/q=1`.

Also the identity from Part A,

`mu d+A=s^2(2-s^2)`,

rearranges to

`A=(2-s^2)s^2-(1-s^2)d`,

which divided by `sqrt(q)` gives the displayed formula for `Ahat`.

Substitution into each term of `G_t` gives exactly:

- `T1=-4(1-s^2)R lambda rho^3H/w`;
- `T2=-2R_gamma lambda^2H^2Ahat rho^5/w^2`;
- `T3=-2R lambda^3Ahat rho^3[3phi H-(2-s^2)sqrt(q)]/w`.

All explicit negative powers of `q` cancel. No symbolic-computation result is used for this check.

## B4. §4 bounds for `rho`, `phi`, `Ahat`, `w`, `H` — PASS

**Lines 102–132.**

On `s in [0,1]`, `2-s^2>=1`. From the scaled identity,

`rho^2<=1`, `lambda^2phi^2<=1`, hence

`0<=rho<=1`, `|phi|<=1/lambda_-`.

The `Ahat` identity gives

`|Ahat|<=2+1/lambda_-`.

Also `w^2=lambda^2+(1-lambda^2)mu^2>=lambda_-^2`.

Finally, with `x=s^2 in [0,1]` and `delta<=1/64`,

`|H|<=|(1-x)(2-x)|+lambda^2|(2-x)(x-delta)|<=2+2lambda_+^2<4`.

## B5. §4 bounds on `R` and `R_gamma` — PASS

**Lines 134–146.**

Write `gamma=cos alpha`, `alpha in [0,pi/2]`.

- `R=alpha/sin alpha>=1` because `sin alpha<=alpha`.
- `R<=pi/2` because `sin alpha>=2alpha/pi` on this interval.

For the derivative, the denominator of

`R_gamma=(gamma R-1)/(1-gamma^2)`

is nonnegative. The numerator is nonpositive because

`gamma R<=1 <=> alpha cos alpha<=sin alpha`,

and `sin alpha-alpha cos alpha` has derivative `alpha sin alpha>=0` and vanishes at `alpha=0`.

For the lower bound, `R>=1>=gamma` gives `gamma R>=gamma^2`, hence

`gamma R-1>=-(1-gamma^2)`.

Therefore `-1<=R_gamma<=0`; the continuous endpoint value at `gamma=1` is finite (in fact `-1/3`).

## B6. §4 coarse `q` bound and T1–T3 majorant — PASS

**Lines 148–175.**

Here `x=s^2 in [0,1]`, `delta in (0,1/64]`, so `|d|=|x-delta|<=1`. Consequently

`q=x(2-x)+lambda^2d^2<=1+lambda_+^2<2`.

Using the bounds already checked:

- `|T1|<=4(pi/2)lambda_+*4/lambda_-`;
- `|T2|<=2lambda_+^2*16*(2+1/lambda_-)/lambda_-^2`;
- `|T3|<=2(pi/2)lambda_+^3(2+1/lambda_-)[12/lambda_-+2sqrt2]/lambda_-`.

Thus the constant `M_N` is valid and integrable on the finite `s` interval.

## B7. §5 south-half compact bound — PASS

**Lines 177–199.**

For `s>=1` and `delta<=1/64`,

`d=s^2-delta>=63/64`,

so `q>=lambda_-^2(63/64)^2>0`. Hence there is no `q=0` corner in the south rectangle. The raw algebraic factors are continuous there. At an internal `gamma=1` point, `R` and `R_gamma` have their analytic `Psi/Psi'` extensions, so the apparent quotient singularity is removable. Compactness gives a finite `M_S`.

## B8. §6 differentiation under the integral — PASS

**Lines 201–219.**

The endpoint lemma supplies `g_axis_ob=integral F_t ds` for all `t<1` in this tube. Sections 4–5 of C2 supply a single integrable bound for `G_t=partial_tF_t`, uniform in `t` up to `1`. Standard dominated differentiation therefore yields

`partial_t g_axis_ob=integral G_t ds`

on `[63/64,1)`.

For fixed `s>0`, the regularized formula has an endpoint limit; dominated convergence then gives the displayed limit of `partial_t g_axis_ob`.

## B9. §6 one-sided derivative at `t=1` — PASS

**Lines 221–236.**

The endpoint lemma supplies continuity of `g_axis_ob` at `t=1`. The bound on `G_t` makes `partial_t g_axis_ob` uniformly bounded near `1` and its limit exists. For every `b<1`, the ordinary fundamental theorem gives

`g(b)-g(t)=integral_t^b partial_r g(r) dr`.

Letting `b->1-` is justified by continuity of `g` and bounded convergence for the derivative. Dividing by `1-t` shows that the left difference quotient tends to the same endpoint integral. Hence the one-sided derivative formula in lines 231–233 is valid.

## B10. Connection to endpoint lemma and scope — PASS

**Lines 50, 201–236.**

The use of the endpoint lemma is within its proved range:

- Lemma 3 supplies the pre-limit representation on `[1/2,1)`;
- Lemma 5 supplies continuity at `t=1`;
- `[5/8,33/50]` satisfies the endpoint lemma's general lambda condition.

No premise is used outside its scope.

## B11. Method extension to `[1/2,1] x [2/5,5/8]` — method-level PASS, not a G0/E1 audit

This is only the opinion requested by the instruction; it is **not** a self-audit of G0/E1.

The C2 mechanism has no structural dependence on `lambda>=5/8` or `t>=63/64`. The domain-specific constants change as follows:

- north half: use `lambda_-=2/5`; the scaled identity still gives finite bounds for `rho`, `phi`, `Ahat`, and `w`;
- with `delta<=1/2`, one still has `|d|<=1` on `s in [0,1]`, so the same type of finite `q` upper bound and `|H|` bound is available;
- south half: the old `d>=63/64` is no longer valid, but `d>=1/2` is valid, yielding the replacement lower bound `q>=lambda_-^2/4`.

Therefore the **method** extends after re-deriving constants on the larger rectangle. The old numerical constants cannot simply be copied. Whether a particular extended lemma has carried out those re-derivations correctly is outside this D6 report because ChatGPT authored G0/E1 v3.

## B12. §7 scope statement — PASS with one separation note

**Lines 238–250.**

The lemma correctly says that it proves the analytic bridge and does not prove the sign of the integral. Items 1–4 of its listed external checks are discharged by Parts B2–B10 of this report.

Item 5 — identity of the machine producer/checker density with the same `G_t` — is an implementation/source-identification obligation, not part of the analytic proposition proved by this file and is not certified by this D6 report. This report therefore does **not** promote any producer/checker result and does not claim implementation equivalence.

**C2-lemma analytic verdict: PASS.**

---

# 2. Findings requiring correction

No mathematical FAIL or GAP was found in either target lemma.

Non-blocking editorial/interpretive notes only:

1. In the endpoint lemma, `R=alpha/sin(alpha)` at `alpha=0` is used with its standard continuous extension `R(0)=1`; the proofs already use that extension implicitly. Making it explicit in §1 would improve readability, but no argument depends on an undefined value after the `Phi/Psi` chart is used.
2. In C2 §4, the phrase “compact north rectangle” occurs while the scaled variables themselves are not defined at the single endpoint corner `(s,t)=(0,1)` where `q=0`. The majorant is actually established for `t<1`, uniformly up to that corner, and the endpoint step uses a pointwise regularized limit for `s>0`. The proof logic is sound; the wording could be sharpened.
3. C2 §7 item 5 remains a separate implementation/source-identification obligation. It is not a defect in the analytic lemma and was outside the assigned D6 analytic verdict.

---

# 3. Comparison with earlier records

I found **no mathematical conclusion in the two target lemma texts that conflicts with the earlier audit conclusions I had seen**.

This report nevertheless differs in evidentiary basis: the PASS above comes from fresh algebra/calculus re-derivation from `5afa815f` and `7cb9b809`, not from the prior chat audit or the earlier symbolic check.

One scope point is worth recording explicitly: C2's own proof is for `[63/64,1] x [5/8,33/50]`. Extending its method to `[1/2,1] x [2/5,5/8]` requires new domain constants, especially replacing the south lower bound by `q>=lambda_-^2/4`. This is a method-level observation only and is not a verdict on G0/E1 v3.

---

# 4. Overall verdict

## `AI_AUDIT_PASS`

- `OBLATE_ENDPOINT_C1_LEMMA` blob `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`: **PASS**.
- `MONOTONE_TUBE_C2_INTERCHANGE_LEMMA` blob `7cb9b8091596510203d74e09387bc1e8188b8b47`: **PASS as the analytic interchange/endpoint-derivative lemma**.
- No FAIL or GAP was found.
- This is `CROSS_LINEAGE_AI_AUDIT / NON_BLIND` exactly as required by the instruction.
- G0/E1 v3 was not audited.
- No numerical or symbolic computation was used.
- No implementation was executed and no repository file was modified or committed.

Per the Judge instruction, whether this `AI_AUDIT_PASS` discharges D6 for FREEZE review is a Judge decision. Astra's later audit and human external audit remain separate conditions for stating the theorems as CLOSED in the paper.
