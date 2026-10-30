# Chapter 6 — final formal workflows and project checklist

Based on main `5ea4e272987348c0debfbcf035fa294b4d4520fd`. [Four workflows / 32 derived units](workflow-register.json) · [Workflow review](REVIEW.md) · [20 project records](project-register.json) · [Project checklist](PROJECT-REVIEW.md) · [Runner](review.py) · [Results and benchmarks](results.json) · [New timing samples](benchmark.json)

CPython 3.12.14, NumPy 2.3.5, Linux: **14 command checks and 66 predicates passed** on the first run; 32 existing methods passed, eight per workflow. Commands cover runtime identity, application/discovery/quiet import per workflow, and compileall. The 32 workflow units contain 24 scoped execution/file passes, four partial setup records and four conceptual reviews. The 20 project records separately map six input axes, eight equations and six acceptance clauses. Historical totals of 2,996 unique methods and 192 supplemental workflows are unchanged.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-final-workflow-review/review.py
```

Eight exact source/test fences are reconstructed as documented siblings. The project runs from its documented parent directory. Known-runtime demos match stdout; performance correctness tests precede the bounded benchmark. Fresh imports are quiet, and listings compile and remain byte-identical. Source API checks distinguish local RNG replay and state ownership from independent statistical validation. Precision-80 Decimal and Fraction calculations independently check tiny and ordinary linking, plus the portfolio's values, weights, contributions and returns. Comparisons use explicit shape, finite-value and tolerance checks.

The original Section 6.15 main ran all three sizes with five samples of three calls per method. The retained report contains actual samples and runtime fields; counts, minima, medians, ratios and payloads were recomputed. The manuscript's historical table also agrees with its own historical samples. New timings are not expected to match those observations. Rankings are local observations, not acceptance thresholds, confidence intervals, application speedups or peak-memory proof. A separate supplemental fault injection confirms that a failed correctness gate prevents timing; the original helpers are restored afterward. This expected diagnostic is separate from the unchanged child benchmark.

The portfolio agrees with independent opening value 1,000, ending values 1,045/895/1,000, P&L 45/−105/0 and returns 4.5%/−10.5%/0. Ownership, domain and identity failures are retained. Mixed Boolean input inference remains a documented caller precondition; arbitrary wire-schema validation is not established. No unexpected failure or new manuscript defect was found. Manuscript files are unchanged. F28/F32 remain open, and F33–F35 history is retained.

All 16 Chapter 6 core workflows now have scoped records. The 20 chapter-wide answers and project checklist are separate. All 128 local exercise/project-extension prompts remain pending. Fresh installation, Windows/macOS, static checking, live parallel RNG, generator quality, financial calibration, isolated hardware/peak memory, production and independent acceptance remain unestablished. Next: Section 6.1's eight local exercises, then the remaining local queue.
