"""Two-weight analytic allocation example; educational use only."""
import math
from numbers import Real

def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def diagnostics(w1, w2, tolerance=1e-12):
    w1, w2, tolerance = finite(w1, "w1"), finite(w2, "w2"), finite(tolerance, "tolerance")
    if tolerance < 0: raise ValueError("tolerance must be nonnegative")
    residual = math.fsum((w1, w2, -1.0))
    violation = max(0.0, -w1, -w2)
    if not math.isfinite(residual): raise OverflowError("residual exceeds float range")
    return {"equality_residual": residual, "long_only_violation": violation,
            "tolerance": tolerance, "feasible": abs(residual) <= tolerance and violation <= tolerance}

def objective(w1, w2, a, b):
    w1, w2, a, b = (finite(v, n) for v, n in ((w1, "w1"), (w2, "w2"), (a, "a"), (b, "b")))
    d1, d2 = w1-a, w2-b
    result = d1*d1 + d2*d2
    if not math.isfinite(result): raise OverflowError("objective exceeds float range")
    return result

def solve(a, b, tolerance=1e-12):
    a, b = finite(a, "a"), finite(b, "b")
    tolerance = finite(tolerance, "tolerance")
    if tolerance < 0: raise ValueError("tolerance must be nonnegative")
    # Halve before addition to reduce avoidable overflow.
    stationary = 0.5 + 0.5*a - 0.5*b
    if not math.isfinite(stationary): raise OverflowError("stationary point exceeds float range")
    w1 = min(1.0, max(0.0, stationary))
    w2 = 1.0-w1
    return {"weights": (w1, w2), "objective": objective(w1, w2, a, b),
            "diagnostics": diagnostics(w1, w2, tolerance),
            "method": "analytic solution for two-weight quadratic"}

if __name__ == "__main__":
    print(solve(.7, .2))
    print("Feasible but nonoptimal:", diagnostics(.5, .5), objective(.5, .5, .7, .2))
