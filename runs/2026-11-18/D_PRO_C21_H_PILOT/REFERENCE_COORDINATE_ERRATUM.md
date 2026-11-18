# Erratum: primitive E reference coordinate mapping
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

**DO NOT USE** the earlier files `primitive_E_references.json`
and `primitive_E_hires.json` as coordinate-consistent H reference
values. They were generated with `p_z = R sin(beta)` in the ORIGINAL
physical E integral, which is incorrect for the normalized R3
rotation ellipsoid coordinates.

The correct mapping is
 `p_x = rho = R cos(beta)`,
 `p_z (in original E) = lambda * z = lambda * R sin(beta)`.
Indeed, in original E,
 `D^2 = (xi_x-rho)^2+xi_y^2+(lambda*xi_z-p_z)^2`,
and with `p_z=lambda*z` this equals
 `|xi-(rho,0,z)|^2+(lambda^2-1)*(xi_z-z)^2`,
the R3 co-rotated geometric D².
Also `h=lambda*(1-rho xi_x)-p_z xi_z
=lambda*(1-rho xi_x-z xi_z)`, so `k=h/lambda`.

Corrected independent references must use `lambda*z` in the
primitive E formula and hold that original p_z fixed in
the rho five-point stencil. The original two files remain
preserved as **INVALID_COORDINATE_MAPPING** forensic records;
the independent E kernel itself was not the problem.
Corrected files have the suffix `_CORRECTED`.

V36 R3 H box2 and the Arb producer are unaffected by this
reference-only mistake. The user-facing earlier uncorrected
E-reference numbers must be explicitly withdrawn/replaced.
