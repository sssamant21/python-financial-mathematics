"""Twenty chapter-wide reference examples; written reasoning is separate."""
from copy import deepcopy
from datetime import date
from fractions import Fraction as Q
import json
from section_1_02 import split_minor_units
from section_1_04 import interval_contains
from section_1_06 import solve_linear_equation, equation_residual
from section_1_07 import maximum_transaction_amount, transaction_report
from section_1_08 import implies
from section_1_09 import fee_metrics
from section_1_10 import simple_accrual
from section_1_11 import minimum_transfer
from section_1_12 import compound_balance, present_value
from section_1_13 import audit_growth, compare_finite
from section_1_14 import run_batch, json_ready


def exercise_batch():
    return {"schema_version": 1, "cases": [
        {"id": "p18-correct", "formula": "growth", "currency": "USD",
         "inputs": {"principal": 200, "rate": 5, "representation": "percent", "periods": 2},
         "observed": "220.5"},
        {"id": "p18-missing", "formula": "growth", "currency": "USD",
         "inputs": {"principal": 100, "rate": 10, "periods": 2}, "observed": 121},
        {"id": "p18-constraint", "formula": "transfer", "currency": "USD",
         "inputs": {"source": 1000, "destination": 200, "reserve": 300, "target": 900,
                    "fixed_fee": 5, "fee_rate": "0.01", "transfer": 700},
         "observed": {"fee": 12, "source_after": 288, "destination_after": 900}}
    ]}


def repaired_batch(document):
    repaired = deepcopy(document)
    repaired["cases"][1]["inputs"]["representation"] = "percent"
    transfer = repaired["cases"][2]
    transfer["inputs"].update(target=700, transfer=500)
    transfer["observed"] = {"fee": 10, "source_after": 490, "destination_after": 700}
    return repaired


def reference_results():
    results = {}
    results["01"] = split_minor_units(101, 4)
    results["02"] = [compound_balance(principal=500, period_rate=r, periods=2)
                     for r in ("0.02", "0.04")]
    results["03"] = [interval_contains(w, .25, .75, right_closed=False)
                     for w in (.25, .50, .75, -.01)]
    results["04"] = present_value(cash_flows=(-200, 110, 121), period_rate="0.10")["total"]
    results["05"] = [solve_linear_equation(a=2, b=7, c=1, d=12),
                     solve_linear_equation(a=3, b=6, c=3, d=6),
                     solve_linear_equation(a=2, b=1, c=2, d=3)]
    policy = dict(fixed_fee=3, fee_rate="0.02", fee_budget=13, amount_cap=600)
    results["06"] = {"maximum": maximum_transaction_amount(**policy),
                     "slacks": [transaction_report(amount=x, **policy)["slacks"]["fee_budget"]
                                for x in (500, 505)]}
    results["07"] = [-2*x + 10 <= 4 for x in (2, 3, 4)]
    results["08"] = {"profit": 100-120, "implication": implies(100 > 0, 100-120 > 0)}
    results["09"] = [i for i, payment in enumerate((1, 0, -1)) if payment <= 0]
    results["10"] = [fee_metrics(amount=x, fixed_fee=0, fee_rate="0.005")["effective"]
                     for x in (100, 200)]
    old, new = Q("0.03"), Q("0.0375")
    results["11"] = {"value": 80*Q("12.50"), "percentage_points": (new-old)*100,
                     "basis_points": (new-old)*10000, "relative_change": (new-old)/old}
    results["12"] = [simple_accrual(principal=9000, currency="USD", rate=4,
        representation="percent", start=date(2024, 2, 28), end=date(2024, 3, 1),
        convention=c)["interest"] for c in ("ACT/360", "ACT/365F")]
    transfer = dict(source=1200, destination=150, reserve=400, target=650, fixed_fee=6, fee_rate="0.02")
    chosen = minimum_transfer(**transfer)
    results["13"] = {"minimum": chosen["transfer"], "fee": chosen["candidate_report"]["fee"],
                     "source_after": chosen["candidate_report"]["source_after"],
                     "destination_after": chosen["candidate_report"]["destination_after"],
                     "higher_target": minimum_transfer(**(transfer | {"target": 950}))["transfer"]}
    results["14"] = {"correct": 80*(1+Q("0.25"))**2,
                     "wrong_grouping": (80*(1+Q("0.25")))**2,
                     "power": 2**3, "xor": 2^3}
    results["15"] = {"discounted": present_value(cash_flows=(-80, 44, "48.4"), period_rate="0.10")["total"],
                     "zero_rate": present_value(cash_flows=(-80, 44, "48.4"), period_rate=0)["total"],
                     "time_two": present_value(cash_flows=(0, 0, 121), period_rate="0.10")["total"],
                     "time_one": present_value(cash_flows=(0, 121), period_rate="0.10")["total"]}
    results["16"] = [compare_finite(1e-10, 0, rel_tol=1e-6, abs_tol=a) for a in (0, 1e-10)]
    audit = audit_growth(principal=300, period_rate="0.10", periods=2, candidate=330)
    results["17"] = {"reference": audit["reference"], "discrepancy": audit["discrepancy"],
                     "relative_error": abs(audit["discrepancy"])/audit["reference"],
                     "weak_checks": [audit["checks"]["nonnegative"], audit["checks"]["direction_bound"]]}
    batch = exercise_batch()
    mixed, repaired = run_batch(batch), run_batch(repaired_batch(batch))
    results["18"] = {"counts": mixed["counts"], "success": mixed["success"]}
    results["19"] = {"counts": repaired["counts"], "success": repaired["success"]}
    base = compound_balance(principal=100, period_rate="0.03", periods=5)
    scaled = compound_balance(principal=400, period_rate="0.03", periods=5)
    wrong = compound_balance(principal=100, period_rate="0.03", periods=4)
    results["20"] = {"balance": base, "scaled": scaled, "scaling_holds": scaled == 4*base,
                     "mistake_rejected": not audit_growth(principal=100, period_rate="0.03",
                                                          periods=5, candidate=wrong)["passed"]}
    return json_ready(results)


def main():
    for number, result in reference_results().items():
        print(f"Problem {number}: {json.dumps(result, sort_keys=True)}")


if __name__ == "__main__":
    main()
