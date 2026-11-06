"""Illustrative 2x2 replication solver, not a general-purpose solver."""
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

def solve_2x2(matrix, target, *, threshold=1e-12):
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix) or len(target) != 2:
        raise ValueError("expected a 2x2 matrix and a two-element target")
    a, b = (finite(x, "coefficient") for x in matrix[0])
    c, d = (finite(x, "coefficient") for x in matrix[1])
    y, z = (finite(x, "target") for x in target)
    threshold = finite(threshold, "threshold")
    if threshold < 0: raise ValueError("threshold must be nonnegative")
    # Work exactly on the represented floats; round only reported results.
    a, b, c, d, y, z = map(Fraction, (a, b, c, d, y, z))
    scale = max(abs(a), abs(b), abs(c), abs(d))
    if scale == 0: raise ValueError("zero matrix is singular")
    det = a*d - b*c
    screen = det / scale**2
    if abs(screen) <= Fraction(threshold):
        raise ValueError("singular or below screening threshold")
    try:
        x1, x2 = float((y*d - b*z)/det), float((a*z - y*c)/det)
    except OverflowError as exc:
        raise OverflowError("solution exceeds float range") from exc
    h1, h2 = Fraction(x1), Fraction(x2)
    try:
        residual = (float(a*h1 + b*h2 - y), float(c*h1 + d*h2 - z))
    except OverflowError as exc:
        raise OverflowError("residual exceeds float range") from exc
    return {"solution": (x1, x2), "residual": residual,
            "normalized_determinant": float(screen), "screening_threshold": threshold}

if __name__ == "__main__":
    print(solve_2x2([[1, 1], [1, 2]], [3, 5]))
