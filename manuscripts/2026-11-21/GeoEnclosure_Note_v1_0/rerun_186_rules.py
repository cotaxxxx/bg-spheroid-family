import gzip,glob,subprocess,sys,collections
d,exe=sys.argv[1],sys.argv[2]
leaves=[]
for f in sorted(glob.glob(d+'/E*.tsv.gz')):
    for i,l in enumerate(gzip.open(f,'rt')):
        if i==0: continue
        p=l.rstrip('\n').split('\t')
        if not p[14].startswith('split'): leaves.append((f[-10:-7],p))
inp=''.join(f"E {p[1]} {p[2]} {p[3]} {p[4]} 0 0 {p[8]} {p[9]}\n" for _,p in leaves)
inpT=''.join(f"T {p[1]} {p[2]} {p[3]} {p[4]} 0 0 {p[8]} {p[9]}\n" for _,p in leaves if p[7]=='T')
out=subprocess.run([exe],input=inp,capture_output=True,text=True); print('rc',out.returncode,out.stderr[:200])
outT=subprocess.run([exe],input=inpT,capture_output=True,text=True)
res=[tuple(map(int,l.split())) for l in out.stdout.splitlines()]
resT=iter([tuple(map(int,l.split())) for l in outT.stdout.splitlines()])
A=collections.Counter(); B=collections.Counter(); moved=collections.Counter(); same=0; sameT=0; nT=0; Hneg=0; left=[]
r0=collections.Counter()
for (e,p),(alo,ahi,blo,bhi) in zip(leaves,res):
    orig=p[14]
    if p[7]=='E':
        same+= (alo,ahi,blo,bhi)==tuple(map(int,p[10:14]))
    else:
        t=next(resT); nT+=1; sameT+= t[:2]==tuple(map(int,p[10:12]))
    if ahi<0: Hneg+=1
    A['excluded' if (alo>0 or ahi<0) else 'undecided']+=1
    if alo>0: c='H_positive'
    elif ahi<0: c='H_negative'
    elif bhi<0: c='radial_curvature_negative'
    elif p[7]=='T' and int(p[11])<0: c='fourth_negative'
    else: c='UNDECIDED'
    B[c]+=1; moved[(orig,c)]+=1
    if int(p[3])==0: r0[(orig,c,alo>0)]+=1
print('E-mode leaves reproduced exactly:',same,'of',sum(1 for _,p in leaves if p[7]=='E'))
print('T-mode leaves reproduced exactly:',sameT,'of',nT)
print('rule A',dict(A)); print('rule B',dict(B)); print('moves',dict(moved)); print('Hneg',Hneg); print('rho=0 boxes',dict(r0))
