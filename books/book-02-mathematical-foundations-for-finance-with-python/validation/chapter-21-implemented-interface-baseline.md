# Chapter 21 implemented interface contracts: next checkpoint

The COV-88 requirements map distinguishes the draft catalog from fulfilled interfaces. The next batch should make this distinction executable without expanding the modules into the general systems described in the draft.

On [pinned source `a3f898d3824e5287da47129b18f58d6ec16af05b`](https://github.com/sssamant21/python-financial-mathematics/blob/a3f898d3824e5287da47129b18f58d6ec16af05b/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_02.py), catalog blob `a36569438bc8ac086445f6c7556852efa908f8e4`, all six entries pass `missing_contract_fields`, but that check only tests three nonblank strings. Actual signatures and output keys were inspected from the pinned Chapter 21 modules:

| Draft area | Actual callable | Current scope |
|---|---|---|
| Cash flow | `present_value(flows, rate, convention)` | Both declared rate conventions; scalar value. |
| Linear algebra | `solve_2x2(matrix, target, *, threshold=1e-12)` | Two-by-two solve, residual, normalized determinant and screening threshold; no condition number. |
| Optimization | `solve(a, b, tolerance=1e-12)` | Fixed two-target quadratic; weights, objective, method and feasibility diagnostics. |
| Continuous time | `scenario_report(initial, rate, flow, years)` | Unconstrained ending balance with metadata; no trajectory or events. |
| Reporting | `build_report()` | Fixed synthetic report; accepts no external results or evidence arguments. |

The draft intentionally remains a design, so its broader descriptions are not counted as code defects. Next: add a separate implemented-interface map or explicit scope reconciliation and check it against actual callable signatures, supported call forms and returned schema. Preserve the draft, distinguish keyword-only arguments from positional ones, and keep review/approval pending. Reuse existing numerical oracles rather than count their examples again. See the [requirements map](chapter-21-capstone-requirements-evidence-map.md).
