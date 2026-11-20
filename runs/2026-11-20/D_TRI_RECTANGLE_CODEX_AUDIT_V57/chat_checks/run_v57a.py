import sys, csv, time; sys.path.insert(0, sys.argv[1])
from fractions import Fraction as Fr
from geoenclosereader import tri2
OUT = sys.argv[2]; U = 5242880
d = list(csv.DictReader(open(f"{OUT}/disk.csv")))
for mode, (r0, r1), floor in (('tau2', (0, 3*U//8), Fr('0.00122408')), ('tau', (3*U//8, U), Fr('0.00018254'))):
    B = [(int(x['t0']), int(x['t1']), int(x['r0']), int(x['r1'])) for x in d if x['mode'] == mode]
    area = sum((b[1]-b[0])*(b[3]-b[2]) for b in B); tgt = (5*U - 2*U)*(r1 - r0)
    inside = all(2*U <= b[0] < b[1] <= 5*U and r0 <= b[2] < b[3] <= r1 for b in B)
    xs = sorted({b[0] for b in B} | {b[1] for b in B}); ys = sorted({b[2] for b in B} | {b[3] for b in B}); holes = over = 0
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            cx, cy = (xs[i]+xs[i+1])/2, (ys[j]+ys[j+1])/2; n = sum(1 for b in B if b[0] < cx < b[1] and b[2] < cy < b[3])
            holes += n == 0; over += n > 1
    lows = [Fr(float(x['lower'])) for x in d if x['mode'] == mode]
    print(f"disk {mode}: {len(B)} boxes, inside {inside}, area==target {area == tgt}, holes {holes}, overlaps {over}, "
          f"all positive {all(x['result']=='positive' for x in d if x['mode']==mode)}, min lower {float(min(lows)):.8f} >= floor {min(lows) >= floor}", flush=True)
s0, s1 = Fr(1), Fr(U + 1, U)
for kind, i, t, sign in (('pole', 1, Fr(17, 8), -1), ('pole', 2, Fr(17, 8), -1), ('centre', 1, Fr(9, 2), 1), ('centre', 2, Fr(9, 2), 1),
                         ('pole', 1, Fr(2), 1), ('pole', 2, Fr(2), 1), ('centre', 1, Fr(5), -1), ('centre', 2, Fr(5), -1)):
    N = 128; T0 = time.time()
    while True:
        e = (tri2.pole_b if kind == 'pole' else tri2.centre_h)(i, s0, s1, t, t, N=N)
        ok = e.lo > 0 if sign > 0 else e.hi < 0
        if ok or N >= 2048: break
        N *= 2
    print(f"census {'b' if kind=='pole' else 'h'}{i}(s in [1,1+1/{U}], t={t}): [{float(e.lo):.7f}, {float(e.hi):.7f}] N={N} "
          f"{'CONFIRMED' if ok else 'NOT_REPRODUCED'} {time.time()-T0:.0f}s", flush=True)
