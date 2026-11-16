# J4 arithmetic-only smoke: NOT_EVIDENCE / NO P1 numerical certification.
# Julia 1.10.13 + IntervalArithmetic.jl 1.0.10 / independent rational checks.
using IntervalArithmetic

const RAT = Rational{BigInt}
rat(a::Integer, b::Integer=1)::RAT = BigInt(a) // BigInt(b)

function arctan_bracket(x::RAT, terms::Int)
    @assert 0 < x < 1 && terms > 0
    s = rat(0)
    for k in 0:(terms - 1)
        term = x^(2k+1) / rat(2k+1)
        s += iseven(k) ? term : -term
    end
    err = x^(2terms+1) / rat(2terms+1)
    return iseven(terms) ? (s, s+err) : (s-err, s)
end

# MPFR interval endpoints are *exactly* converted to dyadic rationals.
# No Float64 literals or rounded point approximations are introduced.
function has_rational_bracket(x, lower::RAT, upper::RAT)
    @assert isguaranteed(x)
    a = RAT(inf(x))
    b = RAT(sup(x))
    return a <= lower < upper <= b
end

setprecision(BigFloat, 256) do
    x = sqrt(interval(rat(2)))
    scale = BigInt(10)^100
    k = isqrt(BigInt(2) * scale^2)
    lo, hi = k//scale, (k+1)//scale
    @assert lo^2 < rat(2) < hi^2
    @assert has_rational_bracket(x, lo, hi)

    y = acos(interval(rat(0)))
    a0,a1 = arctan_bracket(rat(1,5),100)
    b0,b1 = arctan_bracket(rat(1,239),100)
    pi_lower, pi_upper = 16a0-4b1, 16a1-4b0
    @assert rat(3) < pi_lower < pi_upper < rat(22,7)
    # acos(0)=π/2. Machin's identity and alternating arctan remainders
    # provide independent exact rational bounds for this smoke.
    @assert has_rational_bracket(y, pi_lower/2, pi_upper/2)

    @assert isguaranteed(interval(rat(1,10)))
    println("J4_SQRT2_OUTWARD_RATIONAL_BRACKET_PASS")
    println("J4_ACOS0_MACHIN_RATIONAL_BRACKET_PASS")
    println("J4_ISGUARANTEED_TRUE_PASS")
    println("NOT_EVIDENCE_NO_P1_COMPUTATION")
end
