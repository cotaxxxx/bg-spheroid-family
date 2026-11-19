"""Ledger reader for binary-tree interval covers (Codex window / near-boundary format).

Columns: path l0 l1 r0 r1 z0 z1 mode n k alo ahi blo bhi action
- path: 'x' root, children append '0' (lower half) / '1' (upper half) along the split axis.
- l*, r*, z*: integers in units 2^-20 (lambda, rho, z). Degenerate axes have equal endpoints.
- alo..bhi: integers in units 2^-36 (meaning depends on mode); '--' (e.g. empty boxes) reads as None.
- action: 'split' + axis letter (l, r, z) for inner nodes; otherwise a terminal verdict.
"""
import gzip, glob
from fractions import Fraction
from .interval import VUNIT

FIELDS = ["path", "l0", "l1", "r0", "r1", "z0", "z1", "mode", "n", "k", "alo", "ahi", "blo", "bhi", "action"]
INT = {"l0", "l1", "r0", "r1", "z0", "z1", "n", "k", "alo", "ahi", "blo", "bhi"}


def read(path):
    op = gzip.open if path.endswith(".gz") else open
    rows = []
    with op(path, "rt") as f:
        for ln in f:
            if ln.startswith("path"): continue
            p = ln.rstrip("\n").split("\t")
            r = {k: ((None if v in ("--", "") else int(v)) if k in INT else v) for k, v in zip(FIELDS, p)}
            r["box"] = (r["l0"], r["l1"], r["r0"], r["r1"], r["z0"], r["z1"]); r["file"] = path
            rows.append(r)
    return rows


def read_many(pattern):
    out = []
    for fn in sorted(glob.glob(pattern)): out += read(fn)
    return out


def terminals(rows):
    return [r for r in rows if not r["action"].startswith("split")]


def value(x):
    return Fraction(x, VUNIT)


def check_tree(rows):
    """Structural check of one tree: every split node has exactly its two halves as children, children
    are the halves of the parent along the named axis, and terminal volumes add up to the root volume
    (volume over the root's non-degenerate axes, exact rationals)."""
    by = {r["path"]: r for r in rows}; errs = []
    root = by.get("x")
    if root is None: return {"ok": False, "errors": ["no root"]}
    axes = [i for i in range(3) if root["box"][2*i] != root["box"][2*i+1]]
    vol = lambda b: Fraction(1) if not axes else __import__("math").prod(Fraction(b[2*i+1]-b[2*i]) for i in axes)
    ax = {"l": 0, "r": 1, "z": 2}
    for r in rows:
        if r["action"].startswith("split"):
            i = ax.get(r["action"][5:6]); c0 = by.get(r["path"]+"0"); c1 = by.get(r["path"]+"1")
            if i is None or c0 is None or c1 is None: errs.append(f"{r['path']}: missing child or axis"); continue
            b = r["box"]; mid = (b[2*i]+b[2*i+1])//2
            e0 = list(b); e0[2*i+1] = mid; e1 = list(b); e1[2*i] = mid
            if tuple(e0) != c0["box"] or tuple(e1) != c1["box"]: errs.append(f"{r['path']}: children are not halves")
        elif r["path"]+"0" in by or r["path"]+"1" in by: errs.append(f"{r['path']}: terminal has children")
    tv = sum(vol(r["box"]) for r in terminals(rows)); rv = vol(root["box"])
    if tv != rv: errs.append(f"terminal volume {tv} != root volume {rv}")
    return {"ok": not errs, "nodes": len(rows), "terminals": len(terminals(rows)),
            "relative_volume": str(tv/rv) if rv else "n/a", "errors": errs[:20]}
