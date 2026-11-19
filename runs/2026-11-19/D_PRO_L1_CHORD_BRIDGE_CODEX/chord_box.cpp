// DIAGNOSTIC_ONLY / NOT_EVIDENCE. Integer outward enclosures of (F1)-(F3).
// Input: integer coordinates in units 1/4096 (lambda pair, rho pair, z pair), m and phi cells.
// Output: "upper numerator denominator" or "empty 0 1". Each line refers to one full outer box.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Z = std::int64_t;
using Wide = __int128_t;
constexpr int bits=24;
constexpr Z one=Z(1)<<bits, G=2048;
static Z ptab[G+1], qtab[G+1];
struct I { Z lo,hi; };
constexpr I zero{0,0}, unit{one,one};

static inline Z down(Z a,Z b) { return Z((Wide(a)*b)>>bits); }
static inline Z up(Z a,Z b) { return Z((Wide(a)*b+one-1)>>bits); }
// Positive denominator. Ratios in this implementation are nonnegative.
static inline Z ratio_lo(Z a,Z b) { return Z(Wide(a)*one/b); }
static inline Z ratio_hi(Z a,Z b) { return Z((Wide(a)*one+b-1)/b); }
static inline I add(I a,I b) { return {a.lo+b.lo,a.hi+b.hi}; }
static inline I neg(I a) { return {-a.hi,-a.lo}; }
static inline I sub(I a,I b) { return add(a,neg(b)); }
static inline I mul(I a,I b) {
    if(a.lo>=0 && b.lo>=0) return {down(a.lo,b.lo),up(a.hi,b.hi)};
    if(b.lo>=0) return {down(a.lo,(a.lo<0?b.hi:b.lo)),up(a.hi,(a.hi<0?b.lo:b.hi))};
    if(a.lo>=0) return mul(b,a);
    if(a.hi<=0) return neg(mul(neg(a),b));
    if(b.hi<=0) return neg(mul(a,neg(b)));
    return {std::min(down(a.lo,b.hi),down(a.hi,b.lo)),std::max(up(a.lo,b.lo),up(a.hi,b.hi))};
}
static inline I sq(I a) {
    Z mx=std::max(std::abs(a.lo),std::abs(a.hi));
    Z mn=std::max({Z(0),a.lo,-a.hi});
    return {down(mn,mn),up(mx,mx)};
}
static inline I intersect(I a,I b) {
    I c{std::max(a.lo,b.lo),std::min(a.hi,b.hi)};
    if(c.lo>c.hi) throw std::runtime_error("empty arithmetic intersection");
    return c;
}
static inline I sign(I a,int k) {return k>0?a:neg(a);}
static inline I inv(I a) {
    if(a.lo<=0) throw std::runtime_error("non-positive denominator");
    return {ratio_lo(one,a.hi),ratio_hi(one,a.lo)};
}
static inline Z rootfloor(Z a) {
    if(a<0 || a>128*one) throw std::runtime_error("sqrt out of range");
    Z rad=a*one;
    Z t=Z(std::sqrt(double(rad)));
    while(t*t>rad) --t;
    while((t+1)*(t+1)<=rad) ++t;
    return t;
}
static inline I root(I a) {
    Z lo=rootfloor(a.lo),hi=rootfloor(a.hi);
    return {lo,hi+(hi*hi!=a.hi*one)};
}
static inline I one_minus(I a){ return {one-a.hi,one-a.lo}; }

struct Angle {I cos, sin2,mean,var,d0,mean_w,var_w;};
static std::map<int,std::vector<Angle>> angles;
static void read_tables(const std::string& path) {
    std::ifstream f(path);
    std::string banner; std::getline(f,banner);
    Z q,g; f>>q>>g;
    if(q!=one || g!=G || banner!="# DIAGNOSTIC_ONLY / NOT_EVIDENCE")
        throw std::runtime_error("unexpected table");
    for(Z i=0;i<=G;++i) f>>ptab[i]>>qtab[i];
    for(int n=1;n<=128;n*=2) {
        auto& dest=angles[n]; dest.resize(n);
        for(int k=0;k<n;++k){
            int nrow,krow; f>>nrow>>krow;
            if(n!=nrow||k!=krow) throw std::runtime_error("wrong angle row");
            auto& a=dest[k];
            for(I* p:{&a.cos,&a.sin2,&a.mean,&a.var,&a.d0,&a.mean_w,&a.var_w})
                f>>p->lo>>p->hi;
        }
    }
    if(!f) throw std::runtime_error("incomplete table");
}
struct Latitude {I m,m2,s,s2;};
static std::map<int,std::vector<Latitude>> latitudes;
static const std::vector<Latitude>& latitude_grid(int n) {
    auto& v=latitudes[n];
    if(!v.empty()) return v;
    if(n<=0||n>2048||one%n) throw std::runtime_error("unsupported latitude grid");
    for(int i=0;i<n;++i){
        I m{one*i/n,one*(i+1)/n}; I m2=sq(m),s2=one_minus(m2);
        v.push_back({m,m2,root(s2),s2});
    }
    return v;
}

struct Shape { I rho,z,r2,delta,eps2,ecc; };
struct Slice { I c_inv,c_root_inv,u,v0,v1; };
struct End { Z positive,negative; I w; Z square_lo; };

// Enclose v/d in [-1,1], using only positive denominators.
static inline I aligned(I v,I d) {
    auto abslo=[&](Z x){return std::min(one,ratio_lo(x,d.hi));};
    auto abshi=[&](Z x){return d.lo==0?one:std::min(one,ratio_hi(x,d.lo));};
    if(d.hi==0) return {-one,one};
    return {v.lo<0?-abshi(-v.lo):abslo(v.lo),v.hi<0?-abslo(-v.hi):abshi(v.hi)};
}

static inline End end_bounds(const Shape& p,const Latitude& g,const Slice& u,
                             I ex,I j,I d,I vd,I v,int side) {
    I sv=sign(v,side);
    I length=intersect(sub(d,sv),{0,2*d.hi});
    I xi_z=intersect(add(p.z,sign(mul(length,g.m),side)),{-one,one});
    I xi_x=intersect(add(p.rho,sign(mul(length,ex),side)),{-one,one});
    I horiz=intersect(add(sq(xi_x),mul(sq(length),j)),{0,one});
    I B=intersect(intersect(one_minus(mul(p.ecc,sq(xi_z))),add(p.eps2,mul(p.ecc,horiz))),
                  {p.eps2.lo,one});
    I sb=root(B);
    I inv_low_a=inv({sb.lo,sb.lo}), inv_high_a=inv({sb.hi,sb.hi});
    Z gamma_lo=std::min(one,down(down(d.lo,u.c_root_inv.lo),inv_low_a.lo));
    Z gamma_hi=std::min(one,up(up(d.hi,u.c_root_inv.hi),inv_high_a.hi));
    Z pp=up(ptab[gamma_lo/(one/G)],inv_low_a.hi);
    Z nn=down(qtab[(gamma_hi+(one/G)-1)/(one/G)],inv_high_a.lo);
    I a=one_minus(sign(vd,side));
    I w{a.lo/2,(a.hi+1)/2};
    return {pp,nn,w,sq(sub(mul(d,u.u),sv)).lo};
}

static inline Z cell(const Shape& p,const Latitude& g,const Slice& u,const Angle& a,int side) {
    I ex=sign(mul(g.s,a.cos),side);
    I j=mul(g.s2,a.sin2), jbar=mul(g.s2,a.d0);
    I v=intersect(add(u.v0,sign(mul(u.v1,a.cos),side)),{-one,one});
    I v2=sq(v), d2=intersect(add(p.delta,v2),{0,one});
    I tangential=sub(sign(mul(mul(p.rho,g.m),a.cos),side),mul(p.z,g.s));
    d2=intersect(d2,one_minus(add(sq(tangential),mul(p.r2,a.sin2))));
    I d=root(d2), vd=aligned(v,d);
    End e=end_bounds(p,g,u,ex,j,d,vd,v,1), f=end_bounds(p,g,u,ex,j,d,vd,v,-1);
    const End& big=e.positive>f.positive?e:f;
    const End& small=e.positive>f.positive?f:e;
    Z weighted_p=small.positive+up(big.w.hi,big.positive-small.positive);
    const End& large=e.negative>f.negative?e:f;
    const End& little=e.negative>f.negative?f:e;
    I v12=sq(u.v1);
    I mv=intersect(add(sq(add(u.v0,sign(mul(u.v1,a.mean),side))),mul(v12,a.var)),v2);
    I mvw=intersect(add(sq(add(u.v0,sign(mul(u.v1,a.mean_w),side))),mul(v12,a.var_w)),v2);
    I mjv=mul(jbar,mvw);
    I md2=intersect(add(p.delta,mv),d2);
    I md2j=intersect(add(mul(p.delta,jbar),mjv),mul(d2,jbar));
    I projection=one_minus(mul(jbar,u.c_inv));
    Z positive_moment=std::min(up(d2.hi,projection.hi), md2.hi-down(md2j.lo,u.c_inv.lo));
    Z pos=up(up(weighted_p,u.c_root_inv.hi),up(u.c_inv.hi,positive_moment));
    pos=std::min(pos,up(2*d.hi,up(u.c_inv.hi,projection.hi)));
    Z n_moment=down(down(p.delta.lo,sq(u.u).lo),jbar.lo)+down(sq(add(unit,u.u)).lo,mjv.lo);
    Z extra=down(down(down(large.negative-little.negative,large.w.lo),large.square_lo),jbar.lo);
    Z neg_mass=down(u.c_root_inv.lo,down(little.negative,n_moment)+extra);
    return pos-neg_mass;
}

static void eval(Z l0,Z l1,Z r0,Z r1,Z z0,Z z1,int nm,int na) {
    if(!(5*4096<=l0&&l0<=l1&&l1<=8*4096 && 0<=r0&&r0<=r1&&r1<=4096
         &&0<=z0&&z0<=z1&&z1<=4096)) throw std::runtime_error("outer domain");
    const Z factor=one/4096;
    I lam{l0*factor,l1*factor},rho{r0*factor,r1*factor},z{z0*factor,z1*factor};
    I r2=sq(rho),z2=sq(z),eps2=inv(sq(lam)),ecc=one_minus(eps2);
    if(r2.lo+z2.lo>one||z2.lo+eps2.lo>one){
        std::cout<<"empty 0 1"<<std::endl;return;
    }
    z.hi=std::min(z.hi,root({0,one-std::max(eps2.lo,r2.lo)}).hi);
    rho.hi=std::min(rho.hi,root({0,one-z2.lo}).hi);
    r2=sq(rho); z2=sq(z);
    I delta=intersect(one_minus(add(r2,z2)),{0,one});
    Shape shape{rho,z,r2,delta,eps2,ecc};
    I lm2=sub(sq(lam),unit);
    auto it=angles.find(na);
    if(it==angles.end()) throw std::runtime_error("unsupported angular grid");
    Z total=0;
    for(const Latitude& g:latitude_grid(nm)){
        I c=add(unit,mul(lm2,g.m2)), ci=inv(c);
        Slice u{ci,inv(root(c)),one_minus(ci),mul(z,g.m),mul(rho,g.s)};
        for(const Angle& a:it->second)
            total+=cell(shape,g,u,a,1)+cell(shape,g,u,a,-1);
    }
    std::cout<<"upper "<<total<<" "<<(2*Z(nm)*na*one)<<std::endl;
}

int main(int argc,char** argv) {
    try {
        if(argc!=2) throw std::runtime_error("expected table file");
        read_tables(argv[1]);
        Z l0,l1,r0,r1,z0,z1;int nm,na;
        while(std::cin>>l0>>l1>>r0>>r1>>z0>>z1>>nm>>na)
            eval(l0,l1,r0,r1,z0,z1,nm,na);
        if(!std::cin.eof()) throw std::runtime_error("invalid input");
        return 0;
    } catch(const std::exception& e) {
        std::cerr<<"DIAGNOSTIC_ONLY / NOT_EVIDENCE: "<<e.what()<<std::endl;
        return 2;
    }
}
