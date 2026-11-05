# Section 9.9 — Net present value lab and answer review

Baseline `cc946f647f7c99f1afe66f2e05282cdd6b3b1bae`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One workflow and five local answers reviewed. Two documented commands, twenty additional checks and eight existing embedded methods passed after the F46 follow-up. The complete listing was saved verbatim as net_present_value.py, executed and compiled in isolation. The lab includes its own Flow/valuation helper and imports no earlier file. Prepared Linux CPython 3.12.14; standard library only. No external project data or network. Windows substitution and fresh installation were not executed.

F46 was reproduced for both a nonzero acquisition cost and future event amount below float range. Both were silently converted to zero in the original validator. The corrected validator preserves the original scalar during conversion checks and rejects the lost values. Two assertions were added within the existing range method; historical unique method count is unchanged. Initial failures and corrected rerun retained. Reproduce initial results with this runner at the same relative path in a worktree of the baseline.

Independent fractions verify gross PV, initial cost, NPV, cost changes, full rate scenarios, the multiple-zero mixed-sign example and incremental comparison. The supplied aggregate PV/cost practice is supplemental arithmetic; profitability, missing costs and return-unit interpretation are conceptual. Exact source rejects unknown cleanup inputs. This does not establish an appropriate rate, complete costs, real investment acceptability, general root behavior or exact settlement. No image workflow. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-npv-review/review.py
```

Next: Section 9.10 formal lab and local answers.
