# D-OB P2 / B7 — Qhat global lower bound
Date: 2026-11-01 JST. Status: analytic lemma for independent review.
Scope: lambda in [2/5, 93/200], t,u,p,y domain as in Route K; both beta sheets.
Does not certify I(lambda,tau,delta)>0.

Let xi, omega be unit vectors, 0<lambda<=1, and set
  b=|V|^2=omega_x^2+omega_y^2+lambda^2 omega_z^2,
  a=omega_x^2, Hhat=xi dot omega,
  Ehat=Hhat omega_x - xi_x b,
  R=Ehat^2, P=Hhat^2 Uhat^2,
  T=w|V|, G=lambda Hhat.
We have 0<=a<=b<=1, P>=0, 0<=T<=1, and 0<=G<=1.
The last bound uses Hhat>=0, verified from
  Hhat=cos(psi)+sqrt(s_v)*sigma*sin(psi)>=0 on the prescribed domain.

Since |xi|=1 and Ehat=xi dot (omega_x omega - b e_x),
  R<= |omega_x omega-b e_x|^2
    = b^2+a(1-2b).
If b>=1/2, 1-2b<=0, so R<=b^2<=1.
If b<1/2, a<=b and 1-2b>0, so R<=b-b^2<=1/4.
Thus R<=1.

Write
  Qhat = [(1+u^2)T+(1-u^2)G] P
       - [2(1+u^2)T+(1-u^2)G] R.
Because 0<=u<=1, the first bracket is nonnegative,
and the second bracket is between 0 and 3+u^2<=4.
Hence Qhat>=-4.

Therefore under the separately audited normalization and lower bounds,
  KQ = (2*(11/10)*4)/(2/5)^8 = 859375/64.
This uniform bound is shared by the contact-strip loss and cell K floor.
The original Qhat>=-16 variant has KQ=859375/16.
Uncertified numerical scans are not part of this proof.
