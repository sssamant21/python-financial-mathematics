"""Section 8.4: chain rule and financial sensitivity."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def chain_derivative(outer_derivative, inner, inner_derivative, x):
    if not all(callable(fn) for fn in (outer_derivative, inner, inner_derivative)):
        raise TypeError("all function arguments must be callable")
    x = finite(x, "x")
    return finite(outer_derivative(finite(inner(x), "inner(x)")), "outer derivative") * finite(inner_derivative(x), "inner derivative")

def nested_power_derivative(x):
    x = finite(x, "x")
    return 24*x*(3*x*x+2)**3

def rate_from_factor(z):
    return 0.03+0.002*finite(z, "factor")

def variable_rate_pv(amount, years, factor):
    c, t, z = finite(amount, "amount"), finite(years, "years"), finite(factor, "factor")
    if c < 0 or t < 0:
        raise ValueError("amount and years must be nonnegative")
    return c*math.exp(-t*rate_from_factor(z))

def variable_rate_pv_derivative(amount, years, factor):
    t = finite(years, "years")
    return -t*variable_rate_pv(amount, years, factor)*0.002

def nominal_rate(z):
    return 0.04+0.001*finite(z, "factor")

def discrete_future_value(principal, periods_per_year, years, factor):
    p, t, z = finite(principal, "principal"), finite(years, "years"), finite(factor, "factor")
    if type(periods_per_year) is not int or periods_per_year < 1:
        raise ValueError("periods_per_year must be a positive integer")
    if p < 0 or t < 0:
        raise ValueError("principal and years must be nonnegative")
    base = 1+nominal_rate(z)/periods_per_year
    if base <= 0:
        raise ValueError("compounding base must be positive")
    return p*math.exp((periods_per_year*t)*math.log(base))

def discrete_future_value_derivative(principal, periods_per_year, years, factor):
    p, t, z = finite(principal, "principal"), finite(years, "years"), finite(factor, "factor")
    if type(periods_per_year) is not int or periods_per_year < 1:
        raise ValueError("periods_per_year must be a positive integer")
    if p < 0 or t < 0:
        raise ValueError("principal and years must be nonnegative")
    base = 1+nominal_rate(z)/periods_per_year
    if base <= 0:
        raise ValueError("compounding base must be positive")
    return p*t*base**(periods_per_year*t-1)*0.001

def price(t):
    t = finite(t, "time")
    if t <= -50:
        raise ValueError("price model requires t > -50")
    return 100*(1+0.02*t)**3

def log_price_growth(t):
    t = finite(t, "time")
    if t <= -50:
        raise ValueError("price model requires t > -50")
    return 0.06/(1+0.02*t)

def centered_difference(function, x, step=1e-4):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    if h == 0:
        raise ValueError("step must be nonzero")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

if __name__ == "__main__":
    print("Nested power derivative at x=2:", nested_power_derivative(2))
    print("Variable-rate PV at z=1:", variable_rate_pv(1000, 4, 1))
    print("Variable-rate PV sensitivity at z=1:", variable_rate_pv_derivative(1000, 4, 1))
    print("Discrete FV at z=1:", discrete_future_value(2000, 12, 2, 1))
    print("Discrete FV sensitivity at z=1:", discrete_future_value_derivative(2000, 12, 2, 1))
    print("Log-price growth at t=3:", log_price_growth(3))
