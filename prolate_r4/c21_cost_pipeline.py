"""One-shot C21 H 24 case cost-trim pilot and checkpoint packaging.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No covering.
"""
from . import c21_cost_runner as runner
from . import c21_cost_verify as verifier
from . import c21_cost_model as model
from . import c21_cost_receipt as receipt
from . import c21_cost_pack as pack
def main():
 try:
  runner.run()
 finally:
  verifier.verify()
  model.build()
  receipt.build()
  pack.run()
if __name__=="__main__":main()
