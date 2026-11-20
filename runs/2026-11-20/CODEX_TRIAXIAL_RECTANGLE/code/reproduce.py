"""Reproduce in a temporary copy, preserving the delivered ledgers.

DIAGNOSTIC_ONLY / NOT_EVIDENCE. No network, repository mutation, or research
PC is involved. A successful command means the stated checks completed;
it is not a conclusion about the unprocessed mathematical domain.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from verify_package import verify

ROOT = Path(__file__).resolve().parents[1]
ATLAS_SHA256 = '259f721216b2c0b4348f1ccd3351f06b4500ff98903767875798ff778d85b89f'


def extract_source(archive, target):
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ATLAS_SHA256:
        raise ValueError('Original atlas archive differs')
    target.mkdir()
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            dest = (target / info.filename).resolve()
            if target.resolve() not in dest.parents:
                raise ValueError('Unsafe original archive path')
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Archive symlink is not accepted')
        z.extractall(target)
    return verify(target / 'TRIAXIAL_FIRST_ATLAS_20261120', 'MANIFEST.sha256')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Verify records and run recorded short cross-checks (default).')
    mode.add_argument('--rerun', action='store_true', help='Recompute all successful-version numerical plans before checking.')
    args = ap.parse_args()
    integrity = verify(ROOT)
    work = Path(tempfile.mkdtemp(prefix='tri_rectangle_reproduction_'))
    package = work / 'package'
    shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    source_integrity = extract_source(package / 'inputs/TRIAXIAL_FIRST_ATLAS_20261120.zip', work / 'baseline')
    env = dict(os.environ)
    env.update(PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    commands = []
    if args.rerun:
        commands += [
            ['code/center_calibrate.py'],
            ['code/center_pilot_b.py'],
            ['code/center_pilot_c.py'],
            ['code/calibration.py', '--start', '0', '--stop', '1', '--workers', '1', '--output', 'calibration_pilot_c1a.csv'],
            ['code/calibration.py', '--start', '1', '--stop', '32', '--workers', '2', '--output', 'calibration_remaining_c1a.csv'],
            ['code/calibration_extended.py', '--workers', '2'],
            ['code/calibration_position.py'],
            ['code/calibration_normalized.py'],
            ['code/axis_interval.py', '--case', '0', '--output', 'axis_A1.csv'],
            ['code/axis_interval.py', '--case', '1', '--output', 'axis_A2.csv'],
            ['code/axis_interval.py', '--case', '2', '--output', 'axis_B2.csv'],
            ['code/axis_interval.py', '--centers', '--output', 'axis_centers.csv'],
            ['code/axis_wide.py'],
        ]
    commands += [
        ['code/center_check.py'],
        ['code/axis_check.py'],
        ['code/axis_wide_check.py'],
        ['code/axis_validate.py'],
        ['code/calibration_check.py'],
        ['code/calibration_reference.py'],
    ]
    records = []
    outcome = {
        'designation': 'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
        'mode': 'full_numerical_rerun' if args.rerun else 'record_checks_and_short_cross_checks',
        'delivery_hashes': integrity,
        'original_atlas_hashes': source_integrity,
        'python': sys.version,
        'platform': platform.platform(),
        'original_package': str(ROOT),
        'reproduction_package': str(package),
        'records': records,
        'status': 'in_progress',
        'scope': 'No claim of a whole-rectangle classification; analytic proofs require mathematical review.',
    }
    summary = work / 'REPRODUCTION.json'
    for index, command in enumerate(commands):
        print(f'[{index+1}/{len(commands)}] {" ".join(command)}', flush=True)
        before = time.perf_counter()
        run = subprocess.run([sys.executable, *command], cwd=package, env=env, text=True, capture_output=True)
        log = work / f'command_{index+1:02d}.log'
        log.write_text(run.stdout + ('\nSTDERR\n'+run.stderr if run.stderr else ''))
        records.append({'command': command, 'exit_code': run.returncode, 'elapsed_seconds': time.perf_counter()-before, 'log': str(log)})
        if run.returncode:
            outcome['status'] = 'command_failed'
            summary.write_text(json.dumps(outcome, indent=2)+'\n')
            print(f'Command failed; inspect {log}', file=sys.stderr)
            return run.returncode
        summary.write_text(json.dumps(outcome, indent=2)+'\n')
    outcome['status'] = 'all_declared_commands_completed'
    summary.write_text(json.dumps(outcome, indent=2)+'\n')
    print(json.dumps({'status': outcome['status'], 'reproduction_summary': str(summary), 'package': str(package)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
