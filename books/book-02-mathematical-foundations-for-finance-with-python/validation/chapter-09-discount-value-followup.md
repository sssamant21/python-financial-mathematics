# V-164 — Section9.3 complete discounted value

Based on `5386dc2e5da136dbb1f31bbcc015a86b4d4fb190`. [Checker](../chapter-09/code/check_section_03_discount_value.py),[observer](chapter-09-discount-value-observer.txt),[scope runner](chapter-09-discount-value-runner.txt),[scope outcomes](chapter-09-discount-value-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discount-value-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discount-value-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discount-value-runner.txt .
```

[Baseline](chapter-09-discount-value-baseline.json):26 passes/eight failed predicates,actual child exit1;[actual replay](chapter-09-discount-value-baseline-replay.json) identical. [Corrected](chapter-09-discount-value-corrected.json):34/34 predicates/exit0. Observer exit0 records child outcomes,not a numerical pass. Predicate failures are not unique defects.

Eighteen independent1800/2400-digit Decimal complete coefficient-times-exponential references cover saved finite rescue2.233994766161711,underflow rescue,subnormal coefficients,recovered nonzero tiny reports,true final overflow,zero-horizon/zero-rate identities and products exceeding float exponent range. Oracle amplitude guards at1000/−2000 are independently outside binary64 report range;production exponent guards±10000 avoid enormous products without excluding a rescuable finite coefficient. Relative5e−14/zero absolute slack;underflow can report positive zero. Twelve input/domain controls plus two ambient context outcomes/two unchanged-parent-context controls complete34.

Production retains c,t,r validation order and positive-c/nonnegative-t domain. Complete exponent Fraction arithmetic plus private1300-digit Decimal evaluation prevents premature exponential/product overflow/underflow;true final float overflow raises ValueError. This is selected reference agreement,not universal correctly-rounded transcendental certification. Four files compiled,four commands/three checkers pass,four hashes verified before-after;prior affine125 and original section checkers unchanged. Fresh614 Python/401 check-test/615 required-blob inventory is not itself full execution;full pinned refresh records execution separately.

[Later saved-probe disposition](chapter-09-discount-value-resume-disposition.json) resolves the standalone value case only;historical initial/replay/prior OPEN records unchanged. [Scope comparison](chapter-09-discount-value-scope-comparison.json) shows only discount_value text changed. discount_shock invokes it,so its baseline behavior benefits;whole shock/error report correctness is not implied by unchanged wrapper text.

All36 selected COV categories partial,none closed. Next:Section9.3 discounted shock/error reports,then ladder/revenue contracts. Broader resources,conditioning,financial/model/independent mathematical/editorial/platform/release/canonical acceptance pending. Book1 tracked independently.

Executable source/checker bytes verified against `9a00097d0669af492c85f0468cd93c2bd447100c`;[source manifest](chapter-09-discount-value-publication-verification.json).

[Next shock checkpoint](chapter-09-discount-shock-resume-initial.json),[identical replay](chapter-09-discount-shock-resume-replay.json),[runner](chapter-09-discount-shock-resume-probes.txt) retain three OPEN report observations;these do not add passing predicates to the34-value scope.
