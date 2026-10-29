# V06 — Chapter 1 short section exercises

Date: 2026-10-29. Source revision: `ef9b06d8893c180b28a81de6dc07f0ba91fdf307`.

**PASS (scoped): 40 supplemental answer records reviewed; 76 checks passed, zero failed.** The check count includes five source-file hash checks and seven subprocess pipeline cases, not 76 exercises. Counts are not added to the historical reference-method or supplemental-workflow totals.

| Section | Answer records | Scope |
|---|---:|---|
| 1.6 | 4 | FV, scenarios, rate representation, independent expected value |
| 1.7 | 6 | Types, Decimal/float, bond mapping, basis points, missing values |
| 1.8 | 8 | Operators, portfolio weights, growth, percentages, units |
| 1.9 | 10 | Translation, grouping, precedence, known-result cases |
| 1.10 | 12 | Parsing, domains, contracts and complete input/output pipeline |

See [answers](ANSWERS.md), [machine-readable records](answers.json), [executable supplement](review.py) and [actual results/transcripts](results.json).

Run `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-01-short-exercises/review.py` from the repository root. It needs only the standard library. Tested on CPython 3.12.14, Linux x86_64; results include exact environment information. `--cli` runs the new teaching pipeline with actual stdin/stdout and explicit error exits. This is supplemental QA implementation, not a change to manuscript code.

Numerical FV oracles use exact rational arithmetic; default `math.isclose` arguments are preserved as required by Section 1.6.4. Display expectations are independently specified text. Conceptual items are reviewed for prompt alignment, units, rate conventions, assumptions and missing-data meaning; successful runtime predicates alone cannot establish these properties. Source hashes bind each answer to the reviewed section. All 40 records have explicit answers, but not all are executable tasks.

The pipeline chooses positive finite principal, finite annual effective percent greater than -100, and whole nonnegative years. It rejects conversion errors, nonfinite inputs/results, overflow and results underflowing to zero. It uses float teaching arithmetic with display-only formatting; it does not establish a production monetary rounding policy, acceptable numerical error or resource limits. CLI cases cover normal, zero horizon, meaningful negative rate, invalid text, fractional years, nonfinite input and missing input. The matrix is deliberately finite, not exhaustive branch/domain coverage.

No manuscript source was changed; no new manuscript defect was identified. The existing 1,160-fence ledger remains unchanged. The three integrated challenges, remaining environment/platform steps, independent review and broader V05/V06 acceptance remain open. Next: implement and validate the integrated challenge extensions, staged refactor and full boundary matrix.
