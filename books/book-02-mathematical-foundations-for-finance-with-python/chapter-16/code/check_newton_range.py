"""Selected Newton/scalar quasi-Newton references, no BFGS/global claims."""
from fractions import Fraction
import math
from section_16_06 import newton_step, quasi_newton_step, newton_solve


def rejected(call, exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f"expected {exception.__name__}")


def check():
    # Combined exact rational updates have finite results even when a naive
    # intermediate product vanishes or quotient overflows.
    range_pairs = 0
    for sign in (-1,1):
        g = sign*2.0**-1000
        expected = float(-Fraction(2.0**-100)*Fraction(g)/Fraction(2.0**-1000))
        assert newton_step(0,lambda t:g,lambda t:2.0**-1000,2.0**-100) == expected
        range_pairs += 1
        x,g,h = sign*2.0**1023,sign*5*2.0**1021,0.5
        expected = float(Fraction(x)-Fraction(g)/Fraction(h))
        assert newton_step(x,lambda t:g,lambda t:h) == expected
        assert quasi_newton_step(x,lambda t:g,h) == expected
        range_pairs += 2
    # Exact f_a(x)=a*(x-b)^2/2: common positive objective scaling cancels
    # from Newton and from a quasi-Newton update supplied with exact curvature.
    b,x = Fraction(1,4),Fraction(3,2)
    scaling_pairs = 0
    for exponent in (-1000,-500,-20,0,20,500,1000):
        a = 2.0**exponent
        grad = lambda t: a*(t-float(b))
        hess = lambda t: a
        for damping in (1.0,0.5,0.25):
            expected = float(x-Fraction(damping)*(x-b))
            assert newton_step(float(x),grad,hess,damping) == expected
            scaling_pairs += 1
        assert quasi_newton_step(float(x),grad,a) == float(b)
        scaling_pairs += 1
        # Zero gradient tolerance prevents tiny objective scale from accepting
        # the initial point solely because its absolute gradient is small.
        solved = newton_solve(float(x),grad,hess,tolerance=0,max_iterations=1)
        assert solved['x'] == float(b) and solved['iterations'] == 1
        assert solved['status'] == 'gradient_tolerance'
    # A nondyadic result is rounded once, after combining the rational update.
    assert newton_step(1,lambda t:1,lambda t:3) == float(Fraction(2,3))
    assert quasi_newton_step(1,lambda t:1,3) == float(Fraction(2,3))
    tiny = newton_solve(1.5,lambda t:2.0**-1000*(t-0.25),lambda t:2.0**-1000)
    normal = newton_solve(1.5,lambda t:t-0.25,lambda t:1)
    assert tiny['iterations'] == 0 and tiny['x'] == 1.5
    assert normal['iterations'] == 1 and normal['x'] == 0.25
    assert tiny['status'] == normal['status'] == 'gradient_tolerance'
    invalid = 0
    for callback in (lambda t:True,lambda t:math.inf,lambda t:math.nan):
        expected = TypeError if callback(0) is True else ValueError
        rejected(lambda:newton_step(1,callback,lambda t:1),expected)
        rejected(lambda:quasi_newton_step(1,callback,1),expected)
        invalid += 2
    for curvature in (0,-1,math.inf,math.nan,True):
        expected = TypeError if curvature is True else ValueError
        rejected(lambda:newton_step(1,lambda t:1,lambda t:curvature),expected)
        rejected(lambda:quasi_newton_step(1,lambda t:1,curvature),expected)
        invalid += 2
    for damping in (0,-1,1.01,math.inf,True):
        rejected(lambda:newton_step(1,lambda t:1,lambda t:1,damping),
                 TypeError if damping is True else ValueError)
        invalid += 1
    rejected(lambda:newton_step(0,lambda t:2.0**1023,lambda t:0.25))
    rejected(lambda:quasi_newton_step(0,lambda t:2.0**1023,0.25))
    # Correct final rounding can legitimately reach zero or leave x unchanged.
    assert newton_step(0,lambda t:math.ulp(0.0),lambda t:2) == 0.0
    assert newton_step(1e20,lambda t:1,lambda t:1) == 1e20
    return {'finite_range_update_pairs':range_pairs,'scaled_update_pairs':scaling_pairs,
            'one_iteration_scaled_solves':7,'single_rounding_pairs':2,
            'absolute_stopping_scale_examples':2,'invalid_cases':invalid+2,
            'final_rounding_limits':2}


if __name__ == '__main__':
    print(check())
