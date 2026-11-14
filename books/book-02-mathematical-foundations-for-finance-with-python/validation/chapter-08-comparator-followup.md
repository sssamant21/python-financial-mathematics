# V-139 — Complete comparator quotients and exact tolerance reports

Candidate based on `da173ca7e4bffb6ec72bf861f30b242dda78f910`. [Checker](../chapter-08/code/check_section_09_complete_report.py) · [Observer](chapter-08-comparator-observer.txt) · [Scoped runner](chapter-08-comparator-scope-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-comparator-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-comparator-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-comparator-scope-runner.txt .
```

## Initial failures and explicit reporting convention

[Initial77 baseline](chapter-08-comparator-initial77-baseline.json) retained70 passes/7 failures and[corrected77](chapter-08-comparator-initial77-corrected.json) passed. Adding three signed-zero contract cases gives an[expanded80 baseline](chapter-08-comparator-baseline.json) with73 passes/7 failures,[identical predicate replay](chapter-08-comparator-baseline-replay.json) and[80 corrected passes](chapter-08-comparator-corrected.json). Actual subprocess exits/stdout/stderr remain recorded;the baseline observer stores its child failure as evidence rather than claiming its own zero exit means a pass.

Five failures were first/second method pass flags at the smallest positive binary analytic reference,zero absolute tolerance and relative tolerance.75. The exact threshold is.75*minsubnormal,strictly smaller than the reported minsubnormal error,but binary threshold multiplication rounded up and accepted it. The source now compares the finite reported error and controls against the exact represented-input threshold a+r*abs(analytic),using rational arithmetic. It does not reinterpret analytic callbacks as known true derivatives. Signed/absolute errors remain finite reports of estimate-minus-analytic;unreportable error fields still reject.

Two other failures had accepted finite controls and reportable final outputs:large linear callback1e308*x at x0,h1 has all first estimates1e308 and zero errors,but a premature centered numerator/Richardson intermediate overflowed;constant1e308 has second difference0 but multiplying its center by2 overflowed. The comparator now forms complete sampled forward/backward/centered and second quotients from exact returned binary callback values. Richardson combines unrounded coarse/fine quotients before one final report. These are explicit sampled-callback reporting conventions,consistent with Section8.8;they do not correct callback rounding or prove analytic accuracy.

Existing strict preflight remains:x,h,tolerances finite,h positive,a/r nonnegative,both full and half shifts distinct,finite full perturbations and finite2h;when second is requested,h² must be nonzero and finite. These denominator gates remain narrower than a general final-range API. All four first-method reports must be finite even if one preferred method would be usable. Original callback exceptions propagate;validation priority and callback order stay unchanged. Selected zero-stencil signs are preserved explicitly,including negative zeros in first-difference estimates.

## Independent expectations and exact-source execution

Seventy tolerance/method cases use an independent2500-digit Decimal inequality over exact finite binary values:two absolute tolerances times seven relative tolerances times five methods. Expected estimate0,error−minsubnormal and absolute error minsubnormal are independently fixed by constant-zero callbacks. This validates the report predicate,not the supplied analytic oracle. Two range-rescue identities,seven-call and first-only six-call/no-second-field contracts,zero-step preflight,original-exception identity/short circuit,finite step-ladder order/fourteen calls and three signed-zero stencils complete80 predicates. Shared Python arithmetic backends are not independently certified.

[Scoped results](chapter-08-comparator-scope.json):three Python files compiled,two scripts passed,three before/after source hashes matched. The existing Section8.9 checker passed unchanged;its true unreportable-range assertions remain valid. Fresh600 Python/387 check-test/601 required source-fixture inventory is not a full execution. V-136 remains latest full597/384/598 evidence until a separately recorded refresh. Thirty-five selected COV categories remain partial;none closed. Independent mathematical/editorial/platform/release/canonical acceptance remains pending.

Next substantive item:Section8.9 financial model-factory complete-range/domain and report serialization/input-resource contracts. Broader branch/conditioning/noise and arbitrary callback resources remain open. Book1 has separate progression and evidence.
