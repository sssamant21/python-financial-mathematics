"""Chapter 01 project: exact, schema-driven financial formula checks."""
import argparse
from datetime import date
from fractions import Fraction
import json
from pathlib import Path
from section_1_10 import decimal_rate, simple_accrual
from section_1_11 import evaluate_transfer
from section_1_12 import rational
from section_1_13 import audit_growth


COMMON_KEYS = {"id", "formula", "currency", "inputs", "observed"}
INPUT_KEYS = {
    "growth": {"principal", "rate", "representation", "periods"},
    "simple_accrual": {"principal", "rate", "representation", "start", "end", "convention"},
    "transfer": {"source", "destination", "reserve", "target", "fixed_fee", "fee_rate", "transfer"},
}
TRANSFER_OBSERVED = {"fee", "source_after", "destination_after"}


def exact_keys(value, expected, label):
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"{label} must contain exactly: {', '.join(sorted(expected))}")


def iso_date(value):
    if type(value) is not str:
        raise TypeError("dates must be YYYY-MM-DD strings")
    result = date.fromisoformat(value)
    if result.isoformat() != value:
        raise ValueError("dates must use YYYY-MM-DD format")
    return result


def currency_label(value):
    if (type(value) is not str or len(value) != 3
            or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in value)):
        raise ValueError("currency must be an uppercase three-letter label")


def json_ready(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    return value


def evaluate_case(case):
    """Batch validation establishes a dictionary and stable ID first."""
    result = {"id": case["id"], "submitted": case}
    try:
        exact_keys(case, COMMON_KEYS, "case")
        currency_label(case["currency"])
        name = case["formula"]
        if type(name) is not str or name not in INPUT_KEYS:
            raise ValueError("unsupported formula")
        inputs = case["inputs"]
        exact_keys(inputs, INPUT_KEYS[name], "inputs")
        if name == "growth":
            periods = inputs["periods"]
            if type(periods) is not int or not 0 <= periods <= 120:
                raise ValueError("project growth horizon must be an integer from 0 to 120")
            rate = decimal_rate(inputs["rate"], representation=inputs["representation"])
            detail = audit_growth(principal=inputs["principal"], period_rate=rate,
                                  periods=periods, candidate=case["observed"])
            checks = detail["checks"]
        elif name == "simple_accrual":
            args = dict(inputs)
            args["start"], args["end"] = iso_date(args["start"]), iso_date(args["end"])
            detail = simple_accrual(currency=case["currency"], **args)
            observed = rational(case["observed"])
            checks = {"interest_agreement": observed == detail["interest"]}
            detail = {**detail, "discrepancy": observed - detail["interest"]}
        else:
            exact_keys(case["observed"], TRANSFER_OBSERVED, "transfer observed")
            detail = evaluate_transfer(**inputs)
            checks = {key + "_agreement": rational(case["observed"][key]) == detail[key]
                      for key in sorted(TRANSFER_OBSERVED)}
            checks.update(detail["checks"])
        result.update(status="PASS" if all(checks.values()) else "FAIL",
                      checks=checks, details=detail, error=None)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        result.update(status="INVALID", checks={}, details=None,
                      error=f"{type(exc).__name__}: {exc}")
    return json_ready(result)


def run_batch(document):
    exact_keys(document, {"schema_version", "cases"}, "document")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    cases = document["cases"]
    if type(cases) is not list or not 1 <= len(cases) <= 100:
        raise ValueError("provide 1 to 100 cases")
    ids = []
    for case in cases:
        if type(case) is not dict or type(case.get("id")) is not str or not case["id"].strip():
            raise ValueError("each case needs a nonempty string id")
        ids.append(case["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("case ids must be unique")
    results = [evaluate_case(case) for case in cases]
    counts = {status: sum(row["status"] == status for row in results)
              for status in ("PASS", "FAIL", "INVALID")}
    return {"schema_version": 1, "comparison": "exact rational",
            "scope": "declared cases and registered models only",
            "counts": counts, "success": counts["PASS"] == len(results), "cases": results}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_document(path):
    with Path(path).open("rb") as stream:
        payload = stream.read(1_000_001)
    if len(payload) > 1_000_000:
        raise ValueError("project input exceeds 1,000,000 bytes")
    return json.loads(payload.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    default = Path(__file__).resolve().parents[1] / "data" / "section-1.14-cases.json"
    parser.add_argument("cases", nargs="?", type=Path, default=default)
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.resolve() == args.cases.resolve():
            raise ValueError("output must not overwrite input")
        report = run_batch(load_document(args.cases))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"input/output error: {exc}\n")
    for row in report["cases"]:
        print(f"{row['id']}: {row['status']}")
    print(" ".join(f"{name}={count}" for name, count in report["counts"].items()))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
