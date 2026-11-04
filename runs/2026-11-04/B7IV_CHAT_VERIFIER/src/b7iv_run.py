"""Chat independent B7 verifier -- runner.  usage: python3 -I b7iv_run.py LEAVES.json [--workers N] [--limit K]"""
import sys, os, json, time, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from multiprocessing import Pool
import b7iv_vleaf as VL

def work(args):
    outer, chunk = args
    return [(lf['uid'], lb[0], lb[1], lb[2]) for lf, lb in zip(chunk, VL.leaf_bounds(outer, chunk))]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('leaves'); ap.add_argument('--workers', type=int, default=os.cpu_count())
    ap.add_argument('--limit', type=int, default=0); ap.add_argument('--chunk', type=int, default=500)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    raw = open(a.leaves, 'rb').read(); sha = hashlib.sha256(raw).hexdigest()
    d = json.loads(raw); del raw
    outer = tuple(tuple(Fr(x) for x in b) for b in d['config']['outer'])
    if Fr(d['config']['p_cut']) != VL.P0: raise SystemExit('p_cut differs from P0')
    leaves = [VL.parse_leaf(lf, outer) for lf in d['leaves']]
    print('file', a.leaves, 'sha256', sha, '| key', d['config']['key'], '| leaves', len(leaves), '| producer status', d['status'], flush=True)
    t0 = time.time()
    ok, info = VL.check_tiling([lf['cell'] for lf in leaves], ((Fr(0), Fr(1)), (VL.P0, Fr(1)), (Fr(0), Fr(1)), (Fr(0), Fr(1))))
    print('TILING', 'PASS' if ok else 'FAIL', info, '%.1fs' % (time.time() - t0), flush=True)
    if a.limit: leaves = leaves[:a.limit]
    chunks = [(outer, leaves[i:i + a.chunk]) for i in range(0, len(leaves), a.chunk)]
    t0 = time.time(); res = []
    with Pool(a.workers) as pool:
        for k, r in enumerate(pool.imap(work, chunks)):
            res.extend(r)
            if (k + 1) % 20 == 0: print('  chunks', k + 1, '/', len(chunks), '%.0fs' % (time.time() - t0), flush=True)
    total = sum(r[1] for r in res)
    src = {}
    for r in res: src[r[2]] = src.get(r[2], 0) + 1
    fin = VL.final_lower(outer, total)
    print('leaves evaluated', len(res), '| sources', src, '| %.0fs' % (time.time() - t0))
    print('total (chat) = %.12e' % float(total), '| producer aggregate total = %.12e' % float(Fr(int(d['aggregate_raw']['total_lower']), 2**128)))
    print('FINAL LOWER (chat) = %.6e  ->' % float(fin), 'PASS' if (fin > 0 and ok and len(res) == len(d['leaves'])) else 'NOT PASS')
    out = a.out or (os.path.basename(a.leaves) + '.chat_iv.jsonl')
    with open(out, 'w') as f:
        for uid, lo, s, c in res:
            f.write(json.dumps({'uid': uid, 'lower': str(lo), 'src': s, 'cand': {k: str(v) for k, v in c.items()}}) + '\n')
    print('per-leaf output', out)
if __name__ == '__main__': main()
