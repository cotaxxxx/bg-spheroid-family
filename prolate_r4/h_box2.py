"""D-PRO R4 v3 §6: rigorous horizontal H=E_rho/rho box-2 diagnostic.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No global computation, no sign certification.

R3 pinned geometry and Arb jets are IMPORTED READ-ONLY from the frozen R3
source. Unlike W, this uses only the laboratory rho derivative of f.
"""
import argparse, json, sys, time, resource, hashlib
from pathlib import Path
from flint import arb, fmpq as Q, ctx
from prolate_r1.density import common, Domain, seed
from prolate_r1.jets import Jet
from prolate_r1.quadrature import make_mesh, integrate, range_integral
from prolate_r1.intervals import Config, ball, midpoint, radius, bounds, sym
STATUS='DIAGNOSTIC_ONLY / NOT_EVIDENCE'
RBOX=(Q(95,128),Q(97,128))
TBOX=(Q(15,128),Q(17,128))
LBOX=(Q(1279,256),Q(5))
CENTER=(Q(3,4),Q(1,8),Q(2559,512))
REFS=[
 ((Q(3,4),Q(1,8),Q(2559,512)),'-0.159650308008'),
 ((Q(381,512),Q(31,256),Q(5)),'-0.157416037171'),
 ((Q(387,512),Q(33,256),Q(5119,1024)),'-0.162073833546'),
 ((Q(191,256),Q(67,512),Q(2559,512)),'-0.158241706568'),
 ((Q(193,256),Q(61,512),Q(5117,1024)),'-0.161016388647')
]
def decimal_q(s):
    left,dot,right=s.partition('.')
    return Q(int(left+right),10**len(right)) if dot else Q(int(s))
def iv(b): return arb(b[0]).union(arb(b[1]))
def upperabs(x):
    a,b=bounds(x)
    return max(abs(a),abs(b))
def out(x):
    a,b=bounds(x)
    return {'lower':str(a),'upper':str(b),
            'lower_approx':float(arb(a)),'upper_approx':float(arb(b)),
            'mid_approx':float(arb((a+b)/2)),
            'halfwidth_approx':float(arb((b-a)/2))}
def check_input():
    assert RBOX[0]>0 and RBOX[1]<1 and LBOX[1]<=5
    for p,v in REFS:
        assert all(a<=x<=b for x,(a,b) in zip(p,(RBOX,TBOX,LBOX)))
    return True
def density_H(u,v,params,dom,active=(),orders=(0,)):
    # R3 common computes the co-rotating primitive geometry, even though
    # H uses only the laboratory rho derivative and no z derivative.
    R,x,lam,a,b,k,sigma,mx,mz,xx,xz,C,B,g,gg,rr,rp,d,e,jac=common(
        u,v,params,dom,active,orders)
    D=sigma*C.sqrt()
    Rhi=dom.R[1]; Lhi=dom.lam[1]
    # D >= 1-Rhi > 0, D <= lambda_max (1+Rhi)
    invD=D.reciprocal_positive(1-Rhi,Lhi*(1+Rhi))
    invsqrtB=B.sqrt().reciprocal_positive(Q(1,Lhi),Q(1))
    # gamma = k/(D sqrt(B)), tx = (xi_x-rho)/D.
    # d_gamma/d_rho = gamma*(xi_x-rho)/D**2 - xi_x/(D sqrt(B)).
    tx=mx/C.sqrt()
    dx=g*tx-xx*invsqrtB
    f_rho=-xx*gg-2*k*rr*dx*invD
    # rho=R cos(beta), with beta=2 atan(tau)
    tauhi=TBOX[1]; taulo=TBOX[0]
    a_lo=(1-tauhi*tauhi)/(1+tauhi*tauhi)
    a_hi=(1-taulo*taulo)/(1+taulo*taulo)
    invrho=(R*a).reciprocal_positive(dom.R[0]*a_lo,dom.R[1]*a_hi)
    return (f_rho*jac*invrho,)
def run(preflight=False,ratio=Q(1,2),order=4,base_u=16,base_v=32):
    start=time.perf_counter()
    check_input()
    cfg=Config(precision=128,order=order,base_u=base_u,base_v=base_v,
               distance_ratio=ratio,kappa=Q(1,4096))
    # Since R upper < 1 the actual cap removal is zero, NOT cfg.kappa.
    dom=Domain(RBOX,LBOX,Q(0),'equator')
    with ctx.workprec(128):
        if preflight:
            uv=(arb(Q(1,2)),arb(Q(1,3)))
            pt=density_H(*uv,tuple(map(arb,CENTER)),dom)[0].c[0]
            pbox=tuple(iv(x) for x in (RBOX,TBOX,LBOX))
            grads={}
            for name in ('R','x','lam'):
                g=density_H(*uv,pbox,dom,(name,),(1,))[0]
                grads[name]=out(g.coeff(1))
            return {'status':STATUS,'scope':'preflight-only','density_at_uv':out(pt),'grads_at_uv':grads,'wall_s':time.perf_counter()-start}
        mesh=make_mesh(RBOX,Q(0),cfg,lam=LBOX)
        print('MESH',len(mesh),flush=True)
        exactpoint=tuple(map(arb,CENTER))
        ptstart=time.perf_counter()
        pt=integrate(lambda u,v,name,n:density_H(u,v,exactpoint,dom,(name,),(n,)),mesh,cfg.order)[0]
        pttime=time.perf_counter()-ptstart
        print('POINT',out(pt),'seconds',round(pttime,3),flush=True)
        params=tuple(iv(z) for z in (RBOX,TBOX,LBOX))
        correction=arb(0)
        contributions={}
        # Pre-registered H budget: halfwidth <= 1/10; no sign used for path choice.
        for box,name in zip((RBOX,TBOX,LBOX),('R','x','lam')):
            timer=time.perf_counter()
            # Integrate the signed FIRST external Taylor coefficient by a
            # rigorous spatial high-order Taylor rule. In particular NO
            # zeroth-order spatial range sum is used for ANY coefficient.
            def derivative_jet(u,v,axis,n):
                mixed=density_H(u,v,params,dom,(axis,name),(n,1))[0]
                return (Jet((n,),[mixed.coeff(k,1) for k in range(n+1)]),)
            grad=integrate(derivative_jet,mesh,cfg.order)[0]
            symrad=sym(radius(box))
            contrib=grad*symrad
            correction+=contrib
            contributions[name]={'derivative_integral':out(grad),
                                 'correction':out(contrib),
                                 'wall_s':time.perf_counter()-timer}
            print('DERIV',name,contributions[name],flush=True)
        encl=pt+correction
        # Reference values are floating diagnostic checks, NOT inclusion
        # certificates. Inflate by 1e-7 to account for stated errors.
        ref_ok={}
        for p,s in REFS:
            x=decimal_q(s)
            ref_ok['/'.join(str(j) for j in p)]={
                'source_value':s,'included_with_1e-7_margin':bool(bounds(encl)[0]<=x-Q(1,10**7) and x+Q(1,10**7)<=bounds(encl)[1])}
        c0=decimal_q('-0.159650308008')
        obj={'status':STATUS,'scope':'box2-only-v3-H','method':'signed 4th/6th-order R3 spatial Taylor + first-order outer mean-value',
             'precision_bits':128,'python_flint':'0.8.0','R':list(map(str,RBOX)),'tau':list(map(str,TBOX)),
             'lambda':list(map(str,LBOX)),'center':list(map(str,CENTER)),
             'cells':len(mesh),'mesh_policy':{'base_u':base_u,'base_v':base_v,'ratio':str(ratio),'order':order,'kappa':'0'},
             'H_box_enclosure':out(encl),'point_H':out(pt),
             'correction':out(correction),'derivatives':contributions,
             'normalized_halfwidth_vs_abs_H_center':out(encl)['halfwidth_approx']/abs(float(arb(c0))),
             'reference_checks':ref_ok,'h_budget_halfwidth':'1/10',
             'h_budget_result':'PASS' if out(encl)['halfwidth_approx']<=0.1 else 'FAIL',
             'wall_s':time.perf_counter()-start,
             'point_integral_wall_s':pttime,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'W_comparison':{'prior_stage1_executed':False,'W_full_box_halfwidth':None,'W_reference_center':2.0659,
                             'V32_second_order_halfwidth':0.836835755,'V32_second_order_wall_s_other_computer':2728.914},
             'full_domain_proof':'OPEN','geometry_lineage':'R3 frozen physical rho-derivative; no z-derivative and no finite difference',
             'spatial_gradients':'Signed high-order Taylor for all three external derivatives; no zeroth-order coefficient integration'}
        return obj
def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--preflight',action='store_true')
    pa.add_argument('--order',type=int,choices=(2,4,6),default=4)
    pa.add_argument('--base-u',type=int,default=16)
    pa.add_argument('--base-v',type=int,default=32)
    pa.add_argument('--distance-ratio',default='1/2')
    pa.add_argument('--output',default='')
    args=pa.parse_args()
    import flint
    if flint.__version__!='0.8.0':raise RuntimeError('python-flint 0.8.0 required')
    ratio=Q(args.distance_ratio)
    obj=run(args.preflight,ratio,args.order,args.base_u,args.base_v)
    data=json.dumps(obj,indent=2,ensure_ascii=False)
    if args.output:Path(args.output).write_text(data+'\n')
    print(data,flush=True)
if __name__=='__main__':main()
