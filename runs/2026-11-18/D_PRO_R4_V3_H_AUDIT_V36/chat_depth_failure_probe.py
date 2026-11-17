"""chat V36 diagnostic: where does Dig's child-(0,0) B4 cover hit DEPTH_LIMIT_A, and is A large there pointwise?
Same initial patches, same split rule and depth-first order as v35_w_b4_cover.py (reimplemented driver, their majorant)."""
import sys, itertools
sys.path.insert(0, sys.argv[1])
from flint import fmpq as Q, ctx
import stage0 as S, majorant as M, v35_w_split_preflight as V
ctx.prec = 128
f = lambda x: int(x.p)/int(x.q)
H=(-Q(1),Q(0),Q(1,2),Q(3,4),Q(7,8),Q(15,16),Q(31,32),Q(63,64),Q(127,128),Q(1)); VV=(Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)); WW=(Q(0),Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1))
def split(cell):
    L=[(b-a)/(Q(2) if i==0 else Q(1)) for i,(a,b) in enumerate(cell)]; ax=max(range(3),key=lambda i:L[i]); a,b=cell[ax]; m=(a+b)/2
    return [tuple(cell[:ax])+((a,m),)+tuple(cell[ax+1:]), tuple(cell[:ax])+((m,b),)+tuple(cell[ax+1:])]
V.configure(V.RBOUNDS[0], V.TBOUNDS[0])
pending=[(tuple((arr[i],arr[i+1]) for arr,i in zip((H,VV,WW),idx)),0) for idx in itertools.product(range(9),range(4),range(5))]
while pending:
    cell,d=pending.pop(); m=M.majorant(cell)
    if not m["convergent"] or m["A"]>Q(1,4):
        if d>=16:
            print("DEPTH_LIMIT cell:", [(str(a),str(b)) for a,b in cell], "A(cell)=", f(m["A"]), "convergent", m["convergent"])
            for corner in itertools.product(*cell):
                mp_=M.majorant(tuple((c,c) for c in corner)); print("  corner", [str(c) for c in corner], "A=", f(mp_["A"]))
            break
        pending.extend((c,d+1) for c in split(cell))
