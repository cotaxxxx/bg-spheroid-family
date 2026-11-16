# V27 K1 arithmetic-only smoke, NOT_EVIDENCE, no P1 numerical run.
# Julia 1.10.13, IntervalArithmetic.jl 1.0.10.
using IntervalArithmetic

const RAT = Rational{BigInt}
rat(a::Integer, b::Integer=1)::RAT = BigInt(a) // BigInt(b)

function arctan_bracket(x::RAT, terms::Int)
    @assert rat(0) < x < rat(1) && terms > 0
    s = rat(0)
    for k in 0:(terms - 1)
        term = x^(2k + 1) / rat(2k + 1)
        s += iseven(k) ? term : -term
    end
    err = x^(2terms + 1) / rat(2terms + 1)
    return iseven(terms) ? (s, s + err) : (s - err, s)
end

function require_bigfloat_guaranteed_interval(x)
    @assert typeof(x) === Interval{BigFloat} "GUARANTEE_FAILED: interval endpoint type"
    @assert precision(inf(x)) >= 256 && precision(sup(x)) >= 256 "GUARANTEE_FAILED: precision"
    @assert isguaranteed(x) "GUARANTEE_FAILED: isguaranteed"
    @assert isfinite(inf(x)) && isfinite(sup(x)) "GUARANTEE_FAILED: non-finite endpoints"
    @assert inf(x) <= sup(x) "GUARANTEE_FAILED: interval order"
    return x
end

function require_narrow_interval(x)
    require_bigfloat_guaranteed_interval(x)
    exact_width = RAT(sup(x)) - RAT(inf(x))
    @assert rat(0) <= exact_width <= rat(1, BigInt(1) << 240) "GUARANTEE_FAILED: exact rational width"
    @assert diam(x) <= BigFloat(2)^(-240) "GUARANTEE_FAILED: diameter precision bound"
    return x
end

# Independently certified rational brackets, not point approximations.
function has_rational_bracket(x, lower::RAT, upper::RAT)
    require_narrow_interval(x)
    a = RAT(inf(x))
    b = RAT(sup(x))
    return a <= lower < upper <= b
end

setprecision(BigFloat, 256) do
    # Explicit endpoint type. Never use interval(rational) without the type.
    tenth = interval(BigFloat, rat(1, 10))
    require_narrow_interval(tenth)
    @assert RAT(inf(tenth)) <= rat(1, 10) <= RAT(sup(tenth))

    x = sqrt(interval(BigFloat, rat(2)))
    @assert typeof(x) === Interval{BigFloat}
    scale = BigInt(10)^100
    k = isqrt(BigInt(2) * scale^2)
    lo, hi = k // scale, (k + 1) // scale
    @assert lo^2 < rat(2) < hi^2
    @assert has_rational_bracket(x, lo, hi)

    y = acos(interval(BigFloat, rat(0)))
    @assert typeof(y) === Interval{BigFloat}
    a0, a1 = arctan_bracket(rat(1, 5), 100)
    b0, b1 = arctan_bracket(rat(1, 239), 100)
    pi_lower, pi_upper = 16a0 - 4b1, 16a1 - 4b0
    @assert rat(3) < pi_lower < pi_upper < rat(22, 7)
    @assert has_rational_bracket(y, pi_lower / 2, pi_upper / 2)

    println("J4_V27_BIGFLOAT_ENDPOINT_TYPE_PASS")
    println("J4_V27_256BIT_PRECISION_AND_DIAM_LE_2POW_MINUS240_PASS")
    println("J4_V27_RATIONAL_INPUT_ONLY_PASS")
    println("J4_V27_SQRT2_OUTWARD_RATIONAL_BRACKET_PASS")
    println("J4_V27_ACOS0_MACHIN_RATIONAL_BRACKET_PASS")
    println("J4_V27_ISGUARANTEED_TRUE_PASS")
    println("NOT_EVIDENCE_NO_P1_COMPUTATION")
end
