# Chapter 8 — Scoped reference runtime and dashboard review

**Date:** 2026-10-27. **Source:** Book 1 manuscript baseline `f429fb81b8d8f7d228100333c76019d583200d64`; Book 1 Chapter 8 files were unchanged through `7844a56b32490f94a82ff0820a3db1640825be92`. **Reviewer:** Codex.

## Result

PASS for 132 reference test methods: eight each for Sections 8.1–8.12, 16 dashboard acceptance tests in 8.13, and 20 companion solution tests in 8.14. No skips were reported. [Detailed unittest output](all-tests.log) and [machine-readable results](results.json) are retained.

The chapter index reports earlier test passes and visual reviews for all twelve labs and the dashboard. This run independently reproduces the stated test counts; those prior image inspections remain historical claims. The new visual review covers the dashboard only, not all prior chart images.

## Environment and reproduction

Python 3.12.14 on Linux x86_64 (glibc 2.39), NumPy 2.3.5, pandas 2.2.3, Matplotlib 3.10.8, with `MPLBACKEND=Agg`. From the repository root, run:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-runtime/run_reference_suites.py books/book-01-python-foundations-for-financial-mathematics/chapter-08 /tmp/chapter08-repro
```

The script extracts the complete implementation and unittest blocks, and extracts the published CSV fixture for the dashboard. It runs each suite as a separate unittest process in the output directory and saves detailed logs and JSON. An initial harness attempt omitted the CSV fixture and therefore did not load the dashboard suite; the fixture was then extracted and the complete run succeeded. This was a harness setup issue, not a manuscript failure.

## Dashboard inspection

The documented CSV fixture was used with `MPLBACKEND=Agg python dashboard.py --input prices.csv --out visual_review`. The generated [dashboard PNG](dashboard.png) was visually inspected: all four labeled panels rendered, the ALPHA missing-price gap remained visible, and the labels show 11/12 prices, 1/2 complete linked paths, and 3/5 paired returns. Input SHA-256: `0f9ec721d779423c2505a6c7788b81d60fba107e8347c7891c1f4973c006f27c`. PNG SHA-256: `a2432a459ef7d7f386acbc7a7182fa7b1a724932959c7bc50974e0c06c83a258`. This inspection does not establish accessibility across devices or cover all chart examples.

These scoped checks do not independently validate all worked answers, mathematical assumptions, platforms, dependency versions, or the entire manuscript. Comprehensive review and acceptance remain pending.
