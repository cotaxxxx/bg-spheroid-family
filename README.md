# bg-spheroid-family

Assembly and reference repository for the merged manuscript on the certified stationary-point structure of volume-preserving spheroids (prolate–sphere–oblate).

> **NOT_BINDING**: all certificates remain in the upstream repositories and are referenced here only by full SHA-256 pins.

## Scope

This repository assembles the common mathematical framework and manuscript-level comparison for the one-parameter, constant-volume spheroid family

\[
K_\lambda=\left\{(x,y,z)\in\mathbb R^3:
\frac{x^2+y^2}{R_{\rm eq}(\lambda)^2}+\frac{z^2}{R_{\rm pol}(\lambda)^2}\le 1\right\},
\]

with

\[
R_{\rm eq}(\lambda)=R\lambda^{-1/3},\qquad
R_{\rm pol}(\lambda)=R\lambda^{2/3}.
\]

Hence

\[
R_{\rm eq}(\lambda)^2R_{\rm pol}(\lambda)=R^3,
\]

so the enclosed volume is constant:

\[
\operatorname{Vol}(K_\lambda)=\frac{4\pi}{3}R^3.
\]

The parameter convention is

- `lambda > 1`: prolate spheroid,
- `lambda = 1`: sphere,
- `0 < lambda < 1`: oblate spheroid.

The intended manuscript studies the stationary-point structure of the basepoint functional along the full path

**prolate → sphere → oblate**.

## Repository role

This repository is an **assembly/reference layer**, not a certificate authority. Its purposes are to:

1. define the common constant-volume parameterization;
2. align notation and conventions between the prolate and oblate studies;
3. record immutable upstream evidence pins;
4. assemble the global stationary-structure / bifurcation picture;
5. support the merged manuscript and its reproducibility record.

No numerical value or theorem becomes certified merely by appearing in this repository.

## Evidence policy

Certificate-bearing evidence must remain in its originating upstream repository. Every result used by the merged manuscript must be identified by:

- upstream repository;
- full 40-character Git commit SHA when applicable;
- SHA-256 digest for certificate artifacts/manifests;
- certification status stated by the upstream evidence itself.

Short SHAs, floating branch names, and unpinned `main` references are not acceptable as binding evidence.

## Upstream studies

| Regime | Repository | Role |
|---|---|---|
| Prolate | `cotaxxxx/bg-prolate-spheroid` | Prolate research / diagnostic history |
| Oblate | `cotaxxxx/bg-oblate-spheroid` | Oblate research / diagnostic history |
| Sphere | analytic reference case | symmetry and exact comparison point |

Binding certificate repositories and exact immutable pins are recorded separately in `UPSTREAM_PINS.md` only after verification.

## Planned manuscript structure

The merged manuscript is intended to separate four layers clearly:

- **common geometry** — the volume-preserving spheroid family and similarity normalization;
- **prolate regime** — certified stationary-circle / center behavior inherited from pinned upstream evidence;
- **sphere** — the maximally symmetric reference point;
- **oblate regime** — certified stationary-point behavior inherited from pinned upstream evidence.

The synthesis target is a single stationary-structure phase diagram across the complete constant-volume spheroidal path.

## Status

**ASSEMBLY / NOT_BINDING**

This repository must not duplicate, silently modify, or supersede upstream certificates. Any manuscript claim labeled `CERTIFIED` must resolve to independently verifiable upstream evidence through the immutable pins recorded here.
