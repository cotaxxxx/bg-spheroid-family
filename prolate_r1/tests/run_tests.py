"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Each executed test emits PASS/FAIL; full mode is for Dig, not a sign run.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import traceback
from dataclasses import replace
from flint import arb, fmpq as Q, ctx
from .. import angular_raw,angular_quotient,axis_g,equatorial_phi_s,Config
from ..intervals import STATUS,bounds,ball,midpoint,serial
from ..jets import Jet
from .reference import lab_E,lab_gradients,sphere_series

LAMBDAS=(Q(2),Q(7,2),Q(5))
POINTS=((Q(1,8),Q(1,4)),(Q(1,4),Q(1,2)),(Q(1,2),Q(3,4)))
SMALL=((Q(1,8),Q(1,8),Q(5,2)),(Q(1,2),Q(1,2),Q(7,2)),
       (Q(7,8),Q(7,8),Q(9,2)))
BASE=Config()

def contains(a,b):
    # A positive test uses endpoints, not arb midpoint comparisons.
    al,ah=bounds(a); bl,bh=bounds(b)
    return al<=bl and bh<=ah

def smoke():
    # A mixed derivative check on a polynomial with known coefficients.
    x=Jet.constant(Q(2),(4,2),0)
    y=Jet.constant(Q(3),(4,2),1)
    v=(x*y+x**2)/(1+x)
    prod=v*(1+x)-(x*y+x**2)
    assert all(c.contains(0) for c in prod.c)
    # Physical sphere normalization, and exact geometric input rejection.
    assert Q(1176,5)/Q(15,16)**2*(Q(1,65536)+Q(1,33554432))<Q(1,240)
    try:
        angular_quotient(1,Q(1,2),Q(3),angle_kind="tau")
    except TypeError:
        pass
    else:
        raise AssertionError("integer geometric input was accepted")
    root=Path(__file__).resolve().parents[1]
    for path in root.rglob("*.py"):
        if "vendor" in path.parts: continue
        tree=ast.parse(path.read_text())
        assert not any(isinstance(n,ast.Constant) and isinstance(n.value,float)
                       for n in ast.walk(tree)),str(path)
    assert contains(angular_quotient(Q(1,2),Q(0),Q(1),angle_kind="tau").enclosure,arb(0))

def derivative_case(lam,R,tau,cfg,reference_grid):
    raw=angular_raw(R,tau,lam,angle_kind="tau",config=cfg)
    beta=2*arb(tau).atan(); h=arb(Q(1,128))
    def energy(b):
        # The point stays at the same exact ellipsoid radius R.
        return lab_E(arb(R)*b.cos(),arb(lam*R)*b.sin(),arb(lam),R,reference_grid)
    e0,ep,em=energy(beta),energy(beta+h),energy(beta-h)
    # These midpoints are only diagnostic estimates; no enclosure claim is
    # inferred from finite differences. Both containment and overlap are logged.
    fd1=(ep.mid()-em.mid())/(2*h)
    fd2=(ep.mid()-2*e0.mid()+em.mid())/(h*h)
    assert contains(raw.balls[1],fd1),"raw beta derivative misses FD midpoint"
    assert contains(raw.balls[2],fd2),"raw beta2 derivative misses FD midpoint"
    ex,ez=lab_gradients(arb(R)*(1-arb(tau)**2)/(1+arb(tau)**2),
                        arb(lam*R)*2*arb(tau)/(1+arb(tau)**2),arb(lam),R,
                        (reference_grid[0]//2,reference_grid[1]//2))
    rhs=-arb(R)*beta.sin()*ex+arb(lam*R)*beta.cos()*ez
    assert raw.balls[1].overlaps(rhs),"identity (9) disjoint"
    return {"Ebeta":serial(raw.balls[1]),"Ebetabeta":serial(raw.balls[2]),
            "fd_midpoints":[serial(fd1),serial(fd2)],
            "original_gradient_rhs":serial(rhs)}

def sphere_case(cfg):
    t=Q(1,2); refE,refg,refp=sphere_series(t)
    E=angular_raw(t,Q(1,2),Q(1),angle_kind="tau",config=cfg)
    W=angular_quotient(t,(Q(0),Q(1)),Q(1),angle_kind="tau",config=cfg)
    g=axis_g(t,Q(1),config=cfg)
    phi=equatorial_phi_s(t*t,Q(1),config=cfg)
    assert E.balls[0].overlaps(refE)
    assert contains(W.enclosure,arb(0)) and W.enclosure.is_zero()
    assert contains(g.enclosure,refg),"sphere g does not contain independent series"
    assert contains(phi.enclosure,refp),"sphere phi does not contain independent series"
    zero=equatorial_phi_s(Q(0),Q(1),config=cfg)
    assert zero.enclosure.contains(Q(-8,9)),"sphere Phi_s(0) != -8/9"
    assert axis_g(Q(0),Q(1),config=cfg).enclosure.is_zero()
    return {"g":serial(g.enclosure),"phi":serial(phi.enclosure)}

def boundary_case(lam,tau,cfg):
    w=angular_quotient((Q(15,16),Q(1)),tau,lam,angle_kind="tau",config=cfg)
    raw=angular_raw((Q(15,16),Q(1)),tau,lam,angle_kind="tau",config=cfg)
    assert w.enclosure.is_finite() and all(x.is_finite() for x in raw.balls)
    return w.to_json()

def small_box_case(center,cfg):
    R,T,L=center
    B=((R-Q(1,128),R+Q(1,128)),(T-Q(1,128),T+Q(1,128)),
       (L-Q(1,512),L+Q(1,512)))
    box=angular_quotient(*B,angle_kind="tau",config=cfg)
    points=[]
    from itertools import product
    points.extend(tuple(a[i] for a,i in zip(B,corner)) for corner in product((0,1),repeat=3))
    for i in range(12):
        weights=(Q(i+1,13),Q((5*i+3)%13,13),Q((7*i+2)%13,13))
        points.append(tuple(a+(b-a)*w for (a,b),w in zip(B,weights)))
    fine=replace(cfg,base_u=2*cfg.base_u,base_v=2*cfg.base_v)
    lo=bounds(box.enclosure)[0]
    for point in points:
        p=angular_quotient(*point,angle_kind="tau",config=fine)
        assert lo<=bounds(p.enclosure)[0],"box lower above point lower"
    return {"points":len(points),"box":box.to_json()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--full",action="store_true")
    parser.add_argument("--out",default="prolate_r1/outputs/dig_tests.json")
    args=parser.parse_args()
    tests=[("arithmetic_inputs_and_static_policy",smoke)]
    if args.full:
        for lam in LAMBDAS:
            for R,T in POINTS:
                tests.append(("FD_and_identity_"+str((lam,R,T)),
                              lambda l=lam,r=R,t=T:derivative_case(l,r,t,BASE,(64,128))))
        tests.append(("sphere_exact_series",lambda:sphere_case(BASE)))
        for lam in LAMBDAS:
            for tau in (Q(0),Q(1,2),Q(1)):
                tests.append(("boundary_"+str((lam,tau)),
                              lambda l=lam,t=tau:boundary_case(l,t,BASE)))
        for center in SMALL:
            tests.append(("box20_"+str(center),lambda c=center:small_box_case(c,BASE)))
    else:
        # Small local smoke; intentionally no full27 or global sign execution.
        tests.append(("one_sphere_axis",lambda: _quick_axis()))
    output={"status":STATUS,"mode":"full" if args.full else "quick","tests":[]}
    with ctx.workprec(BASE.precision):
        for name,fn in tests:
            try:
                detail=fn()
                row={"name":name,"result":"PASS","detail":detail}
            except Exception:
                row={"name":name,"result":"FAIL","traceback":traceback.format_exc()}
            output["tests"].append(row)
            print(row["result"],name,flush=True)
            if row["result"]=="FAIL": print(row["traceback"],flush=True)
    path=Path(args.out); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
    failures=sum(x["result"]=="FAIL" for x in output["tests"])
    print(STATUS,"tests:",len(tests),"failures:",failures)
    raise SystemExit(int(bool(failures)))

def _quick_axis():
    cfg=replace(BASE,order=2,base_u=2,base_v=2,distance_ratio=Q(2))
    g=axis_g(Q(1,4),Q(1),config=cfg)
    assert contains(g.enclosure,sphere_series(Q(1,4))[1])
    return g.to_json()

if __name__=="__main__":
    main()
