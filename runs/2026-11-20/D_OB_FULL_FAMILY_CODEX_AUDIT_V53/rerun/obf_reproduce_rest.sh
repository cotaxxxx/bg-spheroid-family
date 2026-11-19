#!/usr/bin/env bash
# chat: second half of Codex reproduce.sh (stages after thin), run in a scratch copy because the first run's
# timeout would have deleted its temp dir. Same commands, same order, same comparisons.
set -euo pipefail
src=/tmp/claude-0/-home-claude/c84560e9-80f0-5030-8308-5fed2f20ba54/scratchpad/obfx
tmp=/tmp/claude-0/-home-claude/c84560e9-80f0-5030-8308-5fed2f20ba54/scratchpad/obf_rest_work
rm -rf "$tmp"; mkdir -p "$tmp"; cp "$src"/*.py "$src"/*.cpp "$src"/*.hpp "$src"/*.inc "$tmp/"; cd "$tmp"
fp=(-std=c++20 -O3 -ffp-contract=off -fno-fast-math -frounding-math)
for f in map graded pole rim pole_prec; do g++ "${fp[@]}" "$f.cpp" -o "$f"; done
for d in thin leaves finer low window; do cp -r "$src/$d" ./$d; done   # inputs for the checkers (these five were regenerated identically in run 1)
python3 mixed.py ./rim mixed
python3 recover.py ./rim recovered
python3 salvage.py ./rim salvage
python3 rim.py ./rim > rim.tsv
python3 pole.py ./pole > pole.tsv
for d in mixed recovered salvage; do diff -qr "$src/$d" "$d" && echo "$d identical"; done
cmp "$src/rim.tsv" rim.tsv && echo "rim.tsv identical"
cmp "$src/pole.tsv" pole.tsv && echo "pole.tsv identical"
python3 bracket.py ./pole_prec > bracket.log
cmp "$src/bracket.log" bracket.log && echo "bracket.log identical"
python3 checker.py ./map ./graded leaves finer low window && echo "checker OK"
python3 optional_check.py ./rim thin mixed && echo "optional_check OK"
python3 validate_extra.py ./rim rim recovered salvage && echo "validate_extra OK"
for f in rim.unresolved salvage.unresolved; do cmp "$src/$f" "$f" && echo "$f identical"; done
