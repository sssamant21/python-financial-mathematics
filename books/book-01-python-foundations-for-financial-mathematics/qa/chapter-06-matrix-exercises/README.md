# Chapter 6 — Section 6.11 matrix exercises

Based on main `becc99602fce64025d2b74299906e667323366ab`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Results](results.json)

CPython 3.12.14, NumPy 2.3.5, Linux: **2 command checks and 23 predicates passed** on the first run. Eight original Section 6.11 methods passed once. No unexpected failure or manuscript change. Exercise records, predicates, commands, formal workflows and historical unique methods remain separate; overlapping reruns add no historical methods or workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-matrix-exercises/review.py
```

The runner compiles/reconstructs the original two listings unchanged, executes original discovery/main, compares full demonstration stdout, and retains source/listing hashes and byte equality. Supplemental source calls check the third portfolio, fourth scenario, label/row permutations and duplicate rejection against independent Fraction cell oracles. Fixture comparisons use rtol=1e−12/atol=1e−14, NaNs disallowed. The stale-label probe documents a caller responsibility rather than inferring identity correctness from matching dimensions.

A bounded source run actually returns a (1000,200) float64 table with 1,600,000 element bytes. An adjacent output-budget rejection uses inputs smaller than the limit; peak RSS/backend workspace is not measured. Exact Section 6.10 function calls compare both original portfolio columns; that source file/listing hash is retained separately, and its unittest suite is not rerun or counted here. Successive-period and calibrated-risk conventions are conceptual review records; metadata predicates do not execute or validate those models.

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, static checking, peak-memory/performance measurement, optimization/calibration, time-path/rebalancing integration and independent acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact. Following unnumbered navigation text was excluded only from E8's reviewed prompt; identity/count unchanged.

**88/128 local prompts reviewed; 40 remain.** All 16 core workflows and 20 chapter-wide answers remain separate. Next: Section 6.12 local exercises.
