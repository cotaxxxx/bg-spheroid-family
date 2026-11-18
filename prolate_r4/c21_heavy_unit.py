"""Frozen topology/unit tests; no heavy H numerical box calculations.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from fractions import Fraction as F
from flint import fmpq as Q,arb,ctx
from . import c21_heavy_cover as C
from . import c21_heavy_box as B
def test_geometry():
 reg=C.frozen_registry()
 assert len(reg["roots"])==4096
 assert sum(C.area(x) for x in reg["roots"])==1
 assert reg["roots"][0]["id"]=="R00_T00"
 assert reg["roots"][1]["id"]=="R00_T63"
 assert reg["roots"][2]["id"]=="R63_T00"
 assert reg["roots"][3]["id"]=="R63_T63"
 assert len({x["id"] for x in reg["roots"]})==4096
 expected={"R00_T00":"CENTER_MVT","R00_T63":"AXIS_MVT",
  "R63_T00":"BOUNDARY_COLLAR","R63_T63":"AXIS_MVT",
  "R16_T00":"GENERAL","R16_T63":"AXIS_MVT"}
 for node in reg["roots"]:
  if node["id"] in expected:assert node["route"]==expected[node["id"]]
 r=reg["roots"][0]
 kids,axis=C.split(r)
 assert axis=="R" and sum(map(C.area,kids))==C.area(r)
 R=(Q(0),Q(1,64));T=(Q(63,64),Q(1))
 assert B.route(R,T)=="AXIS_MVT"
 R=(Q(63,64),Q(1));T=(Q(63,64),Q(1))
 assert B.route(R,T)=="AXIS_MVT"
 try:B.configure(R,T)
 except (AssertionError,ArithmeticError):pass
 else:raise AssertionError("boundary+axis must OPEN if extended distance is not positive")
 print("GEOMETRY 4096 roots, exact area, tie-R, overlaps, boundary+axis OPEN: PASS")
def test_taylor_coefficients():
 # Signed Taylor routine already tested in independent cost trim,
 # now verify that the heavy box uses exactly the frozen settings.
 assert B.BASE=={"base_u":16,"base_v":32,"ratio":"1/2","order":4}
 assert B.HESS=={"base_u":8,"base_v":16,"ratio":"1","order":4}
 assert B.KAP==Q(1,4096) and B.L==(Q(79,16),Q(5))
 print("MESH POINT/GRAD and HESS FROZEN PASS")
def main():
 test_geometry();test_taylor_coefficients()
 print(C.STATUS,"TOPOLOGY_ONLY_NOT_H_SIGN_EVIDENCE")
if __name__=="__main__":main()
