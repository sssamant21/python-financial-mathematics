# V-137 — Finite-difference noise and quantization limits

Candidate based on `926330850a54eb97363c131b2d0188e7d7ee0bfa`. No numerical helper was changed. [Runnable checker](../chapter-08/code/check_section_08_noise_contract.py) · [Scoped runner](chapter-08-noise-runner.txt) · [Actual results](chapter-08-noise-results.json) · [Identical predicate/diagnostic replay](chapter-08-noise-replay.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-noise-runner.txt .
```

## Independently derived models

For x=0,h=2^-k,k in5,10,20,30 and eta=2^-40, the selected callback samples are exact binary quantities. A quadratic with sign noise f(x)=x²+eta*sign(x),f(0)=0 has centered first estimate eta/h although its noiseless derivative is0. A quadratic with +eta at nonzero x and -eta at0 has second estimate2+4eta/h² although the noiseless second derivative is2. A constant +eta offset cancels from both differences, giving0 and2. These closed forms derive from the stated deterministic sample values, not from the source quotient helper. The selected powers avoid callback-rounding ambiguity; there is no bound claimed for all real x or arbitrary noisy providers.

For quantized identity q*round(x/q),q=2^-10 and nearest-even ties, first estimates at h=q/4,q/2,q,3q/2,2q are0,0,1,4/3,1. The noiseless identity derivative is1. The default suggested first step at0 is below q/2 and reports0; the suggested second step applied to a similarly quantized square also reports0 although the noiseless second derivative is2. Every chosen quantization residual is bounded by q/2; a finite and distinct represented perturbation alone does not remove quantization bias.

Sixteen noise-formula observations,five quantization observations,two suggested-step observations and four amplitude/grid controls make27 arithmetic/contract predicates; all pass. Twenty-three analytic-accuracy diagnostics use an explicitly chosen nominal absolute tolerance1e-8;10 exceed it. [Initial accuracy screen](chapter-08-noise-accuracy-screen.json) preserves those10 mismatches. That nominal tolerance is an observer diagnostic,not an advertised source guarantee. No failed accuracy diagnostic is relabeled a passed accuracy test or a corrected source defect. Full predicate/diagnostic replay agrees exactly.

## Actual scope and limits

Four Python files compiled,two selected scripts passed,and four Git input hashes matched before/after. Actual per-script stdout/stderr and source manifest are retained. Fresh inventory598 Python files/385 check-test scripts/599 required Python-fixture blobs is not a full run. V-136 at `3db1be648a9acba29d706e2dba0138540adacc7f` remains latest full candidate Linux evidence:597 compiled/384 passed/598 verified input blobs. No full refresh is implied by this one added checker.

This batch establishes selected deterministic noise/cancellation/quantization behavior and correct arithmetic,not derivative accuracy for arbitrary functions,an optimal step selector,provider noise estimation,a smoothness bound,a robust production algorithm or resource guarantees. Thirty-five selected COV categories remain partially addressed;none closed. Independent mathematical/editorial/platform/release/canonical acceptance remains pending.

Next substantive item:COV-51 noisy-step sweep/reporting diagnostics with independently known error trends and explicit callback/input budgets;then remaining helper-copy/conditioning obligations. Book1 has separate trackers and progression.

Executable source revision: `45aee3efd7f82b754b01420f8c170492a6b601ad`. [Publication source manifest](chapter-08-noise-publication-verification.json). Four scoped tested source/checker blobs match this revision; metadata pins do not alter executable inputs.
