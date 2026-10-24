"""Reference checks for Section 5.10 and representative Chapter 05 cases."""
import math
from section_5_10 import assessment_values
from section_5_09 import Period, run_engine, reconcile, closed_form_reference

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-10), (
        actual, expected)

def run():
    values = assessment_values()
    expected = {
        "geometric": 562.432,
        "recurrence_first": 1120,
        "recurrence_second": 1242.4,
        "timing_end": 1150,
        "timing_begin": 1155,
        "stable_equilibrium": 500,
        "tolerance_period": 36,
        "sensitivity": 6.5536,
        "shock": 106.1208,
        "variable_end": 1090.564,
        "variable_begin": 1093.1184,
    }
    assert values.keys() == expected.keys()
    for key, target in expected.items():
        close(values[key], target)
    periods = (Period(0.02, 100), Period(-0.01, -50), Period(0.03, 0))
    for timing in ("end", "begin"):
        result = run_engine(1000, periods, timing, allow_negative=False)
        close(result.closing, values["variable_" + timing])
        close(result.closing, closed_form_reference(1000, periods, timing))
        close(*reconcile(result))
    depletion = run_engine(500, (Period(0.01, -200),) * 3,
                           allow_negative=False)
    assert depletion.first_rejected == 3
    close(depletion.closing, 109.1305)
    close(*reconcile(depletion))
    exact = run_engine(1000, (Period(0, -250),) * 5,
                       allow_negative=False)
    assert exact.first_rejected == 5
    assert exact.ledger[3]["accepted"]
    close(exact.ledger[3]["closing"], 0)
    print("PASS: Section 5.10 cumulative reference checks")

if __name__ == "__main__":
    run()
