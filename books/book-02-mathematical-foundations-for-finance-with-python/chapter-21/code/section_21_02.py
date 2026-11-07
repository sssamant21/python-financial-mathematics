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


# This map describes the current teaching implementations, separately from
# the design catalog above. It does not claim that the planned system exists.
_IMPLEMENTED = {
    "cash_flow": {
        "callables": [
            {"module": "section_21_03", "name": "present_value",
             "signature": "(flows, rate, convention)", "return_kind": "scalar", "fields": []},
        ],
        "limits": ["Scalar valuation under effective or continuous annual rates.",
                   "No currency conversion or dated calendar convention."],
    },
    "sensitivity": {
        "callables": [
            {"module": "section_21_04", "name": "derivatives",
             "signature": "(amount, rate, years)", "return_kind": "pair", "fields": []},
            {"module": "section_21_04", "name": "central_difference",
             "signature": "(amount, rate, years, step)", "return_kind": "scalar", "fields": []},
        ],
        "limits": ["Continuous-discount analytic derivatives and a centered first derivative.",
                   "Units and approximation errors are added by the integrated report."],
    },
    "linear_algebra": {
        "callables": [
            {"module": "section_21_05", "name": "solve_2x2",
             "signature": "(matrix, target, *, threshold=1e-12)", "return_kind": "mapping",
             "fields": ["solution", "residual", "normalized_determinant", "screening_threshold"]},
        ],
        "limits": ["Two-by-two solve with a normalized determinant screen.",
                   "No general rank calculation or condition number."],
    },
    "optimization": {
        "callables": [
            {"module": "section_21_06", "name": "solve",
             "signature": "(a, b, tolerance=1e-12)", "return_kind": "mapping",
             "fields": ["weights", "objective", "diagnostics", "method"]},
        ],
        "limits": ["Fixed two-weight quadratic projection with long-only budget constraints.",
                   "No generic objective callback or iterative termination trace."],
    },
    "continuous_time": {
        "callables": [
            {"module": "section_21_07", "name": "scenario_report",
             "signature": "(initial, rate, flow, years)", "return_kind": "mapping",
             "fields": ["model", "inputs", "ending_balance", "units", "boundary_policy",
                        "validation_execution", "independent_review", "approval"]},
        ],
        "limits": ["Constant-coefficient unconstrained ending balance.",
                   "No trajectory, jumps or depletion events."],
    },
    "reporting": {
        "callables": [
            {"module": "section_21_09", "name": "build_report",
             "signature": "()", "return_kind": "mapping",
             "fields": ["purpose", "cash_flow", "sensitivity", "replication", "allocation",
                        "account", "limitations", "validation_execution",
                        "independent_review", "approval"]},
        ],
        "limits": ["Fixed synthetic examples, with no scenario parameters.",
                   "Execution evidence is external; review and approval remain pending."],
    },
}


def implemented_catalog():
    """Return a detached description of selected implemented teaching entry points."""
    return deepcopy(_IMPLEMENTED)

if __name__ == "__main__":
    for name, entry in interface_catalog().items():
        print(name, "missing:", missing_contract_fields(entry))
    print("Catalog is a design draft; no module validation or approval is claimed.")
