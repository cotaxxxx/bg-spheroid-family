#!/bin/bash
set -u
ROOT=/home/daybreak/gap1-run-v0-4-out/v91_parallel_NOT_EVIDENCE
mkdir -p "$ROOT"
cd /home/daybreak/gap1-run-v0-4
export PYTHONPATH=/home/daybreak/gap1-run-v0-4 PYTHONUNBUFFERED=1
export C1B_PREFLIGHT_RECORD_DIR="$ROOT/preflight_records"
mkdir -p "$C1B_PREFLIGHT_RECORD_DIR"
export -f nothing 2>/dev/null || true
seq 48 116 | sed 's/^/X /' > "$ROOT/jobs.txt"
seq 0 47 | sed 's/^/L /' >> "$ROOT/jobs.txt"
cat "$ROOT/jobs.txt" | xargs -P 10 -n 2 sh -c '/home/daybreak/.pyenv/versions/3.11.16/bin/python /home/daybreak/gap1-run-v0-4-out/v91_parallel_worker.py "$0" "$1" > "'$ROOT'/${0}_${1}.stdout" 2>&1; ret=$?; if [ "$ret" -ne 0 ]; then echo "FAIL_OR_ERROR $0 $1 $ret" >> "'$ROOT'/failures.txt"; fi; exit 0'
python3 - <<'PY'
import json,pathlib,collections
p=pathlib.Path('/home/daybreak/gap1-run-v0-4-out/v91_parallel_NOT_EVIDENCE'); r=[json.loads(f.read_text()) for f in p.glob('[XL]_*.json')];print('COMPLETE',len(r),'PASS',sum(x['PASS'] for x in r),'FAIL',[(x['region'],x['slab']) for x in r if not x['PASS']]);print('ERROR_FILES',[x.name for x in p.glob('*.error')]);print('MISSING',set(('X',i) for i in range(48,117)).union(('L',i) for i in range(48)) - set((x['region'],x['slab']) for x in r))
PY
