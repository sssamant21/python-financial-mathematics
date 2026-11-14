# V-141 — Section8.9 complete financial factories and report controls

Candidate based on `5106894e21bb783f3a895eb6df58e0f66bc9aed9`. [Checker](../chapter-08/code/check_section_09_factory_range.py) · [Observer](chapter-08-factory-observer.txt) · [Scoped runner](chapter-08-factory-scope-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-factory-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-factory-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-factory-scope-runner.txt .
```

[Baseline](chapter-08-factory-baseline.json) retains79 passes/51 mismatches with the reconciled complete-model/input contract;[replay](chapter-08-factory-baseline-replay.json) has identical predicates. [Corrected](chapter-08-factory-corrected.json):130/130 passed. Actual subprocess stdout/stderr/exits retained. These are51 observed predicate mismatches,not51 separate defects:21 numerical/range/convention cases and30 input-type/nonfinite/conversion-policy cases. Final-overflow exception normalization and stronger standalone input checks are explicit adopted conventions,not retrospective claims that every old factory promised them.

## Complete expressions and independently derived references

Accumulation uses P=1000 and the exact represented binary R=float(.04):value P*exp(R*t),first P*R*exp(R*t),second P*R²*exp(R*t). Discounted cash flow uses C=5000,T=4 and represented rate r:value C*exp(-T*r),first -T*C*exp(-T*r),second T²*C*exp(-T*r). Each is evaluated as a complete model expression,not by first reporting a price and then multiplying a derivative coefficient. This can rescue a finite derivative when the price is unreportable,or a finite subnormal result when exp alone underflows. The shared audited Section8.1 scaled helper uses its private1300-digit context and finite-input cutoffs. True unreportable final results raise ValueError;final underflow and its sign are retained.

Profit uses exact represented q in -1000+80q-q²/4,80-q/2 and-.5,with0<=q<=500. Ratio uses (100+8x)/(50+3x),100/(50+3x)² and-600/(50+3x)³,with x>0. Complete rational reporting avoids both overflowing numerator/denominator at large finite x and premature powers in the derivatives. At large x the value approaches8/3 while first/second derivatives can underflow to positive/negative zero. This arithmetic policy changes intermediate-rounding composition explicitly;it does not infer financial meaning or units from numeric success.

All model callables now use the comparator's finite int/float input convention,excluding bool/text,normalizing oversized integer and nonfinite input failures. Accumulation time and discount rate remain signed finite mathematical arguments;profit and ratio keep their stated domains. These controls do not certify real financial time horizons,market rates or cost assumptions.

Independent references evaluate the complete expressions at2000 and2600 Decimal digits and require final binary agreement. Exponential exponents beyond±10000 use a conservative final-range rule for these fixed bounded coefficients. Rational/polynomial references use independent Decimal expressions,not source helper calls. Relative tolerance4e-15,no absolute floor,and exact zero signs are applied. Both share Python's arithmetic backend,so no independent library certification is claimed.

Sixty-three numerical reference cases cover seven accumulation points,six discount rates,five positive ratio scales and three profit points times three outputs. Forty-eight input-type/nonfinite/conversion controls and12 explicit profit/ratio domain cases make60 input controls. Three report controls require four model names,16 default reports and standards-compliant allow_nan=False JSON roundtrip. Four facade checks each verify five function evaluations plus one first and one second analytic callback;these are comparator-facing calls,not a general bound on internals or arbitrary supplied functions. Total130 predicates.

## Scope and remaining obligations

[Scoped results](chapter-08-factory-scope.json):five Python files compiled,three scripts passed,and five before/after hashes matched. This includes unchanged legacy Section8.9 and V-139 comparator report checkers. Fresh601 Python/388 check-test/602 required source-fixture inventory is not a full execution. V-140 remains latest full600/387/601 evidence until a separately recorded refresh. Thirty-five selected COV categories remain partial;none closed.

The default demo has fixed16 reports. step_ladder still consumes a caller iterable into memory with no built-in length cap;callers must bound input,callback cost and output size. Standard JSON roundtrip does not certify schema evolution,serialization portability,provider accuracy or sink publication. Broader conditioning/branch/noise,resource and independent mathematical/editorial/platform/release/canonical acceptance remain open.

Next substantive item:Section8.9 step-ladder/report resource and late-input-failure contracts,then Chapter8 assessment alignment. Preserve earlier accuracy diagnostics;no certification claimed. Book1 progresses through independent trackers.
