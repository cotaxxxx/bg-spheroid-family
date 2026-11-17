"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Resumable R3 tests for Dig; no sign run."""
import argparse
import io
import json
from pathlib import Path
import unittest
from flint import ctx
from . import Config
from .tests import test_revision_r2, test_revision_r3, run_tests, width_r3
from .tests.resumable import cli
from .run_diagnostics import measure

def regression(module):
    suite=unittest.defaultTestLoader.loadTestsFromModule(module)
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    print(stream.getvalue(),flush=True)
    detail={"tests":result.testsRun,"failures":len(result.failures),
            "errors":len(result.errors),"skipped":len(result.skipped)}
    if not result.wasSuccessful():
        raise AssertionError(json.dumps(detail))
    return detail

def case_list(full):
    # --full adds the original 23 and all 36 R3 gates; their contents are fixed.
    tests=[("R2_regression_11",lambda:regression(test_revision_r2)),
           ("R3_regression_6",lambda:regression(test_revision_r3))]
    if full:
        tests += [("legacy_"+name,fn) for name,fn in run_tests.case_list(True)]
        tests += [("width_"+name,fn) for name,fn in width_r3.case_list()]
    return tests

def main():
    cli(case_list,Config().precision,Path(__file__).resolve().parent)

if __name__=="__main__": main()
