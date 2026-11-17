"""DIAGNOSTIC_ONLY / NOT_EVIDENCE: exact public inputs, Arb enclosures."""
from dataclasses import dataclass, field
from flint import arb, fmpq as Q
STATUS = "DIAGNOSTIC_ONLY / NOT_EVIDENCE"

def exact(x):
    if not isinstance(x, Q):
        raise TypeError("geometric inputs must be fmpq, never float or int")
    return x

def iv(x):
    if isinstance(x, Q):
        return x, x
    if not isinstance(x, (tuple, list)) or len(x) != 2:
        raise TypeError("expected fmpq or two fmpq endpoints")
    a, b = map(exact, x)
    if a > b:
        raise ValueError("reversed interval")
    return a, b

def hull(a, b):
    return arb(a).union(arb(b))

def ball(x):
    return hull(*x)

def bounds(x):
    return x.lower().fmpq(), x.upper().fmpq()

def clip(x, a, b):
    lo, hi = bounds(x)
    lo, hi = max(lo, Q(a)), min(hi, Q(b))
    if lo > hi:
        raise ArithmeticError("empty intersection with proven geometric range")
    return hull(lo, hi)

def mag(x):
    a, b = bounds(x)
    return max(abs(a), abs(b))

def sym(x):
    x = mag(x) if isinstance(x, arb) else abs(Q(x))
    return hull(-x, x)

def midpoint(x):
    return (x[0]+x[1])/2

def radius(x):
    return (x[1]-x[0])/2

def serial(x):
    lo, hi = bounds(x)
    return {"lower": str(lo), "upper": str(hi), "width": str(hi-lo)}

def tau_interval(beta, kind):
    x = iv(beta)
    if kind == "tau":
        if not Q(0) <= x[0] <= x[1] <= Q(1):
            raise ValueError("tau outside [0,1]")
        return x
    if kind != "beta":
        raise ValueError("angle_kind must be beta or tau")
    if x[0] < 0 or not arb(x[1]) <= arb.pi()/2:
        raise ValueError("rational beta outside [0,pi/2]; use tau=1 at pole")
    lo = (arb(x[0])/2).tan().lower().fmpq()
    hi = (arb(x[1])/2).tan().upper().fmpq()
    return max(Q(0), lo), min(Q(1), hi)

@dataclass(frozen=True)
class Config:
    precision: int = 128
    order: int = 6
    base_u: int = 32
    base_v: int = 64
    distance_ratio: Q = Q(1,4)
    kappa: Q = Q(1,4096)
    cap_from: Q = Q(15,16)
    center_to: Q = Q(1,16)
    max_depth: int = 28
    max_cells: int = 200000
    center_radial_parts: int = 8
    center_tau_parts: int = 16
    center_bound_order: int = 2

    def __post_init__(self):
        for name in ("precision", "order", "base_u", "base_v", "max_depth", "max_cells",
                     "center_radial_parts", "center_tau_parts", "center_bound_order"):
            if type(getattr(self,name)) is not int:
                raise TypeError(name+" must be int")
        if self.precision < 64 or self.order not in (2,4,6):
            raise ValueError("precision>=64; order in {2,4,6}")
        if self.center_bound_order not in (2,4,6):
            raise ValueError("center_bound_order must be 2,4,6")
        if min(self.center_radial_parts,self.center_tau_parts)<1:
            raise ValueError("positive center partition counts required")
        for name in ("distance_ratio","kappa","cap_from","center_to"):
            exact(getattr(self,name))
        if min(self.base_u,self.base_v,self.max_depth,self.max_cells) < 1:
            raise ValueError("positive resource limits required")
        if not (0 < self.distance_ratio <= 2 and 0 < self.kappa < 1 and
                0 < self.center_to < self.cap_from < 1):
            raise ValueError("invalid geometric policy")

@dataclass
class Result:
    balls: tuple
    point_balls: tuple
    correction: tuple
    cap_errors: tuple
    cells: int
    route: str
    details: dict = field(default_factory=dict)
    status: str = STATUS

    @property
    def enclosure(self):
        if len(self.balls) != 1:
            raise ValueError("result is not scalar")
        return self.balls[0]

    def to_json(self):
        return {"status":self.status, "route":self.route, "cells":self.cells,
                "balls":[serial(x) for x in self.balls],
                "center_point":[serial(x) for x in self.point_balls],
                "mean_value_correction":[serial(x) for x in self.correction],
                "cap_errors":[serial(x) for x in self.cap_errors],
                "details":self.details}
