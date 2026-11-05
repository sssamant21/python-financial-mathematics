# Section 8.11 — Sensitivity and scenario charts review

Baseline `9f66a3c24a0c66a7afc6605a6ccd0b04ac334b0c`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

One formal workflow and eight local answers reviewed. Three documented commands, eleven additional predicates and eight existing methods passed after correction. Both exact complete listings were saved as siblings; discovery, demonstration and compilation ran inside the documented lab directory. Synthetic inputs require no preceding lab, external data, pandas or desktop. Prepared Linux CPython 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8 were used. Fresh installs and other platforms were not executed.

**F43:** A valid Fraction principal failed the declared Real input contract because NumPy's finiteness check raised TypeError. Bounds are now checked before and after float conversion. The initial failure is retained and an assertion was added within an existing test method; historical method count does not increase. Replay the initial run using this runner at the same relative path in a worktree of the baseline.

Independent fractions verify the named cases, full grid and reference deltas. Derivative versus finite-shock arithmetic is supplemental and retained with exact expectations. The mesh values and bars were checked against those references. The PNG was visually inspected for input axes, rate-row orientation, USD colorbar, reference marker and distinct one-factor versus joint cases. The runner regenerates it and records its hash. No scenario probabilities, confidence bands, forecast validation, broad accessibility or independent acceptance are established. F28/F32 remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-scenarios-review/review.py
```

Next: Section 8.12 formal lab and local answers.
