import sys, time; sys.path.insert(0, '.'); sys.path.insert(0, '../v57')
from fractions import Fraction as Fr
from geoenclosereader import tri3
import chat_v57_numeric_lib as num
bad = 0
def chk(name, enc, val):
    global bad; ok = enc.lo <= val <= enc.hi; bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: [{float(enc.lo):.10g}, {float(enc.hi):.10g}] width {float(enc.hi-enc.lo):.2e} ref {val:.10g} contact {tri3.enclose.last['contact_cells']}", flush=True)
for (s, t, q) in ((1.2, 1.5, (0.25, 0.25, 0.5)), (2.5, 4, (0.25, 0.0, 0.5)), (1.5, 2, (0.5, 0.5, 0.0)), (1.5, 2, (0.25, 0.25, 0.0))):
    pt = [(Fr(s), Fr(s)), (Fr(t), Fr(t))] + [(Fr(x), Fr(x)) for x in q]
    for N in (32, 64):
        t0 = time.time()
        for kind in ("E3", "T12", "H33"):
            chk(f"N={N} {kind}{(s, t, q)}", tri3.enclose(kind, pt, N), num.general(kind, s, t, q))
        print("  time", round(time.time() - t0, 1))
# a box (shape and position) contains corner values
bx = [(Fr(3, 2), Fr(3, 2) + Fr(1, 128)), (Fr(2), Fr(2) + Fr(1, 128)), (Fr(1, 4), Fr(1, 4) + Fr(1, 512)), (Fr(1, 4), Fr(1, 4) + Fr(1, 512)), (Fr(1, 2), Fr(1, 2) + Fr(1, 512))]
e = tri3.enclose("E3", bx, 64)
for c in ((1.5, 2, (0.25, 0.25, 0.5)), (1.5 + 1/128, 2 + 1/128, (0.25 + 1/512, 0.25 + 1/512, 0.5 + 1/512))): chk("box E3 corner", e, num.general("E3", c[0], c[1], c[2]))
# boundary point (contact): q = (0.6, 0, 0.8)
pt = [(Fr(3, 2), Fr(3, 2)), (Fr(2), Fr(2)), (Fr(3, 5), Fr(3, 5)), (Fr(0), Fr(0)), (Fr(4, 5), Fr(4, 5))]
for N in (32, 64): chk(f"rim E3 N={N}", tri3.enclose("E3", pt, N), num.general("E3", 1.5, 2, (0.6, 0, 0.8), n=1500))
print("FAILURES", bad)
