"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Generate outward dyadic bounds used by chord_box.cpp."""
import sys
from flint import arb, ctx, fmpq

ctx.prec = 144
Q = 1 << 24
G = 2048
M = 16


def lo(x):
    v=(Q*x).lower().fmpq()
    return int(v.p)//int(v.q)


def hi(x):
    v=(Q*x).upper().fmpq()
    return -((-int(v.p))//int(v.q))


def unit_interval(x):
    a,b=max(0,lo(x)), min(Q,hi(x))
    assert a<=b
    return [a,b]


def main(path):
    aa=[fmpq(1)]
    for k in range(M+1):
        aa.append(aa[-1]*fmpq(2*k+2,2*k+3))
    qb=[(4+2*k)*aa[k]-(k+1)*aa[k+1] for k in range(M+1)]
    with open(path,"w") as f:
        print("# DIAGNOSTIC_ONLY / NOT_EVIDENCE",file=f)
        print(Q,G,file=f)
        for i in range(G+1):
            h=arb(fmpq(G-i,2*G))
            upper=2*sum(arb(aa[k])*h**k for k in range(M+1))+4*h**(M+1)
            lower=sum(arb(qb[k])*h**k for k in range(M+1))
            print(hi(upper),lo(lower),file=f)
        for n in (1,2,4,8,16,32,64,128):
            for i in range(n):
                a,b=arb.pi()*i/(2*n),arb.pi()*(i+1)/(2*n)
                ca,cb,sa,sb=a.cos(),b.cos(),a.sin(),b.sin()
                width=arb.pi()/(2*n)
                moments=[arb(1),(sb-sa)/width]
                for k in (2,3,4):
                    moments.append((sb*cb**(k-1)-sa*ca**(k-1))/(k*width)
                                   +fmpq(k-1,k)*moments[k-2])
                mean=moments[1]
                var=moments[2]-mean**2
                d0=1-moments[2]
                mean_w=(mean-moments[3])/d0
                var_w=(moments[2]-moments[4])/d0-mean_w**2
                vals=[max(0,lo(cb)),min(Q,hi(ca)),max(0,lo(sa**2)),min(Q,hi(sb**2))]
                for x in (mean,var,d0,mean_w,var_w):
                    vals.extend(unit_interval(x))
                print(n,i,*vals,file=f)


if __name__ == "__main__":
    main(sys.argv[1])
