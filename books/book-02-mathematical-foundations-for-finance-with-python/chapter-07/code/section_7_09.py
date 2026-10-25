"""Section 7.9: boundary and continuity investigation capstone."""
import math
from dataclasses import dataclass

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a number, excluding bool")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside float range") from exc
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value

def removable_raw(x):
    x = finite(x, "x")
    if x == 3:
        raise ValueError("undefined at x=3")
    return (x*x-9)/(x-3)

def removable_extension(x):
    return finite(x, "x")+3

def threshold_fee(amount):
    amount = finite(amount, "amount")
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    return 5.0 if amount < 1000 else 10.0

def vertical_sample(x):
    x = finite(x, "x")
    if x == 2:
        raise ValueError("undefined at x=2")
    return 1/(x-2)

def annuity_accumulation(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if r == 0:
        return float(periods)
    result = math.expm1(periods*math.log1p(r))/r
    if not math.isfinite(result):
        raise OverflowError("annuity accumulation overflow")
    return result

def annuity_sum_reference(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    return math.fsum((1+r)**k for k in range(periods))

def bond_residual(yield_rate):
    y = finite(yield_rate, "yield_rate")
    if y <= -1:
        raise ValueError("yield must exceed -1")
    result = 50/(1+y)+1050/(1+y)**2-1000
    if not math.isfinite(result):
        raise OverflowError("bond residual overflow")
    return result

@dataclass(frozen=True)
class RootResult:
    estimate: float
    left: float
    right: float
    residual: float
    iterations: int

def bisection(function, left, right, tolerance=1e-10, max_iterations=200):
    if not callable(function):
        raise TypeError("function must be callable")
    a, b = finite(left, "left"), finite(right, "right")
    tol = finite(tolerance, "tolerance")
    if a >= b or tol <= 0:
        raise ValueError("invalid bracket or tolerance")
    if type(max_iterations) is not int or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    fa, fb = finite(function(a), "f(left)"), finite(function(b), "f(right)")
    if fa == 0:
        return RootResult(a, a, a, 0.0, 0)
    if fb == 0:
        return RootResult(b, b, b, 0.0, 0)
    if (fa > 0) == (fb > 0):
        raise ValueError("bracket endpoints must have opposite signs")
    for iteration in range(1, max_iterations+1):
        mid = a/2+b/2 if a < 0 < b else a+(b-a)/2
        if mid == a or mid == b:
            raise ArithmeticError("floating-point bracket cannot be refined")
        fm = finite(function(mid), "f(midpoint)")
        if fm == 0:
            return RootResult(mid, mid, mid, 0.0, iteration)
        if (fa > 0) == (fm > 0):
            a, fa = mid, fm
        else:
            b, fb = mid, fm
        estimate = a/2+b/2 if a < 0 < b else a+(b-a)/2
        if (b-a)/2 <= tol:
            return RootResult(estimate, a, b, finite(function(estimate), "f(estimate)"), iteration)
    raise RuntimeError("maximum bisection iterations exceeded")

if __name__ == "__main__":
    print("Case A: extension at 3 =", removable_extension(3))
    print("Case B: threshold fees =", [threshold_fee(x) for x in (999.99, 1000, 1000.01)])
    for offset in (0.1, 0.01, 0.001):
        print("Case C:", offset, vertical_sample(2-offset), vertical_sample(2+offset))
    for rate in (-0.01, 0, 1e-10, 0.05):
        print("Case D:", rate, annuity_accumulation(rate, 12))
    print("Case E:", bisection(bond_residual, 0, 0.1))
