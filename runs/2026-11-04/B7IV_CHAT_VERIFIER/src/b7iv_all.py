"""Chat independent B7 verifier -- run every PASS certificate found under a root.

usage (on daybreak-works):
  cd ~/B7_work/b7iv && python3 -I b7iv_all.py ~/B7_work --workers 10
Picks, for each outer key, the most recent *_full.leaves.json whose producer
status is PASS, verifies it independently, and writes B7IV_SUMMARY.txt.
Producer numbers are printed only for comparison; the verdict uses chat's own
tiling check and chat's own per-leaf bounds.
"""
import os, sys, json, glob, time, subprocess, hashlib, argparse
HERE = os.path.dirname(os.path.abspath(__file__))

def head_status(path):
    # status/config live after the big leaves array in some files: parse fully but cheaply enough
    with open(path, 'rb') as f:
        d = json.loads(f.read())
    return d.get('status'), d['config']['key'], d.get('schema'), len(d['leaves'])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--workers', type=int, default=os.cpu_count())
    ap.add_argument('--keys', default=''); a = ap.parse_args()
    st = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'b7iv_selftest.py')], capture_output=True, text=True)
    print(st.stdout[-600:]);
    if st.returncode != 0: raise SystemExit('selftest failed')
    cands = {}
    for p in glob.glob(os.path.join(os.path.expanduser(a.root), '**', '*_full.leaves.json'), recursive=True):
        try: status, key, schema, n = head_status(p)
        except Exception as e: print('skip', p, e); continue
        if status != 'PASS': continue
        if a.keys and key not in a.keys.split(','): continue
        m = os.path.getmtime(p)
        if key not in cands or m > cands[key][0]: cands[key] = (m, p, schema, n)
    print('PASS certificates found:', len(cands))
    lines = []
    for key in sorted(cands):
        _, p, schema, n = cands[key]
        out = os.path.join(HERE, 'out', key + '.chat_iv.jsonl'); os.makedirs(os.path.dirname(out), exist_ok=True)
        t0 = time.time()
        r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'b7iv_run.py'), p, '--workers', str(a.workers), '--out', out], capture_output=True, text=True)
        txt = r.stdout
        tile = [l for l in txt.splitlines() if l.startswith('TILING')]
        fin = [l for l in txt.splitlines() if l.startswith('FINAL LOWER')]
        sha = [l for l in txt.splitlines() if l.startswith('file ')]
        line = '%s | %s | leaves %d | %s | %s | %.0fs | %s' % (key, schema, n, tile[0] if tile else 'TILING ?', fin[0] if fin else 'ERROR ' + r.stderr[-300:], time.time() - t0, sha[0].split('sha256 ')[1].split(' ')[0] if sha else '?')
        print(line, flush=True); lines.append(line)
        with open(os.path.join(HERE, 'out', key + '.log'), 'w') as f: f.write(txt + '\n' + r.stderr)
    src = ''.join(open(os.path.join(HERE, f)).read() for f in ('b7iv_ia.py', 'b7iv_vk.py', 'b7iv_vleaf.py', 'b7iv_run.py', 'b7iv_all.py', 'b7iv_selftest.py'))
    with open(os.path.join(HERE, 'B7IV_SUMMARY.txt'), 'w') as f:
        f.write('chat independent B7 verifier summary %s\nverifier source digest %s\n' % (time.strftime('%F %T'), hashlib.sha256(src.encode()).hexdigest()))
        f.write('\n'.join(lines) + '\n')
    print('summary written:', os.path.join(HERE, 'B7IV_SUMMARY.txt'))
if __name__ == '__main__': main()
