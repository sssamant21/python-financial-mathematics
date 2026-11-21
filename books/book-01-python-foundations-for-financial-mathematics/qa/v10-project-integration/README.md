# V10 — Section 18.14 project report/risk/stream integration

Source pin: `ce38a04197aef40afd31e54adbb8d0bdadc588a3`. [Runnable review](review.py), [first run](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-project-integration/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-project-integration/review.py replay
```

Both runs pass **2,520 predicates** with identical rows. All 81 ordered length-four paths over {80,100,120} are deterministic arithmetic fixtures, not equally likely model draws. Eight project report fields at alpha .625/.75/.96 are checked against independent exact raw moments and atom-CDF/tail-probability expectations: 1,944 fields. Eighty-one loss-conversion lists are checked against direct subtraction. Another 486 VaR/ES comparisons verify Section 18.12 agreement; these sibling comparisons are not independent oracles. Nine fields verify project versus Section 18.13 streaming count/mean/SE for seed42 counts20/101/1000 in the documented serial order.

The atom oracle accumulates state masses through the CDF and then allocates tail probability, distinct from the source's sorted observation-equivalent ES. Sample variance uses the exact centered sum divided by n−1; SE uses its square root divided by sqrt(n). Numeric checks use rtol5e-14/atol1e-12. List equality is exact. The source's displayed-decimal risk convention is preserved and is not confused with Book2's represented-binary-input convention.

Each run executes the complete verbatim project demo, twelve existing unittest methods and compilation of the three extracted sibling listings. Across both runs: four command records, 24 invocations of twelve existing project methods. Sibling listings are imported/compiled, not claimed to have their full test suites rerun. Exact whole-manuscript identity matches the prior F187 evidence. Its eleven baseline failures, corrected56 predicates and observer corrections retain their original scope.

These selected interfaces align for nonnegative terminal values. They do not resolve F185 signed-normal-model terminal incompatibility or F32 shared-model metadata/valuation integration. Quantile/ES sampling uncertainty is not quantified by the mean SE. Configurable probabilities, costs, weights, joint portfolios, replications and acceptance policies remain design extensions. No new workflow, answer, step or historical unique-method totals are added.

Next: **18.15 chapter-wide exercise/applied-problem assumptions**. V10 and Book1 remain in progress; F28/F32/F209/F165/F185 and broader model, resource, platform, release, independent and canonical acceptance remain open.
