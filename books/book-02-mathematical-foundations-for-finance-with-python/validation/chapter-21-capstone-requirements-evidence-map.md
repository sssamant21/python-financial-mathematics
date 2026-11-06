# Chapter 21 — Requirements and evidence map

This map compares the authored F1–F8 list and proposed interfaces with the implemented teaching labs and retained execution evidence. It was assessed against `59f713d346fbcbf14e7125902637cd2f6e2c56e4`. The status below concerns selected evidence only; it does not certify requirement fulfillment.

| Requirement | Implemented behavior and evidence | Remaining obligation |
|---|---|---|
| F1 — Paired inputs and domain | [Valuation code](../chapter-21/code/section_21_03.py) preflights the convention and every finite amount/time pair before calculation. The [cash-flow checker](../chapter-21/code/check_section_21_03.py) covers both orderings of an invalid date and a term that would require `exp(1000)`, and a valid one-shot iterator whose signed sum is 2. | No claim about arbitrary external input formats or large streams. |
| F2 — Rate convention and time units | [Rate and valuation evidence](chapter-21-capstone-rate-range-followup.md) checks continuous and effective conventions, fractional years, and unsupported-domain behavior. The fixed scenario supplies the continuous rate and years; the account specifies units per year. | Broader conventions and external unit validation are outside the teaching interface. |
| F3 — Independent benchmarks and checks | [Valuation](chapter-21-capstone-rate-range-followup.md), [sensitivity](chapter-21-capstone-sensitivity-range-followup.md), [replication](chapter-21-capstone-replication-range-followup.md), [allocation](chapter-21-capstone-allocation-range-followup.md) and [account](chapter-21-capstone-account-range-followup.md) records give selected expectations and reruns. | Coverage varies by module; complete property/domain coverage and independent mathematical review remain open. |
| F4 — Tolerances and diagnostics | [Integrated report](../chapter-21/code/section_21_09.py) includes derivative step/error/units, normalized determinant and screen threshold, and allocation feasibility residual/violation/tolerance. | No general rank/conditioning estimate, iterative termination trace, trajectory, event policy, or approved error budget. |
| F5 — Reproducibility | The [full run](runtime-refresh-2026-11-05-r20.md) supplies source revision, runtime, commands and source hashes; scoped evidence supplies inputs and outcomes. | The generated scenario is not a provenance record. Dependency/platform qualification and authentication are separate. |
| F6 — Failure versus missing evidence | The cash-flow checks separate invalid dates from valid out-of-range computations; the [integrated checks](../chapter-21/code/check_section_21_09.py) exercise failure propagation. The [record helper](../chapter-21/code/section_21_01.py) flags absent fields. | No unified external error schema or evidence authenticity check. |
| F7 — Synthetic scenario | The report keeps inputs, module results, limitations and status; its [checks](../chapter-21/code/check_section_21_09.py) verify fixed values and deterministic JSON. | The five modules illustrate separate problems; no customizable portfolio or suitability conclusion. |
| F8 — Status separation | The [plan](../chapter-21/code/section_21_08.py) and report keep execution, review and approval separate. Execution artifacts are linked outside the example payload. | Independent review and authorization remain pending. |

## Baseline and correction

At `3d4624e1a47463e906fb8897fb88babf955a5583`, a negative date in the second row could be hidden by the first row's overflow; swapping rows returned the domain error. F1 requires input validation before calculation. The corrected lab consumes the iterable once to store normalized pairs, then discounts, so both orders report the invalid date and a valid one-shot iterator still works. This change does not revise discounting arithmetic. [Raw observations](chapter-21-capstone-requirements-evidence-map.json) retain the initial failure, a hash-verified baseline replay with the corrected checker overlaid, the 16-test rerun and the audit outputs. Run `python chapter-21/code/check_section_21_03.py` from the book root; for baseline replace only the checker at the baseline revision.

The proposed catalog and plan remain drafts. The report provides a determinant screen, not a condition number; analytic allocation feasibility, not an iterative solver trace; and an ending balance, not a trajectory or depletion event. The separate execution evidence does not change the report's placeholders.

Run the following from the book root with `python -` to reproduce the scoped audit at the corrected revision (or at baseline to observe the different preflight result):

```python
import json
import sys
sys.path.insert(0, "chapter-21/code")
from section_21_01 import pending_record, missing_fields
from section_21_02 import interface_catalog
from section_21_03 import present_value
from section_21_08 import make_plan
from section_21_09 import build_report

record, catalog, plan, report = pending_record(), interface_catalog(), make_plan(), build_report()
for module, absent in [
    ("replication", {"condition_number", "rank"}),
    ("allocation", {"termination_status", "iterations"}),
    ("account", {"trajectory", "events"}),
]:
    assert absent.isdisjoint(report[module])
assert {"source_commit", "environment", "command", "result"} == set(missing_fields(record))
assert plan["execution"] == report["validation_execution"] == "not run"
assert plan["independent_review"] == report["independent_review"] == "pending"
assert plan["approval"] == report["approval"] == "pending"
assert len(record["requirements"]) == 8
assert {"linear_algebra", "optimization", "continuous_time"} <= set(catalog)
cases = {
    "invalid_row_after_overflowing_term": [(1., 1000.), (2., -1.)],
    "invalid_row_before_overflowing_term": [(2., -1.), (1., 1000.)],
}
observed = {}
for name, flows in cases.items():
    try:
        present_value(flows, -1., "continuous")
    except (ValueError, OverflowError) as exc:
        observed[name] = {"expected": "ValueError", "actual": type(exc).__name__, "message": str(exc)}
    else:
        observed[name] = {"expected": "ValueError", "actual": "returned a value"}
print(json.dumps({
    "requirement_ids": sorted(record["requirements"]),
    "missing_reproducibility_fields": missing_fields(record),
    "plan_ids": [case["id"] for case in plan["cases"]],
    "report_fields": {key: sorted(report[key]) for key in ("replication", "allocation", "account")},
    "report_status": {key: report[key] for key in ("validation_execution", "independent_review", "approval")},
    "cash_flow_preflight": observed,
}, indent=2))
```

COV-88 gains a traceable map and a selected F1/F6 correction. It remains open for wider evidence and manual obligations.
