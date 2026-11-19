"""GeoEncloseReader: an independent re-enclosure reader for GeoEnclosure interval covers.

Reads a binary-tree cover ledger (TSV, units 2^-20 for boxes, 2^-36 for values), checks the tree
structure, and re-encloses selected terminal leaves with its own Arb kernels (not the producer's).
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
__version__ = "0.1.0"
