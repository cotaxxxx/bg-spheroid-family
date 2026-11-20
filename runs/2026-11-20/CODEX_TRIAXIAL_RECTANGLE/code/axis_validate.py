"""Numerical sanity comparison with the unchanged source C quadrature.
This is not a second rigorous integration implementation.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
import csv, hashlib, importlib, json, os, platform, shutil, subprocess, sys, tempfile
import numpy as np
import scipy
from axis_interval import Box, angles, pi_box, DEN

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent/'baseline/TRIAXIAL_FIRST_ATLAS_20261120/code'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    checker = json.loads((ROOT/'out/axis_check.json').read_text())
    constants = {}
    for name, interval, expected in zip(['P(1)', 'F(1)', 'Q(1)'], angles(Box(1)), [2., 0., 10./3.]):
        lo, hi = float(interval.a), float(interval.b)
        require(lo <= expected <= hi, 'Angle constant missing from interval')
        constants[name] = {'interval': [lo, hi], 'numeric_reference': expected}
    pi = pi_box()
    require(float(pi.a) < np.pi < float(pi.b), 'Pi interval sanity mismatch')
    compiler = subprocess.check_output(['gcc', '--version'], text=True).splitlines()[0]
    records = []
    with tempfile.TemporaryDirectory(prefix='axis_source_comparison_') as directory:
        target = Path(directory)
        for name in ['kernel.c', 'common.py', 'refine.py']:
            shutil.copyfile(SOURCE/name, target/name)
        subprocess.run(['gcc', '-O2', '-std=c11', '-fPIC', '-shared', str(target/'kernel.c'), '-lm', '-o', str(target/'kernel.so')], check=True)
        sys.path.insert(0, str(target))
        ref = importlib.import_module('refine')
        for label, case in checker['cases'].items():
            rows = list(csv.DictReader((ROOT/'out'/case['source']).open()))
            s = sum(case['s_integer_endpoints'])/(2*DEN)
            t = 3.
            for end, data in case['endpoint_signs'].items():
                selected = next(row for row in rows if row['mode'] == end and int(row['nmu']) == data['nmu'])
                r = int(selected['r0'])/DEN
                u, h = ref.ax(s, t, case['axis']-1, r, 96)
                g = float(r*u)
                lo, hi = data['g']
                require(lo <= g <= hi, 'Original C endpoint value outside enclosure')
                records.append({'case': label, 'mode': end, 's': s, 't': t, 'r': r, 'n_reference': 96, 'g_reference': g, 'g_interval': [lo, hi]})
            n = case['complete_cover_panels']
            for panel, grid in enumerate(case['selected_panel_grids']):
                selected = {row['quantity']: row for row in rows if row['mode'] == f'band_{n}_{panel}' and int(row['nmu']) == grid}
                row = selected['g']; r = (int(row['r0'])+int(row['r1']))/(2*DEN)
                u, h = ref.ax(s, t, case['axis']-1, r, 96)
                g = float(r*u); ux = float((r*h[case['axis']-1]-g)/(2*r**3))
                vals = dict(zip(['g', 'H11', 'H22', 'H33', 'Ux'], [g, *map(float,h), ux]))
                comparisons = {}
                for quantity, value in vals.items():
                    lo, hi = float(selected[quantity]['lower']), float(selected[quantity]['upper'])
                    require(lo <= value <= hi, 'Original C midpoint value outside enclosure')
                    comparisons[quantity] = {'reference': value, 'interval': [lo, hi]}
                records.append({'case': label, 'mode': f'band_{n}_{panel}', 's': s, 't': t, 'r': r, 'n_reference': 96, 'comparisons': comparisons})
        for label, center in checker['center_results']['centers'].items():
            s = (81920 if label == 'A' else 134349)/DEN
            _, h = ref.ax(s, 3., 0, 0., 96)
            comparisons = {}
            for j in range(3):
                q = f'H{j+1}{j+1}'; value = float(h[j]); lo, hi = center['Hessian'][q]
                require(lo <= value <= hi, 'Original C center value outside enclosure')
                comparisons[q] = {'reference': value, 'interval': [lo, hi]}
            records.append({'case': label+'0', 's': s, 't': 3., 'r': 0., 'n_reference': 96, 'comparisons': comparisons})
    result = {
        'designation': 'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
        'scope': 'Numerical comparison only; original C quadrature is not a rigorous bound.',
        'status': 'all_checked_values_inside_intervals',
        'source_sha256': {n: hashlib.sha256((SOURCE/n).read_bytes()).hexdigest() for n in ['kernel.c', 'common.py', 'refine.py']},
        'python': sys.version, 'platform': platform.platform(), 'numpy': np.__version__, 'scipy': scipy.__version__,
        'compiler': compiler, 'compile_flags': '-O2 -std=c11 -fPIC -shared -lm',
        'constants': constants, 'pi_interval': [float(pi.a), float(pi.b)],
        'comparison_count': len(records), 'comparisons': records,
    }
    target = ROOT/'out/axis_validation.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'count': len(records), 'file': str(target)}))

if __name__ == '__main__':
    main()
