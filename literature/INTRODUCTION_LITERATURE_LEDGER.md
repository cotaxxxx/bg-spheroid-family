# Introduction literature ledger — W2

Status: `MANUSCRIPT_WORKING_NOTE / NOT_BINDING`

Purpose: literature-control table for the merged volume-preserving spheroid manuscript. This file is not theorem evidence and does not alter any upstream certification status.

## Citation-control rule

No reference enters the manuscript bibliography until the title, full author list, year, journal/book, volume/issue, pages/article number, and DOI/arXiv identifier have been checked against the original paper, publisher record, or other primary bibliographic source. The working sequence is: ChatGPT drafts the ledger -> human bibliographic check -> user approval -> bibliography commit.

The eighth field below records the exact manuscript claim or comparison the reference is intended to support. A reference should not be retained merely because it is broadly related.

Bibliographic status labels:

- `BIB_CHECKED`: bibliographic identity has been checked sufficiently for the current working ledger.
- `KNOWN_CHECKED`: user reports the bibliographic data as known and checked; DOI-level normalization may still be done at final `.bib` freeze.
- `RECHECK_BEFORE_BIB`: identity is plausible/partly checked, but one or more bibliography fields must be rechecked before inclusion in the final `.bib`.

## A. Essential references

| # | Title | Full authors | Year | Journal / book | Volume / issue | Pages / article | DOI / arXiv | Claim supported in the manuscript | Status |
|---|---|---|---:|---|---|---|---|---|---|
| 1 | The logarithmic Minkowski problem | K. J. Böröczky; E. Lutwak; D. Yang; G. Zhang | 2013 | Journal of the American Mathematical Society | 26 | 831–852 | DOI to normalize at `.bib` freeze | Cone-volume measure / logarithmic Minkowski problem as established convex-geometric background | `KNOWN_CHECKED` |
| 2 | Centro-affine differential geometry and the log-Minkowski problem | Emanuel Milman | 2025 | Journal of the European Mathematical Society | 27, no. 2 | 709–772 | 10.4171/JEMS/1386 | Modern connection between cone-volume measure, centro-affine geometry, and the log-Minkowski problem | `BIB_CHECKED` |
| 3 | Measures of symmetry for convex sets | Branko Grünbaum | 1963 | Proceedings of Symposia in Pure Mathematics | 7 | 233–270 | DOI / stable identifier to normalize at `.bib` freeze | Classical distinguished-center / symmetry background for convex bodies | `KNOWN_CHECKED` |
| 4 | Affine invariant points | Mathieu Meyer; Carsten Schütt; Elisabeth M. Werner | 2015 | Israel Journal of Mathematics | 208 | 163–192 | DOI to recheck | Modern theory of distinguished points attached to convex bodies; contrast with the present Euclidean/similarity-covariant stationary base point | `RECHECK_BEFORE_BIB` |
| 5 | New affine measures of symmetry for convex bodies | Mathieu Meyer; Carsten Schütt; Elisabeth M. Werner | 2011 | Advances in Mathematics | 228 | 2920–2942 | DOI to recheck | Affine-covariant points and symmetry measures; neighboring theory, not the same invariance class as the present functional | `RECHECK_BEFORE_BIB` |
| 6 | Convex Bodies: The Brunn–Minkowski Theory, 2nd ed. | Rolf Schneider | 2014 | Cambridge University Press | 2nd ed. | book | ISBN / DOI to normalize at `.bib` freeze | Standard reference for convex-body terminology and cone-volume-measure background used in the definition section | `RECHECK_BEFORE_BIB` |

## B. Comparison references

| # | Title | Full authors | Year | Journal / book | Volume / issue | Pages / article | DOI / arXiv | Claim supported in the manuscript | Status |
|---|---|---|---:|---|---|---|---|---|---|
| 7 | Surface Area and Curvature of the General Ellipsoid | Daniel Poelaert; Joachim Schniewind; Frank Janssens | 2011 arXiv posting; manuscript notes ©2004 | arXiv preprint | — | — | arXiv:1104.5145 | Radius–normal angle is a natural geometric quantity in ellipsoid geometry; background only | `BIB_CHECKED` |
| 8 | Surface area and other measures of ellipsoids | Igor Rivin | 2007 | Advances in Applied Mathematics | 39, no. 4 | 409–427 | 10.1016/j.aam.2006.08.009; arXiv:math/0403375 | Peer-reviewed ellipsoid-geometry background; preferred general geometric anchor over an unpublished preprint when possible | `BIB_CHECKED` |
| 9 | Bifurcations of MacLaurin spheroids. A Hamiltonian perspective | Miguel Rodríguez-Olmos | 2026 | Journal of Geometry and Physics | 226 | 105869 | 10.1016/j.geomphys.2026.105869; arXiv:2501.07153 | Classical/modern spheroid bifurcation comparison: equilibrium shape bifurcates, unlike the stationary set of a base-point functional on a prescribed shape family | `BIB_CHECKED` |
| 10 | Bifurcation and stability of uniformly rotating homogeneous ellipsoids surrounded by a massive thin ring | Shin'ichirou Yoshida | 2023 | arXiv preprint | — | — | arXiv:2301.09793 | Axisymmetric-to-triaxial shape bifurcation / symmetry-breaking comparison; distinguishes equilibrium-shape bifurcation from the present stationary-set bifurcation | `BIB_CHECKED` |
| 11 | Dual affine invariant points | Mathieu Meyer; Carsten Schütt; Elisabeth M. Werner | 2015 | Indiana University Mathematics Journal | 64 | 735–768 | DOI to recheck | Further context for distinguished-point theory; likely Introduction/Discussion support rather than a primary definition citation | `RECHECK_BEFORE_BIB` |
| 12 | New results on affine invariant points | Olaf Mordhorst | 2017 | Israel Journal of Mathematics | 219 | 529–548 | DOI to recheck | Shows the continuing development of affine-invariant-point theory after Grünbaum / Meyer–Schütt–Werner | `RECHECK_BEFORE_BIB` |
| 13 | Extremum problems with inequalities as subsidiary conditions | Fritz John | 1948 | Studies and Essays Presented to R. Courant | — | 187–204 | stable identifier to recheck | Historical John ellipsoid / John-center context if a classical distinguished-center example is needed | `KNOWN_CHECKED` |

## C. Computer-assisted / rigorous bifurcation methodology

| # | Title | Full authors | Year | Journal / book | Volume / issue | Pages / article | DOI / arXiv | Claim supported in the manuscript | Status |
|---|---|---|---:|---|---|---|---|---|---|
| 14 | Cusp bifurcations: Numerical detection via two-parameter continuation and computer-assisted proofs of existence | Jean-Philippe Lessard; Alessandro Pugliese | 2025 | Discrete and Continuous Dynamical Systems - B | 30, no. 6 | 2135–2158 | 10.3934/dcdsb.2024181; arXiv:2404.00535 | Example of numerical bifurcation detection followed by constructive computer-assisted proof; methodological comparison only | `BIB_CHECKED` |
| 15 | Computer-assisted bifurcation diagram validation… | Thomas Wanner | 2018 | Proceedings of Symposia in Applied Mathematics | 74 | 123–174 | 10.1090/psapm/074/00638 | General methodological anchor for validated bifurcation diagrams, including symmetry-breaking / pitchfork-type situations | `BIB_CHECKED` |
| 16 | Rigorous verification of saddle-node bifurcations in ODEs | Jean-Philippe Lessard | 2016 | Indagationes Mathematicae | 27 | 1013–1026 | 10.1016/j.indag.2016.06.012 | Rigorous verification of fold/saddle-node bifurcation; methodological comparison for boundary/fold-like certification architecture | `BIB_CHECKED` |
| 17 | The logarithmic Minkowski problem for polytopes | Guangxian Zhu | 2014 | Advances in Mathematics | 262 | 909–931 | DOI to normalize at `.bib` freeze | Development of the logarithmic Minkowski / cone-volume-measure literature beyond the foundational smooth/general setting | `KNOWN_CHECKED` |

## Introduction positioning

The literature should be presented as established neighboring theories rather than as a claim that no related work exists. The intended contrast is:

1. **Cone-volume measure / convex geometry:** the measure is established; the present novelty is not the existence of cone-volume measure itself.
2. **Distinguished points of convex bodies:** classical and affine-invariant-point theories attach special points to a body. The present stationary base point is different: the functional is built from Euclidean angle and cone-volume weighting and is naturally invariant/covariant under rigid motions and similarities, not under general affine transformations.
3. **Ellipsoidal bifurcation:** Maclaurin–Jacobi-type literature studies bifurcation of equilibrium shapes. The present manuscript prescribes the shape family and studies bifurcation of the stationary set of an interior-base-point functional.
4. **Computer-assisted bifurcation:** rigorous numerics and interval/computer-assisted bifurcation proofs are established methodology. The novelty claim should concern the geometric object and stationary-set problem being certified, not the generic fact of using interval computation.

Candidate core contrast sentence for later prose drafting:

> Whereas classical affine-invariant-point theory assigns distinguished points to convex bodies, and classical ellipsoidal bifurcation theory concerns changes of equilibrium shapes, we study the stationary set of an interior-base-point functional on a prescribed family of convex bodies as the body itself is deformed.

This is a working sentence only; it is not yet frozen manuscript text.

## Novelty-language discipline

Do not write that there is "no prior work" unless a dedicated direct-prior-art search supports that statement. Preferred wording is `to the authors' knowledge` and should be tied narrowly to the stationary-set problem for the cone-volume-weighted radial–normal angle functional.

The manuscript should distinguish clearly between:

- established ingredients;
- neighboring theories;
- the new stationary-set question;
- numerical exploration;
- exact analytic statements;
- interval/computer-assisted certification.

## W2 use

This ledger is intended to feed the W2 Introduction draft. Before the bibliography is committed, all `RECHECK_BEFORE_BIB` entries must be resolved and all remaining DOI / ISBN / article-number normalization fields should be checked against primary bibliographic sources.
