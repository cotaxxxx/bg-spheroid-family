#!/usr/bin/env bash
set -euo pipefail
cd /home/daybreak/gap1-run-v0-3
export C1B_PREFLIGHT_RECORD_DIR=/home/daybreak/gap1-run-v0-3-out/run2/preflight_records
export PYTHONUNBUFFERED=1
PY=/home/daybreak/.pyenv/versions/3.11.16/bin/python
OUT=/home/daybreak/gap1-run-v0-3-out/run2
EXPECTED=7ec8e087c1da91e8993cdec6c7ac6334149bced1
[[ "$(git rev-parse HEAD)" == "$EXPECTED" ]] || { echo 'STOP WRONG_COMMIT'; exit 1; }
[[ "$(git branch --show-current)" == 'run/c-gap1-v0-3' ]] || { echo 'STOP WRONG_BRANCH'; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo 'STOP DIRTY_TREE'; exit 1; }
[[ "$($PY -c 'import sys;print(sys.executable)')" == "$PY" ]] || { echo 'STOP WRONG_PYTHON'; exit 1; }
check_preflight() {
 local f="$1" count
 count=$(grep -c '^GAP1_STUB_CONTROL .* PASS$' "$f" || true)
 [[ "$count" == 11 ]] || { echo "STOP STUB_COUNT $f $count"; exit 1; }
 grep -q '^GAP1_READ_ONLY_PIN .* PASS ' "$f" || { echo "STOP READ_ONLY_PIN $f"; exit 1; }
 grep -q '^C1B_PREFLIGHT_ESTIMATES ' "$f" || { echo "STOP ESTIMATES $f"; exit 1; }
 grep -q '^C1B_LEDGER_ONLY_WRITES_REPOSITORY False$' "$f" || { echo "STOP LEDGER_ONLY $f"; exit 1; }
 echo "PREFLIGHT_PASS $f" | tee -a "$OUT/sequence.log"
}
run_step() {
 local name="$1"; shift
 echo "START $name $(date -Is)" | tee -a "$OUT/sequence.log"
 "$PY" "$@" > "$OUT/$name.stdout" 2>&1 || { echo "STOP $name EXIT_NONZERO $(date -Is)" | tee -a "$OUT/sequence.log"; exit 1; }
 echo "EXIT_ZERO $name $(date -Is)" | tee -a "$OUT/sequence.log"
}
run_step producer_preflight -m gap1_producer.global_axial_c1b_producer --ledger-only
check_preflight "$OUT/producer_preflight.stdout"
run_step checker_preflight -m gap1_checker.global_axial_c1b_checker --ledger-only
check_preflight "$OUT/checker_preflight.stdout"
run_step producer_run -m gap1_producer.global_axial_c1b_producer --run-dir "$OUT/producer"
[[ -s "$OUT/producer/checker_replay_exact.jsonl" ]] || { echo 'STOP REPLAY_MISSING' | tee -a "$OUT/sequence.log"; exit 1; }
[[ -s "$OUT/producer/ledger.jsonl" ]] || { echo 'STOP PRODUCER_LEDGER_MISSING' | tee -a "$OUT/sequence.log"; exit 1; }
run_step checker_run -m gap1_checker.global_axial_c1b_checker --run-dir "$OUT/checker" --replay-plan "$OUT/producer/checker_replay_exact.jsonl" --producer-ledger "$OUT/producer/ledger.jsonl"
grep -q 'GAP1_PLAN_ORDER_AUDIT.*PASS' "$OUT/checker_run.stdout" || { echo 'STOP PLAN_ORDER' | tee -a "$OUT/sequence.log"; exit 1; }
echo "RUN2_COMPLETED $(date -Is)" | tee -a "$OUT/sequence.log"
