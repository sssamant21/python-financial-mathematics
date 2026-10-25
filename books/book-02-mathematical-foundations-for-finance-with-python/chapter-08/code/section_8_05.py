"""Section 8.5: exponential and logarithmic derivatives in finance."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def exponential_derivative(x, scale=1.0, growth=1.0):
    x, a, k = finite(x, "x"), finite(scale, "scale"), finite(growth, "growth")
    return a*k*math.exp(k*x)

def logarithm_derivative(x, offset=1.0, slope=2.0):
    x, a, b = finite(x, "x"), finite(offset, "offset"), finite(slope, "slope")
    u = a+b*x
    if u <= 0:
        raise ValueError("logarithm argument must be positive")
    return b/u

def accumulation(principal, rate, years):
    p, r, t = finite(principal, "principal"), finite(rate, "rate"), finite(years, "years")
    if p < 0 or t < 0:
        raise ValueError("principal and years must be nonnegative")
    return p*math.exp(r*t)

def accumulation_time_derivative(principal, rate, years):
    r = finite(rate, "rate")
    return r*accumulation(principal, rate, years)

def accumulation_rate_derivative(principal, rate, years):
    t = finite(years, "years")
    return t*accumulation(principal, rate, years)

def present_value(payment, rate, years):
    c, r, t = finite(payment, "payment"), finite(rate, "rate"), finite(years, "years")
    if c < 0 or t < 0:
        raise ValueError("payment and years must be nonnegative")
    return c*math.exp(-r*t)

def present_value_rate_derivative(payment, rate, years):
    t = finite(years, "years")
    return -t*present_value(payment, rate, years)

def present_value_rate_shock(payment, rate, years, change):
    t, h = finite(years, "years"), finite(change, "change")
    return present_value(payment, rate, years)*math.expm1(-t*h)

def log_return(start, end):
    s, e = finite(start, "start"), finite(end, "end")
    if s <= 0 or e <= 0:
        raise ValueError("prices must be positive")
    return math.log1p((e-s)/s)

def power_elasticity(exponent):
    return finite(exponent, "exponent")

def stable_exponential_difference_quotient(x, step):
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return math.exp(x)*math.expm1(h)/h

def centered_difference(function, x, step=1e-4):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

if __name__ == "__main__":
    print("Derivative of 7e^(3x) at x=1:", exponential_derivative(1, 7, 3))
    print("Derivative of ln(1+2x) at x=2:", logarithm_derivative(2))
    print("Accumulated value:", accumulation(1000, 0.04, 5))
    print("Accumulation time derivative:", accumulation_time_derivative(1000, 0.04, 5))
    print("PV:", present_value(5000, 0.03, 4))
    print("PV rate derivative:", present_value_rate_derivative(5000, 0.03, 4))
    print("Exact PV change for +1 bp:", present_value_rate_shock(5000, 0.03, 4, 0.0001))
    print("Log return 100 to 103:", log_return(100, 103))
