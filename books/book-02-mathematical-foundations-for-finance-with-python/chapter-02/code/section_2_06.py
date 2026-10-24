"""Exact linear bounds, absolute affine bands, and interval intersections."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def interval(lower=None, upper=None, *, left_closed=True, right_closed=True):
    if type(left_closed) is not bool or type(right_closed) is not bool:
        raise TypeError("endpoint flags must be Boolean")
    lo = None if lower is None else rational(lower)
    hi = None if upper is None else rational(upper)
    lc, rc = left_closed and lo is not None, right_closed and hi is not None
    if lo is not None and hi is not None:
        if lo > hi or (lo == hi and not (lc and rc)):
            return None
    return {"lower": lo, "upper": hi, "left_closed": lc, "right_closed": rc}


def contains(region, value):
    x = rational(value)
    if region is None:
        return False
    lo, hi = region["lower"], region["upper"]
    left = lo is None or x > lo or (x == lo and region["left_closed"])
    right = hi is None or x < hi or (x == hi and region["right_closed"])
    return left and right


def intersect(left, right):
    if left is None or right is None:
        return None
    regions = (left, right)
    lowers = [r["lower"] for r in regions if r["lower"] is not None]
    uppers = [r["upper"] for r in regions if r["upper"] is not None]
    lo, hi = max(lowers) if lowers else None, min(uppers) if uppers else None
    lc = all(r["lower"] != lo or r["left_closed"] for r in regions)
    rc = all(r["upper"] != hi or r["right_closed"] for r in regions)
    return interval(lo, hi, left_closed=lc, right_closed=rc)


def linear_upper(*, coefficient, constant, limit, strict=False):
    if type(strict) is not bool:
        raise TypeError("strict must be Boolean")
    a, b, bound = map(rational, (coefficient, constant, limit))
    if a == 0:
        holds = b < bound if strict else b <= bound
        return interval() if holds else None
    endpoint = (bound - b) / a
    if a > 0:
        return interval(upper=endpoint, right_closed=not strict)
    return interval(lower=endpoint, left_closed=not strict)


def absolute_band(*, coefficient, constant, threshold, strict=False):
    if type(strict) is not bool:
        raise TypeError("strict must be Boolean")
    a, b, width = map(rational, (coefficient, constant, threshold))
    if width < 0:
        return None
    if a == 0:
        holds = abs(b) < width if strict else abs(b) <= width
        return interval() if holds else None
    lo, hi = sorted(((-width - b) / a, (width - b) / a))
    return interval(lo, hi, left_closed=not strict, right_closed=not strict)


def display(region):
    if region is None:
        return "empty"
    lo = "-inf" if region["lower"] is None else str(region["lower"])
    hi = "+inf" if region["upper"] is None else str(region["upper"])
    return ("[" if region["left_closed"] else "(") + lo + ", " + hi + ("]" if region["right_closed"] else ")")


def main():
    bound = linear_upper(coefficient=-2, constant=10, limit=4)
    band = absolute_band(coefficient=-2, constant=4, threshold=2)
    weights = absolute_band(coefficient=1, constant="-0.5", threshold="0.1")
    cap = linear_upper(coefficient=1, constant=0, limit="0.55", strict=True)
    feasible = intersect(intersect(weights, interval(0, 1)), cap)
    print("Negative-coefficient bound:", display(bound))
    print("Absolute affine band:", display(band))
    print("Weight band and strict cap:", display(feasible))
    print("Upper weight boundary accepted:", contains(feasible, "0.55"))
    print("Strict zero-width band:", display(absolute_band(
        coefficient=1, constant=0, threshold=0, strict=True)))
    # Profit roots and sign analysis were derived in the manuscript.
    profit_region = interval(20, 80)
    print("Nonnegative profit with capacity 60:", display(intersect(profit_region, interval(0, 60))))


if __name__ == "__main__":
    main()
