"""Section 3.6: monotonicity and exact bounds for finite financial domains."""
from fractions import Fraction

def rational(x):
    if type(x) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(x)

def profit(q, price, variable_cost, fixed_cost):
    q,p,v,f=map(rational,(q,price,variable_cost,fixed_cost))
    if min(q,p,v,f)<0 or q.denominator!=1:
        raise ValueError("nonnegative costs and whole-unit quantity required")
    return (p-v)*q-f

def all_units_revenue(q, threshold=10, high_price=12, low_price=10):
    q,t,h,l=map(rational,(q,threshold,high_price,low_price))
    if min(q,t,h,l)<0 or q.denominator!=1 or t.denominator!=1:
        raise ValueError("whole-unit quantity/threshold and nonnegative values required")
    return q*(h if q<t else l)

def analyze(values):
    """Return monotonicity, exact extrema, and indices for finite ordered values."""
    vals=tuple(rational(v) for v in values)
    if not vals:
        raise ValueError("at least one value required")
    diffs=tuple(vals[i+1]-vals[i] for i in range(len(vals)-1))
    minimum,maximum=min(vals),max(vals)
    return {
        "nondecreasing":all(d>=0 for d in diffs),
        "nonincreasing":all(d<=0 for d in diffs),
        "strictly_increasing":all(d>0 for d in diffs),
        "strictly_decreasing":all(d<0 for d in diffs),
        "minimum":minimum,"maximum":maximum,
        "argmin":tuple(i for i,v in enumerate(vals) if v==minimum),
        "argmax":tuple(i for i,v in enumerate(vals) if v==maximum),
        "differences":diffs
    }

def bounded_profit(price,variable_cost,fixed_cost,capacity):
    cap=rational(capacity)
    if cap<0 or cap.denominator!=1:
        raise ValueError("capacity must be a nonnegative integer")
    return analyze(profit(q,price,variable_cost,fixed_cost) for q in range(int(cap)+1))

def main():
    print("Profit bounds:",bounded_profit(20,12,40,6))
    print("Discount threshold:",analyze(all_units_revenue(q) for q in range(12)))

if __name__=="__main__":
    main()
