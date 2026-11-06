# Section 19.3 applied linear accounts: range follow-up

- Baseline source: [`08821c3755545efe52ed655fbab159b8a858f1ab`](https://github.com/sssamant21/python-financial-mathematics/tree/08821c3755545efe52ed655fbab159b8a858f1ab/books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code).
- Corrected source: [`bf9d4fccf807a1ee631a737cb4b20e507808e0cc`](https://github.com/sssamant21/python-financial-mathematics/tree/bf9d4fccf807a1ee631a737cb4b20e507808e0cc/books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code).
- [Initial investigation](chapter-19-linear-applied-range-baseline.md) · [Exact blob manifests and captured results](chapter-19-linear-applied-range-followup.json) · [Runnable checker](../chapter-19/code/check_linear_applied_range.py) · [V-90 runtime refresh](runtime-refresh-2026-11-06-r09.md).

The checker found 12 mismatches in 27 cases on the baseline, replayed those same 12 mismatches against the baseline blobs with only the checker overlaid, and passed all 27 cases on the corrected sources. Each source snapshot contained 52 verified Python blobs including the checker. The JSON retains the expected and actual results and process exit statuses for the initial failure, replay and corrected run.

Decimal references evaluate the constant-flow balance, affine integral and crossing using the represented inputs at high precision. Exact constructed cases distinguish cancellation and signed zero from true overflow. The piecewise case checks order and rejects a nonrepresentable intermediate segment even when a later segment could restore a finite balance. Euler cases exercise cancellation, a width smaller than the least positive float, and overflow. The assessment values are compared with analytic or geometric references; the review flags remain false.

Section 19.3 now reuses the range-aware affine account and crossing kernels. The integrated exponent and Euler width are carried exactly into their final evaluation. Section 19.3 allows balance underflow to signed zero; the stricter defaults used by Sections 19.2 and 19.8 remain in place. A positive crossing that cannot be represented as a finite nonzero time is rejected.

Run from the repository root at the corrected revision:

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-19/code/check_linear_applied_range.py
```

For baseline replay, check out the baseline in a separate directory and copy only the pinned checker to the same relative path before running the command. This is selected COV-84 evidence on one runtime. It does not establish exhaustive coverage, independent review, supported-platform validation, release acceptance or canonical approval.
