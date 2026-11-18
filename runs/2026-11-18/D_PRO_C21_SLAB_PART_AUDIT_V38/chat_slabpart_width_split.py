"""chat V38: split of the H box half-widths in the slab-part checkpoint (2e3a091a): centre-point width vs outer
mean-value correction, and the size of the true linear term |grad H(mid)|.h estimated from the stored derivative intervals."""
import json, glob, sys, statistics as st
c=[];o=[];lin=[]
for p in sorted(glob.glob(sys.argv[1]+'/boxes/*.json')):
    d=json.load(open(p)); cp=d.get('center_point'); oc=d.get('outer_correction'); dc=d.get('directional_contributions')
    if not cp or not oc or not dc or 'R' not in dc: continue
    c.append(cp['halfwidth']); o.append(oc['halfwidth'])
    lin.append(sum(abs(dc[k]['integrated_signed_derivative']['mid'])*dc[k]['outer_halfwidth_contribution']['halfwidth']/dc[k]['integrated_signed_derivative']['halfwidth'] for k in dc))
print("boxes", len(c))
print("centre-point halfwidth: median %.5f max %.5f" % (st.median(c), max(c)))
print("outer mean-value correction halfwidth: median %.4f max %.4f" % (st.median(o), max(o)))
print("estimated true linear term |grad(mid)|.h: median %.5f max %.5f" % (st.median(lin), max(lin)))
print("inflation outer/linear: median %.0f" % st.median(a/b for a, b in zip(o, lin)))
