"""B7 V5 producer: V4.1 search, proved F>=-275/4 contact and K floor.

NOT an independent verifier. Frozen v4.1 sources are not changed.
"""
import argparse, concurrent.futures, hashlib, heapq, json, os, pickle, time, math
from fractions import Fraction as Q
from pathlib import Path
from v3_fixed_128 import I,iv,S,mulq_interval
from v6_b7_priority_128 import YEDGES,PEDGES,intervals,contact,prefactor_lower,encode_cell
from v6_b7_adaptive_128 import bisect,choose
from v6_b7_safe_128 import centered_main,kernel
from v6_b7_hybrid_128 import main_interval
from v6_b7_delta_local_128 import split_geometric
from b7_constants_v5 import KQ, P0, SIGMA0

SOURCES=('v3_fixed_128.py','v6_b_ad2_128.py','v6_b7_safe_128.py','v6_b7_adaptive_128.py','v6_b7_priority_128.py','v6_b7_hybrid_128.py','v6_b7_unified_outerrem_v5.py','v6_b7_delta_local_128.py','b7_constants_v3.py','b7_constants_v5.py')
def fingerprint():
    h=hashlib.sha256()
    for name in SOURCES:
        h.update(name.encode());h.update((Path(__file__).parent/name).read_bytes())
    return h.hexdigest()
def deltas():
    return [(Q(3,10**8),Q(1,10**4)),(Q(1,10**4),Q(1,10**2)),(Q(1,10**2),Q(1,25)),(Q(1,25),Q(4,25)),(Q(4,25),Q(15,64))]
def boxes():
    for k,d in enumerate(deltas()):
        for i,l in enumerate(intervals([Q(2,5),Q(173,400),Q(93,200)])):
            for j,t in enumerate(intervals([Q(7,8)+Q(n,32) for n in range(5)])):
                yield f'L{i}_T{j}_D{k}',(l,t,d)
def atomic(path,obj,as_json=False):
    tmp=path.with_name(path.name+'.tmp')
    with open(tmp,'w' if as_json else 'wb') as f:
        if as_json:json.dump(obj,f,indent=2,sort_keys=True)
        else:pickle.dump(obj,f,protocol=4)
        f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
# The integrated domain and the discarded contact strip share one P0.
P_CUT=P0
SIGMA_CUT=SIGMA0
P_CUT_EDGES=[P_CUT]+[p for p in PEDGES if p>P_CUT]
def contact_cut(outer):
    return 2*outer[0][1]*KQ*SIGMA_CUT

def geometric_edges(edges,n=4,width_cap=None):
    # Rational geometry; floating logarithm only estimates a partition count.
    result=[edges[0]]
    for a,b in intervals(edges):
        if a==0:
            result.append(b)
            continue
        ratio=float(b/a)
        count=max(1,math.ceil(n*math.log10(ratio)-1e-12))
        if width_cap is not None:
            count=max(count,(b-a).__ceil__() if width_cap==1 else math.ceil(float((b-a)/width_cap)))
        # Geometric interpolation via exact rational bisection, preserving endpoints.
        def root(x,k):
            lo,hi=a,b
            for _ in range(64):
                mid=(lo+hi)/2
                if mid**count*b**(0) < a**(count-k)*b**k:lo=mid
                else:hi=mid
            return (lo+hi)/2
        for k in range(1,count):
            x=root(a,k)
            if result[-1]<x<b:result.append(x)
        result.append(b)
    if width_cap is not None:
        refined=[result[0]]
        for a,b in intervals(result):
            pieces=max(1,math.ceil((b-a)/width_cap))
            refined.extend(a+(b-a)*Q(j,pieces) for j in range(1,pieces+1))
        result=refined
    return result

def inner_grid_v2():
    ye=geometric_edges(YEDGES)
    pe=geometric_edges(P_CUT_EDGES,width_cap=Q(1,8))
    for y in intervals(ye):
        for p in intervals(pe):
            for ti in range(4):
                for ui in range(4):
                    yield (y,p,(Q(ti,4),Q(ti+1,4)),(Q(ui,4),Q(ui+1,4)))

def grid_count():
    return (len(geometric_edges(YEDGES))-1)*(len(geometric_edges(P_CUT_EDGES,width_cap=Q(1,8)))-1)*16

def k_floor_raw(cell):
    # Conditional on F>=-KQ in the sigma,beta,y,u integral normalization.
    (ya,yb),(pa,pb),(ta,tb),(ua,ub)=cell
    sigma=lambda p:2*p/(1+p*p)
    ds=sigma(pb)-sigma(pa)
    db=2*(tb-ta)/(1+ta*ta)  # derivative bound on t>=0
    q=-2*KQ*ds*db*(yb-ya)*(ub-ua)
    return (q*S).__floor__()  # outward lower rounding to 2^-128

def lambda_tau_boxes(delta_boxes,outer_parts):
    # Partition only universal outer parameters. Never add separate-box values.
    from v6_b7_hybrid_128 import partition
    for delta_box in delta_boxes:
        for la in partition(delta_box[0],outer_parts):
            for ta in partition(delta_box[1],outer_parts):
                yield (la,ta,delta_box[2])

def rem_cache_group(cache,number_of_delta_boxes,n):
    # Per-delta-group hull of lambda/tau second derivative enclosures.
    rows=[]
    for j in range(number_of_delta_boxes):
        group=cache[j*n*n:(j+1)*n*n]
        rows.append([I.raw(min(row[i].lo for row in group),
                           max(row[i].hi for row in group)) for i in range(4)])
    return rows

def delta_critical_box(cell,boxes,cache):
    # Cache contains exact outward-rounded unscaled derivative intervals.
    vol=Q(1)
    for a,b in cell:vol*=b-a
    scores=[0]*len(boxes)
    for i in range(4):
        lows=[row[i].lo for row in cache]
        m=min(lows)
        q=vol*(cell[i][1]-cell[i][0])**2/Q(24)
        for j,x in enumerate(lows):
            if x==m:scores[j]+=max(0,-m)*q
    for j in sorted(range(len(boxes)),key=lambda k:(scores[k],-k),reverse=True):
        if split_geometric(boxes[j]) is not None:return j
    return None

def worker(job):
    key,outer,mode,limit,depth,outdir,every,fp,max_parts,max_delta,max_rem_parts,max_rem_kernel_boxes,grid_far=job
    out=Path(outdir);result=out/(key+'_'+mode+'.json');ckpt=out/(key+'_'+mode+'.checkpoint')
    leaf_path=out/(key+'_'+mode+'.leaves.json')
    cfg={'key':key,'outer':encode_cell(outer),'mode':mode,'limit':limit,'depth':depth,'max_parts':list(max_parts),'max_delta':max_delta,'grid_count':grid_count(),'p_cut':str(P_CUT),'sigma_cut':str(SIGMA_CUT),'bound_policy':'max_midpoint_K_floor_zeroth_outerrem_v5_Astra_F_ge_minus_275_over_4','max_rem_parts':max_rem_parts,'max_rem_kernel_boxes':max_rem_kernel_boxes,'grid_far':grid_far,'KQ':str(KQ),'fingerprint':fp}
    if result.exists():
        prior=json.loads(result.read_text())
        if prior.get('config')==cfg and prior.get('status') in ('PASS','DIAGNOSTIC_POSITIVE','LIMIT_REACHED','DOMAIN_FAIL'):
            if not leaf_path.exists():raise RuntimeError('result exists but leaf audit file is missing: '+str(leaf_path))
            digest=hashlib.sha256(leaf_path.read_bytes()).hexdigest()
            if digest!=prior.get('leaf_file_sha256'):raise RuntimeError('leaf audit file checksum mismatch: '+str(leaf_path))
            return key,'SKIPPED',prior.get('final_lower')
        raise RuntimeError('existing result has incompatible configuration: '+str(result))
    t0=time.monotonic()
    if ckpt.exists():
        saved=pickle.loads(ckpt.read_bytes())
        if saved['config']!=cfg:raise RuntimeError('checkpoint configuration mismatch: '+str(ckpt))
        state=saved['state']
    else:
        state={'active':{},'heap':[],'serial':0,'evaluations':0,'main_evaluations':0,'splits':0,
               'outer_refinements':0,'delta_refinements':0,'counts':[0]*4,'main_lo':0,'rem_lo':[0]*4,
               'total_lo':0,'zeroth_lo':0,'initialized':False,'init_cursor':0,'initialization_seconds':0.0,'kernel_evaluation_calls':0,'outerrem_refinements':0}
    active=state['active'];heap=state['heap']
    def volume(cell):
        v=Q(1)
        for a,b in cell:v*=b-a
        return v
    def main_scaled(cell,parts):
        state['main_evaluations']+=1
        return mulq_interval(main_interval(outer,cell,parts),volume(cell))
    def derivative_row(sub,cell):
        # Five enclosures from the original eight AD2 calls.
        # row[0:4] are directional d2, row[4] is the same kernel's
        # two-sheet value enclosure for the whole cell/outer subbox.
        row=[]; zeroth=iv(0)
        for i in range(4):
            h=iv(0)
            for e in (1,-1):
                k=kernel(sub,cell,e,('inner',i))
                h=h+k.d2
                if i==0:zeroth=zeroth+k.v
                state['kernel_evaluation_calls']+=1
            row.append(h)
        return row+[zeroth]
    def remainder_from_cache(cell,cache):
        result=[]
        v=volume(cell)
        for i in range(4):
            lo=min(row[i].lo for row in cache)
            hi=max(row[i].hi for row in cache)
            result.append(mulq_interval(I.raw(lo,hi),v*(cell[i][1]-cell[i][0])**2/Q(24)))
        return result
    def zeroth_from_cache(cell,cache):
        # All outer subboxes are universal, not independent integral parts.
        # Take their hull, then integrate a constant lower bound over K.
        v=volume(cell)
        return mulq_interval(
            I.raw(min(row[4].lo for row in cache),
                  max(row[4].hi for row in cache)),v)
    def select_lower(main,rem,zeroth,floor_raw):
        midpoint=main+sum(rem,iv(0))
        # Stable tie order preserves V3: K floor, then midpoint, then zeroth.
        source,lower=max((('K_FLOOR',floor_raw),
                          ('MIDPOINT',midpoint.lo),
                          ('ZEROTH',zeroth.lo)),key=lambda entry:entry[1])
        return lower,source,midpoint
    def evaluate(cell,d,parts,delta_boxes=None,precomputed=None,pre_rem=None,pre_cache=None,rem_parts=1,pre_zeroth=None):
        if delta_boxes is None:delta_boxes=[outer]
        expected_boxes=len(delta_boxes)*rem_parts*rem_parts
        if expected_boxes>max_rem_kernel_boxes:
            raise ValueError('derivative box budget exceeded')
        if pre_cache is not None and len(pre_cache)!=expected_boxes:
            raise ValueError('cached derivative rows do not match lambda/tau/delta geometry')
        cache=pre_cache if pre_cache is not None else [derivative_row(sub,cell) for sub in lambda_tau_boxes(delta_boxes,rem_parts)]
        if any(len(row)!=5 for row in cache):
            raise ValueError('V4 derivative cache requires 4 d2 enclosures plus zeroth value')
        main=precomputed if precomputed is not None else main_scaled(cell,parts)
        rem=pre_rem if pre_rem is not None else remainder_from_cache(cell,cache)
        zeroth=pre_zeroth if pre_zeroth is not None else zeroth_from_cache(cell,cache)
        axis=choose(rem,cell)
        next_parts=tuple(min(m,2*n) for n,m in zip(parts,max_parts))
        can_delta=(len(delta_boxes)<max_delta and
                   (len(delta_boxes)+1)*rem_parts*rem_parts<=max_rem_kernel_boxes)
        can_outerrem=(rem_parts<max_rem_parts and
                      len(delta_boxes)*min(max_rem_parts,2*rem_parts)**2<=max_rem_kernel_boxes)
        main_width=max(0,main.hi-main.lo) if next_parts!=parts else 0
        rem_width=sum(max(0,r.hi-r.lo) for r in rem) if (can_delta or can_outerrem) else 0
        zeroth_width=max(0,zeroth.hi-zeroth.lo)
        inner_score=3*max(0,-rem[axis].lo)//4 if d<depth else 0
        floor_raw=k_floor_raw(cell)
        selected,source,midpoint=select_lower(main,rem,zeroth,floor_raw)
        score=max(inner_score,main_width,rem_width,zeroth_width)
        if source!='MIDPOINT':score=min(score,abs(selected))
        return {'cell':cell,'depth':d,'parts':parts,'delta_boxes':delta_boxes,'rem_parts':rem_parts,'derivative_cache':cache,
                'main':main,'rem':rem,'midpoint':midpoint,'zeroth':zeroth,'k_floor_raw':floor_raw,
                'bound_source':source,'total_lo_selected':selected,'total':midpoint,
                'axis':axis,'score':score,'next_parts':next_parts,
                'inner_score':inner_score,'main_width':main_width,'rem_width':rem_width,'zeroth_width':zeroth_width}
    def insert(cell,d,parts=(1,1,1),delta_boxes=None,precomputed=None,pre_rem=None,pre_cache=None,rem_parts=1,pre_zeroth=None,pre_leaf=None):
        uid=state['serial'];state['serial']+=1
        leaf=pre_leaf if pre_leaf is not None else evaluate(cell,d,parts,delta_boxes,precomputed,pre_rem,pre_cache,rem_parts,pre_zeroth)
        state['evaluations']+=1
        active[uid]=leaf
        state['main_lo']+=leaf['main'].lo;state['zeroth_lo']+=leaf['zeroth'].lo;state['total_lo']+=leaf['total_lo_selected']
        for i in range(4):state['rem_lo'][i]+=leaf['rem'][i].lo
        if leaf['score']>0:heapq.heappush(heap,(-leaf['score'],uid))
    def remove(uid):
        old=active.pop(uid)
        state['main_lo']-=old['main'].lo;state['zeroth_lo']-=old['zeroth'].lo;state['total_lo']-=old['total_lo_selected']
        for i in range(4):state['rem_lo'][i]-=old['rem'][i].lo
        return old
    def checkpoint():atomic(ckpt,{'config':cfg,'state':state})
    if not state['initialized']:
        if mode=='full':cells=inner_grid_v2()
        else:cells=[((Q(1,10),Q(1,5)),(Q(3,10),Q(2,5)),(Q(1,4),Q(3,8)),(Q(1,4),Q(3,8)))]
        # Deterministic replay of geometry for partially initialized grids.
        init_start=time.monotonic()
        for idx,c in enumerate(cells):
            if idx<state['init_cursor']:continue
            insert(c,0);state['init_cursor']=idx+1
            if state['init_cursor']%every==0:checkpoint()
        state['initialization_seconds']+=time.monotonic()-init_start
        state['initialized']=True;checkpoint()
    loss=contact_cut(outer)
    def value():
        q=Q(state['total_lo'],S)
        return q if mode=='representative' else prefactor_lower(q,outer)-loss
    status='LIMIT_REACHED'
    if value()>0:status='PASS'
    while status!='PASS' and heap:
        # Strict stop: never spend unlimited outer work after reaching leaf cap.
        if len(active)>=limit:break
        _,uid=heapq.heappop(heap)
        if uid not in active:continue
        old=active[uid]
        can_inner=old['depth']<depth and len(active)<limit
        can_outer=old['next_parts']!=old['parts']
        can_delta=(len(old['delta_boxes'])<max_delta and
                   (len(old['delta_boxes'])+1)*old['rem_parts']**2<=max_rem_kernel_boxes)
        can_outerrem=(old['rem_parts']<max_rem_parts and len(old['delta_boxes'])*min(max_rem_parts,2*old['rem_parts'])**2<=max_rem_kernel_boxes)
        choices=[]
        if can_outer:
            candidate=main_scaled(old['cell'],old['next_parts'])
            lower,_,_=select_lower(candidate,old['rem'],old['zeroth'],old['k_floor_raw'])
            choices.append(('outer',max(0,lower-old['total_lo_selected']),candidate,old['rem'],old['zeroth']))
        if can_delta:
            boxes=list(old['delta_boxes'])
            groups=rem_cache_group(old['derivative_cache'],len(boxes),old['rem_parts'])
            j=delta_critical_box(old['cell'],boxes,groups)
            if j is not None:
                pair=split_geometric(boxes[j])
                if pair is not None:
                    boxes[j:j+1]=pair
                    cache=list(old['derivative_cache'])
                    n=old['rem_parts']
                    cache[j*n*n:(j+1)*n*n]=[derivative_row(sub,old['cell']) for sub in lambda_tau_boxes(pair,n)]
                    rem=remainder_from_cache(old['cell'],cache)
                    z=zeroth_from_cache(old['cell'],cache)
                    lower,_,_=select_lower(old['main'],rem,z,old['k_floor_raw'])
                    choices.append(('delta',max(0,lower-old['total_lo_selected']),(boxes,cache),rem,z))
        if can_outerrem:
            # Same eight AD2 kernel calls per newly evaluated subbox as V3.
            n=min(max_rem_parts,2*old['rem_parts'])
            rcache=[derivative_row(sub,old['cell']) for sub in lambda_tau_boxes(old['delta_boxes'],n)]
            rnew=remainder_from_cache(old['cell'],rcache)
            z=zeroth_from_cache(old['cell'],rcache)
            lower,_,_=select_lower(old['main'],rnew,z,old['k_floor_raw'])
            choices.append(('outerrem',max(0,lower-old['total_lo_selected']),(n,rcache),rnew,z))
        if can_inner:
            # Unlike V3's inner heuristic, use ACTUAL three-way selected
            # lower bounds of both prospective children. These calculations
            # are trials: cache their leaf structures if inner is chosen.
            lc,rc=bisect(old['cell'],old['axis'])
            lval=evaluate(lc,old['depth']+1,old['parts'],old['delta_boxes'],rem_parts=old['rem_parts'])
            rval=evaluate(rc,old['depth']+1,old['parts'],old['delta_boxes'],rem_parts=old['rem_parts'])
            lower=lval['total_lo_selected']+rval['total_lo_selected']
            choices.append(('inner',max(0,lower-old['total_lo_selected']),(lc,rc,lval,rval),None,None))
        if not choices:continue
        action,gain,arg,rem,z=max(choices,key=lambda entry:entry[1])
        if gain<=0:continue
        remove(uid)
        if action=='inner':
            lc,rc,lval,rval=arg
            insert(lc,old['depth']+1,old['parts'],old['delta_boxes'],rem_parts=old['rem_parts'],pre_leaf=lval)
            insert(rc,old['depth']+1,old['parts'],old['delta_boxes'],rem_parts=old['rem_parts'],pre_leaf=rval)
            state['counts'][old['axis']]+=1;state['splits']+=1
        elif action=='outer':
            insert(old['cell'],old['depth'],old['next_parts'],old['delta_boxes'],arg,old['rem'],old['derivative_cache'],rem_parts=old['rem_parts'],pre_zeroth=z)
            state['outer_refinements']+=1
        elif action=='delta':
            insert(old['cell'],old['depth'],old['parts'],arg[0],old['main'],rem,arg[1],rem_parts=old['rem_parts'],pre_zeroth=z)
            state['delta_refinements']+=1
        elif action=='outerrem':
            insert(old['cell'],old['depth'],old['parts'],old['delta_boxes'],old['main'],rem,arg[1],rem_parts=arg[0],pre_zeroth=z)
            state['outerrem_refinements']+=1
        if (state['splits']+state['outer_refinements']+state['delta_refinements']+state['outerrem_refinements'])%every==0:checkpoint()
        if value()>0:status='PASS'
    if mode=='representative' and status=='PASS':status='DIAGNOSTIC_POSITIVE'
    data={'status':status,'config':cfg,'leaves':len(active),'evaluations':state['evaluations'],
          'main_evaluations':state['main_evaluations'],'splits':state['splits'],
          'outer_refinements':state['outer_refinements'],
          'delta_refinements':state['delta_refinements'],
          'outerrem_refinements':state['outerrem_refinements'],
          'initial_cells':grid_count() if mode=='full' else 1,
          'initialization_seconds':state['initialization_seconds'],
          'remainder_kernel_evaluation_calls':state['kernel_evaluation_calls'],
          'priority_rule':'V4.1 retained: 3-way selected gain; cached child candidates; non-MIDPOINT heap score capped by abs(selected); zero-gain leaves can leave queue',
          'split_counts':dict(zip('yptu',state['counts'])),
          'main_lower':str(Q(state['main_lo'],S)),
          'zeroth_lower':str(Q(state['zeroth_lo'],S)),
          'remainder_lower':{x:str(Q(r,S)) for x,r in zip('yptu',state['rem_lo'])},
          'total_lower':str(Q(state['total_lo'],S)),
          'total_lower_semantics':'sum max(midpoint.lower,K_floor.lower,zeroth.lower) per leaf; main/remainder/zeroth separately diagnostic', 'contact_loss_upper':str(loss),
          'final_lower':str(value()),'seconds_this_invocation':time.monotonic()-t0,
          'diagnostic_only':mode=='representative'}
    # Keep every final inner leaf for an independent E1/Q-LB/L2 kernel audit.
    # Raw endpoints are exact integer multiples of 2^-128, not rounded decimals.
    def interval_record(v):return {'lo':str(v.lo),'hi':str(v.hi)}
    leaf_records=[]
    for uid,leaf in sorted(active.items()):
        leaf_records.append({'uid':uid,'cell':encode_cell(leaf['cell']),
                             'depth':leaf['depth'],'outer_parts':list(leaf['parts']),
                             'delta_boxes':[encode_cell(b) for b in leaf['delta_boxes']],
                             'rem_parts':leaf['rem_parts'],
                             'main':interval_record(leaf['main']),
                             'zeroth':interval_record(leaf['zeroth']),
                             'remainder':{a:interval_record(v) for a,v in zip('yptu',leaf['rem'])},
                             'total':interval_record(leaf['total']),
                             'k_floor_raw':str(leaf['k_floor_raw']),
                             'selected_lower_raw':str(leaf['total_lo_selected']),
                             'bound_source':leaf['bound_source']})
    leaf_data={'schema':'V6-B7-LEAVES-v2','scale_denominator':str(S),
               'config':cfg,'status':status,'leaves':leaf_records,
               'aggregate_raw':{'main_lower':str(state['main_lo']),
                                'zeroth_lower':str(state['zeroth_lo']),
                                'remainder_lower':{a:str(v) for a,v in zip('yptu',state['rem_lo'])},
                                'total_lower':str(state['total_lo'])},
               'contact_loss_upper':str(loss),'final_lower':str(value())}
    atomic(leaf_path,leaf_data,True)
    data['leaf_file']=leaf_path.name
    data['leaf_file_sha256']=hashlib.sha256(leaf_path.read_bytes()).hexdigest()
    data['leaf_schema']='V6-B7-LEAVES-v2'
    atomic(result,data,True);ckpt.unlink(missing_ok=True)
    return key,status,data['final_lower']
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=('representative','full'),default='representative')
    ap.add_argument('--workers',type=int,default=1)
    ap.add_argument('--max-leaves',type=int,default=32)
    ap.add_argument('--max-depth',type=int,default=12)
    ap.add_argument('--checkpoint-every',type=int,default=20)
    ap.add_argument('--outer-limit',type=int,default=0,help='0 means all selected outer boxes (default all 40)')
    ap.add_argument('--keys',default=None,help='comma-separated outer box keys; if omitted all 40 boxes are selected')
    ap.add_argument('--out-dir',default='v6_b7_hybrid_runs')
    ap.add_argument('--max-parts',default='2,2,4')
    ap.add_argument('--max-delta-boxes',type=int,default=16)
    ap.add_argument('--max-rem-parts',type=int,choices=(1,2,4),default=4)
    ap.add_argument('--max-rem-kernel-boxes',type=int,default=32,help='budget on product of lambda*tau and delta boxes')
    ap.add_argument('--grid-far',action='store_true',help='reserved; not yet implemented')
    args=ap.parse_args()
    parts=tuple(int(x) for x in args.max_parts.split(','))
    if len(parts)!=3 or any(x<1 for x in parts):raise ValueError('invalid max-parts')
    if args.max_delta_boxes<1 or args.max_rem_kernel_boxes<1:raise ValueError('invalid outer-box budget')
    if args.grid_far:raise NotImplementedError('selective far grid pending separate audit')
    if args.workers<1 or args.max_leaves<1 or args.max_depth<0 or args.checkpoint_every<1:raise ValueError('invalid limits')
    if args.mode=='full' and args.max_leaves<grid_count():raise ValueError(f'full mode needs at least {grid_count()} leaves')
    Path(args.out_dir).mkdir(parents=True,exist_ok=True)
    if args.outer_limit < 0:raise ValueError('outer-limit must be nonnegative')
    all_boxes=dict(boxes())
    if args.keys is None:
        selected_keys=list(all_boxes)
    else:
        if args.outer_limit:raise ValueError('--keys and positive --outer-limit cannot be combined')
        selected_keys=[key.strip() for key in args.keys.split(',')]
        if not selected_keys or any(not key for key in selected_keys):
            raise ValueError('--keys requires a nonempty comma-separated key list')
        if len(selected_keys)!=len(set(selected_keys)):
            raise ValueError('duplicate keys are not allowed')
        unexpected=[key for key in selected_keys if key not in all_boxes]
        if unexpected:
            raise ValueError('unknown outer box key(s): '+','.join(unexpected))
    if args.outer_limit>0:selected_keys=selected_keys[:args.outer_limit]
    jobs=[(key,all_boxes[key],args.mode,args.max_leaves,args.max_depth,args.out_dir,args.checkpoint_every,fingerprint(),parts,args.max_delta_boxes,args.max_rem_parts,args.max_rem_kernel_boxes,args.grid_far) for key in selected_keys]
    if args.workers==1:rows=[worker(j) for j in jobs]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
            rows=list(pool.map(worker,jobs))
    for row in rows:print(*row,flush=True)
    records=[json.loads((Path(args.out_dir)/(j[0]+'_'+args.mode+'.json')).read_text()) for j in jobs]
    selection_pass=all(r['status']=='PASS' for r in records) and args.mode=='full'
    covers_all_40=set(selected_keys)==set(all_boxes) and len(selected_keys)==40
    summary={'outer_boxes_processed':len(records),
             'selected_keys':selected_keys,
             'covers_all_40':covers_all_40,
             'status_counts':{s:sum(r['status']==s for r in records) for s in sorted({r['status'] for r in records})},
             'minimum_final_lower':str(min(Q(r['final_lower']) for r in records)),
             'all_pass':selection_pass,
             'global_all_pass':selection_pass and covers_all_40,
             'aggregation':'MIN outer; SUM inner','fingerprint':fingerprint()}
    atomic(Path(args.out_dir)/'summary.json',summary,True)
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
