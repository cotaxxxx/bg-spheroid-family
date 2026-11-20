"""Check the separately planned wider-box ledger, retaining unresolved outcomes.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Structural/sign check, not an independent kernel.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
import csv, hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
DEN = 65536
SHAPES = {'WA': (81664, 82176), 'WB': (134144, 134656)}
SPECS = {'WA1': ('WA', 1, Fraction(3,8), Fraction(1,2), [-1,1,1]),
         'WA2': ('WA', 2, Fraction(27,32), Fraction(29,32), [-1,-1,1]),
         'WB2': ('WB', 2, Fraction(7,8), Fraction(15,16), [-1,-1,1])}
HASHES = {'plans/PLAN_AXIS_WIDE.md': '3b028842f50ffd316cdf0527f0a2d66ac42ca56482d2e0e2a46692b9f03dc56c',
          'code/axis_wide.py': '172c1c208bdb46e8ef5695127782141e5be0ea62008bdfeba3cf5e6380c0ddda',
          'code/axis_interval.py': '09a1747b77163068910e293dec3bee1b2cb6f5b72460bce6dd131db90c68004e'}

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hsigns(stage, signs):
    return all(stage[f'H{i+1}{i+1}']['lower'] > 0 if sign > 0 else stage[f'H{i+1}{i+1}']['upper'] < 0 for i,sign in enumerate(signs))

def bounds(stage, quantities):
    return {q: [stage[q]['lower'], stage[q]['upper']] for q in quantities}

def main():
    for name, value in HASHES.items():
        require(digest(ROOT/name) == value, 'Frozen input hash mismatch')
    stages = defaultdict(dict)
    for row in csv.DictReader((ROOT/'out/axis_wide.csv').open()):
        for key in ['axis','s0','s1','t0','t1','shape_den','r0','r1','r_den','nmu','nw']:
            row[key] = int(row[key])
        for key in ['lower','upper','seconds']:
            row[key] = float(row[key]); require(math.isfinite(row[key]), 'Nonfinite entry')
        require(row['lower'] <= row['upper'], 'Reversed interval')
        require((row['s0'],row['s1']) == SHAPES[row['shape']], 'Wrong shape s')
        require((row['t0'],row['t1'],row['shape_den'],row['r_den']) == (196352,196864,DEN,DEN), 'Wrong shape t/denominator')
        require(row['nmu'] == 2*row['nw'], 'Wrong grid aspect')
        key = (row['run'],row['mode'],row['nmu'])
        require(row['quantity'] not in stages[key], 'Duplicate quantity')
        stages[key][row['quantity']] = row
    centers = {}
    endpoints = defaultdict(dict)
    bands = defaultdict(lambda: defaultdict(dict))
    last_endpoints = defaultdict(dict)
    unresolved = 0
    for (label,mode,m), stage in stages.items():
        row = stage['g']; sh = row['shape']
        expected = {'g'} if mode in ['left','right'] else {'g','H11','H22','H33'}
        if mode.startswith('band_'):
            expected.add('Ux')
        require(set(stage) == expected, 'Missing/extra quantity')
        fields = set(row)-{'quantity','lower','upper'}
        require(all(all(v[k] == row[k] for k in fields) for v in stage.values()), 'Inconsistent stage metadata')
        rlo,rhi = Fraction(row['r0'],DEN),Fraction(row['r1'],DEN)
        if mode == 'center':
            require(label == sh+'0' and row['axis'] == 1 and rlo == rhi == 0, 'Wrong center')
            require(m in [128,256,512,1024,2048], 'Undeclared center grid')
            signs = [1,1,1] if sh == 'WA' else [-1,1,1]
            good = hsigns(stage, signs)
            if good:
                centers[sh] = {'status': 'verified_inclusions', 'nmu': m, 'Hessian': bounds(stage,['H11','H22','H33']), 'Morse_index': signs.count(-1)}
        else:
            esh,axis,ra,rb,signs = SPECS[label]
            require((sh,row['axis']) == (esh,axis), 'Wrong branch')
            if mode in ['left','right']:
                require(rlo == rhi == (ra if mode == 'left' else rb), 'Wrong endpoint')
                require(m in [256,512,1024,2048,4096,8192], 'Undeclared endpoint grid')
                good = row['lower'] > 0 if mode == 'left' else row['upper'] < 0
                last_endpoints[label][mode] = {'nmu':m,'g':[row['lower'],row['upper']],'status':'sign_obtained' if good else 'unresolved'}
                if good:
                    endpoints[label][mode] = last_endpoints[label][mode]
            else:
                require(mode.startswith('band_'), 'Unknown mode')
                _,ns,ps = mode.split('_'); n,p = int(ns),int(ps)
                require(n in [8,16] and 0 <= p < n, 'Undeclared panel')
                require(m in [128,256,512,1024,2048], 'Undeclared panel grid')
                require(rlo == ra+(rb-ra)*p/n and rhi == ra+(rb-ra)*(p+1)/n, 'Wrong panel radius')
                good = hsigns(stage,signs) and stage['Ux']['upper'] < 0
                if good:
                    bands[label][n][p] = stage
        require(row['result'] == ('sign' if good else 'unresolved'), 'Recorded sign decision inconsistent')
        unresolved += not good
    cases = {}
    for label,(sh,axis,ra,rb,signs) in SPECS.items():
        record = {'status': 'unresolved', 's_integer_endpoints':SHAPES[sh], 't_integer_endpoints':[196352,196864],
                  'shape_denominator':DEN, 'axis':axis, 'rational_bracket':[str(ra),str(rb)],
                  'last_endpoint_results':last_endpoints[label]}
        complete = [n for n,v in bands[label].items() if set(v) == set(range(n))]
        if set(endpoints[label]) == {'left','right'} and complete:
            n = min(complete); selected = [bands[label][n][p] for p in range(n)]
            record.update(status='verified_inclusions', complete_cover_panels=n,
                          selected_panel_grids=[v['g']['nmu'] for v in selected],
                          whole_bracket_envelopes={q:[min(v[q]['lower'] for v in selected),max(v[q]['upper'] for v in selected)] for q in ['H11','H22','H33','Ux']},
                          Hessian_signs=signs, Morse_index=signs.count(-1))
        local_stages = [v for (lab,_,_),v in stages.items() if lab == label]
        record['stage_count'] = len(local_stages)
        record['all_stage_seconds'] = sum(v['g']['seconds'] for v in local_stages)
        cases[label] = record
    run = json.loads((ROOT/'out/axis_wide_run.json').read_text())
    require(run['ledger_sha256'] == digest(ROOT/'out/axis_wide.csv'), 'Run summary ledger hash mismatch')
    success = sum(v['status'] == 'verified_inclusions' for v in cases.values())
    result = {'designation':'DIAGNOSTIC_ONLY / NOT_EVIDENCE', 'checker_scope':'Frozen hashes, declared integer boxes/grids, complete panel covers and strict signs. No independent integral re-evaluation.',
              'status':'checked_with_unresolved_results' if success < len(SPECS) else 'verified_inclusions',
              'successful_branch_count':success, 'cases':cases, 'centers':centers,
              'stage_count':len(stages), 'unresolved_stage_count':unresolved,
              'total_evaluation_seconds':sum(v['g']['seconds'] for v in stages.values()),
              'angular_cell_evaluations':sum(v['g']['nmu']*v['g']['nw'] for v in stages.values()),
              'run_status':run['status'], 'cpu_seconds':run['cpu_seconds'],
              'ledger_sha256':run['ledger_sha256'], 'frozen_hashes':HASHES,
              'limitations':['No axial root exclusion outside the three brackets.', 'No off-axis or boundary exclusion.', 'No total root count.']}
    path = ROOT/'out/axis_wide_check.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'successful_branches':success,'file':str(path)}))

if __name__ == '__main__':
    main()
