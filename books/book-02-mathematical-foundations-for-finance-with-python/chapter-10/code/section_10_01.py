"""Section 10.1: accumulation and Riemann sums."""
import json
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def boundaries(a, b, n):
    left, right = finite(a, "a"), finite(b, "b")
    if type(n) is not int or n <= 0:
        raise ValueError("n must be a positive integer")
    if not left < right:
        raise ValueError("require a < b")
    step = (right-left)/n
    if not math.isfinite(step) or step <= 0:
        raise ValueError("invalid partition width")
    points = [left+(right-left)*i/n for i in range(n)]
    points.append(right)
    if any(x >= y for x, y in zip(points, points[1:])):
        raise ValueError("partition points are not distinct")
    return points

def riemann_sum(function, partition, rule="midpoint"):
    if not callable(function):
        raise TypeError("function must be callable")
    if rule not in ("left", "right", "midpoint"):
        raise ValueError("rule must be left, right, or midpoint")
    points = [finite(x, "partition point") for x in partition]
    if len(points) < 2 or any(x >= y for x, y in zip(points, points[1:])):
        raise ValueError("partition must contain strictly increasing points")
    terms = []
    for a, b in zip(points, points[1:]):
        sample = a if rule == "left" else b if rule == "right" else a+(b-a)/2
        rate = finite(function(sample), "payment rate")
        terms.append(rate*(b-a))
    total = math.fsum(terms)
    if not math.isfinite(total):
        raise ValueError("nonfinite accumulated amount")
    return total

def uniform_sums(function, a, b, n):
    points = boundaries(a, b, n)
    return {"n":n, "mesh":max(y-x for x,y in zip(points,points[1:])),
            "left":riemann_sum(function,points,"left"),
            "right":riemann_sum(function,points,"right"),
            "midpoint":riemann_sum(function,points,"midpoint")}

def convergence_report(function, a, b, counts, exact):
    target = finite(exact, "exact")
    rows = []
    for n in counts:
        row = uniform_sums(function, a, b, n)
        for rule in ("left","right","midpoint"):
            row[rule+"_absolute_error"] = abs(row[rule]-target)
        rows.append(row)
    return {"interval":[finite(a,"a"),finite(b,"b")],
            "exact":target,"rows":rows}

if __name__ == "__main__":
    result = {
        "linear":convergence_report(lambda t:100+20*t,0,2,[2,4,8,16],240),
        "quadratic":convergence_report(lambda t:t*t,0,1,[2,4,8,16,32],1/3),
        "nonuniform":riemann_sum(lambda t:100+20*t,[0,0.2,0.7,2],"midpoint")}
    print(json.dumps(result,indent=2,allow_nan=False))
