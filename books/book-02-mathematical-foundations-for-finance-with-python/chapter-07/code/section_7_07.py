"""Section 7.7: Intermediate Value Theorem and bracketed bisection."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric (excluding bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} out of finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def bisection(function, left, right, *, tolerance=1e-10, max_iterations=200):
    """Return (midpoint, final_bracket, iterations) for a continuous sign-bracketed function.

    Continuity is a caller responsibility; endpoint sign checks cannot prove it.
    """
    a, b = finite(left, "left"), finite(right, "right")
    tol = finite(tolerance, "tolerance")
    if not callable(function):
        raise TypeError("function must be callable")
    if not a < b:
        raise ValueError("left must be smaller than right")
    if tol <= 0:
        raise ValueError("tolerance must be positive")
    if type(max_iterations) is not int or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    fa = finite(function(a), "f(left)")
    fb = finite(function(b), "f(right)")
    if fa == 0:
        return a, (a, a), 0
    if fb == 0:
        return b, (b, b), 0
    if (fa > 0) == (fb > 0):
        raise ValueError("endpoints must have opposite signs")
    for iteration in range(1, max_iterations + 1):
        midpoint = a/2 + b/2 if (a < 0 < b) else a + (b-a)/2
        if midpoint == a or midpoint == b:
            raise ArithmeticError("floating-point bracket cannot be refined")
        fm = finite(function(midpoint), "f(midpoint)")
        if fm == 0:
            return midpoint, (midpoint, midpoint), iteration
        if (fa > 0) == (fm > 0):
            a, fa = midpoint, fm
        else:
            b, fb = midpoint, fm
        estimate = a/2 + b/2 if a < 0 < b else a + (b-a)/2
        if (b-a)/2 <= tol:
            return estimate, (a, b), iteration
    raise RuntimeError("bisection did not converge within max_iterations")

def project_profit(units, unit_price=20, variable_cost=12, fixed_cost=1000):
    q = finite(units, "units")
    p = finite(unit_price, "unit_price")
    v = finite(variable_cost, "variable_cost")
    fixed = finite(fixed_cost, "fixed_cost")
    if q < 0 or p < 0 or v < 0 or fixed < 0:
        raise ValueError("volumes and costs must be nonnegative")
    return (p-v)*q-fixed

def bond_yield_residual(yield_rate, payments, price):
    y = finite(yield_rate, "yield_rate")
    p = finite(price, "price")
    if y <= -1:
        raise ValueError("yield_rate must exceed -1")
    if p <= 0:
        raise ValueError("price must be positive")
    flows = [finite(c, "payment") for c in payments]
    if not flows:
        raise ValueError("payments must be nonempty")
    if any(c <= 0 for c in flows):
        raise ValueError("all payments must be positive")
    result = math.fsum(c / ((1+y)**k) for k, c in enumerate(flows, start=1)) - p
    if not math.isfinite(result):
        raise OverflowError("bond residual overflow")
    return result

if __name__ == "__main__":
    root, bracket, iterations = bisection(lambda x: x*x-2, 1, 2)
    print(f"sqrt(2): {root:.12f}; bracket={bracket}; iterations={iterations}")
    root, bracket, iterations = bisection(project_profit, 100, 200)
    print(f"break-even units: {root:.8f}; iterations={iterations}")
    residual = lambda y: bond_yield_residual(y, (50, 1050), 1000)
    root, bracket, iterations = bisection(residual, 0, 0.1)
    print(f"bond yield: {root:.10%}; residual={residual(root):.3g}")
