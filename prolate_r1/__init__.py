"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Runtime validation pending; see VALIDATION.md."""
import flint
if flint.__version__ != "0.8.0":
    raise RuntimeError("python-flint==0.8.0 is required")
from .intervals import Config, Result, STATUS
from .api import angular_raw, angular_quotient, axis_g, equatorial_phi_s
__all__ = ["Config", "Result", "angular_raw", "angular_quotient", "axis_g", "equatorial_phi_s"]
