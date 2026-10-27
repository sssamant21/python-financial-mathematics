"""Educational interface catalog; entries describe planned components."""
from copy import deepcopy

CATALOG = {
    "cash_flow": {"inputs": "amount-time pairs, continuous annual rate",
                  "output": "value in common currency",
                  "errors": "invalid inputs or numerical range"},
    "sensitivity": {"inputs": "model inputs and differentiation method",
                    "output": "derivative, units and diagnostics",
                    "errors": "invalid domain or numerical failure"},
    "linear_algebra": {"inputs": "matrix and vector",
                       "output": "solution, residual and conditioning information",
                       "errors": "invalid shape, rank or numerical failure"},
    "optimization": {"inputs": "objective, constraints and tolerances",
                     "output": "candidate, feasibility and termination diagnostics",
                     "errors": "invalid problem or nonconvergence"},
    "continuous_time": {"inputs": "initial state, coefficients and horizon",
                        "output": "trajectory and event information",
                        "errors": "invalid input or solver failure"},
    "reporting": {"inputs": "results, assumptions and evidence",
                  "output": "structured scenario report",
                  "errors": "missing or inconsistent information"},
}

def interface_catalog():
    return deepcopy(CATALOG)

def missing_contract_fields(entry):
    if not isinstance(entry, dict):
        raise TypeError("entry must be a dictionary")
    return [key for key in ("inputs", "output", "errors")
            if not isinstance(entry.get(key), str) or not entry[key].strip()]

if __name__ == "__main__":
    for name, entry in interface_catalog().items():
        print(name, "missing:", missing_contract_fields(entry))
    print("Catalog is a design draft; no module validation or approval is claimed.")
