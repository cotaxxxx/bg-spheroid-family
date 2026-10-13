# D4 independent derivation — phase A, before counterpart access

2026-10-14. DRAFT / NOT FROZEN / EXECUTION PROHIBITED / CHAT AUDIT REQUESTED.
No Claude Code fourth-order formula or the contents of 07db380e / 74f0608e have been read during this derivation. The user's summary (including the approximate 0.509 claim) is known. This is formula-level independent derivation, not independence from all background mathematics or a claim about different model lineage.

## A1. Independent homogeneous expansion

Use the P1 density F=h G(gamma), G=acos²(gamma), with signed basepoint coordinates x=rho,z. At the physical centre set q=1-(1-lambda²)mu², gamma0=lambda/(w sqrt(q)), b=sqrt(1-mu²)cos(phi).

Let ell=b x+lambda mu z, k=b x+(mu/lambda)z, v2=x²+z². Then h=lambda(1-k), D²=q-2ell+v2, gamma=gamma0(1-k)(1+(-2ell+v2)/q)^(-1/2).

The homogeneous degree 1,2,3,4 components gamma/gamma0-1 are:

d1=ell/q-k.

d2=-v2/(2q)+3ell²/(2q²)-k ell/q.

d3=-3ell v2/(2q²)+5ell³/(2q³)+k v2/(2q)-3k ell²/(2q²).

d4=3v2²/(8q²)-15ell²v2/(4q³)+35ell⁴/(8q⁴)+3k ell v2/(2q²)-5k ell³/(2q³).

Define T0=d4-k d3, T1=d1 d3+d2²/2-k d1 d2, T2=d1²d2/2-k d1³/6, T3=d1⁴/24. Since G^(j+1)=-2R^(j), the homogeneous fourth-order part of F is

F[4]=-2lambda sum(j=0..3) gamma0^(j+1) R^(j)(gamma0) Tj.

Phi mean is the exact linear functional b^(odd)->0, b²->(1-mu²)/2, b⁴->3(1-mu²)²/8. Let A40_j=<[x⁴]Tj>, A22_j=<[x²z²]Tj>. The mu integral kernels for the ENERGY DERIVATIVES (not Taylor coefficients) are

K40=-24 sum gamma0^(j+1)R^(j) A40_j,
K22=-4 sum gamma0^(j+1)R^(j) A22_j.

E_rhorhorhorho(0,0)=integral[-1,1]K40 dmu;
E_rhorhozz(0,0)=integral[-1,1]K22 dmu.

The factors use E=(1/(4pi lambda))integral F dphi dmu, 4! for x⁴, and 2!2! for x²z². The H expansion coefficients are E40/6 and E22/2, respectively. These three notions must not be interchanged.

The companion exact SymPy script expands these four polynomials and checks a separate directional chain-rule formula. No numerical values, parameter sweep, or certificate computation is used.

## A2. Explicit uniform fourth-derivative bound on the SWEPT NEIGHBOURHOOD

Work on |diag(1,1,lambda)^(-1)p|<=1/8 and lambda in [119/200,33/50]. All signed meridional FTC segments lie here. The earlier distance proof gives D>=833/1600>1/2, lambda>1/2, h<=wD, and |h_v|<=w for any Euclidean unit direction v.

For n=1..4, the inverse-distance expansion uses Legendre polynomials P_n(a), |a|<=1, with |P_n(a)|<=1. This bound follows directly from the four polynomials P1=a, P2=(3a²-1)/2, P3=(5a³-3a)/2, P4=(35a⁴-30a²+3)/8. Thus |(D^-1)^(n)|<=n!D^(-n-1), and affinity of h yields

|gamma^(n)|<=2 n! D^(-n), n>=1 up to 4.

Use R(gamma)=2 integral[0,1] [1+gamma+(1-gamma)s²]^-1 ds. On [0,1], this gives

|G'|<=4, |G''|<=2, |G'''|<=64/15, |G''''|<=384/35.

The second bound uses |R'|<=1; the next two use integrals of (1-s²)² and (1-s²)³ with denominator>=1. The fourth directional chain rule gives

|F_vvvv| <= w D^-3 C4,
C4=16*(384/35)+128*(64/15)+240*2+96*4 =166496/105.

Hence |E_vvvv|<=C4/(lambda D_min³)<16C4<25600. This is uniform on the entire swept domain, not just the centre.

For orthonormal e_rho,e_z, Q(v)=D_v^4 E obeys
12 E_rhorhozz=Q(e_rho+e_z)+Q(e_rho-e_z)-2Q(e_rho)-2Q(e_z).
Homogeneity of Q gives |E_rhorhozz|<=25600 as well. Consequently legitimate explicit bounds are M40=M22=25600. They are conservative and do not close r<=1/8 via the coarse second-order remainder criterion.

## A3. An explicit analytic central patch

rho<=r, z<=lambda r*16/65<r/6. Therefore the remainder loss is at most (13/72)*25600*r². At delta=1/128 this is 325/1152, strictly below the old verified m*=1547/4860 (difference 5629/155520).

Thus the paper argument yields a strictly positive central patch 0<=r<=1/128, all tau in [0,1/8], all lambda in [119/200,33/50], subject to chat audit. It is not a machine certificate nor a Judge discharge. It does not use the claimed 0.509 improvement.

## A4. Stronger central lower bound independently recoverable

Keeping N(y,c)=1/2+(1/2-c)y-c²y²(1-y) before integrating gives
L(lambda)=lambda[4/3-2(1-lambda²)/3-4(1-lambda²)²/35].
It is increasing on the target interval: the bracket is positive and decreases with c, while c decreases with lambda. The exact value at 119/200 must be used rather than rounding the displayed 0.509 upward. The script records the exact fraction and its difference from 509/1000. The cited external L formula has not yet been read; no identity is presumed.

## A5. Outstanding comparison

After the phase-A files and hashes are fixed: retrieve the counterpart formula and source L; compare the phi means with exact SymPy differences, allowing only documented changes of coordinates/normalization. If unequal or counterpart absent, mark the comparison UNRESOLVED. Historical timestamp evidence requires both submission and first-access records; a commit timestamp alone proves no absence of prior access.
