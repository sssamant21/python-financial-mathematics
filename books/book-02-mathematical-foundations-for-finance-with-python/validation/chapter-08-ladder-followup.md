# V-143 — Step-ladder/report resource and late-failure contracts

Candidate based on `953fa30f7a29cc4a27a2817238e5b72f25c635ef`. No source helper changed. [Checker](../chapter-08/code/check_section_09_ladder_contract.py) · [Runner](chapter-08-ladder-runner.txt) · [Initial pass](chapter-08-ladder-initial.json) · [Results](chapter-08-ladder-results.json) · [Identical predicates/resource-report replay](chapter-08-ladder-replay.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-ladder-runner.txt .
```

## Independent report expectations

At x=2 for f(x)=x³,the analytic first/second derivatives are12. On h=.5 and.25,forward is12+6h+h²,backward12−6h+h²,centered12+h²,Richardson12,and the second estimate12. These exact binary polynomial identities independently determine signed/absolute errors and zero-tolerance pass flags. All10 method rows and both full report key sets match;optional second output is absent for first-only requests. These are selected exact report references,not general accuracy or independent mathematical acceptance.

## Consumption,failure and caller budgets

Order and duplicate steps are retained;duplicates are reevaluated without caching. Two second-derivative reports perform14 facade callbacks;first-only performs6 per step. Empty steps return[] without per-step validation,even with otherwise invalid controls. A noniterable steps object raises TypeError before callbacks. These are observed contracts,not a new eager-validation policy.

After a valid first step,a zero second step raises ValueError without returning a partial list. The first report's seven successful callbacks have already occurred;the invalid step is consumed,but the third step remains in the caller's iterator. A callback error on the next report preserves the original exception identity and prior work;the failed callback attempt is counted separately from seven prior successful trace entries. An iterator's own exception likewise propagates after prior work. No callback side-effect rollback or transactional guarantee is implemented.

A caller-controlled itertools.islice prefix bounds a deliberately open-ended generator to two pulled steps and14 observed facade callbacks,without over-reading. This demonstrates the caller's bound,not a built-in step_ladder cap. Two selected reports serialize with sorted keys,compact separators and allow_nan=False to1225 bytes in this runtime,under an explicitly selected4096-byte QA budget,and roundtrip exactly. The threshold is a fixture budget,not a source-enforced or cross-serializer/global output-size guarantee.

Twenty-five predicates passed,with actual initial execution and identical replay retained;no failed source test or source fix is invented. Four Python files compiled,two scripts passed,and four before/after input hashes matched. The exact source manifest and actual stdout/stderr are retained in results. Fresh602 Python/389 check-test/603 required source-fixture inventory is not a full run. V-142 at `a847812cb63d75354199723e5489cd84a579988d` remains latest full601/388/602 candidate Linux evidence. Only one checker was added;no numerical source changed.

Arbitrary iterable length,callback cost,nested provider behavior,total output memory,timeouts/cancellation and concurrent writers remain caller/environment obligations. Finite-prefix evidence does not close the broader resource gap. Thirty-five selected COV categories remain partial;none closed. Independent mathematical/editorial/platform/release/canonical acceptance remains pending.

Next substantive item:Chapter8 Section8.10 assessment prompt-to-source/reference alignment and uncovered exact exercise inputs identified in the existing coverage map. Remaining branch/conditioning/resource and independent obligations stay open. Book1 has separate progression and evidence.

Executable source/checker revision: `4c927c1a3345a86fbe696544badf13c7d53f8943`. [Publication source manifest and pinned inventory](chapter-08-ladder-publication-verification.json). All four scoped tested Python blobs match this revision;inventory is not full execution.
