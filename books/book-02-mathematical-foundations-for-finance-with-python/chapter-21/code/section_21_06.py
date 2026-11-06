"""Two-weight analytic allocation example; educational use only."""
import math
from fractions import Fraction
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
    residual = Fraction(w1) + Fraction(w2) - 1
    violation = max(0.0, -w1, -w2)
    try:
        displayed_residual = float(residual)
    except OverflowError as exc:
        raise OverflowError("residual exceeds float range") from exc
    return {"equality_residual": displayed_residual, "long_only_violation": violation,
            "tolerance": tolerance,
            "feasible": abs(residual) <= Fraction(tolerance) and violation <= tolerance}

def objective(w1, w2, a, b):
    w1, w2, a, b = (finite(v, n) for v, n in ((w1, "w1"), (w2, "w2"), (a, "a"), (b, "b")))
    d1, d2 = Fraction(w1)-Fraction(a), Fraction(w2)-Fraction(b)
    try:
        return float(d1*d1 + d2*d2)
    except OverflowError as exc:
        raise OverflowError("objective exceeds float range") from exc

def solve(a, b, tolerance=1e-12):
    a, b = finite(a, "a"), finite(b, "b")
    tolerance = finite(tolerance, "tolerance")
    if tolerance < 0: raise ValueError("tolerance must be nonnegative")
    # Clip the exact stationary point, then round each coordinate separately.
    stationary = (1 + Fraction(a) - Fraction(b)) / 2
    first = min(Fraction(1), max(Fraction(0), stationary))
    w1, w2 = float(first), float(1-first)
    return {"weights": (w1, w2), "objective": objective(w1, w2, a, b),
            "diagnostics": diagnostics(w1, w2, tolerance),
            "method": "analytic solution for two-weight quadratic"}

if __name__ == "__main__":
    print(solve(.7, .2))
    print("Feasible but nonoptimal:", diagnostics(.5, .5), objective(.5, .5, .7, .2))
