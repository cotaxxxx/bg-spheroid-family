#!/usr/bin/env bash
# DIAGNOSTIC_ONLY / NOT_EVIDENCE. Rebuild, integrate and check in a fresh directory.
set -euo pipefail
pkg=$(cd -- "$(dirname -- "$0")" && pwd -P)
if [[ $# -gt 1 ]]; then echo "usage: bash reproduce.sh [NEW_DIRECTORY]" >&2; exit 2; fi
if [[ $# -eq 1 ]]; then
    mkdir -- "$1"
    out=$(cd -- "$1" && pwd -P)
else
    out=$(mktemp -d)
fi
fp=${FLINT_PYTHON:-python3}
np=${NUMPY_PYTHON:-python3}
py=${PYTHON:-python3}
cc=${CXX:-g++}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
(cd "$pkg" && sha256sum -c SHA256SUMS && for h in PRE{1..5}.sha256; do sha256sum -c "$h"; done)
"$fp" -I -c 'import flint; assert flint.__version__=="0.8.0"'
"$np" -I -c 'import numpy'
"$fp" -IB "$pkg/make_tables.py" "$out/geometry.tbl"
cmp "$out/geometry.tbl" "$pkg/geometry.tbl"
"$cc" -std=c++20 -O3 -fno-fast-math "$pkg/chord_box.cpp" -o "$out/chord_box"
"$cc" -std=c++20 -O2 -fsanitize=undefined -fno-sanitize-recover=all -fno-fast-math "$pkg/chord_box.cpp" -o "$out/chord_replay"
cd "$out"
timeout 90 "$fp" -IB "$pkg/chord_tail.py" > probe1.stdout.jsonl 2>probe1.stderr
timeout 90 "$py" -IB "$pkg/finite_pilot.py" ./chord_box geometry.tbl > probe2.stdout.jsonl 2>probe2.stderr
timeout 960 "$py" -IB "$pkg/run_cover.py" ./chord_box geometry.tbl . > cover3.stdout.jsonl 2>cover3.stderr
"$py" -IB "$pkg/verify_cover.py" . > cover3.verify.jsonl 2>cover3.verify.stderr
timeout 960 "$py" -IB "$pkg/verify_cover.py" . --replay ./chord_replay geometry.tbl > cover3.replay.jsonl 2>cover3.replay.stderr
for k in 5 6 7; do cmp "cover_$k.tsv.gz" "$pkg/cover_$k.tsv.gz"; done
timeout 90 "$np" -IB "$pkg/original_crosscheck.py" > original4.stdout.jsonl 2>original4.stderr
timeout 360 "$fp" -IB "$pkg/spot_arb.py" > spot4.stdout.jsonl 2>spot4.stderr
timeout 300 "$fp" -IB "$pkg/spot_followup.py" spot4.stdout.jsonl > spot5.stdout.jsonl 2>spot5.stderr
"$py" -IB "$pkg/check_claims.py" . | tee EXACT_RESULTS.json
echo "DIAGNOSTIC_ONLY / NOT_EVIDENCE. Outputs in $out"
