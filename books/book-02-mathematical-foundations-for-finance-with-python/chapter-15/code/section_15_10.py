"""Book 02 Section 15.10: Chapter 15 integrated assessment."""
import json
import math
from section_15_09 import assessment as engine_assessment
from section_15_08 import assessment as level_set_assessment
from section_15_07 import assessment as taylor_assessment

def finite(value):
    if isinstance(value,bool):
        return
    if isinstance(value,(float,int)):
        if not math.isfinite(value):
            raise ValueError("assessment produced nonfinite numeric value")
    elif isinstance(value,(tuple,list)):
        for item in value:
            finite(item)
    elif isinstance(value,dict):
        for item in value.values():
            finite(item)

def assessment():
    engine=engine_assessment()
    level=level_set_assessment()
    taylor=taylor_assessment()
    result={
        "chapter":"15 — Multivariable Calculus",
        "section":"15.10 — Exercises and Applied Problems",
        "worked_exercises":50,
        "hands_on_steps":12,
        "polynomial_base":15.0,
        "polynomial_gradient":(8.0,11.0),
        "polynomial_hessian":((2.0,3.0),(3.0,4.0)),
        "polynomial_exact_change":-1.37,
        "engine_base_values":engine["base_values"],
        "engine_exact_changes":engine["exact_changes"],
        "engine_first_order_changes":engine["first_order_changes"],
        "engine_second_order_changes":engine["second_order_changes"],
        "engine_portfolio_exact_change":engine["portfolio_exact_change"],
        "iso_value_slope":level["iso_value_slope"],
        "iso_variance_slope":level["unconstrained_iso_variance_slope"],
        "feasible_variance_derivative":level["fully_invested_derivative"],
        "future_value_taylor_change":taylor["future_value"]["second_order_change"],
        "runtime_certified":False,
        "independent_review_completed":False,
    }
    finite(result)
    return result

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
