# V-170 — Section9.4 complete Taylor change and selector policy

Based on `824ab9a1f874f18f379e8137812958f3a841f15a`. [Checker](../chapter-09/code/check_section_04_quadratic_contracts.py),[observer](chapter-09-quadratic-contract-observer.txt),[scope runner](chapter-09-quadratic-contract-runner.txt),[scope outcomes](chapter-09-quadratic-contract-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-quadratic-contract-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-quadratic-contract-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-quadratic-contract-runner.txt .
```

[Baseline](chapter-09-quadratic-contract-baseline.json):38 passes/18 failed predicates,actual child exit1;[actual replay](chapter-09-quadratic-contract-baseline-replay.json) identical. [Corrected](chapter-09-quadratic-contract-corrected.json):56/56 predicates/exit0. Observer exit0 records a child result,not a numerical pass. Twelve numeric/report failures include two exact-zero sign-policy alignments;six failures concern the newly declared strict integer selector policy. These are not18 unique preexisting mathematical defects.

Fourteen derivative/shock vectors at both orders use independent1800/2400-digit complete Decimal polynomial references. Complete rational d1*h+d2*h²/2 evaluation precedes float reporting;intermediate overflow/underflow/cancellation does not determine the final value. True final overflow raises ValueError;nonzero underflow may return signed zero,exact complete zero positive zero. Relative5e−14/zero absolute slack. Six selector-type,three selector-domain,16 scalar-input and three retained-priority/default controls complete56. Both derivatives and shock remain validated before order;unused second derivative still validated for order1.

Three files compiled,three commands/two checkers pass,three hashes verified before-after;original section checker unchanged. Only taylor_change text changes ([comparison](chapter-09-quadratic-contract-scope-comparison.json));single/portfolio shock functions use it transitively,but their whole numerical reports remain pending. Eight escaped manuscript backticks repaired around actual lab command/path fences;both printed commands execute. Fresh617 Python/404 check-test/618 required-blob inventory is not full execution;full pinned refresh records execution separately.

[Later dispositions](chapter-09-quadratic-contract-resume-disposition.json) resolve two saved quadratic numeric cases and adopt a strict selector policy;the saved single-cash-flow finite-value rescue remains OPEN. Historical initial/replay records unchanged. All36 selected COV categories partial,none closed. Next:Section9.4 single-cash-flow complete value/first/second/normalized reports,then portfolio/shock contracts. Broader conditioning,resources,financial/model/independent mathematical/editorial/platform/release/canonical acceptance pending. Book1 tracked independently.

Executed source/checker bytes verified against `f8aa4390a2cf5bd69b885a099d0da2ad6082216f`;[source manifest](chapter-09-quadratic-contract-publication-verification.json).

[Next single-flow checkpoint](chapter-09-single-flow-resume-initial.json),[actual replay](chapter-09-single-flow-resume-replay.json),[runner](chapter-09-single-flow-resume-probes.txt) retain two OPEN numerical cases and one separate whole-report range-policy observation;not part of the56 passing predicates.
