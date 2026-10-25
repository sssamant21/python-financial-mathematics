"""Section 9.2: elasticity calculations and financial interpretation."""
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

def point_elasticity(x, value, derivative):
    x, y, d = finite(x, "x"), finite(value, "value"), finite(derivative, "derivative")
    if x == 0 or y == 0:
        raise ValueError("point elasticity requires nonzero input and output")
    return x*d/y

def arc_elasticity(x1, x2, y1, y2):
    x1, x2, y1, y2 = (finite(v,n) for v,n in
                       ((x1,"x1"),(x2,"x2"),(y1,"y1"),(y2,"y2")))
    if x1 == x2 or x1+x2 == 0 or y1+y2 == 0:
        raise ValueError("midpoint arc elasticity denominators must be nonzero")
    return ((y2-y1)/(0.5*(y1+y2)))/((x2-x1)/(0.5*(x1+x2)))

def constant_elasticity_demand(price, scale=400, exponent=-1.5):
    p, a, e = finite(price,"price"), finite(scale,"scale"), finite(exponent,"exponent")
    if p <= 0 or a <= 0:
        raise ValueError("price and scale must be positive")
    q = a*p**e
    return {"quantity":q,"derivative":e*q/p,
            "elasticity":point_elasticity(p,q,e*q/p)}

def linear_demand(price, intercept=100, slope=2):
    p, a, b = finite(price,"price"), finite(intercept,"intercept"), finite(slope,"slope")
    if p <= 0 or a <= 0 or b <= 0 or a-b*p <= 0:
        raise ValueError("require positive price, intercept, slope, and quantity")
    q = a-b*p
    return {"quantity":q,"derivative":-b,
            "elasticity":point_elasticity(p,q,-b),
            "revenue":p*q,"revenue_derivative":q-b*p}

def income_elasticity(income, scale=5, exponent=0.7):
    i, a, e = finite(income,"income"), finite(scale,"scale"), finite(exponent,"exponent")
    if i <= 0 or a <= 0:
        raise ValueError("income and scale must be positive")
    q = a*i**e
    return point_elasticity(i,q,e*q/i)

def discounted_rate_elasticity(rate, years):
    r, t = finite(rate,"rate"), finite(years,"years")
    if r == 0 or t < 0:
        raise ValueError("rate must be nonzero and years nonnegative")
    return -r*t

def centered_elasticity(function, x, step=1e-4):
    if not callable(function):
        raise TypeError("function must be callable")
    x, h = finite(x,"x"), finite(step,"step")
    if x == 0 or h <= 0 or x+h == x or x-h == x:
        raise ValueError("nonzero input and representable positive step required")
    value = finite(function(x),"f(x)")
    derivative = (finite(function(x+h),"f(x+h)")-
                  finite(function(x-h),"f(x-h)"))/(2*h)
    return point_elasticity(x,value,derivative)

if __name__ == "__main__":
    print("Constant elasticity:",constant_elasticity_demand(20))
    print("Linear demand at 10:",linear_demand(10))
    print("Linear demand at 25:",linear_demand(25))
    print("Income elasticity:",income_elasticity(50000))
    print("Discounted rate elasticity:",discounted_rate_elasticity(0.04,5))
    print("Midpoint arc elasticity:",arc_elasticity(10,12,80,70))
