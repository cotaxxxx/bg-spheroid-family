"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Rectangular mixed Arb Taylor jets. Coefficient alpha is derivative/alpha!.
Series coefficients/tail method reused from the pinned W1 implementation.
"""
from functools import lru_cache
from itertools import product
from math import factorial
from flint import arb, fmpq as Q, ctx
from .intervals import hull, clip

@lru_cache(maxsize=64)
def structure(orders):
    indices = tuple(sorted(product(*(range(n+1) for n in orders)),
                           key=lambda a:(sum(a),a)))
    pos = {a:i for i,a in enumerate(indices)}
    pairs = []
    for a in indices:
        row=[]
        for i,b in enumerate(indices):
            if all(x<=y for x,y in zip(b,a)):
                c=tuple(y-x for x,y in zip(b,a))
                row.append((i,pos[c]))
        pairs.append(tuple(row))
    return indices,pos,tuple(pairs)

class Jet:
    __slots__ = ("orders","c")
    def __init__(self, orders, values):
        self.orders=tuple(orders)
        self.c=tuple(x if isinstance(x,arb) else arb(x) for x in values)
        if len(self.c)!=len(structure(self.orders)[0]):
            raise ValueError("wrong coefficient count")
    @classmethod
    def constant(cls,x,orders,active=None):
        indices,pos,_=structure(tuple(orders))
        c=[arb(0) for _ in indices]; c[0]=arb(x)
        if active is not None:
            a=[0]*len(orders); a[active]=1
            c[pos[tuple(a)]]=arb(1)
        return cls(orders,c)
    def lift(self,x):
        if isinstance(x,Jet):
            if x.orders!=self.orders: raise ValueError("jet shape mismatch")
            return x
        return Jet.constant(x,self.orders)
    def __add__(self,x):
        x=self.lift(x)
        return Jet(self.orders,[a+b for a,b in zip(self.c,x.c)])
    __radd__=__add__
    def __neg__(self):
        return Jet(self.orders,[-x for x in self.c])
    def __sub__(self,x): return self+-self.lift(x)
    def __rsub__(self,x): return self.lift(x)-self
    def __mul__(self,x):
        x=self.lift(x)
        return Jet(self.orders,[sum((self.c[i]*x.c[j] for i,j in row),arb(0))
                               for row in structure(self.orders)[2]])
    __rmul__=__mul__
    def reciprocal(self):
        out=[1/self.c[0]]
        for row in structure(self.orders)[2][1:]:
            out.append(-out[0]*sum((self.c[i]*out[j] for i,j in row if i),arb(0)))
        return Jet(self.orders,out)
    def reciprocal_positive(self, lower, upper):
        """Reciprocal using an independently proved positive VALUE range.

        lower/upper bound the true value at every base point, not derivatives.
        No inverse of a widened product is taken. Coefficients remain D^alpha/alpha!.
        """
        if not isinstance(lower,Q) or not isinstance(upper,Q):
            raise TypeError("positive reciprocal bounds must be fmpq")
        if not 0 < lower <= upper:
            raise ArithmeticError("positive reciprocal needs 0 < lower <= upper")
        if not all(x.is_finite() for x in self.c):
            raise ArithmeticError("non-finite input to positive reciprocal")
        lo=max(lower,self.c[0].lower().fmpq())
        hi=min(upper,self.c[0].upper().fmpq())
        if lo>hi:
            raise ArithmeticError("positive reciprocal: empty proven range")
        # Exact endpoint reciprocals are rounded outward by Arb. Even if the
        # resulting ball protrudes, it is only MULTIPLIED, never inverted again.
        out=[hull(1/hi,1/lo)]
        for row in structure(self.orders)[2][1:]:
            out.append(-out[0]*sum((self.c[i]*out[j] for i,j in row if i),arb(0)))
        if not all(x.is_finite() for x in out):
            raise ArithmeticError("non-finite positive reciprocal coefficients")
        return Jet(self.orders,out)
    def __truediv__(self,x): return self*self.lift(x).reciprocal()
    def __rtruediv__(self,x): return self.lift(x)*self.reciprocal()
    def __pow__(self,n):
        if type(n) is not int: raise TypeError("integer powers only")
        if n<0: return self.reciprocal()**(-n)
        out=self.lift(1); a=self
        while n:
            if n%2: out=out*a
            n//=2
            if n: a=a*a
        return out
    def sqrt(self):
        out=[self.c[0].sqrt()]
        for k,row in enumerate(structure(self.orders)[2][1:],1):
            mid=sum((out[i]*out[j] for i,j in row if i and j),arb(0))
            out.append((self.c[k]-mid)/(2*out[0]))
        return Jet(self.orders,out)
    def compose(self,derivatives):
        n=sum(self.orders)
        if len(derivatives)!=n+1: raise ValueError("wrong derivative order")
        delta=Jet(self.orders,(arb(0),)+self.c[1:])
        out=self.lift(0); p=self.lift(1)
        for k,d in enumerate(derivatives):
            out=out+p*(d/factorial(k))
            if k<n: p=p*delta
        return out
    def sin(self):
        s,c=self.c[0].sin(),self.c[0].cos()
        return self.compose([(s,c,-s,-c)[k%4] for k in range(sum(self.orders)+1)])
    def cos(self):
        s,c=self.c[0].sin(),self.c[0].cos()
        return self.compose([(c,-s,-c,s)[k%4] for k in range(sum(self.orders)+1)])
    def cap(self,lo,hi):
        return Jet(self.orders,(clip(self.c[0],lo,hi),)+self.c[1:])
    def coeff(self,*a):
        return self.c[structure(self.orders)[1][tuple(a)]]

@lru_cache(maxsize=1)
def rational_coeffs():
    c=[Q(1)]
    for n in range(97):
        c.append(c[-1]*Q(n+1,2*n+3))
    return tuple(c)

def angle(g):
    n=sum(g.orders)
    if n>12: raise ValueError("mixed total order >12 unsupported")
    c=rational_coeffs(); q=1-g.c[0]
    # Horner evaluations remain rigorous even if the outward Arb ball q
    # protrudes a little outside [0,1]. Tail bounds use the TRUE gamma range.
    p=[arb(0) for _ in range(n+2)]
    for j in range(96,-1,-1):
        for k in range(n+1,0,-1):
            p[k]=p[k]*q+k*p[k-1]
        p[0]=p[0]*q+arb(c[j])
    d=[]
    for k in range(n+2):
        fall=factorial(97)//factorial(97-k)
        ratio=Q(98,2*(98-k))
        tail=c[97]*fall/(1-ratio)
        v=p[k]+hull(0,tail)
        d.append(-v if k%2 else v)
    gp=arb(2*c[96]/97)
    for j in range(95,-1,-1):
        gp=gp*q+arb(2*c[j]/(j+1))
    g0=q*gp+hull(0,4*c[97]/98)
    return (g.compose([g0]+[-2*d[k-1] for k in range(1,n+1)]),
            g.compose(d[:n+1]), g.compose(d[1:n+2]))
