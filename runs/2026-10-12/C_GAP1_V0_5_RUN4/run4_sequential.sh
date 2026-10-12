#!/usr/bin/env bash
set -euo pipefail
WT=/home/daybreak/gap1-run-v0-5
ROOT=/home/daybreak/gap1-run-v0-5-out
OUT=$ROOT/run4
PY=/home/daybreak/.pyenv/versions/3.11.16/bin/python
EXPECTED=26d81e1049340d44ef7f08ae8e17d0692983395b
EXPECTED_PARENT=85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b
EXPECTED_TSV=$ROOT/v0_5_expected_25.tsv
FAMILY_WT=/home/daybreak/bg-spheroid-family-gap1-run4
FAMILY_BASE=01450596c13b3ae6b0a89909959edf8810f06b9f
mkdir -p "$OUT/preflight_records"
cd "$WT"
export C1B_PREFLIGHT_RECORD_DIR="$OUT/preflight_records" PYTHONUNBUFFERED=1
printf '%s\n' "$EXPECTED" > "$OUT/RUN_COMMIT.txt"

finalize_evidence(){
  local status="$1" reason="$2" dest commit tarstate
  echo "FINALIZE $status $reason $(date -Is)" | tee -a "$OUT/sequence.log"
  # Push immutable RUN_COMMIT branch. If this fails, downgrade to STOP but still try to save evidence.
  if ! git -C "$WT" push -q origin "refs/heads/run/c-gap1-v0-5:refs/heads/run/c-gap1-v0-5"; then
    status=STOP; reason="$reason;CODE_BRANCH_PUSH_FAILED"
    echo "FINALIZE_NOTE CODE_BRANCH_PUSH_FAILED $(date -Is)" | tee -a "$OUT/sequence.log"
  fi
  if [[ "$status" == PASS ]]; then
    dest="$FAMILY_WT/runs/2026-10-12/C_GAP1_V0_5_RUN4"
  else
    dest="$FAMILY_WT/runs/2026-10-12/C_GAP1_V0_5_RUN4_STOP"
  fi
  git -C "$FAMILY_WT" fetch -q origin main || { echo "LOCAL_STOP FAMILY_FETCH_FAILED"; return 20; }
  if [[ "$(git -C "$FAMILY_WT" rev-parse origin/main)" != "$FAMILY_BASE" ]]; then
    echo "LOCAL_STOP FAMILY_MAIN_CHANGED expected=$FAMILY_BASE actual=$(git -C "$FAMILY_WT" rev-parse origin/main)" | tee -a "$OUT/sequence.log"
    return 21
  fi
  [[ -z "$(git -C "$FAMILY_WT" status --porcelain)" ]] || { echo "LOCAL_STOP FAMILY_STAGING_DIRTY"; return 22; }
  [[ "$(git -C "$FAMILY_WT" rev-parse HEAD)" == "$FAMILY_BASE" ]] || { echo "LOCAL_STOP FAMILY_STAGING_HEAD_CHANGED"; return 23; }
  [[ ! -e "$dest" ]] || { echo "LOCAL_STOP EVIDENCE_DEST_EXISTS $dest"; return 24; }
  mkdir -p "$dest"
  cp -a "$OUT" "$dest/run4"
  cp "$WT/gap1_analysis/GAP1_RESUMABLE_PINS.json" "$dest/GAP1_RESUMABLE_PINS.json"
  cp "$ROOT/run4_sequential.sh" "$dest/run4_sequential.sh"
  cp "$EXPECTED_TSV" "$dest/RUN_COMMIT_25_BLOBS.tsv"
  cat > "$dest/README.md" <<EOF
# C_GAP1 v0.5 run4 — $status

Status: **$status**
Reason: \`$reason\`
RUN_COMMIT: \`$EXPECTED\`
Parent: \`$EXPECTED_PARENT\`
Branch: \`run/c-gap1-v0-5\`
Execution: FREEZE instruction v1 steps 0–6, sequential runner, Python 3.11.16.
Preflight comparison: run3 rule (4 required checks plus FAIL-line set compared lineage-by-lineage with run2).
The earlier v9/v9.1 parallel diagnostics remain NOT_EVIDENCE and are not used as run4 proof evidence.
EOF
  (cd "$dest" && find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS.txt)
  git -C "$FAMILY_WT" add "runs/2026-10-12/$(basename "$dest")"
  git -C "$FAMILY_WT" commit -q -m "C gap1 v0.5 run4 $status evidence (2026-10-12)"
  commit=$(git -C "$FAMILY_WT" rev-parse HEAD)
  if ! git -C "$FAMILY_WT" push -q origin HEAD:main; then
    echo "LOCAL_STOP FAMILY_EVIDENCE_PUSH_FAILED commit=$commit" | tee -a "$OUT/sequence.log"
    return 25
  fi
  echo "PUSH_COMPLETE status=$status family_commit=$commit run_commit=$EXPECTED reason=$reason $(date -Is)" | tee -a "$OUT/sequence.log"
  return 0
}

stop(){
  local reason="$*"
  echo "STOP $reason $(date -Is)" | tee -a "$OUT/sequence.log"
  set +e
  finalize_evidence STOP "$reason"
  rc=$?
  set -e
  if [[ "$rc" -ne 0 ]]; then
    echo "STOP_EVIDENCE_NOT_PUSHED finalize_rc=$rc reason=$reason $(date -Is)" | tee -a "$OUT/sequence.log"
  fi
  exit 1
}

check_preflight(){
  local f="$1" count
  count=$(grep -c '^GAP1_STUB_CONTROL .* PASS$' "$f" || true)
  [[ "$count" == 11 ]] || stop "STUB_COUNT $f $count"
  grep -q '^GAP1_READ_ONLY_PIN .* PASS ' "$f" || stop "READ_ONLY_PIN $f"
  grep -q '^C1B_PREFLIGHT_ESTIMATES ' "$f" || stop "ESTIMATES $f"
  grep -q '^C1B_LEDGER_ONLY_WRITES_REPOSITORY False$' "$f" || stop "LEDGER_ONLY $f"
  echo "PREFLIGHT_PASS $f" | tee -a "$OUT/sequence.log"
}

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
 print('BASELINE_ONLY',sorted(a-b)); print('CURRENT_ONLY',sorted(b-a)); sys.exit(1)
PYCOMPARE
}

run_step(){
  local name="$1"; shift
  echo "START $name $(date -Is)" | tee -a "$OUT/sequence.log"
  set +e
  "$PY" "$@" > "$OUT/$name.stdout" 2>&1
  local rc=$?
  set -e
  [[ "$rc" -eq 0 ]] || stop "$name EXIT_NONZERO rc=$rc"
  echo "EXIT_ZERO $name $(date -Is)" | tee -a "$OUT/sequence.log"
}

# Step 0 — exclusive occupancy.
if ps -eo pid,args | grep -E '[g]lobal_axial_c1b_(producer|checker).*--run-dir|[D]5.*run' | grep -v "$$" > "$OUT/other_run_check.txt"; then
  stop OTHER_RUN_ACTIVE
fi
echo "STEP0_PASS no_other_full_run $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 1 — exact RUN_COMMIT / branch / cleanliness / 25 blobs.
[[ "$(git rev-parse HEAD)" == "$EXPECTED" ]] || stop WRONG_COMMIT
[[ "$(git rev-parse HEAD~1)" == "$EXPECTED_PARENT" ]] || stop WRONG_PARENT
[[ "$(git branch --show-current)" == run/c-gap1-v0-5 ]] || stop WRONG_BRANCH
[[ -z "$(git status --porcelain)" ]] || stop DIRTY_TREE
[[ "$($PY -c 'import sys;print(sys.executable)')" == "$PY" ]] || stop WRONG_PYTHON
n=0
while read -r p e; do
  n=$((n+1)); a=$(git rev-parse "HEAD:$p")
  [[ "$a" == "$e" ]] || stop "BLOB_MISMATCH $p actual=$a expected=$e"
done < "$EXPECTED_TSV"
[[ "$n" == 25 ]] || stop "BLOB_TABLE_COUNT $n"
echo "STEP1_PASS RUN_COMMIT_25_BLOBS $EXPECTED $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 2 — import-only origin test.
set +e
"$PY" - <<'PYIMPORT' > "$OUT/import_only.stdout" 2>&1
import importlib.util
from gap1_analysis import c1b_resumable_driver as p
pin=p.load_pins()['producer']
root='/home/daybreak/gap1-run-v0-5/'
for rel in pin['blob_paths']:
    if rel.startswith('gap1_') or rel.startswith(('producer/','checker/')):
        name=rel[:-3].replace('/','.') if rel.endswith('.py') else rel
        s=importlib.util.find_spec(name)
        assert s is not None and s.origin is not None and s.origin.startswith(root),(name,s)
        print('IMPORT_ONLY_PASS',name,s.origin)
PYIMPORT
rc=$?
set -e
[[ "$rc" -eq 0 ]] || stop IMPORT_ONLY
count=$(grep -c '^IMPORT_ONLY_PASS ' "$OUT/import_only.stdout" || true)
[[ "$count" == 24 ]] || stop "IMPORT_ONLY_COUNT $count"
echo "STEP2_PASS import_only count=$count $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 3 — producer then checker preflight; compare FAIL-line sets against run2 lineage-by-lineage.
run_step producer_preflight -m gap1_producer.global_axial_c1b_producer --ledger-only
check_preflight "$OUT/producer_preflight.stdout"
check_negative_fail_lines "$OUT/producer_preflight.stdout"
run_step checker_preflight -m gap1_checker.global_axial_c1b_checker --ledger-only
check_preflight "$OUT/checker_preflight.stdout"
check_negative_fail_lines "$OUT/checker_preflight.stdout"
echo "STEP3_PASS both_preflights $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 4 — producer full run, sequential.
run_step producer_run -m gap1_producer.global_axial_c1b_producer --run-dir "$OUT/producer"
[[ -s "$OUT/producer/checker_replay_exact.jsonl" ]] || stop REPLAY_MISSING
[[ -s "$OUT/producer/ledger.jsonl" ]] || stop PRODUCER_LEDGER_MISSING
grep -q '^C1B_RESUMABLE_FINAL PASS ' "$OUT/producer_run.stdout" || stop PRODUCER_FINAL_PASS_MISSING
"$PY" - "$OUT/producer/ledger.jsonl" <<'PYCHECKP' || stop PRODUCER_LEDGER_FINAL_STATE
import json,sys
r=[json.loads(x) for x in open(sys.argv[1]) if x.strip()]
ends=[x for x in r if x.get('record_type')=='segment_end']
assert ends and ends[-1]['payload']['reason']=='completed', ends[-1] if ends else None
assert ends[-1]['payload'].get('exact_union') is True, ends[-1]
sl=[x['payload'] for x in r if x.get('record_type')=='slab_record']
assert not any(x.get('decision')=='ABORT' for x in sl)
print('PRODUCER_LEDGER_FINAL_STATE PASS accepted',sum(x.get('decision')=='ACCEPT' for x in sl),'attempts',len(sl))
PYCHECKP
echo "STEP4_PASS producer $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 5 — checker fixed replay, sequential.
run_step checker_run -m gap1_checker.global_axial_c1b_checker --run-dir "$OUT/checker" --replay-plan "$OUT/producer/checker_replay_exact.jsonl" --producer-ledger "$OUT/producer/ledger.jsonl"
grep -q '^GAP1_PLAN_ORDER_AUDIT PASS ' "$OUT/checker_run.stdout" || stop PLAN_ORDER
grep -q '^C1B_CHECKER_FIXED_REPLAY_FINAL PASS ' "$OUT/checker_run.stdout" || stop CHECKER_FINAL_PASS_MISSING
[[ -s "$OUT/checker/ledger.jsonl" ]] || stop CHECKER_LEDGER_MISSING
"$PY" - "$OUT/producer/checker_replay_exact.jsonl" "$OUT/checker/ledger.jsonl" <<'PYCHECKC' || stop CHECKER_REPLAY_FINAL_STATE
import json,sys
plan=[json.loads(x) for x in open(sys.argv[1]) if x.strip()]
r=[json.loads(x) for x in open(sys.argv[2]) if x.strip()]
sl=[x['payload'] for x in r if x.get('record_type')=='slab_record']
ends=[x for x in r if x.get('record_type')=='segment_end']
assert len(sl)==len(plan),(len(sl),len(plan))
assert all(x.get('checker_decision')=='REPLAYED' for x in sl)
assert ends and ends[-1]['payload']['reason']=='completed',ends[-1] if ends else None
assert ends[-1]['payload'].get('exact_union') is True,ends[-1]
print('CHECKER_REPLAY_FINAL_STATE PASS replayed',len(sl))
PYCHECKC
echo "STEP5_PASS checker $(date -Is)" | tee -a "$OUT/sequence.log"

# Step 6 — immutable branch + run evidence push.
echo "RUN4_COMPLETED $(date -Is)" | tee -a "$OUT/sequence.log"
if ! finalize_evidence PASS COMPLETED; then
  echo "STOP STEP6_EVIDENCE_PUSH_FAILED $(date -Is)" | tee -a "$OUT/sequence.log"
  exit 1
fi
exit 0
