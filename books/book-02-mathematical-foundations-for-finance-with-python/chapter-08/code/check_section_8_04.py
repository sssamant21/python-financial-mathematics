"""Reference checks for Section 8.4."""
import math
from section_8_04 import (
    finite, chain_derivative, nested_power_derivative, variable_rate_pv,
    variable_rate_pv_derivative, discrete_future_value,
    discrete_future_value_derivative, price, log_price_growth,
    centered_difference)

def close(a, b, rel_tol=1e-7, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    for x in (-3, -1, 0, 1, 2, 5):
        close(nested_power_derivative(x), 24*x*(3*x*x+2)**3)
        close(chain_derivative(lambda u:4*u**3, lambda z:3*z*z+2,
                               lambda z:6*z, x), nested_power_derivative(x))
        close(centered_difference(lambda z:(3*z*z+2)**4, x, 1e-5),
              nested_power_derivative(x), rel_tol=1e-6)
    close(variable_rate_pv_derivative(1000, 4, 1), -8*math.exp(-0.128))
    for z in (-5, 0, 1, 5):
        for years in (0, 1, 4):
            pv = lambda v:variable_rate_pv(1000, years, v)
            close(centered_difference(pv, z), variable_rate_pv_derivative(1000, years, z))
            fv = lambda v:discrete_future_value(2000, 12, years, v)
            close(centered_difference(fv, z), discrete_future_value_derivative(2000, 12, years, z))
    for t in (0, 1, 3, 10):
        close(centered_difference(lambda x:math.log(price(x)), t),
              log_price_growth(t))
    rejects(ValueError, variable_rate_pv, -1, 4, 0)
    rejects(ValueError, variable_rate_pv, 1000, -1, 0)
    rejects(ValueError, discrete_future_value, 1000, 0, 2, 0)
    rejects(ValueError, discrete_future_value, 1000, 12, -1, 0)
    rejects(ValueError, discrete_future_value, 1000, 12, 2, -20000)
    rejects(ValueError, price, -50)
    rejects(ValueError, centered_difference, lambda x:x*x, 2, 0)
    rejects(TypeError, chain_derivative, None, lambda x:x, lambda x:1, 0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.4 reference checks")

if __name__ == "__main__":
    run()
