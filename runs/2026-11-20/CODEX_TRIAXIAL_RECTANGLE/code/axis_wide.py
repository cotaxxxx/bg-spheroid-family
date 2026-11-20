"""Separately planned wider-input experiment, budgeted to 300 CPU seconds.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
import csv, hashlib, json, resource, signal, time
import axis_interval as kernel

ROOT = Path(__file__).resolve().parents[1]
DEN = 65536
S_BOUNDS = {'WA': (81664, 82176), 'WB': (134144, 134656)}
T_BOUNDS = (196352, 196864)
EXPECTED_KERNEL = '09a1747b77163068910e293dec3bee1b2cb6f5b72460bce6dd131db90c68004e'
CASES = [('WA', 0, 3/8, 1/2, [-1, 1, 1]), ('WA', 1, 27/32, 29/32, [-1, -1, 1]), ('WB', 1, 7/8, 15/16, [-1, -1, 1])]

class BudgetStop(Exception):
    pass

def cpu_seconds():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_utime + usage.ru_stime

def budget_check():
    if cpu_seconds() >= 285:
        raise BudgetStop('No new stage after 285 CPU seconds')

def budget_signal(signum, frame):
    raise BudgetStop('300-second CPU soft limit reached')

def wide_shape(which):
    lo, hi = S_BOUNDS[which]
    s = kernel.Box(lo/DEN, hi/DEN)
    t = kernel.Box(T_BOUNDS[0]/DEN, T_BOUNDS[1]/DEN)
    return [kernel.Box(1), s.sq(), (s*t).sq()]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if digest(ROOT/'code/axis_interval.py') != EXPECTED_KERNEL:
        raise ValueError('Frozen base kernel hash differs')
    signal.signal(signal.SIGXCPU, budget_signal)
    resource.setrlimit(resource.RLIMIT_CPU, (300, 305))
    kernel.shape = wide_shape
    summary = {'designation': 'DIAGNOSTIC_ONLY / NOT_EVIDENCE', 'status': 'running', 'cases': {}, 'centers': {},
               'plan_sha256': digest(ROOT/'plans/PLAN_AXIS_WIDE.md'), 'wrapper_sha256': digest(Path(__file__)),
               'kernel_sha256': EXPECTED_KERNEL, 'cpu_soft_limit': 300, 'cpu_hard_limit': 305,
               'start_new_stage_before_cpu_seconds': 285}
    path = ROOT/'out/axis_wide.csv'
    wall_start = time.perf_counter()
    with path.open('w') as f:
        writer = csv.writer(f, lineterminator='\n'); writer.writerow(kernel.HEADER); f.flush()
        def evaluate(label, sh, axis, mode, radius, m, hessian, predicate):
            budget_check()
            start = time.perf_counter()
            vals = kernel.integral(sh, axis, radius, m, hessian)
            elapsed = time.perf_counter()-start
            good = bool(predicate(vals))
            for name, value in zip(['g', 'H11', 'H22', 'H33', 'Ux'], vals):
                writer.writerow([label, sh, axis+1, mode, *S_BOUNDS[sh], *T_BOUNDS, DEN,
                                 round(float(radius.a)*DEN), round(float(radius.b)*DEN), DEN, m, m//2,
                                 name, float(value.a), float(value.b), elapsed, 'sign' if good else 'unresolved'])
            f.flush()
            print(label, mode, m, good, 'wall_seconds', elapsed, 'total_cpu_seconds', cpu_seconds(), flush=True)
            return good
        try:
            for sh, signs in [('WA', [1,1,1]), ('WB', [-1,1,1])]:
                good = False
                for m in [128,256,512,1024,2048]:
                    good = evaluate(sh+'0', sh, 0, 'center', kernel.Box(0), m, True,
                                    lambda vals: all(bool(v.a > 0 if s > 0 else v.b < 0) for v,s in zip(vals[1:4], signs)))
                    if good:
                        break
                summary['centers'][sh] = 'signs_obtained' if good else 'unresolved'
            for sh, axis, ra, rb, signs in CASES:
                label = f'{sh}{axis+1}'; summary['cases'][label] = {'status': 'running', 'endpoints': {}}
                for mode, r, sign in [('left', ra, 1), ('right', rb, -1)]:
                    good = False
                    for m in [256,512,1024,2048,4096,8192]:
                        good = evaluate(label, sh, axis, mode, kernel.Box(r), m, False,
                                        lambda vals: vals[0].a > 0 if sign > 0 else vals[0].b < 0)
                        if good:
                            break
                    summary['cases'][label]['endpoints'][mode] = 'sign_obtained' if good else 'unresolved'
                if any(v == 'unresolved' for v in summary['cases'][label]['endpoints'].values()):
                    summary['cases'][label]['status'] = 'endpoint_unresolved'; continue
                done = False
                for n in [8,16]:
                    accepted = 0
                    for panel in range(n):
                        radius = kernel.Box(ra+(rb-ra)*panel/n, ra+(rb-ra)*(panel+1)/n)
                        for m in [128,256,512,1024,2048]:
                            good = evaluate(label, sh, axis, f'band_{n}_{panel}', radius, m, True,
                                            lambda vals: all(bool(v.a > 0 if s > 0 else v.b < 0) for v,s in zip(vals[1:4], signs)) and bool(vals[4].b < 0))
                            if good:
                                accepted += 1; break
                    if accepted == n:
                        done = True; break
                summary['cases'][label]['status'] = 'complete_bracket_inclusions' if done else 'derivative_cover_unresolved'
                summary['cases'][label]['last_panel_count'] = n
            summary['status'] = 'finished_declared_attempts'
        except BudgetStop as error:
            summary['status'] = 'cpu_budget_reached'
            summary['budget_reason'] = str(error)
    summary['cpu_seconds'] = cpu_seconds()
    summary['wall_seconds'] = time.perf_counter()-wall_start
    summary['ledger_sha256'] = digest(path)
    (ROOT/'out/axis_wide_run.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary), flush=True)

if __name__ == '__main__':
    main()
