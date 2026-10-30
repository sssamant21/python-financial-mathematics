"""Exact represented-number secant contracts; scalar example, not BFGS."""
from fractions import Fraction
import math
from section_16_06 import scalar_secant_curvature


def rejected(call, exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f"expected {exception.__name__}")


def check():
    pairs = []
    # Independently known curvature of f(t)=t^2 is two. The product 2*s^2
    # can lie below/above float range while y/s remains exactly two.
    for exponent in (-600, -300, -30, 0, 300, 600):
        s = math.ldexp(1.0, exponent)
        for old, new in ((0.0, s), (s, 0.0)):
            exact_s = Fraction(new)-Fraction(old)
            exact_y = 2*exact_s
            assert exact_s*exact_y > 0
            actual = scalar_secant_curvature(old, new, lambda t: 2*t, threshold=0)
            assert Fraction(actual) == exact_y/exact_s == 2
            pairs.append((exponent, old == 0))
    # Strict comparison at an exactly representable product and its adjacent
    # thresholds. Reversing the pair changes both signs, not the product.
    h = 2.0**-20
    product = float(2*Fraction(h)**2)
    gates = 0
    for old, new in ((0.0,h),(h,0.0)):
        for threshold in (math.nextafter(product,0), product,
                          math.nextafter(product,math.inf)):
            expected = 2*(Fraction(new)-Fraction(old))**2 > Fraction(threshold)
            call = lambda: scalar_secant_curvature(old,new,lambda t: 2*t,threshold)
            if expected:
                assert call() == 2
            else:
                rejected(call)
            gates += 1
    # Exact product exceeds one, but its float multiplication rounds to one.
    s, y = math.nextafter(1.0,math.inf), math.nextafter(1.0,0.0)
    assert s*y == 1.0 and Fraction(s)*Fraction(y) > 1
    result = scalar_secant_curvature(0,s,lambda t: y if t else 0.0,1.0)
    assert result == float(Fraction(y)/Fraction(s))
    # Default absolute threshold intentionally rejects sufficiently small pairs.
    rejected(lambda: scalar_secant_curvature(0,2.0**-30,lambda t: 2*t))
    rejected(lambda: scalar_secant_curvature(0,2.0**-600,lambda t: 2*t,
                                           math.ulp(0.0)))
    invalid = 0
    for output in (True,False,math.inf,math.nan,"bad"):
        for at_new in (True,False):
            def callback(t):
                return output if bool(t)==at_new else (0.0 if at_new else 2.0)
            rejected(lambda: scalar_secant_curvature(0,1,callback,0),
                     TypeError if type(output) in (bool,str) else ValueError)
            invalid += 1
    for old,new,callback,threshold in (
        (1,1,lambda t: 2*t,0),
        (0,1,lambda t: -2*t,0),
        (0,1,lambda t: 1.0,0),
        (-1e308,1e308,lambda t: 0.0,0),
        (0,1,lambda t: 1e308 if t else -1e308,0),
        (0,1,lambda t: 2*t,-1),
        (0,1,lambda t: 2*t,math.inf),
        (0,2.0**1000,lambda t: 2.0**-1000 if t else 0.0,0),
        (0,2.0**-1000,lambda t: 2.0**1000 if t else 0.0,0),
    ):
        rejected(lambda: scalar_secant_curvature(old,new,callback,threshold))
        invalid += 1
    return {"exact_quadratic_pairs":len(pairs),"adjacent_threshold_gates":gates,
            "rounded_product_boundary":1,"absolute_threshold_rejections":2,
            "invalid_callback_or_range_cases":invalid}


if __name__ == "__main__":
    print(check())
