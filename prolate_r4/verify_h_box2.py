"""Independent file/contract checker for D-PRO R4 v3 H box2.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Checks exact rational endpoint arithmetic and supplied reference data.
Does NOT independently certify the producer's calculus or quadrature.
"""
import json,sys
from fractions import Fraction as F
from pathlib import Path
RUN=Path(sys.argv[1]) if len(sys.argv)>1 else Path('runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT/H_box2.json')
j=json.loads(RUN.read_text())
def ends(x):return F(x['lower']),F(x['upper'])
def frac(x):return F(str(x))
assert j['scope']=='box2-only-v3-H'
assert j['precision_bits']==128 and j['python_flint']=='0.8.0'
assert j['cells']>0 and j['mesh_policy']['kappa']=='0'
hl,hu=ends(j['H_box_enclosure'])
pl,pu=ends(j['point_H'])
cl,cu=ends(j['correction'])
assert hl<=pl+cl and hu>=pu+cu
assert hl<=hu and pl<=pu and cl<=cu
box=((F(95,128),F(97,128)),(F(15,128),F(17,128)),(F(1279,256),F(5)))
assert all(tuple(map(F,ax))==tuple(p) for ax,p in zip((j['R'],j['tau'],j['lambda']),box))
centers=(F(3,4),F(1,8),F(2559,512))
assert tuple(map(F,j['center']))==centers
def val(s):
    head,point,tail=s.partition('.')
    return F(int(head+tail),10**len(tail)) if point else F(int(s))
refs=[
 ('3/4/1/8/2559/512','-0.159650308008'),
 ('381/512/31/256/5','-0.157416037171'),
 ('387/512/33/256/5119/1024','-0.162073833546'),
 ('191/256/67/512/2559/512','-0.158241706568'),
 ('193/256/61/512/5117/1024','-0.161016388647')
]
for key,ref in refs:
    assert j['reference_checks'][key]['included_with_1e-7_margin']
    a=val(ref); e=F(1,10**7)
    assert hl<=a-e and a+e<=hu
assert len(j['derivatives'])==3
radii={'R':F(1,128),'x':F(1,128),'lam':F(1,512)}
for name,row in j['derivatives'].items():
    lo,hi=ends(row['derivative_integral'])
    co_lo,co_hi=ends(row['correction'])
    r=radii[name]
    M=max(abs(lo),abs(hi))*r
    assert co_lo<=-M and co_hi>=M, (name,'correction interval lost a bound')
    assert co_lo<=0<=co_hi
budget=F(1,10)
assert (hu-hl)/2<=budget if j['h_budget_result']=='PASS' else (hu-hl)/2>budget
print(json.dumps({
 'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
 'file_contract':'PASS','all_reference_checks':5,
 'H_interval_approx':[float(hl),float(hu)],
 'H_halfwidth_approx':float((hu-hl)/2),
 'normalized_halfwidth_approx':float((hu-hl)/2)/abs(-0.159650308008),
 'wall_seconds':j['wall_s'],
 'cells':j['cells'],
 'warning':'No independent mathematical proof of producer interval quadrature'
},indent=2))
