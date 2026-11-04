#!/usr/bin/env python3
"""chat: B7 watch -- raw data + producer progress + independent-verification ledger (+ optional auto-verify).

Usage (daybreak-works):
  python3 b7_watch.py                         # one report
  python3 b7_watch.py --watch 1200            # repeat every 20 min
  python3 b7_watch.py --watch 1200 --auto-verify --py ~/B7_work/b7iv/venv/bin/python --workers 4

What it shows
  * RAW DATA first (skip with --no-raw): latest monitor.log block verbatim, producer result
    fields exactly as written (fractions), verifier log lines verbatim, ledger tail
  * processes, memory, memguard stops, age of the last monitor.log entry
  * per running box: leaves / cap, J lower, final lower, final-lower rate per hour,
    linear ETA to final>0, linear ETA to the leaf cap, and CAP RISK when the cap comes first
  * finished producer results (PASS / LIMIT_REACHED / DOMAIN_FAIL)
  * independent verification (chat B7IV) read from ~/B7_work/b7iv/out/<KEY>.log:
    a box counts as VERIFIED only if its log says TILING PASS and "-> PASS" AND the
    verified leaf-file SHA-256 equals the current producer certificate's SHA-256
  * producer PASS certificates not yet independently verified

--auto-verify runs b7iv_run.py on each such certificate, one at a time, with few workers
(production keeps running).  Output: out/<KEY>.chat_iv.jsonl, out/<KEY>.log, and one line
appended to B7IV_LEDGER.txt (append-only; B7IV_SUMMARY.txt is never touched).
Everything else is read-only; the large checkpoints are never opened.
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys, time
from datetime import datetime
from fractions import Fraction as Q

ap = argparse.ArgumentParser()
ap.add_argument('--work', default=os.path.expanduser('~/B7_work'))
ap.add_argument('--dir', default=None, help='producer output folder (default <work>/b7_v52/full_v52)')
ap.add_argument('--iv', default=None, help='verifier folder (default <work>/b7iv)')
ap.add_argument('--watch', type=int, default=0, help='repeat every N seconds (0 = once)')
ap.add_argument('--window', type=float, default=60.0, help='minutes used for rates')
ap.add_argument('--auto-verify', action='store_true')
ap.add_argument('--py', default=sys.executable, help='python used for the verifier (needs numpy)')
ap.add_argument('--workers', type=int, default=4)
ap.add_argument('--no-raw', action='store_true', help='table only (skip the raw-data dump)')
ap.add_argument('--progress-log', default=None, help='old-style monitor.log to show running boxes (off by default; V5.3 progress: use b7_raw.py)')
ap.add_argument('--min-mem-gib', type=float, default=6.0, help='auto-verify only if MemAvailable is at least this')
args = ap.parse_args()
WORK = os.path.abspath(os.path.expanduser(args.work))
OUT = os.path.abspath(os.path.expanduser(args.dir or os.path.join(WORK, 'b7_v52', 'full_v52')))
IV = os.path.abspath(os.path.expanduser(args.iv or os.path.join(WORK, 'b7iv')))
ALL = [f'L{i}_T{j}_D{d}' for d in range(5) for i in range(2) for j in range(4)]
RUN_KEYS = [k for k in ALL if not k.endswith('_D0')]

HEAD = re.compile(r'^===== (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)')
BOX = re.compile(r'^\[(L\d_T\d_D\d)\] init (\d+)/(\d+) (done|running) \| leaves (\d+)/(\d+)')
SUM = re.compile(r'^\s+sum lower \(J units\) (\S+)')
FIN = re.compile(r'^\s+final lower .*?: (\S+)\s+->')

_sha_cache = {}
def sha256(path):
    st = os.stat(path); key = (path, st.st_mtime_ns, st.st_size)
    if key not in _sha_cache:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
        _sha_cache[key] = h.hexdigest()
    return _sha_cache[key]

def parse_log(path):
    series = {}; t = None; cur = None
    try: lines = open(path, errors='replace').read().splitlines()
    except FileNotFoundError: return series, None
    for ln in lines:
        m = HEAD.match(ln)
        if m: t = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S'); cur = None; continue
        m = BOX.match(ln)
        if m and t: cur = [m.group(1), t, int(m.group(5)), int(m.group(6)), None, None, m.group(4) == 'done']; continue
        m = SUM.match(ln)
        if m and cur: cur[4] = float(m.group(1)); continue
        m = FIN.match(ln)
        if m and cur:
            cur[5] = float(m.group(1)); series.setdefault(cur[0], []).append(tuple(cur[1:])); cur = None
    return series, t

def producer_results(ivs=None):
    """key -> (result dict, leaves path).
    PASS certificates anywhere under WORK are candidates, but only those whose leaf file exists
    (copies kept elsewhere, e.g. compressed archives in a publish repo, are ignored).  Among them,
    the one whose leaf SHA equals the independently verified SHA is preferred; otherwise the latest.
    Non-PASS results are shown only if they are in the current producer folder OUT."""
    cands = {}; current = {}; nofile = {}
    for p in glob.glob(os.path.join(WORK, '**', '*_full.json'), recursive=True):
        if os.sep + 'b7iv' + os.sep in p: continue
        try: r = json.load(open(p))
        except Exception: continue
        k = r.get('config', {}).get('key')
        if not k: continue
        lp = os.path.join(os.path.dirname(p), r.get('leaf_file') or os.path.basename(p)[:-5] + '.leaves.json')
        m = os.path.getmtime(p)
        if r.get('status') == 'PASS':
            if os.path.exists(lp): cands.setdefault(k, []).append((m, r, lp))
            else: nofile[k] = lp
        elif os.path.dirname(os.path.abspath(p)) == OUT:
            current[k] = (m, r, lp)
    out = {k: (v[1], v[2]) for k, v in current.items()}
    for k, lst in cands.items():
        lst.sort(key=lambda x: -x[0])
        pick = lst[0]
        want = (ivs or {}).get(k, {}).get('sha')
        if want:
            for c in lst:
                d = c[1].get('leaf_file_sha256')
                if (d == want) or (d is None and sha256(c[2]) == want): pick = c; break
        out[k] = (pick[1], pick[2])
    producer_results.nofile = {k: v for k, v in nofile.items() if k not in cands}
    return out

def iv_status():
    """key -> dict(verdict, final, sha, tiling) from verifier logs."""
    out = {}
    for p in glob.glob(os.path.join(IV, 'out', '*.log')):
        k = os.path.basename(p)[:-4]
        if not re.fullmatch(r'L\d_T\d_D\d', k): continue
        txt = open(p, errors='replace').read()
        sha = re.findall(r'sha256 ([0-9a-f]{64})', txt)
        til = re.findall(r'^TILING (PASS|FAIL)', txt, re.M)
        fin = re.findall(r'^FINAL LOWER \(chat\) = (\S+)\s+->\s+(PASS|NOT PASS)', txt, re.M)
        out[k] = {'sha': sha[-1] if sha else None, 'tiling': til[-1] if til else None,
                  'final': float(fin[-1][0]) if fin else None,
                  'verdict': 'PASS' if (fin and fin[-1][1] == 'PASS' and til and til[-1] == 'PASS') else
                             ('NOT PASS' if fin else 'ERROR/INCOMPLETE')}
    return out

def procs():
    n = {'producer': 0, 'workers': 0, 'monitor': 0, 'guard': 0, 'verifier': 0}
    for p in glob.glob('/proc/[0-9]*/cmdline'):
        try: c = open(p, 'rb').read().replace(b'\0', b' ').decode(errors='ignore')
        except Exception: continue
        if 'b7_monitor' in c: n['monitor'] += 1
        elif 'b7iv_run' in c: n['verifier'] += 1
        elif 'memguard' in c: n['guard'] += 1
        elif 'v6_b7_unified_outerrem' in c:
            if 'forkserver' in c or 'multiprocessing' in c: n['workers'] += 1
            else: n['producer'] += 1
    return n

def mem():
    d = {}
    for ln in open('/proc/meminfo'):
        k, v = ln.split(':'); d[k] = int(v.split()[0]) / 1048576
    return d.get('MemTotal', 0), d.get('MemAvailable', 0), d.get('SwapTotal', 0) - d.get('SwapFree', 0)

def eta(h):
    if h is None: return '    -'
    if h <= 0: return '  now'
    return f'{h:5.1f}h' if h < 100 else ' >99h'

def run_verifier(key, leaves_path):
    os.makedirs(os.path.join(IV, 'out'), exist_ok=True)
    log = os.path.join(IV, 'out', key + '.log')
    cmd = [os.path.expanduser(args.py), '-I', os.path.join(IV, 'b7iv_run.py'), leaves_path,
           '--workers', str(args.workers), '--out', os.path.join(IV, 'out', key + '.chat_iv.jsonl')]
    print(f'   auto-verify {key}: {" ".join(cmd)}', flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    with open(log, 'w') as f: f.write(r.stdout + '\n' + r.stderr)
    st = iv_status().get(key, {})
    line = '%s | %s | %s | final %s | tiling %s | sha %s | %.0fs' % (
        datetime.now().strftime('%F %T'), key, st.get('verdict'), st.get('final'), st.get('tiling'), st.get('sha'), time.time() - t0)
    with open(os.path.join(IV, 'B7IV_LEDGER.txt'), 'a') as f: f.write(line + '\n')
    print('   ' + line, flush=True)

def raw_dump(res):
    """Print the underlying data verbatim: last monitor.log block, producer result fields
    (exact fractions as written), verifier log lines, ledger tail."""
    W = 104
    print('#' * W); print('RAW DATA')
    print('--- monitor.log (latest block, verbatim) ---')
    try:
        txt = open(args.progress_log or os.path.join(OUT, 'monitor.log'), errors='replace').read()
        i = txt.rfind('\n=====')
        print(txt[i + 1:] if i >= 0 else txt[-6000:])
    except FileNotFoundError:
        print('(no monitor.log)')
    print('--- producer result JSONs (fields as written) ---')
    for k in ALL:
        if k not in res: continue
        r, lp = res[k]
        print(f'{k} status={r.get("status")} leaves={r.get("leaves")} total_lower={r.get("total_lower")} '
              f'final_lower={r.get("final_lower")} leaf_file_sha256={r.get("leaf_file_sha256")} leaf_file={lp}')
    print('--- verifier logs (verbatim lines) ---')
    for p in sorted(glob.glob(os.path.join(IV, 'out', '*.log'))):
        for ln in open(p, errors='replace').read().splitlines():
            if ln.startswith(('file ', 'TILING', 'leaves evaluated', 'total (chat)', 'FINAL LOWER', 'Traceback')) or 'Error' in ln:
                print(f'{os.path.basename(p)[:-4]}: {ln}')
    led = os.path.join(IV, 'B7IV_LEDGER.txt')
    if os.path.exists(led):
        print('--- B7IV_LEDGER.txt (last 20 lines) ---')
        print('\n'.join(open(led).read().splitlines()[-20:]))
    print('#' * W)

def report():
    series, last_t = parse_log(args.progress_log) if args.progress_log else ({}, None)
    ivs = iv_status(); res = producer_results(ivs); pr = procs(); tot, avail, swap = mem()
    if not args.no_raw: raw_dump(res)
    now = datetime.now()
    W = 104
    print('=' * W, flush=True)
    print(f'B7 watch  {now:%Y-%m-%d %H:%M:%S}   producer {OUT}   verifier {IV}')
    print(f'processes: producer {pr["producer"]} workers {pr["workers"]} monitor {pr["monitor"]} memguard {pr["guard"]} '
          f'verifier {pr["verifier"]} | memory available {avail:.1f}/{tot:.1f} GiB, swap {swap:.2f} GiB'
          + (f' | progress log {last_t:%H:%M} ({int((now - last_t).total_seconds() // 60)} min ago)' if last_t else ' | running-box progress: use b7_raw.py'))
    for g in glob.glob(os.path.join(WORK, '**', 'memguard*.log'), recursive=True):
        stops = [l for l in open(g, errors='replace').read().splitlines() if 'stop' in l.lower()]
        if stops: print(f'!! MEMGUARD STOP in {g}: {stops[-1]}')
    if last_t and (now - last_t).total_seconds() > 2.5 * 3600: print('!! monitor.log has not been updated for over 2.5 h')
    if pr['producer'] == 0: print('!! no producer process found')
    if pr['verifier'] > 1: print('!! more than one verifier process is running')
    print('-' * W)
    print(f'{"box":10s} {"state":13s} {"leaves":>15s} {"J lower":>10s} {"final":>10s} {"final/h":>9s} {"ETA>0":>6s} {"ETAcap":>6s}  independent')
    running = []
    for k in ALL:
        rr = res.get(k); s = series.get(k); iv = ivs.get(k)
        ivtxt = ''
        if iv:
            ivtxt = f'B7IV {iv["verdict"]}' + (f' {iv["final"]:+.3g}' if iv['final'] is not None else '')
        if rr:
            r, lp = rr
            st = r.get('status', '?')
            if st == 'PASS' and iv and iv['verdict'] == 'PASS' and os.path.exists(lp) and iv['sha'] != sha256(lp):
                ivtxt += '  !! SHA differs from current certificate'
            print(f'{k:10s} {st:13s} {r.get("leaves", 0):15d} {float(Q(r["total_lower"])):10.4g} {float(Q(r["final_lower"])):10.4g} '
                  f'{"":>9s} {"":>6s} {"":>6s}  {ivtxt}')
            continue
        if not s: continue
        t, lv, cap, J, fl, done = s[-1]
        old = [x for x in s if (t - x[0]).total_seconds() >= args.window * 60 * 0.9]
        rate = lrate = None
        if done and old and old[-1][5]:
            t0, lv0, _, _, f0, _ = old[-1]; dt = (t - t0).total_seconds() / 3600
            if dt > 0: rate = (fl - f0) / dt; lrate = (lv - lv0) / dt
        e0 = (-fl / rate) if (rate and rate > 0 and fl < 0) else (0 if fl > 0 else None)
        ec = ((cap - lv) / lrate) if (lrate and lrate > 0) else None
        risk = '  CAP RISK' if (fl < 0 and ec is not None and (e0 is None or e0 > ec)) else ''
        st = ('init' if not done else 'running') + (' (stale)' if (now - t).total_seconds() > 2.5 * 3600 else '')
        print(f'{k:10s} {st:13s} {lv:7d}/{cap:<7d} {J:10.4g} {fl:10.4g} {(f"{rate:+.4f}" if rate is not None else "-"):>9s} '
              f'{eta(e0):>6s} {eta(ec):>6s}  {ivtxt}{risk}')
        running.append(k)
    print('-' * W)
    prodpass = [k for k in ALL if k in res and res[k][0].get('status') == 'PASS']
    verified = [k for k in prodpass if k in ivs and ivs[k]['verdict'] == 'PASS'
                and os.path.exists(res[k][1]) and ivs[k]['sha'] == sha256(res[k][1])]
    pending = [k for k in prodpass if k not in verified]
    tried = [k for k in pending if k in ivs and os.path.exists(res[k][1]) and ivs[k]['sha'] == sha256(res[k][1])]
    if tried: print('!! verified this exact certificate but NOT PASS (chat to judge, no auto-retry):', ' '.join(tried))
    todo = [k for k in pending if k not in tried]
    bad_iv = [k for k in ivs if ivs[k]['verdict'] != 'PASS']
    notpass = [k for k in RUN_KEYS if k in res and res[k][0].get('status') not in ('PASS',)]
    nf = getattr(producer_results, 'nofile', {})
    if nf: print('!! PASS result found only as a copy without its leaf file (not counted):', ' '.join(sorted(nf)))
    waiting = [k for k in RUN_KEYS if k not in res and k not in running] if args.progress_log else []
    print(f'B7 producer PASS {len(prodpass)}/40 | independently VERIFIED {len(verified)}/40 | OPEN {40 - len(verified)}')
    if pending: print('PASS awaiting independent verification:', ' '.join(pending))
    if bad_iv: print('!! verifier logs not PASS:', ', '.join(f'{k}={ivs[k]["verdict"]}' for k in bad_iv))
    if notpass: print('!! producer NOT PASS (needs decision):', ', '.join(f'{k}={res[k][0].get("status")}' for k in notpass))
    if waiting: print('waiting (not started):', ' '.join(waiting))
    print('note: rates and ETAs are linear extrapolations; final-lower growth usually slows near the end.')
    return todo, res

LOCK = None
if args.auto_verify:
    import fcntl
    os.makedirs(IV, exist_ok=True)
    LOCK = open(os.path.join(IV, '.b7_watch_autoverify.lock'), 'w')
    try:
        fcntl.flock(LOCK, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        sys.exit('another b7_watch --auto-verify is already running (lock held); not starting a second one')
    LOCK.write(str(os.getpid())); LOCK.flush()

while True:
    try:
        pending, res = report()
        if args.auto_verify:
            for k in pending:
                r, lp = res[k]
                if not os.path.exists(lp):
                    print(f'   auto-verify {k}: leaf file missing {lp}'); continue
                declared = r.get('leaf_file_sha256')
                actual = sha256(lp)
                if declared and declared != actual:
                    print(f'   !! auto-verify {k}: SKIPPED, leaf file SHA {actual[:16]} != producer-declared {declared[:16]}'); continue
                avail = mem()[1]
                if avail < args.min_mem_gib:
                    print(f'   auto-verify {k}: postponed, MemAvailable {avail:.1f} GiB < {args.min_mem_gib} GiB', flush=True); break
                run_verifier(k, lp)
    except Exception as e:
        print('watch cycle failed:', type(e).__name__, e, flush=True)
    if args.watch <= 0: break
    time.sleep(args.watch)
