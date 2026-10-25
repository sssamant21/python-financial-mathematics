"""Chapter 6 assessment: independent cash-flow calculations and analytic answers."""
import math

def valid(first, growth, rate, n):
    if any(type(x) not in (int, float) for x in (first, growth, rate)):
        raise TypeError("payment and rates must be numeric, excluding bool")
    c, g, r = map(float, (first, growth, rate))
    if not all(map(math.isfinite, (c, g, r))):
        raise ValueError("inputs must be finite")
    if g <= -1 or r <= -1:
        raise ValueError("growth and discount rates must exceed -1")
    if type(n) is not int:
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be nonnegative")
    return c, g, r

def analytic_pv(first, growth, rate, n, due=False):
    c, g, r = valid(first, growth, rate, n)
    if n == 0 or c == 0:
        return 0.0
    x = math.log1p(g) - math.log1p(r)
    factor = n if x == 0 else math.expm1(n*x) / math.expm1(x)
    result = c / (1+r) * factor
    if due:
        result *= 1+r
    if not math.isfinite(result):
        raise OverflowError("nonfinite analytic value")
    return result

def enumerated_pv(first, growth, rate, n, due=False):
    c, g, r = valid(first, growth, rate, n)
    return math.fsum(
        c * (1+g)**k / (1+r)**(k if due else k+1)
        for k in range(n)
    )

def future_value(first, growth, rate, n, due=False):
    _, _, r = valid(first, growth, rate, n)
    result = analytic_pv(first, growth, r, n, due) * (1+r)**n
    if not math.isfinite(result):
        raise OverflowError("nonfinite future value")
    return result

def perpetuity(first, growth, rate):
    c, g, r = valid(first, growth, rate, 0)
    if c == 0:
        return 0.0
    if r <= g:
        raise ValueError("nonzero growing perpetuity requires rate > growth")
    return c/(r-g)

def tail(first, growth, rate, n):
    _, g, r = valid(first, growth, rate, n)
    result = perpetuity(first, g, r)
    return result * math.exp(n*(math.log1p(g)-math.log1p(r)))

def relative_horizon(ratio, tolerance):
    if type(ratio) not in (int, float) or type(tolerance) not in (int, float):
        raise TypeError("ratio and tolerance must be numeric")
    q, eps = float(ratio), float(tolerance)
    if not math.isfinite(q) or not math.isfinite(eps):
        raise ValueError("inputs must be finite")
    if not 0 <= q < 1 or not 0 < eps < 1:
        raise ValueError("require 0 <= ratio < 1 and 0 < tolerance < 1")
    if q == 0:
        return 1
    return math.ceil(math.log(eps)/math.log(q))

def report():
    scenarios = [
        ("ordinary annuity", 100, 0, 0.05, 3),
        ("growing annuity", 100, 0.03, 0.05, 3),
        ("equal growth/discount", 100, 0.04, 0.04, 5),
        ("zero rate", 80, 0, 0, 12),
        ("capstone", 1000, 0.03, 0.05, 10),
    ]
    for label, c, g, r, n in scenarios:
        pv = analytic_pv(c, g, r, n)
        direct = enumerated_pv(c, g, r, n)
        assert math.isclose(pv, direct, rel_tol=1e-11, abs_tol=1e-9)
        print(f"{label}: PV={pv:.8f}; FV={future_value(c,g,r,n):.8f}; independent={direct:.8f}; PASS")
    total = perpetuity(1000, 0.03, 0.05)
    first10 = analytic_pv(1000, 0.03, 0.05, 10)
    remainder = tail(1000, 0.03, 0.05, 10)
    assert math.isclose(first10+remainder, total, rel_tol=1e-11)
    print(f"capstone perpetuity={total:.8f}; first10={first10:.8f}; tail={remainder:.8f}; PASS")

if __name__ == "__main__":
    report()
