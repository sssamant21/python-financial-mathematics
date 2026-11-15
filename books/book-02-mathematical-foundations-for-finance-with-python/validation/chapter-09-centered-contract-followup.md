# V-160 — Section9.2 centered sampled reporting and callbacks

Based on `14675f3f86154c3cdc5438c2808287592342eca8`. [Checker](../chapter-09/code/check_section_02_centered_contracts.py),[observer](chapter-09-centered-contract-observer.txt),[scope runner](chapter-09-centered-contract-runner.txt),[scope outcomes](chapter-09-centered-contract-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-centered-contract-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-centered-contract-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-centered-contract-runner.txt .
```

[Baseline](chapter-09-centered-contract-baseline.json):41 passes/seven failed predicates,actual child exit1;[actual replay](chapter-09-centered-contract-baseline-replay.json) identical. [Corrected](chapter-09-centered-contract-corrected.json):48/48 predicates/exit0. Observer exit0 is evidence recording,not itself a numerical pass. Seven predicate failures are not a unique defect count.

Eleven independent1800/2400-digit Decimal sampled-ratio references cover ordinary quadratic,negative input,overflowing difference/2h,underflowing derivative,overflowing normalization,subnormal input,exact zero,final underflow and true final overflow. Formula uses exact represented x,h and callback samples evaluated at rounded x±h;the denominator stays nominal2h. No analytic derivative equivalence or discretization error bound claimed. Relative5e−14/zero absolute slack;exact-zero difference is positive zero,negative nonzero underflow retains sign.

Fourteen preflight controls,21 sample/exception-stage controls,one zero-center consumption control and one callable-priority control complete48. Finite/distinct perturbations are checked before callback. Then central/plus/minus order is retained;the first invalid output or callback exception stops later calls. Zero central output rejects after the three finite callbacks,as before. No retry/rollback. Input/domain/smoothness/noise/side-effect policy remains a caller obligation.

Seven files compiled,six commands/five checker invocations pass,seven hashes verified before-after;prior checkers and all other Section9.2 function text unchanged ([comparison](chapter-09-centered-scope-comparison.json)). Fresh612 Python/399 check-test/613 required-blob inventory is not itself full execution. A full pinned refresh records execution separately.

[Later scoped disposition](chapter-09-centered-resume-disposition.json) resolves the retained nonfinite-perturbation callback observation only;historical initial/prior OPEN records remain unchanged. All36 selected COV categories remain partial,none closed. Independent mathematical/editorial/platform/release/canonical acceptance pending. Next:Section9.3 first-order Taylor complete affine update,discounted-change/error report and callback contracts. Book1 tracked independently.
