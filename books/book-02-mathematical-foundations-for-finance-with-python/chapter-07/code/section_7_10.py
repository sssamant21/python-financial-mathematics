"""Section 7.10: chapter review financial mathematics assessment."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def discrete_future_value(principal, nominal_rate, periods_per_year, years):
    p = finite(principal, "principal")
    j = finite(nominal_rate, "nominal_rate")
    t = finite(years, "years")
    if type(periods_per_year) is not int or periods_per_year <= 0:
        raise ValueError("periods_per_year must be a positive integer")
    if t < 0 or 1+j/periods_per_year <= 0:
        raise ValueError("invalid time or compounding base")
    return p*math.exp(periods_per_year*t*math.log1p(j/periods_per_year))

def continuous_future_value(principal, rate, years):
    p, r, t = finite(principal, "principal"), finite(rate, "rate"), finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return p*math.exp(r*t)

def continuous_present_value(payment, rate, years):
    p, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return p*math.exp(-r*t)

def effective_from_continuous(rate):
    return math.expm1(finite(rate, "rate"))

def continuous_from_effective(rate):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(r)

def log_return(start, end):
    a, b = finite(start, "start"), finite(end, "end")
    if a <= 0 or b <= 0:
        raise ValueError("prices must be positive")
    return math.log(b/a)

def annuity_factor(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    if r == 0:
        return float(periods)
    return math.expm1(periods*math.log1p(r))/r

def bond_residual(yield_rate):
    y = finite(yield_rate, "yield_rate")
    if y <= -1:
        raise ValueError("yield must exceed -1")
    return 60/(1+y)+1060/(1+y)**2-1000

def bisection(function, left, right, tolerance=1e-10, max_iterations=200):
    a, b = finite(left, "left"), finite(right, "right")
    tol = finite(tolerance, "tolerance")
    if not callable(function):
        raise TypeError("function must be callable")
    if a >= b or tol <= 0 or type(max_iterations) is not int or max_iterations < 1:
        raise ValueError("invalid bracket, tolerance, or iteration count")
    fa, fb = finite(function(a), "f(left)"), finite(function(b), "f(right)")
    if fa == 0:
        return a, (a, a), 0
    if fb == 0:
        return b, (b, b), 0
    if (fa > 0) == (fb > 0):
        raise ValueError("endpoints must have opposite signs")
    for iteration in range(1, max_iterations+1):
        m = a/2+b/2 if a < 0 < b else a+(b-a)/2
        if m == a or m == b:
            raise ArithmeticError("floating-point bracket cannot be refined")
        fm = finite(function(m), "f(midpoint)")
        if fm == 0:
            return m, (m, m), iteration
        if (fa > 0) == (fm > 0):
            a, fa = m, fm
        else:
            b, fb = m, fm
        estimate = a/2+b/2 if a < 0 < b else a+(b-a)/2
        if (b-a)/2 <= tol:
            return estimate, (a, b), iteration
    raise RuntimeError("bisection failed to converge")

if __name__ == "__main__":
    print("Annual accumulation:", discrete_future_value(2500, 0.06, 1, 3))
    print("Continuous accumulation:", continuous_future_value(2500, 0.06, 3))
    print("Effective 5% continuous:", effective_from_continuous(0.05))
    print("Continuous equivalent of 8% effective:", continuous_from_effective(0.08))
    print("PV of 10000:", continuous_present_value(10000, 0.03, 4))
    print("Log return 100 to 103:", log_return(100, 103))
    print("Zero-rate 10-payment annuity:", annuity_factor(0, 10))
    print("Bond yield:", bisection(bond_residual, 0, 0.2))
