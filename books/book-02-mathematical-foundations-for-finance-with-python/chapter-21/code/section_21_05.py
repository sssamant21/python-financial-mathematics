"""Illustrative 2x2 replication solver, not a general-purpose solver."""
import math
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
    scale = max(abs(a), abs(b), abs(c), abs(d))
    if scale == 0: raise ValueError("zero matrix is singular")
    aa, bb, cc, dd = a/scale, b/scale, c/scale, d/scale
    det = aa*dd - bb*cc
    if abs(det) <= threshold: raise ValueError("singular or below screening threshold")
    yy, zz = y/scale, z/scale
    x1, x2 = (yy*dd - bb*zz)/det, (aa*zz - yy*cc)/det
    if not all(math.isfinite(x) for x in (x1, x2)):
        raise OverflowError("solution exceeds float range")
    try:
        residual = (math.fsum((a*x1, b*x2, -y)),
                    math.fsum((c*x1, d*x2, -z)))
    except (OverflowError, ValueError) as exc:
        raise OverflowError("residual exceeds float range") from exc
    if not all(math.isfinite(x) for x in residual):
        raise OverflowError("residual exceeds float range")
    return {"solution": (x1, x2), "residual": residual,
            "normalized_determinant": det, "screening_threshold": threshold}

if __name__ == "__main__":
    print(solve_2x2([[1, 1], [1, 2]], [3, 5]))
