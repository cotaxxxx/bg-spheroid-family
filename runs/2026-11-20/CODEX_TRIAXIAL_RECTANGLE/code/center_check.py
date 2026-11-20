"""Check frozen center pilots and their exact shape geometry.

DIAGNOSTIC_ONLY / NOT_EVIDENCE. This checks ledger structure and signs;
it does not independently re-integrate the kernels or prove the new
integration-by-parts theorem.
"""
from pathlib import Path
from fractions import Fraction
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]


def require(value, message):
    if not value:
        raise ValueError(message)


def check_manifest(name, archived=None):
    archived = archived or {}
    checked = []
    for line in (ROOT / 'plans' / name).read_text().splitlines():
        digest, path = line.split(maxsplit=1)
        selected = archived.get(path, path)
        actual = hashlib.sha256((ROOT / selected).read_bytes()).hexdigest()
        require(actual == digest, f'Frozen hash mismatch: {name}: {selected}')
        checked.append({'recorded_path': path, 'stored_path': selected, 'sha256': digest})
    return checked


def geometry(row):
    c = int(row['case'])
    mode = row.get('mode')
    if mode:
        j, i = divmod(c, 4)
        lower_s, lower_t = 1280 + 704*i, 1280 + 800*j
        bounds = [lower_s, lower_s+704, lower_t, lower_t+800]
        if mode == 'shape_midpoint':
            bounds = [lower_s+352]*2 + [lower_t+400]*2
        require(mode in ['full_shape_box', 'shape_midpoint'], 'Unknown center mode')
        return bounds, 1280
    shrink = int(row['shrink'])
    if c == 32:
        return [524288-90112//shrink, 524288, 983040-102400//shrink, 983040], 163840
    j, i = divmod(c, 4)
    sm, tm = (1280+704*i+352)*128, (1280+800*j+400)*128
    ds, dt = 45056//shrink, 51200//shrink
    return [sm-ds, sm+ds, tm-dt, tm+dt], 163840


def check_ledger(name, expected_keys, key_fields):
    rows = list(csv.DictReader((ROOT / 'out' / name).open()))
    actual_keys = []
    groups = {}
    for row in rows:
        key = tuple(row[k] for k in key_fields)
        actual_keys.append(key)
        expected, scale = geometry(row)
        actual = [int(row[k]) for k in ['slo_i', 'shi_i', 'tlo_i', 'thi_i']]
        require(actual == expected and int(row['scale']) == scale, 'Center box geometry mismatch')
        s0, s1, t0, t1 = [Fraction(n, scale) for n in actual]
        require(1 <= s0 <= s1 <= Fraction(16, 5) and 1 <= t0 <= t1 <= 6, 'Center box outside R')
        require(int(row['component']) == 3, 'Unexpected component')
        require(int(row['nw'])*2 == int(row['nmu']), 'Unexpected angular aspect ratio')
        lo, hi = float(row['lower']), float(row['upper'])
        require(math.isfinite(lo) and math.isfinite(hi) and lo <= hi, 'Invalid center interval')
        require(row['result'] == ('positive' if lo > 0 else 'unresolved'), 'Center sign mismatch')
        group = (row.get('mode', 'finite_shape_box'), row.get('mapping', '1'), row['nmu'])
        g = groups.setdefault(group, {'rows': 0, 'positive': 0, 'min_lower': math.inf, 'elapsed_seconds': 0})
        g['rows'] += 1
        g['positive'] += lo > 0
        g['min_lower'] = min(g['min_lower'], lo)
        g['elapsed_seconds'] += float(row['elapsed_seconds'])
    require(len(actual_keys) == len(set(actual_keys)), 'Duplicate center pilot record')
    require(set(actual_keys) == expected_keys, 'Missing or extra center pilot records')
    return {'file': name, 'rows': len(rows), 'groups': [dict(mode=k[0], mapping=k[1], nmu=int(k[2]), **v) for k,v in sorted(groups.items())]}


def main():
    manifests = {}
    for label in ['A', 'A1', 'B', 'C']:
        archive = {'code/center_interval.py': 'code/center_interval_A_original.py'} if label == 'A' else {}
        manifests[label] = check_manifest(f'PLAN_CENTER_{label}.sha256', archive)
    a = {(str(c), m, str(n)) for c in range(32) for m in ['full_shape_box', 'shape_midpoint'] for n in [64,128,256]}
    b = {(str(c), str(shrink), str(n)) for c in [0,7,20,27,31,32] for shrink in [8,16,32,64,128] for n in [512,1024]}
    c = {(str(c), str(shrink), str(mapping), str(n)) for c in [0,7,20,27,31,32] for shrink in [16,32] for mapping in [2,4,8] for n in [128,256,512]}
    ledgers = [
        check_ledger('center_calibration.csv', a, ['case','mode','nmu']),
        check_ledger('center_pilot_b.csv', b, ['case','shrink','nmu']),
        check_ledger('center_pilot_c.csv', c, ['case','shrink','mapping','nmu']),
    ]
    result = {
        'designation': 'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
        'status': 'recorded_geometry_hashes_and_signs_consistent',
        'scope': 'No global numerical cover is claimed. The whole-R h3 bound is analytical; see proofs/center_audit.md.',
        'original_A_error': 'Integer divided by interval was unsupported before any numerical result. The original code and empty ledger remain archived.',
        'frozen_files': manifests,
        'ledgers': ledgers,
    }
    target = ROOT / 'out/center_check.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'ledger_rows': sum(x['rows'] for x in ledgers)}))


if __name__ == '__main__':
    main()
