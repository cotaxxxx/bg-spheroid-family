"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. PASS/FAIL are software test labels only."""
import ast
import json
import sys
import time
import traceback
from pathlib import Path
import mpmath as mp
from flint import arb,fmpq as Q,ctx
from .. import kernel as k
from ..make_boxes import specification
from .reference import sphere_reference,numerical

ROOT=Path(__file__).resolve().parents[1]
RESULTS=[]


def check(name,fn):
    start=time.perf_counter_ns()
    try:
        detail=fn()
        row={'name':name,'result':'PASS','detail':detail}
    except Exception:
        row={'name':name,'result':'FAIL','traceback':traceback.format_exc()}
    row.update(status=k.STATUS,wall_ns=time.perf_counter_ns()-start)
    RESULTS.append(row)
    print(json.dumps(row),flush=True)


def contains_reference(ball,value):
    # Check the rounded 30-digit NUMERICAL reference, not a proof interval.
    target=arb(mp.nstr(value,40))
    assert ball.contains(target), (str(ball),mp.nstr(value,30))


def sphere():
    pts=[(Q(0),Q(1,8)),(Q(1,8),Q(1,8)),(Q(1,4),Q(1,2)),
         (Q(1,2),Q(1,4)),(Q(0),Q(3,4))]
    rows=[]
    for rho,z in pts:
        ref=sphere_reference(rho,z)
        ee,ez,ezz=k.point_balls(rho,z,Q(1),128).balls
        contains_reference(ee,ref[0])
        contains_reference(ez/arb(z),ref[1])
        contains_reference(ezz,ref[2])
        rows.append({'rho':str(rho),'z':str(z),'ref_V':mp.nstr(ref[1],30),
                     'ref_Ezz':mp.nstr(ref[2],30),'V_ball':str(ez/arb(z)),'Ezz_ball':str(ezz)})
    return rows


def reflection():
    rows=[]
    for rho,z,lam in [(Q(1,8),Q(1,4),Q(2)),(Q(1,4),Q(1,2),Q(3)),
                       (Q(1,2),Q(3,4),Q(5)),(Q(0),Q(1),Q(7,2)),
                       (Q(3,8),Q(0),Q(3))]:
        a=k.point_balls(rho,z,lam,128).balls
        b=k.point_balls(rho,-z,lam,128).balls
        assert a[0].overlaps(b[0]) and a[1].overlaps(-b[1]) and a[2].overlaps(b[2])
        if z:
            assert (a[1]/arb(z)).overlaps(b[1]/arb(-z))
        else:
            assert a[1].contains(0)
        rows.append([str(rho),str(z),str(lam)])
    return {'points':rows,'test':'interval overlap (symmetry is proved in LEMMAS_DRAFT)'}


def differences():
    pts=[(Q(0),Q(1,4)),(Q(1,8),Q(0)),(Q(1,4),Q(1,4)),
         (Q(3,8),Q(1,2)),(Q(1,2),Q(3,4))]
    h=Q(1,1024)
    rows=[]
    for rho,z in pts:
        ee,ez,ezz=k.point_balls(rho,z,Q(3),128).balls
        pm=k.point_balls(rho,z-h,Q(3),128).balls
        pp=k.point_balls(rho,z+h,Q(3),128).balls
        assert ez.overlaps((pp[0]-pm[0])/arb(2*h))
        assert ezz.overlaps((pp[1]-pm[1])/arb(2*h))
        # Also use independent high-precision 2D quadratures, to avoid a test
        # consisting only of very wide difference intervals.
        ref=numerical(rho,z,Q(3),128)
        coarse=numerical(rho,z,Q(3),96)
        assert max(abs(a-b) for a,b in zip(ref,coarse))<mp.mpf(1)/10**9
        for ball,val in zip((ee,ez,ezz),ref): contains_reference(ball,val)
        minus=numerical(rho,z-h,Q(3),128)
        plus=numerical(rho,z+h,Q(3),128)
        with mp.workdps(35):
            fd=[(plus[j]-minus[j])*1024/2 for j in (0,1)]
            for val,exact in zip(fd,ref[1:]):
                assert abs(val-exact)<mp.mpf(1)/10**5
            contains_reference(ez,fd[0]);contains_reference(ezz,fd[1])
        rows.append({'rho':str(rho),'z':str(z),'ref_Ez':mp.nstr(ref[1],30),
                     'ref_Ezz':mp.nstr(ref[2],30),'fd_Ez':mp.nstr(fd[0],30),
                     'fd_Ezz':mp.nstr(fd[1],30)})
    return rows


def box_sanity():
    # Separate test fixtures, not a run of the 27-box calibration manifest.
    fixtures=[((Q(1,4),Q(17,64)),(Q(0),Q(1,64)),(Q(3),Q(769,256))),
              ((Q(1,4),Q(17,64)),(Q(1,2),Q(33,64)),(Q(3),Q(769,256)))]
    detail=[]
    for rr,tt,ll in fixtures:
        box=k.V_box_details(rr,tt,ll,128)
        points=[]
        # 20 exact rational points in EACH box, including z=0 for first box.
        for i in range(20):
            r=rr[0]+(rr[1]-rr[0])*Q(i,19)
            t=tt[0]+(tt[1]-tt[0])*Q((7*i)%20,19)
            lam=ll[0]+(ll[1]-ll[0])*Q((11*i)%20,19)
            rho=r*(1-t*t)/(1+t*t);z=lam*r*2*t/(1+t*t)
            v=k.V_ball(rho,z,lam,128)
            assert box.lower <= v.lower(), (box.route,i,str(box.lower),str(v.lower()))
            points.append({'R':str(r),'tau':str(t),'lam':str(lam),'point_lower':str(v.lower().fmpq())})
        detail.append({'route':box.route,'box_lower':str(box.lower.fmpq()),'points':points})
    return detail


def analytic_regressions():
    with ctx.workprec(128):
        g=k.J(1,1)
        gg,rr,rp=k.angle_values(g)
        assert gg.c[0].contains(0) and rr.c[0].contains(1) and rp.c[0].contains(Q(-1,3))
        for j in range(11):
            gamma=Q(j,10)
            g=k.J(arb(gamma),1)
            _,r,rp=k.angle_values(g)
            # mpmath's integral, independent of the series recurrence.
            with mp.workdps(40):
                gm=mp.mpf(j)/10
                ref=mp.quad(lambda t:1/(gm+mp.cosh(t)),[0,1,mp.inf])
                dr=mp.quad(lambda t:-1/(gm+mp.cosh(t))**2,[0,1,mp.inf])
            contains_reference(r.c[0],ref);contains_reference(rp.c[0],dr)
    return 'gamma=1 limits and 11 integral-representation angle checks'


def input_and_plan():
    files=list(ROOT.rglob('*.py'))
    for p in files:
        tree=ast.parse(p.read_text())
        assert not any(isinstance(n,ast.Constant) and isinstance(n.value,float) for n in ast.walk(tree)),str(p)
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='float' for n in ast.walk(tree)),str(p)
    # Explicit rejection of float inputs, without a floating-point literal.
    try: k.E_ball(1/8,Q(0),Q(3),128)
    except TypeError: pass
    else: raise AssertionError('float input accepted')
    for call in [lambda:k.E_ball(Q(1),Q(0),Q(3),128),
                 lambda:k.V_box_lower((Q(0),Q(1)),(Q(0),Q(1)),(Q(2),Q(5)),128)]:
        try:call()
        except ValueError:pass
        else:raise AssertionError('out-of-domain input accepted')
    spec=json.loads((ROOT/'boxes.json').read_text())
    assert spec==specification() and len(spec['boxes'])==27
    for b in spec['boxes']:
        assert Q(b['R'][1])-Q(b['R'][0])==Q(1,64)
        assert Q(b['tau'][1])-Q(b['tau'][0])==Q(1,64)
        assert Q(b['lam'][1])-Q(b['lam'][0])==Q(1,256)
    return {'python_files_checked':len(files),'boxes':27,'float_literals':0}


def main():
    ctx.prec=128
    for name,fn in [('input_and_plan',input_and_plan),('angle_limits',analytic_regressions),
                    ('sphere_5_points',sphere),('reflection_5_points',reflection),
                    ('differences_lambda3_5_points',differences),('boxes_20_points_each',box_sanity)]:
        check(name,fn)
    path=ROOT/'outputs'/'tests.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({'status':k.STATUS,'meaning':'software comparisons only; no theorem verdict',
                                'results':RESULTS},indent=2)+'\n')
    failures=sum(row['result']=='FAIL' for row in RESULTS)
    print(f'{k.STATUS}: {len(RESULTS)-failures} test groups PASS, {failures} test groups FAIL',flush=True)
    return int(failures>0)


if __name__=='__main__': sys.exit(main())
