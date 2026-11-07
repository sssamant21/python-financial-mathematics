"""Illustrative validation-plan catalog; no tests are executed here."""
from copy import deepcopy

PLAN = [
    {"id": "CF-01", "layer": "known_value", "description": "continuous PV: 100 at ln(2), one year -> 50"},
    {"id": "CF-02", "layer": "boundary", "description": "zero horizon returns the amount"},
    {"id": "CF-03", "layer": "invalid", "description": "negative horizon is rejected"},
    {"id": "CF-04", "layer": "property",
     "description": "same-date splitting preserves mathematical PV; compare float outputs within a rounding bound",
     "acceptance": {
         "amount_identity": "exact sum of normalized split floats equals merged float",
         "range_scope": "each discounted term and final value finite",
         "comparison": "absolute rounding bound",
         "bound": "half-ulp of every split discounted term, merged discounted term, and split final value",
         "exclusions": "individual-term or final overflow; changed amount or date",
     }},
    {"id": "INT-01", "layer": "integration",
     "description": "equivalent factors agree within propagated conversion and factor rounding error",
     "acceptance": {
         "domain": "finite converted rate and finite positive factors",
         "comparison": "conversion-error propagation plus factor rounding",
         "bound": "effective factor * abs(expm1(-conversion_error * years)) plus half-ulp of each factor",
         "conversion_error": "represented converted rate minus high-precision log1p of the represented effective rate",
         "exclusions": "invalid rates, conversion overflow, factor overflow or factor underflow to zero",
     }},
    {"id": "CT-01", "layer": "known_value", "description": "zero-rate account: 1000 + 200*3 = 1600"},
]

def make_plan():
    """Create a fresh plan with no execution or approval claim."""
    return {"cases": deepcopy(PLAN), "execution": "not run",
            "independent_review": "pending", "approval": "pending"}

def missing_case_fields(case):
    if not isinstance(case, dict): raise TypeError("case must be a dictionary")
    return [key for key in ("id", "layer", "description")
            if not isinstance(case.get(key), str) or not case[key].strip()]

if __name__ == "__main__":
    plan = make_plan()
    print("Planned cases:", len(plan["cases"]))
    print("Execution:", plan["execution"], "Review:", plan["independent_review"])
