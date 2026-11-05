# Section 9.14 — Solving for time lab and answer review

Baseline `c8c7a10dc8a2e74e11f32a0b517a242387b12bb6`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Six answers](ANSWERS.md).

One workflow and six local answers scoped. Two documented commands, nineteen additional predicates and eight existing embedded methods passed after F49 correction. The sole Python listing was extracted verbatim as solving_for_time.py, run in an isolated temporary directory, and compiled. Prepared Linux CPython 3.12.14; standard library only. Save-before-run and filename contracts hold; no prior module, dataset or network dependency. The console output matches the documented two-year example. Fresh installation and other platforms were not executed.

**F49:** subtracting logarithms of adjacent balances near 1e300 erased nonzero growth, returning zero time for both an increase and a decline, and accepting an opposed-rate target. Independent 100-digit Decimal references yield about 3.047780088e-15 and 2.899047383e-15 years. Two additional probes exposed elapsed-time division underflow and a nonfinite nominal log factor, both silently returning zero. All five initial failures remain in initial-results.json; the original eight methods passed even then. Nearby magnitudes now use log1p of relative change; separated magnitudes retain log differences to avoid ratio overflow. Nonfinite factors and zero output for nonzero represented growth are rejected. Five regression assertions were added inside the existing invalid-input method; no historical unique methods were added. Reproduce initial results by running this runner at the same relative location against the baseline source.

Independent Decimal logarithms/exponentials at precision 100 and exact rational powers derive expectations. They are QA oracles, not replacement lab implementations. Source calls cover all six practice prompts, nominal and continuous conventions, signed balances and zero-rate feasibility. Exact rational inequalities verify the first full posting; no schedule engine or calendar implementation was created. Formal lab steps are save, execute and compile, all exercised; rate units, nonzero same-sign balances, positive periodic factors and nonnegative time are explicit preconditions. Fractional modeled time is distinct from contractual posting. Float range rejection does not promise arbitrary-range accuracy. No image/notebook workflow. F28/F32, platform and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-solving-time-review/review.py
```

Next: Section 9.15 formal lab and local answers.
