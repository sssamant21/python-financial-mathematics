"""Direct project input/report contract checks for Section 13.9."""
import json
import math
from copy import deepcopy
from check_section_13_09 import inputs
from section_13_09 import analyze

def rejected(args, exception):
    try:
        analyze(*args)
    except exception:
        return
    raise AssertionError("expected " + exception.__name__)

def run():
    original = inputs()
    snapshot = deepcopy(original)
    report = analyze(*original)
    assert original == snapshot
    required = {"positions", "achieved", "residual_target_minus_achieved",
                "standardized_residual", "weighted_objective", "weighted_gradient",
                "factor_units", "factor_pass", "decision", "solver", "runtime_certified"}
    assert required <= report.keys()
    assert report["factor_units"] == original[6]
    assert report["solver"] == "educational_householder_qr"
    assert report["runtime_certified"] is False
    for factor, expected in (("RATE", -1/3), ("CREDIT", -1/3), ("LIQUIDITY", 1/3)):
        assert math.isclose(report["standardized_residual"][factor], expected, abs_tol=1e-12)
    encoded = json.dumps(report, sort_keys=True, allow_nan=False)
    assert encoded == json.dumps(analyze(*original), sort_keys=True, allow_nan=False)
    assert json.loads(encoded)["decision"] == "REJECT"
    # Direct project entry-point rejection, not only primitive helper coverage.
    for index in (2, 3, 4, 5):
        for invalid, exception in ((float("nan"), ValueError), (float("inf"), ValueError),
                                   (-float("inf"), ValueError), (True, TypeError)):
            args = deepcopy(list(original))
            if index == 2:
                rows = [list(row) for row in args[2]]
                rows[0][0] = invalid
                args[2] = rows
            else:
                args[index]["RATE"] = invalid
            rejected(args, exception)
    for index, invalid in ((4, 0), (4, -1), (5, -1)):
        args = deepcopy(list(original))
        args[index]["RATE"] = invalid
        rejected(args, ValueError)
    for index in (0, 1):
        args = list(original)
        args[index] = (args[index][0],) * len(args[index])
        rejected(args, ValueError)
    for rows in (((1, 0), (0, 1)), ((1, 0), (0,), (1, 1))):
        args = list(original)
        args[2] = rows
        rejected(args, ValueError)
    for invalid_units in ({"RATE": "unit"}, {"RATE": 1, "CREDIT": "unit", "LIQUIDITY": "unit"}):
        args = list(original)
        args[6] = invalid_units
        rejected(args, ValueError)
    print("PASS: Section 13.9 direct input and report contract checks")

if __name__ == "__main__":
    run()
