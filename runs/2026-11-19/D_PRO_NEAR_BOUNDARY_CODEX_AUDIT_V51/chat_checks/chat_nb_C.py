import sys, json, time; sys.path.insert(0,'.')
from flint import fmpq
from chat_lowerV3 import lowerV3
import chat_nb_check as N
KW = dict(NM=1024, NP=192, SUBM=4, KR=16, SUBR=4, SUB0=16, BAND=fmpq(1,4))
def run(it):
    nm, box = it; t0 = time.monotonic(); todo = [(tuple(box), 0)]; vals = []; ok = True; n = 0
    while todo:
        b, d = todo.pop()
        if b[2]*b[2] + b[4]*b[4] >= 2**40: continue
        v = lowerV3(b, **KW); n += 1
        if v > 0: vals.append(float(v))
        elif d < 6: todo += [(c, d+1) for c in N.bisect(b)]
        else: ok = False; vals.append(float(v)); todo = []
    return {'name': nm, 'confirmed': ok, 'evals': n, 'leaves': len(vals), 'min': min(vals) if vals else None, 'seconds': round(time.monotonic()-t0, 1)}
if __name__ == '__main__':
    src = {r['name']: r['box'] for r in map(json.loads, open('nb_check.jsonl'))}
    for r in map(json.loads, open('nb_B2.jsonl')):
        if r['kind'] == 'V' and not r['confirmed']: print(json.dumps(run((r['name'], src[r['name']]))), flush=True)
