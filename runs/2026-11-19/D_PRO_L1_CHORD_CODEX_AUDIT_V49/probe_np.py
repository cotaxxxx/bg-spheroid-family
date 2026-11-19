import mpmath as mp
mp.mp.dps=30
def Q(y):
    return 4*mp.quad(lambda t:(2*(1+t*t)+(1-t*t)*y)/((1+t*t)+(1-t*t)*y)**2,[0,1])
def parts(lam):
    l=mp.sqrt(lam**2-1)
    Y=lambda x:(1-(x/l)**2)/2; J=lambda x:(1-(x/l)**2)**2/8
    C=lambda x:1+x*x; U=lambda x:1-1/C(x); qC=lambda x:Q(1/mp.sqrt(C(x)))
    Pc=mp.quad(lambda x:2*(1-Y(x)/C(x))/C(x),[0,1,l]); Pe=mp.quad(lambda x:(1+Y(x)-(Y(x)+J(x))/C(x))/C(x),[0,1,l]); Pp=mp.quad(lambda x:(1+(x/l)**2)*(1-Y(x)/C(x))/C(x),[0,1,l])
    Nc=mp.quad(lambda x:qC(x)*U(x)**2*Y(x)/mp.sqrt(C(x)),[0,1,l]); Ne=mp.quad(lambda x:qC(x)*(1+U(x))**2*J(x)/mp.sqrt(C(x)),[0,1,l]); Np=mp.quad(lambda x:qC(x)*(1+U(x))**2*(x/l)**2*Y(x)/mp.sqrt(C(x)),[0,1,l])
    return Pc,Pe,Pp,Nc,Ne,Np
for lam in [5,8,20]:
    Pc,Pe,Pp,Nc,Ne,Np=parts(lam); l=mp.sqrt(lam**2-1)
    print(lam,'Pc',mp.nstr(Pc,6),'closed',mp.nstr((mp.mpf(3)/2+1/(2*l*l))*mp.atan(l)-1/(2*l),6),'Pe',mp.nstr(Pe,6),'Pp',mp.nstr(Pp,6),'| Nc',mp.nstr(Nc,6),'Ne',mp.nstr(Ne,6),'Np',mp.nstr(Np,6))
    print('   uniform-P minus N:', mp.nstr(3*mp.pi/4-Nc,6), mp.nstr(3*mp.pi/4-Ne,6), mp.nstr(mp.pi/2-Np,6))
