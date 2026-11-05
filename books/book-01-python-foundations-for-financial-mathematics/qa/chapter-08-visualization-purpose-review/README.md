# Section 8.1 — Visualization purpose: lab and answer review

Baseline: `9d5c9ce9786c2963561a64905d73a6e6a4bf73f0`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected rerun](results.json) · [Answer review](ANSWERS.md).

The two Python listings were extracted verbatim, saved as siblings under `visualization_lab_81`, and run from that directory with the prepared Linux Python 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8 environment. The fixture is built in; no previous lab, vendor data, GUI or pandas is required. The three commands (test discovery, demonstration, compilation) passed and eight existing test methods passed. Ten additional predicates passed after correction. The source demonstration created `output/why_visualization.png`; the runner copies it next to the evidence and records its SHA-256. Agg is selected by the source before pyplot. No fresh installs or Windows/macOS interactive paths were exercised.

The PNG was inspected for legible labels, distinct marker shapes, the irregular day spacing, the DIP drawdown, and the missing GAP line segment and return markers. Artist predicates and rational arithmetic are separate from visual inspection. Overlapping endpoint markers are resolved by the numerical table. This is a single fixture inspection, not a general accessibility audit.

**F39:** Prices 1, 10⁻³⁰⁸, 1 yield a finite recovery return around 10³⁰⁸, but multiplying by 100 for plotting exceeds binary64 range (maximum about 1.798×10³⁰⁸). The original plotted an infinite value and emitted an overflow warning, losing a valid observation from the chart. The corrected plotting function rejects unsupported percentages before allocating a figure. The existing artist method includes a regression; no extra method was added. The normal output and PNG hash are unchanged between the retained attempts. To reproduce the initial result, place the same runner at this path in a worktree of the baseline.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-visualization-purpose-review/review.py
```

One core lab and eight local answers have scoped records. F28, F32, broader accessibility and independent acceptance remain open. Next: Section 8.2.
