# Section 7.15 — Price to return transformation

Source baseline: `a6045562df26603dc69339e9b9ffc28549df57b4`. [Worked answers](ANSWERS.md) · [Prompt register](answer-register.json) · [Runner](review.py) · [Corrected results](results.json) · [Initial failure](initial-results.json).

**Eight scoped answers. Three documented commands, 24 predicates and eight existing methods passed after correction.** Methods overlap prior coverage; the new regression is inside an existing method. Python 3.12.14, pandas 2.2.3 and NumPy 2.3.5 on Linux; FutureWarning treated as error. No fresh install, Windows/macOS or notebook execution. No prior lab module is required; both verbatim Python listings are saved as siblings and invoked from their parent directory. Full demonstration output is checked with whitespace normalization; compileall and unittest discovery ran.

Run from the repository root:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-07-price-return-exercises/review.py
```

**F38:** For positive prices 100, 10⁻⁶, 10⁻¹⁵ the adjacent gross ratios are 10⁻⁸ and 10⁻⁹, but the exact endpoint gross is 10⁻¹⁷. That is below half the float64 gap above −1 (2⁻⁵⁴), so the cumulative return rounds to −1. The original source returned normally despite the stated range restriction. The [initial runner](initial-review.py) and captured result preserve the failing rejection predicate; to replay, run that runner from the same relative evidence directory in a worktree at the baseline (its output is results.json). The corrected source rejects the cumulative result and the corrected suite preserves the earlier demonstration and method count.

The rational expectations are separate from the executed listing. Raw fill mechanics and the FX illustration are supplemental. A simple-only API and vendor adjustment metadata are design/conceptual reviews. Live data, total-return accounting and independent acceptance remain outside this scope. F28/F32 remain open.

**120/136 local prompts scoped; 16 remain.** Next: Section 7.16 local exercises.
