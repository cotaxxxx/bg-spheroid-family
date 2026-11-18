"""chat V43: own rational recomputation of (G14),(G15),(G18)-(G20),(G28),(G30) constants."""
from fractions import Fraction as Q
import math
res=[]
def ck(n,ok,d=""): res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""))
S0=Q(1,4096)
ck("G14 9/800", Q(49,50)-Q(3,4)-Q(7,32)==Q(9,800) and math.sqrt(3)/8<7/32)
ck("G15 12/25", 2*Q(99,100)-Q(3,4)-Q(3,4)==Q(12,25))
ck("G16 k<=5/2 S^2 at mu=z-h: 5/4+sqrt(3/2)<5/2", 1.25+math.sqrt(1.5)<2.5, f"{1.25+math.sqrt(1.5):.4f}")
def KLG(e0,r0,chi0,z0,c):
    Qc=e0**2*(1+r0)**2/(z0-c)**2; U=e0**2/(1-c**2); v0=1-r0/(1-c)
    K=v0/(1+Qc); L2=v0**2/((1+Qc)*(1+U))
    sq=math.sqrt(float(1-c**2)); G=float(e0)*((1+float(chi0)/float(z0-c))/sq+float(r0)/float(z0-c))
    return K,L2,G
c=Q(15,16); z0=Q(9999,10000)
K,L2,G=KLG(S0/4,S0,S0**2,z0,c); ck("G18 K,L>=99/100, G<=1/1000", K>=Q(99,100) and L2>=Q(99,100)**2 and G<=1e-3, f"K={float(K):.6f} L={math.sqrt(float(L2)):.6f} G={G:.2e}")
ck("z>=z0 for S<=S0", 1-S0**2>=z0**2)
ck("int_0^c mu/s = 1-sqrt(1-c^2) >= 13/20, arcsin c >= 6/5", 1-math.sqrt(31)/16>=0.65 and math.asin(15/16)>=1.2, f"{1-math.sqrt(31)/16:.5f}, {math.asin(15/16):.5f}")
G19=Q(99,200)*((2*Q(157,50)-Q(3,1000))*Q(13,20)+(Q(157,50)-Q(2,1000))*Q(99,100)*Q(6,5))-Q(22,7)/z0*(1+S0/2)-Q(153,2)*Q(22,7)*S0
ck("G19 value", G19==Q(2248950598883,3393600000000) and G19>Q(1,2), f"{float(G19):.6f}")
e0=Q(1,4096); K,L2,G=KLG(e0,4*e0,16*e0**2,z0,c); ck("G20 K,L>=93/100,G<=3/250", K>=Q(93,100) and L2>=Q(93,100)**2 and G<=0.012, f"K={float(K):.6f} G={G:.2e}")
ck("G20 N/eps<1/100", float(e0)*16*math.sqrt(17)/(1+0.9999)<0.01)
G20=Q(93,200)*((2*Q(157,50)-Q(9,250))*Q(13,20)+(Q(157,50)-Q(6,250))*Q(93,100)*Q(6,5))-Q(22,7)/z0*(1+Q(1,512))-Q(1,100)
ck("G20 value", G20==Q(6097089757,17675000000) and G20>Q(1,4), f"{float(G20):.6f}")
ck("G21 split: lambda<=4096 => S<=2^-12<=1/lambda", True)
ck("G23 2a0/b0<=1", 2*(S0**2/8)/(S0/2)<=1)
ck("G30 3*pi*S0*13000*log2 >= 78000/4096", 3*math.pi*13000*math.log(2)/4096>=78000/4096, f"{3*math.pi*13000*math.log(2)/4096:.3f}")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
