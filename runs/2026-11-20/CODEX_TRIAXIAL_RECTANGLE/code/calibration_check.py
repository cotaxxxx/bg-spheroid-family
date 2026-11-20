"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Ledger validation, replay and budget report.

The non-interval quadrature is an implementation cross-check only. It is never
inserted into an interval ledger or used to remove an unresolved case.
"""
from pathlib import Path
from fractions import Fraction
import csv,json,hashlib,math,statistics,argparse,platform
from collections import Counter,defaultdict
import numpy as np
import mpmath as mp
import calibration as c1
import calibration_extended as c2
import calibration_position as c3
import calibration_normalized as c4

ROOT=c1.ROOT
INT_KEYS=['shape','slo','shi','tlo','thi','q1lo','q1hi','q2lo','q2hi','q3lo','q3hi','unit','nmu','nw','sphere_cells','half','contact_cells']

def read_rows(name):
    rows=list(csv.DictReader((ROOT/'out'/name).open()))
    for row in rows:
        for key in INT_KEYS:
            if key in row:row[key]=int(row[key])
        for key in ['lower','upper','width','seconds']:row[key]=float(row[key])
    return rows

def ident(row):
    return row['shape'],row['mode'],row.get('experiment','C1A'),row.get('half',16)

def group(rows):
    out=defaultdict(list)
    for row in rows:out[ident(row)].append(row)
    for v in out.values():v.sort(key=lambda row:row['nmu'])
    return out

def state(row):
    return 'positive' if row['lower']>0 else ('negative' if row['upper']<0 else 'unresolved')

def validate(rows,expected,ladder):
    groups=group(rows);specs={ident(x):x for x in expected}
    assert set(groups)==set(specs),(len(groups),len(specs))
    for key,items in groups.items():
        assert [r['nmu'] for r in items]==ladder[:len(items)]
        assert all(state(r)!='positive' for r in items[:-1])
        for row in items:
            for k,v in specs[key].items():assert row[k]==v,(key,k,row[k],v)
            assert row['unit']==65536 and row['nw']==row['nmu']//2
            assert row['sphere_cells']==4*row['nmu']*row['nw']
            assert all(math.isfinite(row[k]) for k in ['lower','upper','width','seconds'])
            assert row['lower']<=row['upper'] and row['width']==row['upper']-row['lower']
            assert row['seconds']>0 and row['result']==state(row)
            assert 65536<=row['slo']<=row['shi']<=209716
            assert 65536<=row['tlo']<=row['thi']<=6*65536
            for i in [1,2,3]:assert 0<=row[f'q{i}lo']<=row[f'q{i}hi']
            min_norm2=sum(row[f'q{i}lo']**2 for i in [1,2,3])
            max_norm2=sum(row[f'q{i}hi']**2 for i in [1,2,3])
            if row.get('domain')=='intersection_closed_ball':assert min_norm2<=65536**2
            else:assert max_norm2<65536**2
            if row['mode']=='D12':assert row['q1lo']>0 and row['q2lo']>0 and row['q3hi']==0
            elif row.get('experiment')!='H33_collar':assert row['q3lo']>0
        assert state(items[-1])=='positive' or len(items)==len(ladder)
    finals=[v[-1] for v in groups.values()]
    return {'cases':len(groups),'stages':len(rows),'final_results':dict(Counter(state(x) for x in finals)),
            'final_nmu':dict(Counter(str(x['nmu']) for x in finals)),
            'sum_evaluation_wall_seconds':sum(x['seconds'] for x in rows),
            'minimum_final_lower':min(x['lower'] for x in finals),
            'maximum_final_width':max(x['width'] for x in finals)}

def check_frozen_files():
    checks=[]
    for name in ['PLAN_CALIBRATION','PLAN_CALIBRATION_C1A','PLAN_CALIBRATION_C2','PLAN_CALIBRATION_C3','PLAN_CALIBRATION_C4','PLAN_CALIBRATION_C5']:
        for line in (ROOT/'plans'/f'{name}.sha256').read_text().splitlines():
            digest,recorded=line.split(None,1);recorded=recorded.strip();actual=recorded
            if name=='PLAN_CALIBRATION' and recorded=='code/calibration.py':actual='code/calibration_c1_initial.py'
            got=hashlib.sha256((ROOT/actual).read_bytes()).hexdigest()
            assert digest==got,(name,recorded,actual)
            checks.append({'plan':name,'recorded_path':recorded,'historical_actual_path':actual,'sha256':got,'consistent':True})
    return checks

def angle_check():
    mp.mp.dps=90;table=c1.angle_table();qt=c4.q_table();records=[]
    def inside(value,interval,index=None):
        a,b=(float(interval.a),float(interval.b)) if index is None else (float(interval.a[index]),float(interval.b[index]))
        assert mp.mpf(a)<=value<=mp.mpf(b),(str(value),a,b)
    inside(mp.pi,c1.pi_box())
    for j in [0,2048,16384,32768,49152,63488,65535,65536]:
        g=mp.mpf(j)/65536
        if j==65536:P=mp.mpf(2);Q=mp.mpf(10)/3;F=mp.mpf(0)
        else:
            theta=mp.acos(g);P=2*theta/mp.sqrt(1-g*g);F=theta*theta
            Q=2*P+g*(g*P-2)/(1-g*g)
        values={'P':P,'F':F,'R':g*P,'J':g*P-F,'K':g*g*P}
        for key,value in values.items():inside(value,table[key],j)
        inside(Q,qt,j);records.append({'gamma_numerator':j,'gamma_denominator':65536,'all_six_kernels_contained':True})
    return {'pi_contained':True,'mpmath_dps':90,'angle_checks':records,'role':'implementation diagnostic, not a proof of all table entries'}

def point_gradient(s,t,q,n):
    # Independent spherical quadrature, using both signs of all coordinates.
    # No interval kernel, rational-w parametrization or angle table is reused.
    mu,weights=np.polynomial.legendre.leggauss(n)
    phi=2*np.pi*(np.arange(2*n)+.5)/(2*n)
    radial=np.sqrt(1-mu*mu)[:,None]
    xi=np.stack(np.broadcast_arrays(radial*np.cos(phi),radial*np.sin(phi),mu[:,None]),axis=-1)
    v=xi-q;A=np.array([1,s*s,(s*t)**2]);D=np.sqrt(np.sum(A*v*v,axis=-1))
    S=np.sqrt(np.sum(xi*xi/A,axis=-1));k=1-np.sum(q*xi,axis=-1)
    g=np.clip(k/(D*S),0,1);theta=np.arccos(g)
    den=np.sqrt(np.maximum(1-g*g,1e-300));P=2*theta/den
    d=1-g;P=np.where(d<1e-7,2*(1+d/3+2*d*d/15+2*d*d*d/35),P)
    J=g*P-theta*theta;K=g*g*P;b=A*v/D[...,None]
    integrand=xi*J[...,None]-b*S[...,None]*K[...,None]
    return np.sum(integrand*(weights[:,None,None]/(4*n)),axis=(0,1))

def point_checks(datasets):
    selected=[]
    for name,rows in datasets.items():
        for items in group(rows).values():
            r=items[-1]
            choose=(name=='C1A' and r['shape'] in [0,31]) or (name=='C2' and r['experiment']=='boundary_box' and r['shape'] in [0,31]) or (name=='C4' and r['mode']=='G3_123')
            if choose:selected.append((name,r))
    records=[]
    for name,row in selected:
        s=(row['slo']+row['shi'])/(2*65536);t=(row['tlo']+row['thi'])/(2*65536)
        q=np.array([(row[f'q{i}lo']+row[f'q{i}hi'])/(2*65536) for i in [1,2,3]])
        if row.get('experiment')=='boundary_box':
            q={'G3_123':np.array([2/3,1/3,2/3]),'G3_13':np.array([3/5,0,4/5]),
               'G3_23':np.array([0,3/5,4/5]),'D12':np.array([3/5,4/5,0])}[row['mode']]
        values=[]
        for n in [80,160]:
            grad=point_gradient(s,t,q,n)
            val=(grad[1]/q[1]-grad[0]/q[0])/(s*s-1) if row['mode']=='D12' else grad[2]/q[2]
            assert row['lower']<=val<=row['upper'],(name,ident(row),val,row['lower'],row['upper'])
            values.append(float(val))
        records.append({'plan':name,'shape':row['shape'],'mode':row['mode'],'point':q.tolist(),
            'orders':[80,160],'noninterval_values':values,'order_difference':abs(values[1]-values[0]),
            'inside_recorded_enclosure':True})
    return {'role':'non-interval diagnostics; never used as evidence or to change a ledger result','records':records}

def replay(datasets):
    selected=[]
    for name,rows in datasets.items():
        for items in group(rows).values():
            r=items[-1]
            if (name=='C1A' and r['shape']==31 and r['mode']=='D12') or (name=='C2' and r['shape']==31 and r['mode']=='D12' and r['experiment']=='boundary_box') or (name=='C4' and r['shape']==0 and r['mode']=='G3_123'):
                selected.append((name,r))
    records=[]
    for name,row in selected:
        value=c1.enclosure(row,row['nmu']) if name=='C1A' else (c2.enclosure(row,row['nmu'])[0] if name=='C2' else c4.enclosure(row,row['nmu']))
        assert float(value.a)==row['lower'] and float(value.b)==row['upper']
        records.append({'plan':name,'shape':row['shape'],'mode':row['mode'],'nmu':row['nmu'],
                        'lower_hex':float(value.a).hex(),'upper_hex':float(value.b).hex(),'bitwise_same':True})
    return {'role':'same-code numerical reproduction, not independent validation','records':records}

def costs(rows):
    groups=group(rows);records=[]
    for half in [256,1024,4096]:
        items=[v for v in groups.values() if v[-1]['experiment']=='position_width' and v[-1]['half']==half]
        elapsed=[sum(r['seconds'] for r in v) for v in items];median=statistics.median(elapsed)
        cells_per_axis=65536//(2*half);shape_cells=math.ceil(Fraction(11,5)/Fraction(1,8))*40
        spatial_cells=cells_per_axis**3+3*cells_per_axis**2;count=shape_cells*spatial_cells
        records.append({'nominal_shape_full_width':'1/8','shape_grid_cells':shape_cells,
             'position_full_width':str(Fraction(2*half,65536)),'positive_calibration_cases':sum(v[-1]['result']=='positive' for v in items),
             'total_calibration_cases':len(items),'median_case_seconds_all_stages':median,
             'maximum_case_seconds_all_stages':max(elapsed),'cube_plus_three_faces_cells_per_shape':spatial_cells,
             'total_hypothetical_cells':count,'serial_equivalent_days_at_observed_median':count*median/86400,
             'ideal_two_worker_days':count*median/86400/2,
             'whole_proof_cost_bound':False})
    return {'warning':'Hypothetical fixed grids only. The 1/8 shape width was clipped at four corners; it was not tested on every shape cell. Position cases include unresolved results. These are budget arithmetic, not completion-time estimates. All sphere-outside cube cells may be culled, but axis and boundary collars require extra work.',
            'records':records,'adaptive_cost':'Not estimated: success widths and stopping depth outside the finite calibration patches are unknown.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-replay',action='store_true');args=parser.parse_args()
    data={'C1A':read_rows('calibration_pilot_c1a.csv')+read_rows('calibration_remaining_c1a.csv'),
          'C2':read_rows('calibration_extended.csv'),'C3':read_rows('calibration_position.csv'),'C4':read_rows('calibration_normalized.csv')}
    expected={'C1A':[c1.case(i,m) for i in range(32) for m in c1.MODES],
              'C2':c2.make_cases(),'C3':c3.make_cases(),'C4':c4.make_cases()}
    ladders={'C1A':c1.LADDER,'C2':c2.LADDER,'C3':c3.LADDER,'C4':c4.LADDER}
    frozen=check_frozen_files();summaries={k:validate(v,expected[k],ladders[k]) for k,v in data.items()}
    for plan,name in [('C3','calibration_position_run.json'),('C4','calibration_normalized_run.json')]:
        run=json.loads((ROOT/'out'/name).read_text());assert not run['timed_out'] and not run['unprocessed'];assert run['completed_cases']==len(expected[plan]);summaries[plan]['run']=run
    with (ROOT/'out/calibration_c1a_all.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(data['C1A'][0]),lineterminator='\n');writer.writeheader();writer.writerows(data['C1A'])
    summary={'label':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','integrity_status':'consistent',
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform()},
        'plans':summaries,'frozen_hashes':frozen,'angle_kernel_checks':angle_check(),
        'point_checks':point_checks(data),'replay':{'skipped':True} if args.skip_replay else replay(data),
        'budget':costs(data['C3']),
        'unprocessed_domain':{
          'shape':'R minus the union of recorded positive shape-position boxes; a positive projected shape box does not cover every position.',
          'G3':'For each m in {123,13,23}, (R x D_m) minus the union of positive C1A,C2,C3 boxes and positive C4 collars (q3>0).',
          'D12':'(R x D_12) minus the union of positive C1A,C2,C3 D12 boxes. The tested direct q1 collar remains unresolved.',
          'q3_zero':'The H33 continuation at q3=0 is a value of extended G3, not a nonzero E3 on that plane.',
          's_one':'Some C2 positive finite shape boxes include s=1 by the factored D12 extension. The rest of the symmetric edge and its neighborhood remain unprocessed.',
          'boundary':'Sixteen finite boundary patches were positive, but the remainder of the sphere boundary was not covered.',
          'axes':'q1*q2=0, center, coordinate axes and untested collars remain assigned to analytical or separate interval work.'}}
    (ROOT/'out/calibration_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'label':summary['label'],'integrity_status':'consistent','plans':summaries},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
