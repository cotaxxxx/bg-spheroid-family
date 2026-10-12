#!/usr/bin/env bash
set -euo pipefail
WT=/home/daybreak/gap1-run-v0-4
OUT=/home/daybreak/gap1-run-v0-4-out/run3
PY=/home/daybreak/.pyenv/versions/3.11.16/bin/python
mkdir -p "$OUT/preflight_records"
cd "$WT"
export C1B_PREFLIGHT_RECORD_DIR="$OUT/preflight_records" PYTHONUNBUFFERED=1
EXPECTED=d68dfd918b73f3de0158947f5330ee2605646a4b
stop(){ echo "STOP $* $(date -Is)" | tee -a "$OUT/sequence.log"; exit 1; }
[[ "$(git rev-parse HEAD)" == "$EXPECTED" ]] || stop WRONG_COMMIT
[[ "$(git branch --show-current)" == run/c-gap1-v0-4 ]] || stop WRONG_BRANCH
[[ -z "$(git status --porcelain)" ]] || stop DIRTY_TREE
[[ "$($PY -c 'import sys;print(sys.executable)')" == "$PY" ]] || stop WRONG_PYTHON
ps -eo args | grep -E '[g]lobal_axial_c1b_(producer|checker).*--run-dir|[D]5.*run' | grep -v "${0##*/}" && stop OTHER_RUN_ACTIVE || true
"$PY" - <<'PY' > "$OUT/import_only.stdout" 2>&1 || stop IMPORT_ONLY
import importlib.util,json
from gap1_analysis import c1b_resumable_driver as p
pin=p.load_pins()['producer']
for rel in pin['blob_paths']:
 if rel.startswith('gap1_') or rel.startswith(('producer/','checker/')):
  name=rel[:-3].replace('/','.') if rel.endswith('.py') else rel
  s=importlib.util.find_spec(name)
  assert s is not None and s.origin is not None and s.origin.startswith('/home/daybreak/gap1-run-v0-4/'),(name,s)
  print('IMPORT_ONLY_PASS',name,s.origin)
PY
check_preflight(){
 local f="$1" count
 count=$(grep -c '^GAP1_STUB_CONTROL .* PASS$' "$f" || true)
 [[ "$count" == 11 ]] || stop "STUB_COUNT $f $count"
 grep -q '^GAP1_READ_ONLY_PIN .* PASS ' "$f" || stop "READ_ONLY_PIN $f"
 grep -q '^C1B_PREFLIGHT_ESTIMATES ' "$f" || stop "ESTIMATES $f"
 grep -q '^C1B_LEDGER_ONLY_WRITES_REPOSITORY False$' "$f" || stop "LEDGER_ONLY $f"

 echo "PREFLIGHT_PASS $f" | tee -a "$OUT/sequence.log"
}
run_step(){
 local name="$1";shift
 echo "START $name $(date -Is)" | tee -a "$OUT/sequence.log"
 "$PY" "$@" > "$OUT/$name.stdout" 2>&1 || stop "$name EXIT_NONZERO"
 echo "EXIT_ZERO $name $(date -Is)" | tee -a "$OUT/sequence.log"
}
# Resume: producer preflight already completed successfully, do not rerun.
[[ -s "$OUT/producer_preflight.stdout" ]] || stop PRODUCER_PREFLIGHT_MISSING
check_preflight "$OUT/producer_preflight.stdout"
check_negative_fail_lines(){
 local f="$1"
 "$PY" - "$f" <<'PYCOMPARE' || stop "NEGATIVE_FAIL_LINES_MISMATCH $f"
from pathlib import Path
import sys
baseline=Path('/home/daybreak/gap1-run-v0-3-out/run2/'+('checker_preflight.stdout' if 'checker_preflight' in sys.argv[1] else 'producer_preflight.stdout'))
current=Path(sys.argv[1])
a={line for line in baseline.read_text().splitlines() if 'FAIL' in line}
b={line for line in current.read_text().splitlines() if 'FAIL' in line}
print('NEGATIVE_FAIL_LINE_SET',len(a),len(b),'PASS' if a==b else 'FAIL',flush=True)
if a!=b:
 print('BASELINE_ONLY',sorted(a-b));print('CURRENT_ONLY',sorted(b-a));sys.exit(1)
PYCOMPARE
}
check_negative_fail_lines "$OUT/producer_preflight.stdout"
# Resume: checker preflight already completed with exit code zero; do not rerun.
[[ -s "$OUT/checker_preflight.stdout" ]] || stop CHECKER_PREFLIGHT_MISSING
check_preflight "$OUT/checker_preflight.stdout"
check_negative_fail_lines "$OUT/checker_preflight.stdout"
run_step producer_run -m gap1_producer.global_axial_c1b_producer --run-dir "$OUT/producer"
[[ -s "$OUT/producer/checker_replay_exact.jsonl" ]] || stop REPLAY_MISSING
[[ -s "$OUT/producer/ledger.jsonl" ]] || stop PRODUCER_LEDGER_MISSING
run_step checker_run -m gap1_checker.global_axial_c1b_checker --run-dir "$OUT/checker" --replay-plan "$OUT/producer/checker_replay_exact.jsonl" --producer-ledger "$OUT/producer/ledger.jsonl"
grep -q 'GAP1_PLAN_ORDER_AUDIT.*PASS' "$OUT/checker_run.stdout" || stop PLAN_ORDER
[[ -s "$OUT/checker/ledger.jsonl" ]] || stop CHECKER_LEDGER_MISSING
echo "RUN3_COMPLETED $(date -Is)" | tee -a "$OUT/sequence.log"
