"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Small regressions, not full width validation."""
from contextlib import redirect_stdout
from dataclasses import replace
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from flint import arb, fmpq as Q, ctx
from .. import Config
from ..center_bounds import partition, derivative_mean_value
from ..density import Domain
from ..intervals import ball, bounds
from ..jets import Jet
from ..quadrature import Cell, axis_arc_upper, make_mesh, distance_lower_squared, q_of_u
from .resumable import run_suite, read_json
from .width_r3 import specifications, WidthFailure

class R3Tests(unittest.TestCase):
    def test_axis_arc_at_opposite_pole(self):
        with ctx.workprec(128):
            a,b=Q(63,64),Q(1)
            arc=axis_arc_upper(a,b)
            self.assertGreater(arc,4*(b-a))
            self.assertTrue(arb(arc).is_finite())
            reference=arb.pi()-2*arb(a).asin()
            self.assertGreaterEqual(arc,reference.lower().fmpq())

    def test_lambda_scaled_mesh_covers_and_meets_rule(self):
        cfg=replace(Config(),base_u=2,base_v=4,distance_ratio=Q(1))
        with ctx.workprec(128):
            R=(Q(1,2),Q(1,2)); L=(Q(5),Q(5))
            cells=make_mesh(R,Q(0),cfg,lam=L)
            area=Q(0)
            for c in cells:
                lo,hi=c.u
                delta=4*(hi-lo)+Q(22,7)*min(Q(1),4*hi,4*(1-lo))*(c.v[1]-c.v[0])
                ds=distance_lower_squared(R,q_of_u(lo))
                self.assertLessEqual(delta**2,cfg.distance_ratio**2*min(ds/L[1]**2,1/L[1]**2))
                area+=(hi-lo)*(c.v[1]-c.v[0])
            self.assertEqual(area,1)
            self.assertGreater(len(cells),cfg.base_u*cfg.base_v)

    def test_fixed_partition_no_gap_or_overlap(self):
        for lo,hi,count in ((Q(-1,32),Q(1,32),8),(Q(0),Q(1),16)):
            boxes=partition(lo,hi,count)
            self.assertEqual(len(boxes),count)
            self.assertEqual(boxes[0][0],lo); self.assertEqual(boxes[-1][1],hi)
            self.assertTrue(all(a[1]==b[0] for a,b in zip(boxes,boxes[1:])))

    def test_center_integral_mean_value_on_known_polynomial(self):
        # Independent derivative: d_R^4[R^4(1+x+x^2)(1+lam)+R^6]
        # =24(1+x+x^2)(1+lam)+360R^2. Integrand independent of u,v.
        def polynomial(u,v,params,dom,active,orders,mode):
            def var(value,name):
                return Jet.constant(value,orders,active.index(name) if name in active else None)
            r,x,lam=(var(v,n) for v,n in zip(params,("R","x","lam")))
            return (r**4*(1+x+x*x)*(1+lam)+r**6,)
        B=((Q(-1,32),Q(1,32)),(Q(1,4),Q(5,16)),(Q(2),Q(33,16)))
        mesh=(Cell((Q(0),Q(1)),(Q(0),Q(1))),)
        with ctx.workprec(128),patch("prolate_r1.center_bounds.evaluate",polynomial):
            value=derivative_mean_value(B,Domain(B[0],B[2]),mesh,"energy",4,2)
            for r in B[0]+(Q(0),):
                for x in B[1]:
                    for lam in B[2]:
                        exact=24*(1+x+x*x)*(1+lam)+360*r*r
                        self.assertTrue(value.contains(exact),(r,x,lam))

    def test_width_failure_keeps_observation_and_traceback(self):
        detail={"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","name":"fixture",
                "half_width":"1","half_width_limit":"1/20","evaluation_ns":123}
        def fail(): raise WidthFailure(detail)
        with TemporaryDirectory() as tmp,redirect_stdout(io.StringIO()):
            out=Path(tmp)/"width.json"
            code=run_suite([("fixture",fail)],"fixture",out,{"fixture":"r3"})
            row=read_json(out)["tests"][0]["attempts"][0]
            self.assertEqual(code,1); self.assertEqual(row["detail"],detail)
            self.assertIn("WidthFailure",row["traceback"])

    def test_width_plan_not_empty_and_exact_thresholds(self):
        cases=specifications()
        self.assertEqual(len(cases),36)
        self.assertEqual(sum(c.kind=="g" for c in cases),9)
        self.assertEqual(sum(c.kind=="phi" for c in cases),9)
        self.assertEqual(cases[8].args,(Q(1,2),Q(1,2),Q(5)))
        self.assertEqual(cases[33].name,"W_box_2")
        self.assertTrue(all(c.limit==Q(1,100) for c in cases if c.kind=="g"))

if __name__=="__main__": unittest.main(verbosity=2)
