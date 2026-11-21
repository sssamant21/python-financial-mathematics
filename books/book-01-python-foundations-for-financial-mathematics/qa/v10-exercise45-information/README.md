# V10 — Section18.15 partial Exercise45 information-loss checkpoint

Pin: `278fe361a26394ce4d2c5d1e1955d804994e150a`. [Runnable review](review.py), [first](first.json), [replay](replay.json), [initial observer](initial-observer.json), [initial observer replay](initial-observer-replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-exercise45-information/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-exercise45-information/review.py replay
```

Both corrected runs pass21 predicates: two exact snippet mean/SE references, ten streaming fields for two samples, eight project VaR/ES values, and one tolerant agreement comparison. The complete18.15 snippet executes twice per run (module import and separate CLI command), and all three extracted sibling listings compile. There are two retained command records per run. Project/performance are imported; their unittest suites are not newly run in this checkpoint. Exact snippets and source identities are recorded. The same fixed-seed snippet result does not establish RNG independence or statistical coverage.

Terminal sample A is [98,100,100,100,100,100,100,102]; B is [99,99,99,99,101,101,101,101]. Both have exact mean100, M2=8, sample variance8/7 and mean-SE sqrt(1/7). Loss is100−terminal. At alpha.75, A has VaR0/ES1 while B has VaR1/ES1. At alpha.90, A has VaR2/ES2 while B has VaR1/ES1. These values follow directly from equal atom probabilities and the source's stated quantile/tail convention. First two exact moments therefore do not identify empirical VaR or the loss ordering. This supports Exercise45 without adding an exact-quantile sketch implementation.

The initial observer incorrectly required bit-identical Welford accumulator states across different observation sequences. Twenty predicates passed and that assertion failed on both runs; both are retained. Source moment fields agree with the independent exact targets within rtol5e-14/atol1e-12, so the comparison now uses that arithmetic tolerance. No source defect or source change is claimed. Exact mathematical moment equality and floating reduction-order differences remain distinct.

This is a **partial18.15** checkpoint, not a new complete workflow, fifty-answer review, twelve-step lab or historical-method count. Resume the remaining chapter-wide exercise/applied-problem assumption obligations, starting with the paired-difference uncertainty contract (Exercise46) and the boundary-frequency/model-review decisions (49–50). Exercise45 counterexample and snippet arithmetic should not be repeated as new work. V10/Book1, F28/F32/F209/F165/F185 and broader acceptance remain open.
