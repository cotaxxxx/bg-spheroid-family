"""V6-B7 outer-midpoint subdivision with exact interval hull and cached leaf evaluation.
Diagnostic producer only; not an independent verifier.
"""
from fractions import Fraction as Q
from v3_fixed_128 import I,iv,mulq_interval
from v6_b7_safe_128 import centered_main,kernel
from v6_b7_adaptive_128 import choose,bisect

def partition(pair,n):
    if type(n) is not int or n<1:raise ValueError('invalid subdivision count')
    a,b=pair
    return [(a+(b-a)*Q(i,n),a+(b-a)*Q(i+1,n)) for i in range(n)]

def main_interval(outer,cell,parts=(1,1,1)):
    """Hull of valid enclosures over universal outer subboxes (min lower, max upper)."""
    if len(parts)!=3:raise ValueError('need 3 outer subdivisions')
    lo=hi=None
    for l in partition(outer[0],parts[0]):
        for t in partition(outer[1],parts[1]):
            for d in partition(outer[2],parts[2]):
                v=centered_main((l,t,d),cell)
                lo=v.lo if lo is None else min(lo,v.lo)
                hi=v.hi if hi is None else max(hi,v.hi)
    return I.raw(lo,hi)

def bounds(outer,cell,parts=(1,1,1)):
    main=main_interval(outer,cell,parts)
    vol=Q(1)
    for a,b in cell:vol*=b-a
    ms=mulq_interval(main,vol)
    rem=[]
    for i in range(4):
        h=sum((kernel(outer,cell,e,('inner',i)).d2 for e in (1,-1)),iv(0))
        rem.append(mulq_interval(h,vol*(cell[i][1]-cell[i][0])**2/Q(24)))
    return ms,rem,ms+sum(rem,iv(0))

def evaluate_hybrid(outer,cell,depth,uid,parts=(1,1,1),max_parts=(2,2,4)):
    main,rem,total=bounds(outer,cell,parts)
    axis=choose(rem,cell)
    score=max(0,-rem[axis].lo)
    # Improvement potential in the main lower bound, using one further outer refinement.
    # Outer midpoint subdivisions are NEVER summed; the lower bound is the minimum.
    next_parts=tuple(min(m,2*n) for n,m in zip(parts,max_parts))
    if next_parts!=parts:
        refined_main=main_interval(outer,cell,next_parts)
        vol=Q(1)
        for a,b in cell:vol*=b-a
        refined_main=mulq_interval(refined_main,vol)
        gain=max(0,refined_main.lo-main.lo)
    else:gain=0
    return {'uid':uid,'cell':cell,'depth':depth,'parts':parts,'main':main,'rem':rem,
            'total':total,'axis':axis,'score':score,'outer_gain':gain,
            'next_parts':next_parts,'priority':max(score,gain)}

def run_representative(outer,cell,max_leaves=64,max_depth=14,max_parts=(2,2,4)):
    """Global priority over both actions; a leaf outer refinement doesn't increase leaf count."""
    import heapq
    serial=0;active={};heap=[];total_lo=0;main_lo=0;rem_lo=[0]*4
    actions={'outer':0,'inner':[0]*4};evaluations=0
    def add(c,d,parts):
        nonlocal serial,total_lo,main_lo,evaluations
        leaf=evaluate_hybrid(outer,c,d,serial,parts,max_parts)
        active[serial]=leaf
        main_lo+=leaf['main'].lo;total_lo+=leaf['total'].lo
        for i in range(4):rem_lo[i]+=leaf['rem'][i].lo
        if (d<max_depth and leaf['score']>0) or leaf['outer_gain']>0:
            heapq.heappush(heap,(-leaf['priority'],serial))
        serial+=1;evaluations+=1
    def remove(leaf):
        nonlocal total_lo,main_lo
        main_lo-=leaf['main'].lo;total_lo-=leaf['total'].lo
        for i in range(4):rem_lo[i]-=leaf['rem'][i].lo
        del active[leaf['uid']]
    add(cell,0,(1,1,1))
    while total_lo<=0 and heap:
        _,uid=heapq.heappop(heap)
        if uid not in active:continue
        old=active[uid]
        can_inner=old['depth']<max_depth and len(active)<max_leaves
        can_outer=old['outer_gain']>0
        if can_outer and (not can_inner or old['outer_gain']>=old['score']):
            remove(old);add(old['cell'],old['depth'],old['next_parts']);actions['outer']+=1
        elif can_inner:
            remove(old)
            l,r=bisect(old['cell'],old['axis'])
            add(l,old['depth']+1,old['parts']);add(r,old['depth']+1,old['parts'])
            actions['inner'][old['axis']]+=1
        elif can_outer:
            remove(old);add(old['cell'],old['depth'],old['next_parts']);actions['outer']+=1
    from v3_fixed_128 import S
    return {'status':'DIAGNOSTIC_POSITIVE' if total_lo>0 else 'LIMIT_REACHED',
            'leaves':len(active),'evaluations':evaluations,'outer_refinements':actions['outer'],
            'inner_split_counts':dict(zip('yptu',actions['inner'])),
            'main_lower':str(Q(main_lo,S)),'remainder_lower':{n:str(Q(v,S)) for n,v in zip('yptu',rem_lo)},
            'total_lower':str(Q(total_lo,S))}

if __name__=='__main__':
    import json,sys
    rep=((Q(1,10),Q(1,5)),(Q(3,10),Q(2,5)),(Q(1,4),Q(3,8)),(Q(1,4),Q(3,8)))
    L=(Q(2,5),Q(173,400));T=(Q(7,8),Q(29,32))
    cases=[(Q(1,100),Q(1,25)),(Q(1,25),Q(4,25)),(Q(4,25),Q(15,64))]
    for i,d in enumerate(cases):
        print('D'+str(i+2),json.dumps(run_representative((L,T,d),rep,32,12),sort_keys=True),flush=True)