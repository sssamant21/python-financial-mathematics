"""Reference checks for Section 8.8."""
import math
from section_8_08 import (
    finite, validated_step, forward_difference, backward_difference,
    centered_difference, second_difference, suggested_step,
    richardson_first, discounted_price, rate_sensitivity)

def close(a, b, rel_tol=1e-7, abs_tol=1e-7):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def check_helper_guards():
    methods=(forward_difference,backward_difference,centered_difference,
             second_difference,richardson_first)
    for method in methods:
        for x,h,exc in ((1,0,ValueError),(1,-0.1,ValueError),
                        (1,1e-30,ValueError),(1,True,TypeError),
                        (True,0.1,TypeError),(math.inf,0.1,ValueError),
                        (1e308,1e308,ValueError)):
            calls=[]
            def callback(z):
                calls.append(z)
                return z
            rejects(exc,method,callback,x,h)
            assert not calls
        rejects(ValueError,method,lambda z:math.nan,0,0.25)
        rejects(TypeError,method,lambda z:True,0,0.25)
        assert method(lambda z:3*z+4,0,0.25)==(0 if method is second_difference else 3)
    # Finite callback results can still overflow the subtraction or stencil.
    rejects(ValueError,forward_difference,lambda z:-1e308 if z==0 else 1e308,0,1)
    rejects(ValueError,backward_difference,lambda z:1e308 if z==0 else -1e308,0,1)
    rejects(ValueError,centered_difference,lambda z:1e308*z,0,1)
    rejects(ValueError,second_difference,lambda z:1e308*z*z,0,1)
    # Equivalent Richardson rearrangement avoids the overflowing 4*fine product.
    assert richardson_first(lambda z:1e308*z,0,0.25)==1e308
    for h in (1e-200,1e200):
        calls=[]
        rejects(ValueError,second_difference,lambda z:calls.append(z) or z*z,0,h)
        assert not calls
    calls=[]
    rejects(ValueError,centered_difference,lambda z:calls.append(z) or z,0,1e308)
    assert not calls
    # h works at full scale but h/2 is too small at the selected base point.
    rejects(ValueError,richardson_first,lambda z:z,1,2.0**-52)

def run():
    check_helper_guards()
    f = lambda x:x**3
    close(forward_difference(f, 2, 0.1), 12.61)
    close(backward_difference(f, 2, 0.1), 11.41)
    close(centered_difference(f, 2, 0.1), 12.01)
    close(richardson_first(f, 2, 0.1), 12, rel_tol=1e-10)
    for x in (-3, -1, 0, 1, 3):
        close(second_difference(lambda z:z*z, x, 0.01), 2, rel_tol=1e-9)
        close(centered_difference(lambda z:3*z+4, x, 0.01), 3)
    for order in (1, 2):
        h = suggested_step(0.04, order)
        assert h > 0
        validated_step(0.04, h)
    assert suggested_step(0.04, 2) > suggested_step(0.04, 1)
    close(discounted_price(1000, 5, 0.04), 1000*math.exp(-0.2))
    result = rate_sensitivity(1000, 5, 0.04, 1e-3)
    close(result["duration"], 5, rel_tol=1e-5)
    close(result["convexity"], 25, rel_tol=1e-5)
    close(centered_difference(abs, 0, 0.1), 0)
    assert forward_difference(abs, 0, 0.1) == 1
    assert backward_difference(abs, 0, 0.1) == -1
    rejects(ValueError, validated_step, 1, 0)
    rejects(ValueError, validated_step, 1, 1e-20)
    rejects(ValueError, suggested_step, 1, 3)
    rejects(ValueError, suggested_step, 1, 1, -1)
    rejects(ValueError, discounted_price, 0, 5, 0.04)
    rejects(ValueError, discounted_price, 1000, -1, 0.04)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.8 reference checks")

if __name__ == "__main__":
    run()
