import gzip,sys,glob,collections
from fractions import Fraction as Fr
d=sys.argv[1]; U=1<<20
term=collections.Counter(); allrows=0; area=Fr(0); roots=[]; bad=[]
r0touch=collections.Counter(); r1touch=collections.Counter(); modes=collections.Counter()
Hneg=0; depth=collections.Counter(); nk=collections.Counter()
amb=collections.Counter(); splits=collections.Counter()
for f in sorted(glob.glob(d+'/E*.tsv.gz')):
    rows={}
    for i,l in enumerate(gzip.open(f,'rt')):
        if i==0: continue
        p=l.rstrip('\n').split('\t'); rows[p[0]]=p
    allrows+=len(rows)
    x=rows['x']; roots.append((int(x[1]),int(x[2]),int(x[3]),int(x[4])))
    for k,p in rows.items():
        l0,l1,r0,r1=map(int,p[1:5]); act=p[14]
        kids=[c for c in (k+'0',k+'1') if c in rows]
        if act.startswith('split'):
            if len(kids)!=2: bad.append((f,k,'split without 2 kids')); continue
            a=rows[k+'0']; b=rows[k+'1']
            A=tuple(map(int,a[1:5])); B=tuple(map(int,b[1:5]))
            if act=='splitr':
                m=(r0+r1)//2; ok=(r0+r1)%2==0 and A==(l0,l1,r0,m) and B==(l0,l1,m,r1)
            elif act=='splitl':
                m=(l0+l1)//2; ok=(l0+l1)%2==0 and A==(l0,m,r0,r1) and B==(m,l1,r0,r1)
            else: ok=False
            splits[act]+=1
            if not ok: bad.append((f,k,'bad split '+act))
        else:
            if kids: bad.append((f,k,'terminal with kids'))
            term[act]+=1; modes[(p[7],act)]+=1; area+=Fr((l1-l0)*(r1-r0),U*U)
            depth[len(k)-1]+=1; nk[(p[8],p[9])]+=1
            alo,ahi,blo,bhi=map(int,p[10:14])
            if r0==0: r0touch[(p[7],act)]+=1
            if r1==U: r1touch[(p[7],act)]+=1
            if p[7]=='E' and ahi<0: Hneg+=1
            # sanity of the recorded action against recorded bounds
            if act=='H_positive' and not alo>0: bad.append((f,k,'H_positive but alo<=0'))
            if act=='radial_curvature_negative' and not bhi<0: bad.append((f,k,'curv but bhi>=0'))
            if act=='radial_decreasing' and not ahi<0: bad.append((f,k,'T but ahi>=0'))
            if act=='radial_curvature_negative' and alo>0: amb['curv box where H>0 also holds']+=1
        if k!='x' and k[:-1] not in rows: bad.append((f,k,'orphan'))
roots.sort()
print('files',len(roots),'rows',allrows)
print('roots',[(Fr(a,U),Fr(b,U),Fr(c,U),Fr(e,U)) for a,b,c,e in roots][:3],'...')
print('roots tile lambda:',all(roots[i][1]==roots[i+1][0] for i in range(len(roots)-1)), Fr(roots[0][0],U), Fr(roots[-1][1],U), set((b-a,c,e) for a,b,c,e in roots))
print('terminals',sum(term.values()),dict(term)); print('area',area); print('modes',dict(modes))
print('touch r=0',dict(r0touch)); print('touch r=1',dict(r1touch)); print('H upper<0 boxes',Hneg)
print('splits',dict(splits)); print('depth',sorted(depth.items())); print('n,k',dict(nk)); print('amb',dict(amb)); print('bad',bad[:10],len(bad))
