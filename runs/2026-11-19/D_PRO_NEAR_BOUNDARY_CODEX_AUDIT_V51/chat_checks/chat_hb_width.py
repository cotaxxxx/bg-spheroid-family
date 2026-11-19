import sys; sys.path.insert(0,'.')
from chat_vz_check_B import *
from flint import arb, fmpq
lam=arb(fmpq(1998848,2**20)).union(arb(fmpq(2031616,2**20))); e2=1/(lam*lam); L2=lam*lam
NT=int(sys.argv[1]); NP=int(sys.argv[2]); rows=[0.0]*8; tot=arb(0); mid=arb(0)
for i in range(NT):
  for k in range(NP):
    t=(arb(i)+U01)/NT; ph=PI*(arb(k)+U01)/NP
    co=ph.cos(); si=ph.sin(); m2=(1-t*t)*sq(co); j=(1-t*t)*sq(si); C=1+(L2-1)*m2; c=1/C
    B=clip(1-4*(1-e2)*t*t*m2,e2.lower(),1); T=(c/B).sqrt(); g=clip(t*T,0,1)
    v=T*t*t*(P_enc(g)*c*(1-j*c)-Q_enc(g)*j*sq(2-c)); rows[i*8//NT]+=float(v.rad())*2; tot+=arb(v.lower()); mid+=arb(v.mid())
print(NT,NP,'lower',(tot/(NT*NP)).lower(),'mid',float(mid/(NT*NP)),'width by t-octile',[round(r/(NT*NP),5) for r in rows])
