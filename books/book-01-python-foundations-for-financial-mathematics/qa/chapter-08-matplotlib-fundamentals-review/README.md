# Section 8.2 — Matplotlib fundamentals review

Baseline `e5bb22c3c22d2c59a8d7fcde5bf01249a331b87a`. [Runner](review.py) · [Answers](ANSWERS.md) · [Initial results](initial-results.json) · [Corrected results](results.json).

One formal workflow and eight local answers reviewed. Three documented commands, eight existing test methods and twelve additional predicates passed after correction. The runner reconstructs the two complete Python listings as siblings, then runs discovery, demonstration and compilation from the lab directory. The lab uses its own synthetic schedule and Agg; no earlier lab files, pandas, desktop or external data are prerequisites. Prepared Linux Python 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8 were used; fresh installations, Windows/macOS and interactive rendering were not tested.

**F40:** The original bounds accepted the declared Real interface but used a NumPy finiteness call that raised TypeError for Fraction. The two initial failing probes are retained. The corrected source checks bounds before and after scalar conversion, so 1/20 yields the expected schedule and −1 + 2⁻⁶⁰ is rejected rather than rounding to −1 and producing zero balances. Regression assertions are inside existing methods. To replay the initial failure, place the runner at the same path in a worktree of the baseline.

Independent rational balances and gains were compared with the source. Figure ownership and style restoration were checked on the source; an injected SVG write failure exercised the real main function's cleanup. The 1×1 shape, line-list and raster sizing examples are separate supplemental probes. PNG was inspected for labels, references, annotation and both panels; SVG was parsed, not visually rendered. No accessibility or independent acceptance is implied. F28 and F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-matplotlib-fundamentals-review/review.py
```

The runner regenerates the PNG and records its hash. Next: Section 8.3 formal lab and local answers.
