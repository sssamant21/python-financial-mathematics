"""Integrated synthetic teaching scenario; validation and approval pending."""
import math
from section_21_03 import present_value
from section_21_04 import derivatives, central_difference
from section_21_05 import solve_2x2
from section_21_06 import solve
from section_21_07 import scenario_report

def build_report():
    analytic = derivatives(100, 0, 2)
    step = 1e-5
    numeric = central_difference(100, 0, 2, step)
    error = numeric - analytic[0]
    replication = solve_2x2([[1, 1], [1, 2]], [3, 5])
    allocation = solve(.7, .2)
    return {
        "purpose": "educational synthetic scenario",
        "cash_flow": {"inputs": {"amount": 100, "years": 1, "continuous_rate": math.log(2)},
                      "value": present_value([(100, 1)], math.log(2), "continuous"),
                      "units": "currency"},
        "sensitivity": {"inputs": {"amount": 100, "rate": 0, "years": 2},
                        "first_second": analytic,
                        "finite_difference": {"method": "centered first derivative",
                                              "step": step, "estimate": numeric,
                                              "signed_error": error,
                                              "absolute_error": abs(error),
                                              "units": "currency per decimal-rate unit"},
                        "units": "currency per decimal-rate unit and its square"},
        "replication": {"inputs": {"matrix": [[1, 1], [1, 2]], "target": [3, 5]}, **replication},
        "allocation": {"inputs": {"target_a": .7, "target_b": .2,
                                  "constraints": "long-only; weights sum to one"}, **allocation},
        "account": scenario_report(1000, 0, 200, 3),
        "limitations": ["synthetic examples are separate, not one investable portfolio",
                        "replication solver is limited to 2x2",
                        "allocation objective is a specific teaching example",
                        "account is unconstrained"],
        "validation_execution": "not run",
        "independent_review": "pending",
        "approval": "pending",
    }

if __name__ == "__main__":
    import json
    print(json.dumps(build_report(), sort_keys=True, indent=2, allow_nan=False))
