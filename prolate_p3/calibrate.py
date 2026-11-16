"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Fixed 27-box / 2-precision calibration.

Each measurement runs in a fresh process so Linux ru_maxrss is per task.
No adaptive refinement, retries, sign target, or automatic box rewriting.
"""
import argparse
import csv
import hashlib
import json
import platform
import resource
import subprocess
import sys
import time
import traceback
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
import flint
from flint import fmpq,ctx
from .kernel import V_box_details,STATUS,DEFAULT_CELLS,SERIES_N

ROOT = Path(__file__).resolve().parent


def verify_seal():
    seal = json.loads((ROOT/'PRE_RUN_SHA256.json').read_text())
    for name,expected in seal['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('pre-run file changed: '+name)
    if flint.__version__ != '0.8.0':
        raise RuntimeError('requires python-flint==0.8.0')
    spec = json.loads((ROOT/'boxes.json').read_text())
    if tuple(spec['cells']) != DEFAULT_CELLS or spec['series_N'] != SERIES_N:
        raise RuntimeError('quadrature specification mismatch')
    return spec


def worker(index,prec):
    spec = verify_seal()
    box = spec['boxes'][index]
    row = {'status':STATUS,'box_id':index,'prec_bits':prec,
           'box':box,'python':platform.python_version(),'python_flint':flint.__version__,
           'platform':platform.platform(),'started_utc':datetime.now(timezone.utc).isoformat()}
    start = time.perf_counter_ns()
    try:
        res = V_box_details(*(tuple(map(fmpq,box[k])) for k in ('R','tau','lam')),prec)
        with ctx.workprec(prec):
            row.update({'outcome':'computed','route':res.route,
                        'lower_dyadic':str(res.lower.fmpq()),
                        'upper_dyadic':str(res.enclosure.upper().fmpq()),
                        'enclosure_width_dyadic':str(res.width.fmpq()),
                        'lower_bound_interval_width':'0',
                        'cells':res.cells,'density_evaluations':res.density_evaluations,
                        'lower_sign':'positive' if res.lower>0 else ('negative' if res.lower<0 else 'zero')})
    except Exception:
        row.update({'outcome':'error','traceback':traceback.format_exc()})
    row['wall_ns'] = time.perf_counter_ns()-start
    row['wall_seconds'] = str(Decimal(row['wall_ns'])/Decimal(10**9))
    row['max_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    row['rss_scope'] = 'fresh Python worker process including imports; Linux KiB'
    print(json.dumps(row),flush=True)
    return int(row['outcome'] != 'computed')


def main():
    ap = argparse.ArgumentParser(description=STATUS)
    ap.add_argument('--one-box',type=int,choices=range(27))
    ap.add_argument('--out',type=Path,default=Path('p3_calibration'))
    ap.add_argument('--worker',nargs=2,type=int,help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.worker is not None:
        return worker(*args.worker)
    spec = verify_seal()
    if sys.platform != 'linux':
        raise RuntimeError('RSS units contract requires Linux')
    args.out.mkdir(parents=True,exist_ok=False)
    ids = range(27) if args.one_box is None else (args.one_box,)
    rows = []
    # Preserve complete fixed list before starting any measurement.
    (args.out/'boxes_used.json').write_bytes((ROOT/'boxes.json').read_bytes())
    (args.out/'seal_used.json').write_bytes((ROOT/'PRE_RUN_SHA256.json').read_bytes())
    for i in ids:
        for prec in spec['precisions']:
            run = subprocess.run([sys.executable,'-m','prolate_p3.calibrate','--worker',str(i),str(prec)],
                                 capture_output=True,text=True)
            (args.out/f'box_{i:02d}_{prec}.stdout').write_text(run.stdout)
            (args.out/f'box_{i:02d}_{prec}.stderr').write_text(run.stderr)
            try:
                row = json.loads(run.stdout)
            except Exception:
                row = {'status':STATUS,'box_id':i,'prec_bits':prec,'outcome':'error',
                       'traceback':'worker failed; see raw stdout/stderr','returncode':run.returncode}
            rows.append(row)
            print(f'{STATUS} box={i} bits={prec} outcome={row["outcome"]}',flush=True)
            (args.out/'results.json').write_text(json.dumps({'status':STATUS,'results':rows},indent=2)+'\n')
    fields = ['status','box_id','prec_bits','outcome','route','wall_seconds','max_rss_kib',
              'enclosure_width_dyadic','lower_bound_interval_width','cells','density_evaluations',
              'lower_dyadic','upper_dyadic','lower_sign']
    with (args.out/'results.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore')
        writer.writeheader();writer.writerows(rows)
    return int(any(r['outcome'] != 'computed' for r in rows))


if __name__ == '__main__':
    sys.exit(main())
