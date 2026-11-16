"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
R2 regressions separate from the unchanged original 23-case suite.
"""
from contextlib import redirect_stdout
import io
import json
from math import comb
import os
from pathlib import Path
import signal
from tempfile import TemporaryDirectory
import unittest
from flint import arb, fmpq as Q, ctx
from .. import Config,axis_g
from ..density import Domain,axial
from ..intervals import ball,bounds,hull
from ..jets import Jet
from .resumable import run_suite,read_json

class PositiveReciprocalTests(unittest.TestCase):
    def test_mixed_jet_inverse_identity(self):
        with ctx.workprec(128):
            x=Jet.constant(Q(2),(4,2),0)
            y=Jet.constant(Q(3),(4,2),1)
            a=x+y
            inv=a.reciprocal_positive(Q(5),Q(5))
            residual=a*inv-1
            self.assertTrue(all(c.contains(0) for c in residual.c))

    def test_wide_inverse_cube_coefficients(self):
        with ctx.workprec(128):
            D=Jet.constant(hull(Q(1),Q(4)),(6,),0)
            inv=D.reciprocal_positive(Q(1),Q(4))
            cube=inv*inv*inv
            self.assertTrue(all(x.is_finite() for x in cube.c))
            for d in (Q(1),Q(3,2),Q(5,2),Q(4)):
                for n in range(7):
                    expected=Q((-1)**n*comb(n+2,2))/d**(n+3)
                    self.assertTrue(cube.coeff(n).contains(expected),(d,n))

    def test_nonpositive_or_inconsistent_proof_rejected(self):
        x=Jet.constant(Q(1),(2,))
        with self.assertRaises(ArithmeticError):
            x.reciprocal_positive(Q(0),Q(1))
        with self.assertRaises(ArithmeticError):
            x.reciprocal_positive(Q(2),Q(3))

    def test_reported_axis_cell(self):
        with ctx.workprec(128):
            interval=(Q(3,4),Q(7,8))
            params=(arb(Q(1,2)),arb(Q(3)))
            dom=Domain((Q(1,2),Q(1,2)),(Q(3),Q(3)))
            for order in (2,4,6):
                cell=axial(ball(interval),arb(0),params,dom,("u",),(order,))[0]
                self.assertTrue(all(x.is_finite() for x in cell.c),order)
                for y in (Q(3,4),Q(13,16),Q(7,8)):
                    point=axial(arb(y),arb(0),params,dom,("u",),(order,))[0]
                    self.assertTrue(all(x.is_finite() for x in point.c))
                    self.assertTrue(all(a.overlaps(b) for a,b in zip(cell.c,point.c)))
            for active in ("R","lam"):
                j=axial(ball(interval),arb(0),params,dom,(active,),(1,))[0]
                self.assertTrue(all(x.is_finite() for x in j.c))

    def test_reported_axis_api_default_config(self):
        result=axis_g(Q(1,2),Q(3),config=Config())
        self.assertTrue(result.enclosure.is_finite())
        self.assertGreater(result.cells,0)

class DurableRunnerTests(unittest.TestCase):
    identity={"test_fixture":"r2-journal-v1"}
    def execute(self,tests,out,**kwargs):
        with redirect_stdout(io.StringIO()):
            return run_suite(tests,"fixture",out,self.identity,**kwargs)

    def test_save_each_case_and_resume_without_reexecution(self):
        calls=[]
        tests=[("a",lambda:calls.append("a")),("b",lambda:calls.append("b"))]
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            self.assertEqual(self.execute(tests,out,max_cases=1),2)
            report=read_json(out)
            self.assertFalse(report["complete"])
            self.assertEqual(report["counts"]["PASS"],1)
            self.assertEqual(self.execute(tests,out,resume=True),0)
            self.assertEqual(calls,["a","b"])
            self.assertTrue(read_json(out)["all_tests_passed"])

    def test_failure_traceback_is_durable_and_not_silently_retried(self):
        calls=[]
        def failure():
            calls.append(1)
            raise ValueError("intentional runner regression")
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            tests=[("failure",failure),("later",lambda:None)]
            self.assertEqual(self.execute(tests,out),1)
            row=read_json(out)["tests"][0]
            self.assertIn("intentional runner regression",row["attempts"][0]["traceback"])
            self.assertEqual(self.execute(tests,out,resume=True),1)
            self.assertEqual(calls,[1])

    def test_recover_missing_result_and_keep_attempt_history(self):
        calls=[]
        tests=[("a",lambda:calls.append("a")),("b",lambda:calls.append("b"))]
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            self.assertEqual(self.execute(tests,out,max_cases=1),2)
            work=out.with_name(out.name+".cases")
            # Fault injection only in a temporary fixture: model a kill before
            # the atomic result commit, with the start record already durable.
            (work/"000"/"0001.result.json").unlink()
            self.assertEqual(self.execute(tests,out,resume=True),0)
            hist=read_json(out)["tests"][0]["attempts"]
            self.assertEqual([x["result"] for x in hist],["INTERRUPTED","PASS"])
            self.assertIsNone(hist[0]["traceback"])
            self.assertEqual(calls,["a","a","b"])

    @unittest.skipUnless(os.name=="posix","POSIX signal regression")
    def test_sigterm_saves_stack_and_can_resume(self):
        calls=[]
        def case():
            calls.append(1)
            if len(calls)==1: os.kill(os.getpid(),signal.SIGTERM)
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            tests=[("signal",case)]
            self.assertEqual(self.execute(tests,out),128+signal.SIGTERM)
            row=read_json(out)["tests"][0]["attempts"][0]
            self.assertEqual(row["result"],"INTERRUPTED")
            self.assertIn("case",row["interrupted_stack"])
            self.assertTrue(Path(row["stderr"]).read_text())
            self.assertEqual(self.execute(tests,out,resume=True),0)
            self.assertEqual(len(read_json(out)["tests"][0]["attempts"]),2)

    def test_source_identity_change_rejected(self):
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            tests=[("a",lambda:None)]
            self.assertEqual(self.execute(tests,out),0)
            with self.assertRaises(ValueError):
                with redirect_stdout(io.StringIO()):
                    run_suite(tests,"fixture",out,{"test_fixture":"different"},resume=True)

    def test_existing_output_needs_explicit_resume(self):
        with TemporaryDirectory() as tmp:
            out=Path(tmp)/"report.json"
            tests=[("a",lambda:None)]
            self.assertEqual(self.execute(tests,out),0)
            with self.assertRaises(FileExistsError):
                self.execute(tests,out)

if __name__=="__main__":
    unittest.main(verbosity=2)
