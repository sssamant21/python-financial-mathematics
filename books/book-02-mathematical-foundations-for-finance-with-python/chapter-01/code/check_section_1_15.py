"""Executable examples for all twenty problems, not automatic prose grading."""
from copy import deepcopy
from fractions import Fraction as Q
import json
from section_1_15 import reference_results, exercise_batch, repaired_batch
from section_1_06 import equation_residual
from section_1_12 import compound_balance
from section_1_14 import run_batch

assert __debug__, "run without -O: assertions are required"
results = reference_results()
expected = {
    "01": [26, 25, 25, 25],
    "02": ["2601/5", "2704/5"],
    "03": [True, True, False, False],
    "04": "0",
    "05": [["unique", "5"], ["all", None], ["none", None]],
    "06": {"maximum": "500", "slacks": ["0", "-1/10"]},
    "07": [False, True, True],
    "08": {"profit": -20, "implication": False},
    "09": [1, 2],
    "10": ["1/200", "1/200"],
    "11": {"value": "1000", "percentage_points": "3/4", "basis_points": "75", "relative_change": "1/4"},
    "12": ["2", "144/73"],
    "13": {"minimum": "500", "fee": "16", "source_after": "684", "destination_after": "650", "higher_target": None},
    "14": {"correct": "125", "wrong_grouping": "10000", "power": 8, "xor": 1},
    "15": {"discounted": "0", "zero_rate": "62/5", "time_two": "100", "time_one": "110"},
    "16": [False, True],
    "17": {"reference": "363", "discrepancy": "-33", "relative_error": "1/11", "weak_checks": [True, True]},
    "18": {"counts": {"PASS": 1, "FAIL": 1, "INVALID": 1}, "success": False},
    "19": {"counts": {"PASS": 3, "FAIL": 0, "INVALID": 0}, "success": True},
    "20": {"balance": "11592740743/100000000", "scaled": "11592740743/25000000", "scaling_holds": True, "mistake_rejected": True},
}
assert set(results) == set(expected)
for number in expected:
    assert results[number] == expected[number], (number, results[number], expected[number])
# Structural checks support the interpretation in the worked solutions.
assert sum(results["01"]) == 101 and max(results["01"])-min(results["01"]) == 1
assert equation_residual(a=2, b=7, c=1, d=12, x=5) == 0
assert Q(results["13"]["source_after"])+Q(results["13"]["destination_after"]) == 1350-Q(16)
batch = exercise_batch()
before = deepcopy(batch)
repaired = repaired_batch(batch)
assert batch == before
report = run_batch(batch)
checks = report["cases"][2]["checks"]
assert not checks["source_reserve"] and all(v for k,v in checks.items() if k != "source_reserve")
assert run_batch(repaired)["success"]
duplicate = deepcopy(batch)
duplicate["cases"][1]["id"] = duplicate["cases"][0]["id"]
try:
    run_batch(duplicate)
except ValueError:
    pass
else:
    raise AssertionError("duplicate IDs accepted")
for operation, error in [
    (lambda: compound_balance(principal=100, period_rate="0.03", periods=True), TypeError),
    (lambda: compound_balance(principal=100, period_rate=-1, periods=1), ValueError),
    (lambda: compound_balance(principal=100, period_rate="0.03", periods=-1), ValueError),
]:
    try:
        operation()
    except error:
        pass
    else:
        raise AssertionError("invalid growth input accepted")
print("PASS: " + json.dumps({"problem_reference_checks": len(expected), "batch_immutability": True,
                            "duplicate_id_rejected": True, "invalid_growth_cases": 3}, sort_keys=True))
