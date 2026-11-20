"""Structural/sign checker for the axis ledger; not an independent interval kernel.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import csv, hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
DEN = 65536
PLAN_HASH = 'cfa70836e2409497545b071ced6392155ff09478c59e567b21ee3f5f84325618'
KERNEL_HASH = '09a1747b77163068910e293dec3bee1b2cb6f5b72460bce6dd131db90c68004e'
S_BOUNDS = {'A': (81919, 81921), 'B': (134348, 134350)}
CASES = {
    'A1': ('A', 1, Fraction(3, 8), Fraction(1, 2), [-1, 1, 1]),
    'A2': ('A', 2, Fraction(27, 32), Fraction(29, 32), [-1, -1, 1]),
    'B2': ('B', 2, Fraction(7, 8), Fraction(15, 16), [-1, -1, 1]),
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load(name):
    path = ROOT / 'out' / name
    stages = defaultdict(dict)
    for row in csv.DictReader(path.open()):
        for key in ['axis', 's0', 's1', 't0', 't1', 'shape_den', 'r0', 'r1', 'r_den', 'nmu', 'nw']:
            row[key] = int(row[key])
        for key in ['lower', 'upper', 'seconds']:
            row[key] = float(row[key])
            require(math.isfinite(row[key]), 'Nonfinite ledger entry')
        require(row['lower'] <= row['upper'], 'Reversed value interval')
        require(row['seconds'] >= 0, 'Negative runtime')
        require((row['s0'], row['s1']) == S_BOUNDS[row['shape']], 'Wrong shape box')
        require((row['t0'], row['t1'], row['shape_den'], row['r_den']) == (196607, 196609, DEN, DEN), 'Wrong endpoints/denominator')
        require(row['nw'] * 2 == row['nmu'], 'Wrong angular grid aspect')
        key = (row['run'], row['mode'], row['nmu'])
        require(row['quantity'] not in stages[key], 'Duplicate quantity')
        stages[key][row['quantity']] = row
    for stage in stages.values():
        exemplar = next(iter(stage.values()))
        expected = {'g'} if exemplar['mode'] in ('left', 'right') else {'g', 'H11', 'H22', 'H33'}
        if exemplar['mode'].startswith('band_'):
            expected.add('Ux')
        require(set(stage) == expected, 'Incomplete stage quantities')
        metadata = set(exemplar) - {'quantity', 'lower', 'upper'}
        require(all(all(row[k] == exemplar[k] for k in metadata) for row in stage.values()), 'Inconsistent stage metadata')
    return path, stages

def bounds(row):
    return [row['lower'], row['upper']]

def hessian_signs(stage, signs):
    return all(stage[f'H{i+1}{i+1}']['lower'] > 0 if sign > 0 else stage[f'H{i+1}{i+1}']['upper'] < 0 for i, sign in enumerate(signs))

def check_case(label):
    sh, axis, ra, rb, signs = CASES[label]
    path, stages = load('axis_' + label + '.csv')
    ends = {}
    bands = defaultdict(dict)
    unresolved = 0
    for (run, mode, m), stage in stages.items():
        row = stage['g']
        require((run, row['shape'], row['axis']) == (label, sh, axis), 'Wrong branch metadata')
        rlo, rhi = Fraction(row['r0'], DEN), Fraction(row['r1'], DEN)
        if mode in ('left', 'right'):
            require(m in [256, 512, 1024, 2048, 4096, 8192], 'Undeclared endpoint grid')
            require(rlo == rhi == (ra if mode == 'left' else rb), 'Wrong endpoint radius')
            good = row['lower'] > 0 if mode == 'left' else row['upper'] < 0
            if good:
                ends[mode] = {'nmu': m, 'g': bounds(row), 'seconds': row['seconds']}
        else:
            require(mode.startswith('band_'), 'Unknown mode')
            _, ns, ps = mode.split('_')
            n, panel = int(ns), int(ps)
            require(n in [8, 16, 32, 64] and 0 <= panel < n, 'Undeclared panel')
            require(m in [128, 256, 512, 1024, 2048], 'Undeclared panel grid')
            require(rlo == ra+(rb-ra)*panel/n and rhi == ra+(rb-ra)*(panel+1)/n, 'Wrong panel endpoints')
            good = hessian_signs(stage, signs) and stage['Ux']['upper'] < 0
            if good:
                bands[n][panel] = stage
        require(row['result'] == ('sign' if good else 'unresolved'), 'Ledger reason inconsistent with values')
        unresolved += not good
    require(set(ends) == {'left', 'right'}, 'Endpoint sign missing')
    complete = [n for n, panels in bands.items() if set(panels) == set(range(n))]
    require(complete, 'No complete derivative/Hessian cover')
    n = min(complete)
    selected = [bands[n][p] for p in range(n)]
    envelopes = {q: [min(st[q]['lower'] for st in selected), max(st[q]['upper'] for st in selected)] for q in ['H11', 'H22', 'H33', 'Ux']}
    return {
        'status': 'verified_inclusions', 'source': path.name, 'sha256': digest(path),
        'shape': sh, 'axis': axis, 's_integer_endpoints': S_BOUNDS[sh],
        't_integer_endpoints': [196607, 196609], 'shape_denominator': DEN,
        'rational_bracket': [str(ra), str(rb)], 'endpoint_signs': ends,
        'complete_cover_panels': n,
        'selected_panel_grids': [st['g']['nmu'] for st in selected],
        'selected_radius_integer_endpoints': [[st['g']['r0'], st['g']['r1']] for st in selected],
        'radius_denominator': DEN, 'whole_bracket_envelopes': envelopes,
        'Hessian_signs': signs, 'Morse_index': signs.count(-1),
        'stage_count': len(stages), 'unresolved_stage_count': unresolved,
        'all_stage_seconds': sum(st['g']['seconds'] for st in stages.values()),
        'selected_stage_seconds': sum(st['g']['seconds'] for st in selected)+sum(v['seconds'] for v in ends.values()),
        'angular_cell_evaluations': sum(st['g']['nmu']*st['g']['nw'] for st in stages.values()),
    }

def check_centers():
    path, stages = load('axis_centers.csv')
    selected = {}
    for (run, mode, m), stage in stages.items():
        row = stage['g']; sh = row['shape']
        require(run == sh+'0' and mode == 'center' and row['axis'] == 1, 'Wrong center metadata')
        require(row['r0'] == row['r1'] == 0, 'Nonzero center radius')
        require(m in [128, 256, 512, 1024, 2048], 'Undeclared center grid')
        signs = [1, 1, 1] if sh == 'A' else [-1, 1, 1]
        good = hessian_signs(stage, signs)
        require(row['result'] == ('sign' if good else 'unresolved'), 'Center reason inconsistent with values')
        if good:
            selected[sh] = {'nmu': m, 'Hessian': {q: bounds(stage[q]) for q in ['H11', 'H22', 'H33']}, 'Morse_index': signs.count(-1)}
    require(set(selected) == {'A', 'B'}, 'Missing center inclusion')
    return {'status': 'verified_inclusions', 'source': path.name, 'sha256': digest(path), 'centers': selected,
            'all_stage_seconds': sum(st['g']['seconds'] for st in stages.values()),
            'angular_cell_evaluations': sum(st['g']['nmu']*st['g']['nw'] for st in stages.values())}

def main():
    require(digest(ROOT/'plans/PLAN_AXIS.md') == PLAN_HASH, 'Plan hash changed')
    require(digest(ROOT/'code/axis_interval.py') == KERNEL_HASH, 'Kernel hash changed')
    cases = {key: check_case(key) for key in CASES}
    centers = check_centers()
    result = {'designation': 'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
              'checker_scope': 'Hashes, endpoint signs, declared integer boxes, complete panel coverage and strict Hessian/Ux signs; no independent re-evaluation of interval kernels.',
              'plan_sha256': PLAN_HASH, 'kernel_sha256': KERNEL_HASH,
              'status': 'verified_inclusions', 'cases': cases, 'center_results': centers,
              'total_evaluation_seconds': sum(c['all_stage_seconds'] for c in cases.values())+centers['all_stage_seconds'],
              'limitations': ['No exclusion of axial roots outside the stated brackets.',
                              'No off-axis exclusion.', 'No center or boundary collar estimate.',
                              'No global root count or global main-rectangle estimate.']}
    target = ROOT/'out/axis_check.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'file': str(target), 'seconds': result['total_evaluation_seconds']}))

if __name__ == '__main__':
    main()
