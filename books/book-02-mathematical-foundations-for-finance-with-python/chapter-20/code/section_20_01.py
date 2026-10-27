"""Book 02 Section 20.1: present-value verification lab (draft)."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def present_value(cash_flow,continuous_rate,years):
    flow=finite(cash_flow,"cash_flow")
    rate=finite(continuous_rate,"continuous_rate")
    time=finite(years,"years")
    if time<0:
        raise ValueError("years must be nonnegative")
    try:
        value=flow*math.exp(-rate*time)
    except OverflowError as exc:
        raise ValueError("present value overflow") from exc
    return finite(value,"present_value")

def assess():
    return {
        "zero_rate":present_value(1000,0,5),
        "zero_horizon":present_value(1000,0.05,0),
        "known_value":present_value(1000,0.05,2),
        "negative_rate":present_value(1000,-0.02,2),
        "additivity_left":present_value(400+600,0.05,2),
        "additivity_right":present_value(400,0.05,2)+present_value(600,0.05,2),
        "requirements":{"finite_inputs":"source_authored",
                        "nonnegative_horizon":"source_authored",
                        "analytic_oracle":"source_authored",
                        "assumption_review":"pending"},
        "runtime_certified":False,
        "independent_review_completed":False
    }

if __name__=="__main__":
    print(json.dumps(assess(),indent=2,allow_nan=False))
