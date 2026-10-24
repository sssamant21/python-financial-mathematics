"""Project acceptance: classifications, exact values, schema failures, and CLI."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from section_1_14 import load_document, run_batch

assert __debug__, "run without -O: assertions are required"
counts = {}


def record(category):
    counts[category] = counts.get(category, 0) + 1


chapter = Path(__file__).resolve().parents[1]
fixture = chapter / "data" / "section-1.14-cases.json"
program = chapter / "code" / "section_1_14.py"
document = load_document(fixture)
original = deepcopy(document)
report = run_batch(document)
assert document == original
assert report["counts"] == {"PASS": 4, "FAIL": 2, "INVALID": 2}
assert not report["success"]
assert [row["status"] for row in report["cases"]] == [
    "PASS", "FAIL", "INVALID", "PASS", "INVALID", "PASS", "FAIL", "PASS"]
assert report["cases"][1]["details"]["discrepancy"] == "-11"
breach = report["cases"][6]["checks"]
assert not breach["source_reserve"]
assert all(value for name, value in breach.items() if name != "source_reserve")
assert report["cases"][2]["checks"] == {} and report["cases"][2]["details"] is None
json.dumps(report, allow_nan=False)
record("fixture_cases")


def one(case):
    return run_batch({"schema_version": 1, "cases": [case]})["cases"][0]


growth, accrual, transfer = [deepcopy(document["cases"][i]) for i in (0, 3, 5)]
for p, r, n in product([0, 1, 100], [Q(-1, 10), Q(0), Q(1, 10)], [0, 1, 3]):
    expected = Q(p)
    for _ in range(n):
        expected += expected * r
    case = deepcopy(growth)
    case["inputs"] = {"principal": p, "rate": str(r), "representation": "decimal", "periods": n}
    case["observed"] = str(expected)
    assert one(case)["status"] == "PASS"
    case["observed"] = str(expected + 1)
    assert one(case)["status"] == "FAIL"
    record("growth_reference_cases")
for value, representation in [("0.10", "decimal"), (10, "percent"), (1000, "basis_points")]:
    case = deepcopy(growth)
    case["inputs"].update(rate=value, representation=representation)
    assert one(case)["details"]["reference"] == "121"
    assert one(case)["status"] == "PASS"
    record("rate_equivalence_cases")
case = deepcopy(accrual)
case["inputs"]["convention"] = "ACT/365F"
case["observed"] = "3600/73"
assert one(case)["status"] == "PASS"
case["observed"] = 50
assert one(case)["status"] == "FAIL"
case["inputs"].update(start="2024-02-28", end="2024-03-01", convention="ACT/360")
case["observed"] = "10/3"
assert one(case)["status"] == "PASS"
record("accrual_exact_cases")
case = deepcopy(transfer)
case["inputs"].update(source=300, destination=200, reserve=300, target=200, transfer=0)
case["observed"] = {"fee": 0, "source_after": 300, "destination_after": 200}
assert one(case)["status"] == "PASS"
case["observed"]["fee"] = 5
assert one(case)["status"] == "FAIL"
record("zero_transfer_cases")
for field in transfer["observed"]:
    case = deepcopy(transfer)
    case["observed"][field] += 1
    result = one(case)
    assert result["status"] == "FAIL" and not result["checks"][field + "_agreement"]
    record("transfer_observation_cases")
# Exact-key failures are checked across all three model interfaces.
for template in (growth, accrual, transfer):
    for key in template["inputs"]:
        case = deepcopy(template)
        del case["inputs"][key]
        assert one(case)["status"] == "INVALID"
        record("schema_rejection_cases")
    case = deepcopy(template)
    case["inputs"]["unexpected"] = 1
    assert one(case)["status"] == "INVALID"
    record("schema_rejection_cases")
invalid_cases = []
for patch in [{"currency": "usd"}, {"currency": "US"}, {"formula": "unknown"},
              {"observed": None}, {"observed": True}, {"observed": 121.0}]:
    invalid_cases.append(deepcopy(growth) | patch)
for patch in [{"periods": True}, {"periods": -1}, {"periods": 121},
              {"rate": .1}, {"rate": -100}, {"representation": "pct"}]:
    case = deepcopy(growth)
    case["inputs"].update(patch)
    invalid_cases.append(case)
for patch in [{"start": "2025-02-30"}, {"start": "20250101"},
              {"start": "2026-01-01"}, {"convention": "ACT/365"}]:
    case = deepcopy(accrual)
    case["inputs"].update(patch)
    invalid_cases.append(case)
case = deepcopy(transfer)
case["observed"] = {"fee": 10}
invalid_cases.append(case)
for case in invalid_cases:
    assert one(case)["status"] == "INVALID"
    record("domain_rejection_cases")
malformed = [{}, {"schema_version": True, "cases": [growth]},
             {"schema_version": 2, "cases": [growth]},
             {"schema_version": 1, "cases": []},
             {"schema_version": 1, "cases": [growth, growth]},
             {"schema_version": 1, "cases": [{}]},
             {"schema_version": 1, "cases": [growth] * 101}]
for batch in malformed:
    try:
        run_batch(batch)
    except ValueError:
        pass
    else:
        raise AssertionError("malformed batch accepted")
    record("batch_rejection_cases")
with TemporaryDirectory() as directory:
    root = Path(directory)
    path, output = root / "input.json", root / "report.json"

    def cli(expected, *arguments):
        result = subprocess.run([sys.executable, str(program), *map(str, arguments)],
                                capture_output=True, text=True)
        assert result.returncode == expected, (result.returncode, result.stdout, result.stderr)
        record("cli_cases")
        return result

    mixed = cli(1, fixture, "--output", output)
    assert mixed.stdout.rstrip().endswith("PASS=4 FAIL=2 INVALID=2")
    assert json.loads(output.read_text()) == report
    all_pass = {"schema_version": 1, "cases": [deepcopy(document["cases"][i]) for i in (0, 3, 5, 7)]}
    path.write_text(json.dumps(all_pass))
    cli(0, path, "--output", output)
    assert json.loads(output.read_text())["success"]
    before = path.read_bytes()
    cli(2, path, "--output", path)
    assert path.read_bytes() == before
    for payload in ['{"schema_version":1,"schema_version":1,"cases":[]}',
                    '{"schema_version":1,"cases":[],"x":NaN}',
                    '{"schema_version":1,"cases":[],"x":Infinity}',
                    '{', '{"schema_version":1,"cases":[]}']:
        path.write_text(payload)
        cli(2, path)
    path.write_bytes(b'\xff')
    cli(2, path)
    path.write_bytes(b' ' * 1_000_001)
    cli(2, path)
    cli(2, root / "missing.json")
    cli(2, "--unsupported")
print("PASS: " + json.dumps(counts, sort_keys=True))
