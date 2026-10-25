"""Independent reference checks for Section 8.9 comparator."""
import math
from section_8_09 import (
    finite, compare_derivatives, step_ladder, accumulation_model,
    discounted_cash_flow_model, profit_model, ratio_model, run_demo)

def close(a, b, rel_tol=1e-7, abs_tol=1e-7):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a,b)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    f = lambda x:x**3
    d1 = lambda x:3*x*x
    d2 = lambda x:6*x
    result = compare_derivatives(f,d1,2,0.1,d2,abs_tol=0.02,rel_tol=0)
    close(result["analytic_first"],12)
    close(result["first_derivatives"]["forward"]["estimate"],12.61)
    close(result["first_derivatives"]["backward"]["estimate"],11.41)
    close(result["first_derivatives"]["centered"]["estimate"],12.01)
    close(result["first_derivatives"]["richardson"]["estimate"],12)
    close(result["second_derivative"]["estimate"],12)
    assert result["first_derivatives"]["centered"]["pass"]
    assert not result["first_derivatives"]["forward"]["pass"]
    for factory in (accumulation_model,discounted_cash_flow_model,
                    profit_model,ratio_model):
        function, first, second, x, unit = factory()
        assert unit
        reports = step_ladder(function,first,x,(1e-2,1e-3,1e-4),second)
        assert len(reports)==3
        for item in reports:
            close(item["analytic_first"],first(x))
            close(item["second_derivative"]["analytic"],second(x))
        assert reports[1]["first_derivatives"]["centered"]["pass"]
        assert reports[1]["second_derivative"]["pass"]
    _, d1_profit, d2_profit, x_profit, _ = profit_model()
    close(d1_profit(x_profit),0)
    close(d2_profit(x_profit),-0.5)
    _, d1_pv, d2_pv, x_rate, _ = discounted_cash_flow_model()
    assert d1_pv(x_rate)<0 and d2_pv(x_rate)>0
    _, d1_ratio, d2_ratio, x_ratio, _ = ratio_model()
    assert d1_ratio(x_ratio)>0 and d2_ratio(x_ratio)<0
    assert len(run_demo())==4
    rejects(ValueError, compare_derivatives, f, d1, 1, 0)
    rejects(ValueError, compare_derivatives, f, d1, 1, 1e-20)
    rejects(ValueError, compare_derivatives, f, d1, 1, 0.01, None, -1)
    rejects(TypeError, compare_derivatives, f, None, 1, 0.01)
    rejects(ValueError, compare_derivatives, ratio_model()[0], ratio_model()[1],
            0.0001, 0.01)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    # Nonsmooth function: a zero centered estimate at the kink is not a derivative.
    kink = compare_derivatives(abs,lambda x:0,0,0.01)
    close(kink["first_derivatives"]["centered"]["estimate"],0)
    assert kink["first_derivatives"]["forward"]["estimate"]==1
    assert kink["first_derivatives"]["backward"]["estimate"]==-1
    print("PASS: Section 8.9 independent reference checks")

if __name__ == "__main__":
    run()
