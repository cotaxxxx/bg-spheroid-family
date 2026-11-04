#!/usr/bin/env python3
"""chat: B7 RAW monitor -- reads the producer's raw state on daybreak-works directly.

Reads every checkpoint (*_full.checkpoint: the producer's full in-memory state, all active
leaves) and every result (*_full.json) in the producer folder.  It does NOT use monitor.log.
Read-only for the computation: checkpoints are replaced atomically by the producer, so reading
them is safe.  It only writes its own log (raw_monitor.log) and a small state file for deltas.

Usage (must run inside the producer folder so the pickled interval class can be imported):
  cd ~/B7_work/b7_v52 && python3 b7_raw.py                 # once
  cd ~/B7_work/b7_v52 && python3 b7_raw.py --watch 1200    # every 20 min
  options: --dir full_v52   --top 5   --keys L0_T2_D2,L1_T1_D2
Per box it prints, from the raw leaves:
  leaves/limit, splits, evaluations, checkpoint age
  sum of selected lower bounds (J units, exact) and the final lower bound recomputed exactly
  change since the previous run of this script
  per bound source: number of leaves, positive sum, negative sum
  negative mass by p band and by t band (where the deficit sits)
  the most negative leaves (cell, source, value)
  estimate of the gain from the tighter beta-width bound 2(tb-ta)/(1+ta tb)
"""
import argparse, glob, json, os, pickle, sys, time
from datetime import datetime
from fractions import Fraction as Q

ap = argparse.ArgumentParser()
ap.add_argument('--dir', default='full_v52')
ap.add_argument('--watch', type=int, default=0)
ap.add_argument('--top', type=int, default=5)
ap.add_argument('--keys', default='')
args = ap.parse_args()
sys.path.insert(0, os.getcwd())
import v3_fixed_128  # noqa: F401  (needed to unpickle interval objects)

S = 1 << 128
KQ = Q(275, 4); P0 = Q(1, 2000000); SIG0 = 2 * P0 / (1 + P0 * P0)
OUT = os.path.abspath(args.dir)
STATE = os.path.join(OUT, 'raw_monitor_state.json')
LOG = os.path.join(OUT, 'raw_monitor.log')
PB = [Q(1, 10**4), Q(1, 10**3), Q(1, 10**2), Q(1, 10), Q(1)]
TB = [Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]

def final(total, lam):
    lo, hi = lam
    pre = total * lo * Q(7, 11) if total >= 0 else total * hi * Q(2, 3)   # producer bracket for 2/pi
    return pre - 2 * hi * KQ * SIG0

def band(x, edges):
    for i, e in enumerate(edges):
        if x <= e: return i
    return len(edges) - 1

def f(x): return f'{float(x):+.6g}'

def box_report(ck, prev, out):
    saved = pickle.load(open(ck, 'rb'))
    st, cfg = saved['state'], saved['config']
    key = cfg['key']; lam = tuple(Q(x) for x in cfg['outer'][0])
    act = st['active']
    age = (time.time() - os.path.getmtime(ck)) / 60
    tot = 0; src = {}; negp = [0] * len(PB); negt = [0] * len(TB); worst = []; tot_db = 0
    for lf in act.values():
        v = lf['total_lo_selected']; s = lf.get('bound_source', '?'); tot += v
        c = src.setdefault(s, [0, 0, 0]); c[0] += 1
        if v >= 0: c[1] += v
        else:
            c[2] += v
            negp[band(Q(lf['cell'][1][1]), PB)] += v
            negt[band(Q(lf['cell'][2][1]), TB)] += v
            worst.append((v, s, lf['cell']))
        ta, tb = (Q(x) for x in lf['cell'][2]); r = (1 + ta * ta) / (1 + ta * tb)
        alt = [lf['k_floor_raw'] * r, lf['midpoint'].lo, lf['zeroth'].lo]
        if 'astra3_floor_raw' in lf: alt.append(lf['astra3_floor_raw'] * r)
        tot_db += max(alt)
    if abs(tot - st['total_lo']) > 0: out.append(f'   !! sum of leaves {tot} != state total_lo {st["total_lo"]}')
    J = Q(tot, S); fin = final(J, lam); fin_db = final(Q(tot_db, S), lam)
    p = prev.get(key)
    d = ''
    if p:
        dt = (time.time() - p['t']) / 3600
        d = f' | since last {dt:.2f} h: leaves {len(act) - p["leaves"]:+d}, final {float(fin) - p["final"]:+.5g}'
    out.append(f'[{key}] leaves {len(act)}/{cfg.get("limit")} splits {st.get("splits")} evaluations {st.get("evaluations")} '
               f'| checkpoint age {age:.0f} min{d}')
    out.append(f'   J lower (exact) {J.numerator}/{J.denominator}')
    out.append(f'   J lower {f(J)}   FINAL lower {f(fin)}   (with tighter Dbeta+ estimate: {f(fin_db)}, gain {f(fin_db - fin)})')
    for s, (n, pos, neg) in sorted(src.items()):
        out.append(f'   source {s:9s} leaves {n:7d}  positive {f(Q(pos, S))}  negative {f(Q(neg, S))}')
    out.append('   negative by p_hi band  ' + '  '.join(f'<={float(e):g}:{f(Q(v, S))}' for e, v in zip(PB, negp)))
    out.append('   negative by t_hi band  ' + '  '.join(f'<={float(e):g}:{f(Q(v, S))}' for e, v in zip(TB, negt)))
    worst.sort(key=lambda w: w[0])
    for v, s, c in worst[:args.top]:
        out.append(f'   worst {f(Q(v, S))} {s:9s} y{[str(x) for x in c[0]]} p{[str(x) for x in c[1]]} t{[str(x) for x in c[2]]} u{[str(x) for x in c[3]]}')
    return key, {'t': time.time(), 'leaves': len(act), 'final': float(fin)}

def once():
    prev = {}
    try: prev = json.load(open(STATE))
    except Exception: pass
    out = ['=' * 100, f'B7 RAW  {datetime.now():%Y-%m-%d %H:%M:%S}  folder {OUT}']
    keys = set(args.keys.split(',')) if args.keys else None
    new = dict(prev)
    for rp in sorted(glob.glob(os.path.join(OUT, '*_full.json'))):
        try: r = json.load(open(rp))
        except Exception as e: out.append(f'{os.path.basename(rp)} unreadable {e}'); continue
        k = r.get('config', {}).get('key', '?')
        if keys and k not in keys: continue
        out.append(f'[{k}] RESULT status {r.get("status")} leaves {r.get("leaves")} final_lower {r.get("final_lower")} '
                   f'(= {float(Q(r["final_lower"])):+.6g}) leaf_file_sha256 {r.get("leaf_file_sha256")}')
    for ck in sorted(glob.glob(os.path.join(OUT, '*_full.checkpoint'))):
        k = os.path.basename(ck).replace('_full.checkpoint', '')
        if keys and k not in keys: continue
        if os.path.exists(ck.replace('.checkpoint', '.json')): continue      # finished: shown above
        try:
            key, s = box_report(ck, prev, out); new[key] = s
        except Exception as e:
            out.append(f'[{k}] checkpoint unreadable now ({type(e).__name__}); retry next cycle')
    txt = '\n'.join(out)
    print(txt, flush=True)
    with open(LOG, 'a') as fh: fh.write(txt + '\n')
    tmp = STATE + '.tmp'
    json.dump(new, open(tmp, 'w')); os.replace(tmp, STATE)

while True:
    once()
    if args.watch <= 0: break
    time.sleep(args.watch)
