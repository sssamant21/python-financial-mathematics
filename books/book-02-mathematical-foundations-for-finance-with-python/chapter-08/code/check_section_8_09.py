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

def check_error_fields_and_gates():
    f=lambda x:x**3
    first=lambda x:3*x*x
    second=lambda x:6*x
    expected={"forward":(13.5625,1.5625),"backward":(10.5625,-1.4375),
              "centered":(12.0625,0.0625),"richardson":(12.0,0.0)}
    for absolute,relative in ((0.0625,0),(math.nextafter(0.0625,0),0),
                              (1/64,1/256),(0,0)):
        report=compare_derivatives(f,first,2,0.25,second,absolute,relative)
        assert report["abs_tol"]==absolute and report["rel_tol"]==relative
        assert report["comparison_rule"]=="abs(error) <= abs_tol + rel_tol*abs(analytic)"
        for method,(estimate,error) in expected.items():
            row=report["first_derivatives"][method]
            assert row["estimate"]==estimate
            assert row["signed_error"]==error and row["absolute_error"]==abs(error)
            assert row["pass"] is (abs(error)<=absolute+12*relative)
        row=report["second_derivative"]
        assert row["analytic"]==row["estimate"]==12
        assert row["signed_error"]==row["absolute_error"]==0 and row["pass"]
    boundary=compare_derivatives(f,first,2,0.25,abs_tol=0.0625,rel_tol=0)
    outside=compare_derivatives(f,first,2,0.25,abs_tol=math.nextafter(0.0625,0),rel_tol=0)
    assert boundary["first_derivatives"]["centered"]["pass"] is True
    assert outside["first_derivatives"]["centered"]["pass"] is False

    # Zero-reference gates depend on absolute tolerance; no division by zero.
    zero=compare_derivatives(lambda x:x*x,lambda x:0,0,0.25,lambda x:2,0,1)
    assert zero["first_derivatives"]["forward"]["signed_error"]==0.25
    assert zero["first_derivatives"]["backward"]["signed_error"]==-0.25
    assert not zero["first_derivatives"]["forward"]["pass"]
    assert not zero["first_derivatives"]["backward"]["pass"]
    assert zero["first_derivatives"]["centered"]["pass"]
    assert zero["second_derivative"]["pass"]

    # A wrong analytic oracle must not pass solely because the stencil is stable.
    wrong=compare_derivatives(f,lambda x:0,2,0.25,lambda x:0,0,0)
    assert all(not row["pass"] for row in wrong["first_derivatives"].values())
    assert wrong["second_derivative"]["pass"] is False
    assert wrong["second_derivative"]["signed_error"]==12
    assert wrong["second_derivative"]["absolute_error"]==12
    # Finite callback values may still overflow a stencil or error subtraction.
    rejects(ValueError,compare_derivatives,lambda z:1e308*z,lambda z:-1e308,
            0,1,None,0,2)
    rejects(ValueError,compare_derivatives,lambda z:1e308*z*z,lambda z:0,
            0,1,lambda z:0,0,0)
    first_only=compare_derivatives(f,first,2,0.25)
    assert "second_derivative" not in first_only

def run():
    check_error_fields_and_gates()
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
