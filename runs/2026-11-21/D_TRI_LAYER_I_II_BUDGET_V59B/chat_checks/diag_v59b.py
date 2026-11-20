import sys, json, time, math
sys.path.insert(0, '../GER2')
from fractions import Fraction as F
from geoenclosereader import tri3
S = [json.loads(l) for l in open('res_v59b.jsonl')]
r = [x for x in S if x['status']=='UNRESOLVED' and x['kind']=='H33' and x['tile']==[3,7] and x['cell']==[0,23,0]][0]
box = [tuple(F(v) for v in pr) for pr in r['box']]
L3 = float(box[0][1]*box[1][1]); g = max(0, min(4, round(math.log2(L3))))
for N in (256, 512):
    t = time.time(); e = tri3.H33(box, N, g); L = tri3.enclose.last
    print(json.dumps(dict(N=N, lo=e.lo, hi=e.hi, angular=L['angular_width'], terms={str(k): v for k, v in L['terms'].items()}, contact=L['contact_cells'], sec=round(time.time()-t,1)), default=lambda x: float(x) if getattr(x,'size',1)==1 else x.tolist()), flush=True)
