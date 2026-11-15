# V-186 — Section 9.6 complete parallel-shock reports

Baseline: `7d6add00a538b049ca8bdeedc8af508c32238221`. The [scope comparison](chapter-09-parallel-report-scope.json) verifies that only `parallel_shock` changed. Baseline, helper, validator and spot function text is unchanged.

The [independent checker](../chapter-09/code/check_section_06_parallel_reports.py) computes the full eligible baseline, direct endpoint changes, Taylor changes and error fields at 1,800 and 2,400 decimal digits. Both references must agree. Sixteen vectors × six fields, 11 input/priority cases and five ownership/iterator/order/scaling/context controls give **112 source predicates**. Numeric fields use relative tolerance `5e-14` and absolute tolerance zero. Zero signs are compared numerically.

## Retained initial evidence

The [baseline](chapter-09-parallel-report-baseline.json) passed 95 predicates and failed 17; the [actual replay](chapter-09-parallel-report-baseline-replay.json) reproduces the same results. [Baseline command output](chapter-09-parallel-report-baseline-run.json) and [replay command output](chapter-09-parallel-report-baseline-replay-run.json) retain exits and diagnostics. Twelve failed fields came from two rejected reports: the saved `expm1` rescue and an eligible tiny leg. Five more fields concern complete error reporting. These are 17 failed predicates, not 17 unique bugs.

The [corrected results](chapter-09-parallel-report-corrected.json) pass all 112 source predicates. [Actual corrected execution](chapter-09-parallel-report-corrected-run.json) and the [four-file/four-command scoped run](chapter-09-parallel-report-results.json) are retained. The [observer](chapter-09-parallel-report-observer.txt) stages baseline source with the new checker when run as:

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-parallel-report-observer.txt . baseline-replay
```

Use `corrected` for the working source. The [scoped runner](chapter-09-parallel-report-runner.txt) compiles four files and executes the demo and three checkers, including the unchanged 141 baseline predicates. The fresh inventory of 625 Python files, 412 check/test scripts and 626 required blobs is distinct from a full runtime result.

## Contract and limits

The existing full-baseline prerequisite is retained: positive reported value and finite scalar/list fields, including per-cash derivatives. The saved zero-shock case with an unused, unrepresentable baseline field still rejects. This is a retained design/range restriction, not a repaired numerical case or independent financial approval. A less restrictive parent API remains a broader design question.

Complete latent expressions in a private 1,700-digit context avoid rounded-baseline products, `expm1` range failures and selected small-error cancellation. All returned changes and errors must be finite. Under the eligible-baseline and positive-flow assumptions, endpoints above exponent 10,000 cannot be rescued into a finite change; below −10,000, amounts are omitted beyond finite-input product rescue. Arbitrarily large collections and universal correctly rounded exponential results are unproved.

The saved parallel finite-change case is resolved within this scope. Historical diagnostic records remain unchanged. The [fresh spot observations](chapter-09-spot-resume-r12-initial.json), [actual identical replay](chapter-09-spot-resume-r12-replay.json) and [runner](chapter-09-spot-resume-r12-probes.txt) retain three open numerical cases: finite spot value/derivative exponential rescue, derivative loss after discount-factor underflow, and spot-shock `expm1` overflow. They are diagnostics, not passing parallel predicates.

Next: complete `spot_curve_sensitivity` value, per-spot derivative, parallel-first and collection contracts; then `spot_shock` changes, errors and prerequisites. All 37 selected COV categories remain partial, none closed. Independent mathematical/editorial/model/platform/release/canonical acceptance remains pending. Book 1 is tracked separately.

Executed source pin: `39ebd9690c5c5b3d946ffd6141b7165b0b8e9388`. [Hash verification](chapter-09-parallel-report-publication-verification.json).
