# V-138 — Preset noisy-step sweep and callback report

Candidate based on `2b521783ba191220b3f1f3318ad4d94575e68c4b`. No source numerical helper changed. [Checker](../chapter-08/code/check_section_08_noisy_sweep.py) · [Runner](chapter-08-noisy-sweep-runner.txt) · [Initial execution](chapter-08-noisy-sweep-initial.json) · [Results](chapter-08-noisy-sweep-results.json) · [Identical predicates/report replay](chapter-08-noisy-sweep-replay.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-noisy-sweep-runner.txt .
```

## Independently derived error curves

At x=0,the noiseless cubic's first derivative is0. For samples x³+eta*sign(x),eta=2^-30,centered difference has signed and absolute error h²+eta/h. The first term is truncation;the second is the selected deterministic callback noise. On h=2^-k,k1–16,the exact error minimum is at k10:h²=2^-20 and eta/h=2^-20 give total2^-19. The coarsest and finest grid points both have larger errors. This is a minimum on the stated grid,not the global continuous optimum h=(eta/2)^(1/3),nor a noise-estimation algorithm.

For the quartic at0,the noiseless second derivative is0. With +eta at shifted samples and -eta at the center,eta=2^-40,the second estimate/error is2h²+4eta/h². On k1–18,the minimum is also k10:2h²=2^-19 and4eta/h²=2^-18 give3*2^-19. The continuous stationary point solves h^4=2eta; a finite-grid minimum is not that point by definition.

All selected callback samples and error components are exact binary quantities. The checker derives expectations from these polynomial/noise identities using exact rational arithmetic and final binary reporting;it does not call the source derivative helper to construct expected values. The same Python Fraction arithmetic backend is shared,so this is independent algebraic/model expectation,not independent arithmetic-library acceptance.

## Actual reporting and budgets

The report retains all34 steps,estimates,noiseless derivatives,errors,independently expected errors,truncation/noise components,callback input hex values and call counts. First derivatives use exactly2 callbacks per step (32calls total),in+h,−h order;second derivatives use3 (54calls total),in+h,0,−h order. The measured total is86. The preset grid has a fixed34-step/86-call budget;it is not an input-configurable production selector. No retries,provider requests or adaptive stopping are implemented.

Seventy-five predicates passed:34 exact error curves,34 callback-order/budget records,two finite-grid minima,four coarse/fine-versus-minimum comparisons,and one total-budget check. All initial results passed;no failed source test or source fix is claimed. An actual rerun reproduces the predicates and full sweep report exactly. V-137's10 nominal accuracy exceedances remain separate and unchanged;this report does not relabel them as accuracy passes.

Four Python files compiled,two scripts passed,and four source hashes verified before/after. Fresh599 Python/386 check-test/600 required source-fixture inventory is not a full execution. V-136 at `3db1be648a9acba29d706e2dba0138540adacc7f` remains latest full597/384/598 candidate Linux evidence. Thirty-five selected COV categories remain partial;none closed. Arbitrary functions,estimated/stochastic provider noise,actual finance callback units/conditioning,global step optimality,resource limits and independent mathematical/editorial/platform/release/canonical acceptance remain open.

Next substantive item:Section8.9 derivative-comparator/project report fields,complete quotient/error/tolerance and callback/input-budget contracts identified by the existing Chapter8 coverage map. This follows the completed selected Section8.8 preset sweep;it does not close broader noise/conditioning obligations. Book1 progresses through its own trackers.
