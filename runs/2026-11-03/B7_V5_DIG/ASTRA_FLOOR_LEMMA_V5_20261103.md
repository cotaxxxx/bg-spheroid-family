# B7 V5 — Astra floor lemma (2026-11-03)

Status: **mathematically established, given the listed kernel identities**. This
file is a proof statement, not a certificate for the 40 outer boxes.

## Domain

\(2/5\le\lambda\le93/200\), \(7/8\le\tau\le1\),
\(3/10^8\le\delta\le15/64\), \((y,p,t,u)\in[0,1]^4\),
\(\varepsilon=\pm1\), with all quantities as defined by
\`v6_b7_safe_128.py\` (_kernel_form).

Put \(a=|V|^2\), \(h=\widehat H\), \(e=\widehat E\),
\(U^2=a-\omega_x^2\), \(w^2=\lambda^2(\xi_x^2+\xi_y^2)+\xi_z^2\).
We use the exact identity
\(e=h\omega_x-\xi_x a\), where \(h=\xi\cdot\omega\).
The companion \`chk_e3_symbolic.py\` proves this identity modulo the
defining unit-circle and kappa relations (Groebner remainder zero).

## Lemma: weighted Cauchy–Schwarz

Let

\[
r=(\lambda\xi_x,\lambda\xi_y,\xi_z),\quad
z=(\omega_x^2-a,\omega_x\omega_y,\lambda\omega_x\omega_z).
\]

Then \(r\cdot z=\lambda e\), \(|r|^2=w^2\), and

\[
 |z|^2=(\omega_x^2-a)^2+\omega_x^2\omega_y^2+
     \lambda^2\omega_x^2\omega_z^2
      =a(a-\omega_x^2)=aU^2.
\]

By Cauchy–Schwarz,

\[
  \boxed{\lambda^2 e^2\le w^2 aU^2.}
\]

This is equivalently the exact SOS identity

\[
 w^2aU^2-\lambda^2e^2
  =\sum_{1\le i<j\le3}(r_iz_j-r_jz_i)^2\ge0.
\]

## Lemma: integrand floor

Write \(X=(1+u^2)T>0\), \(Y=(1-u^2)G\ge0\), so
\(\widehat B=X+Y\) and

\[
 \widehat{\mathcal Q}
   =\widehat B\,h^2U^2-(2X+Y)e^2
   \ge -2\widehat B e^2.
\]

Using \(\widehat B\ge T=w\sqrt a>0\), \(W\ge0\), and the SOS bound,

\[
 F=\frac{W\widehat{\mathcal Q}}{a^2\widehat B^2}
 \ge-\frac{2We^2}{a^2\widehat B}
 \ge-\frac{2WwU^2}{\lambda^2 a^{3/2}}.
\]

Since \(U^2\le a\), \(w\le1\), \(\sqrt a\ge\lambda\),
\(W\le11/5\) and \(\lambda\ge2/5\),

\[
 \boxed{F\ge-\frac{2W}{\lambda^3}\ge-\frac{275}{4}.}
\]

The full domain includes \(p=0\), where \(W=0\) and \(F=0\).
All factors divided by above are strictly positive on the domain.

## Application

Old \(K_Q=859375/64\). New \(K'=275/4\).

\[
 K'/K_Q=16/3125,\qquad K_Q/K'=3125/16=195.3125.
\]

Both uses must change together:

1. Contact loss: \(2\lambda^+ K'\sigma_0\);
2. Cell floor:
   \(-2K'[\sigma(p_b)-\sigma(p_a)]
       [2(t_b-t_a)/(1+t_a^2)](y_b-y_a)(u_b-u_a)\).

The cell floor is outward-rounded down by multiplying by \(S=2^{128}\)
and taking mathematical floor. Midpoint and zeroth interval values are
NOT scaled or changed.

**No assertion is made that every outer box is positive.**
Reauthenticated checkpoints, finite exact cover, recorded interval
enclosures, and final rational inequalities still require independent audit.