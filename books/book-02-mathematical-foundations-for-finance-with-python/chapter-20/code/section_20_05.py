"""Floating-point comparison examples; educational draft."""
import math
from numbers import Real
from fractions import Fraction

def _finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real and not bool")
    try:
        x = float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def errors(actual, reference):
    a, b = _finite(actual, "actual"), _finite(reference, "reference")
    absolute = abs(a - b)
    return absolute, None if b == 0 else absolute / abs(b)

def close_to_reference(actual, reference, *, atol, rtol):
    """Asymmetric sum rule; reference sets relative scale."""
    a, b = _finite(actual, "actual"), _finite(reference, "reference")
    atol, rtol = _finite(atol, "atol"), _finite(rtol, "rtol")
    if atol < 0 or rtol < 0:
        raise ValueError("tolerances must be nonnegative")
    # Evaluate the rule exactly for the represented binary floats. This avoids
    # overflow and extra rounding at a tolerance boundary; it is not a fast path.
    a, b, atol, rtol = map(Fraction.from_float, (a, b, atol, rtol))
    return abs(a - b) <= atol + rtol * abs(b)

if __name__ == "__main__":
    print("0.1 + 0.2:", 0.1 + 0.2)
    print("Close:", close_to_reference(0.1 + 0.2, 0.3, atol=1e-15, rtol=1e-12))
    print("Errors:", errors(101, 100))
    x = 1e-12
    print("Direct and stable:", math.exp(x) - 1, math.expm1(x))
