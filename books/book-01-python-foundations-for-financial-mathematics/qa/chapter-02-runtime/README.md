# Chapter 2 — Scoped script and scenario-analyzer validation

**Date:** 2026-10-27. **Reviewer / execution owner:** Codex. **Source:** Book 1 baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 2 manuscript and companion files were unchanged through `8e83acebcc2f369c6f61763ce810c01cfd1e90be`; GitHub comparison returned no changed Book 1 Chapter 2 paths. [results.json](results.json) preserves source SHA-256 values, selected zero-based Python-block indices, controlled overrides, outputs, expected rejections and statuses.

## Scoped result

PASS: twelve selected example groups, twelve controlled project cases and twenty-four compilation checks. No manuscript corrections were required.

Chapter 2 has no unittest or doctest suites in the surveyed Python fences. These script executions and validation cases are recorded separately; they add **zero unittest methods** to the cumulative tracker total. They do not automatically grade all sixty companion answers.

## Selected examples

One group was run for each section 2.1–2.11, plus one group of eight self-contained companion snippets. The [runner](run_reference_checks.py) concatenates only the recorded fences in source order and supplies `from decimal import Decimal` as a documented prelude. Examples cover Boolean conditions, comparisons, branching, decision rules, bounded loops, cash-flow iteration, period ranges, nested flow, loop control and defensive validation. An execution pass establishes that the selected code ran successfully in this environment; it is not a known-answer check for every variable or statement.

Companion blocks 0–5, 7 and 8 were executed. Fragments that assume additional caller data, pseudocode, potentially unbounded illustrative loops and the remaining worked answers were not treated as complete standalone programs.

## Scenario-analyzer cases

The baseline executes the exact Section 2.12 Python block. Other cases change only declared top-level input constants using AST assignment replacement; the validation and projection logic are retained. The runner captures the resulting program state and stdout in fresh subprocesses.

| Case | Verified outcome |
|---|---|
| Published baseline | Four scenarios evaluated; no rejections; first target years 12, 10, 9 and 8 for returns 3%, 5%, 7% and 9% |
| Zero rate, horizon 15 | Target reached exactly in final year 15, balance 100000 |
| Zero rate, horizon 14 | Target not reached; terminal balance 95000 |
| Target already attained | Year 0 retained for each supplied valid scenario |
| Mixed invalid and zero rates | Seven invalid scenarios rejected; the observed zero rate evaluated |
| Reversed scenario order | Results preserve supplied order and match the same independent expectations |
| Boolean horizon | Required integer validation diagnostic; no projection results |
| Zero horizon | Required positive-horizon diagnostic; no projection results |
| Horizon 101 | Supported-horizon diagnostic; no projection results |
| Negative contribution | Nonnegative-contribution diagnostic; no projection results |
| Non-finite initial investment | Finiteness diagnostic; no projection results |
| Zero target | Positive-target diagnostic; no projection results |

For valid cases, the checker uses 50-digit Decimal arithmetic and the closed-form end-of-period contribution balance:

```text
B(n) = P*(1+r)**n + C*((1+r)**n - 1)/r, if r != 0
B(n) = P + n*C, if r == 0
```

The expected first crossing is the earliest supported integer period whose closed-form balance reaches the target, including period zero. Amounts are compared with an absolute tolerance of `1e-18`; period identities, scenario counts, rejected counts and target/non-target reconciliation are checked exactly. This is a bounded benchmark for these fixtures, not a proof for every input or Decimal context.

Expected shared-input failures are verified through their diagnostics and absence of projection results. The published script prints validation errors while exiting normally; no nonzero CLI rejection contract is asserted.

## Environment and reproduction

Python 3.12.14 on Linux x86_64 with glibc 2.39; standard-library dependencies only.

From the repository root, choose a new output directory:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-02-runtime/run_reference_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-02 /tmp/chapter02-repro
```

All child executions use `-W error::FutureWarning` and a twenty-second timeout. Each example group and project case has a separate working directory. Compilation uses `python -m compileall -q .`; all twenty-four extracted directories passed. [all-checks.log](all-checks.log) retains detailed output, and [results.json](results.json) records the observed analyzer states and benchmark results.

## Remaining scope

Earlier canonical labels are publication-history claims. This run does not establish all worked-answer reasoning, unselected fragments, universal numerical bounds, live financial suitability, external data correctness or cross-platform behavior. Independent mathematical, source, editorial and acceptance reviews remain pending.

**Next action:** Chapter 1 runtime evidence reconciliation.
