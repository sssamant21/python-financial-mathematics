# Section 18.13 — initial execution and prerequisite checkpoint

Exact source revision: `a02160a18fcb320ffb537ea5b5cf7bce8e64a3d3`. [Results](results.json) · [Runnable observer](run.txt).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-performance-checkpoint/run.txt .
```

Run against that revision or confirm the retained manuscript SHA256 before comparison. This extracts the reference fence unchanged into a temporary directory, runs the displayed script and compile commands (12 existing unique test methods; no new historical methods), and executes the optional NumPy fence unchanged in a separate process. All three command records passed. NumPy is available in this candidate environment; its output is not required to match the Python RNG sequence.

Seven supplemental predicates passed. Independent exact rational sums give sample mean100, sample variance400 and SE20/sqrt(3) for [80,100,120]; the probability-weighted three-state population mean100 and variance200 are distinct. Storage is202400000 element bytes (193.023681640625 MiB), excluding overhead. The101-path, batch10 run exactly matches streaming under the source's shared generator/draw order; final partial batch size1 follows divmod(101,10), not an observed worker-count metric.

Five supplemental timings are retained with median/range:10000 draws, seed42, RNG/accumulator setup included, imports excluded. These describe one shared candidate Linux environment, not a speedup or representative hardware benchmark. Peak memory, profiler, vectorized accuracy/SE, parallel stream validation and full environment/library configuration remain unmeasured.

Two initial range probes retain nonfinite-update rejection and the mutated accumulator state afterward. The prose already acknowledges overflow; this is a limitation/contract screen, not a substantiated new defect or a corrected rerun. Do not reuse a rejected accumulator pending review of transactional-update expectations.

Formal forty-answer prompt alignment and twelve-step acceptance remain unfinished. This checkpoint executes parts of lab steps1–9/11 and records limitations for12; it does not declare those step contracts fully reviewed. Next: finish the Section18.13 answer/lab matrix, classify range/state semantics, and record peak-memory methodology versus actual measurements separately. F28/F32/F165/F185 remain open. No source edits, independent acceptance or platform certification.
