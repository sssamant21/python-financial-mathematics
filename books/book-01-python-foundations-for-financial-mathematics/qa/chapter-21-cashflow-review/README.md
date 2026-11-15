# Section 21.6 — Scoped cash-flow review and updated artifact

Baseline: `7d6add00a538b049ca8bdeedc8af508c32238221`.

The [runnable harness](package-review.py) stages the exact cash-flow module, exports, example and tests, together with the TVM dependencies and earlier scaffold metadata, README and tests. [Actual commands and outputs](package-results.json), [artifact comparison](artifact-manifest.json), [40 answer records](answer-records.json) and [12 lab-step records](lab-step-records.json) are retained.

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-21-cashflow-review/package-review.py SOURCE_REVISION
```

## Executed scope

All 11 new packaging commands passed. They include editable and separate clean-wheel suites of 36 methods each, the example outside the hidden source tree, import provenance and 62 wheel contract predicates. The predicates comprise 38 retained one-period/TVM cases and 24 NPV cases. Three additional [source properties](source-properties.json), executed by their [runner](source-properties.py), check aligned additivity, positive future-flow monotonicity and a mixed-sign counterexample. These three properties are separate from the wheel predicates.

The new wheel hash differs from the Section 21.5 artifact, although the illustrative draft version remains `0.1.0`. The build environment uses preprovisioned system-site tools; the clean consumer does not. Pip uses `--no-index --no-build-isolation --no-deps`. The consumer runs with `-I`, no `PYTHONPATH`, and the source tree hidden. No global packages or network downloads were used. Generated binaries and temporary environments are not committed; byte-for-byte reproducibility is not claimed.

The [earlier three source commands](../chapter-21-cashflow-resume/results.json) are reused after matching seven Python fence digests. The evidence chain contains 14 packaging/source commands plus the separate source-properties run. It covers 36 existing methods and 108 method invocations: 36 each in source, editable and wheel runs. No historical unique methods were added. The harness caption mentions the original 12 wheel checks; the actual 62 JSON rows define the current scope.

NPV expectations use independent Fraction formulas and the declared tolerances: relative `5e-13`, absolute `1e-10` in amount units. The accepted 1,001-entry zero schedule checks a boundary, not workload performance.

## Retained limits and progression

Three separate observations retain rounded-base TVM loss, discounted-leg overflow before cancellation, and `fsum` intermediate overflow despite a finite complete NPV. These are documented method limits, not new failed acceptance predicates. Executable fences are unchanged. Historical statements about unexecuted publication tests now link to later QA evidence.

This local cash-flow/TVM integration does not close the broader F32 shared-input gap. F28/F32/F209, Section 20.11 static checking, F165/F185, R08–10, ownership, resource limits, supported platforms, model suitability, security, release and independent acceptance remain open.

Chapter 21 now has six scoped workflows and 240 reviewed local answers. Next: Section 21.7, Loan Module.

Candidate source/evidence pin: `39ebd9690c5c5b3d946ffd6141b7165b0b8e9388`. [Hash verification](publication-verification.json).
