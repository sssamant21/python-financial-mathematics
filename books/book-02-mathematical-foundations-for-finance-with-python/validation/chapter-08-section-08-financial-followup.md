# V-134 — Section 8.8 complete financial expressions

Candidate based on `39c3e62d59aade825ff6c414ba6bbbcd66666a90`. This is assistant-run exact-source execution on Python 3.12.14/Linux, not independent mathematical, editorial, platform, release or canonical acceptance.

## Contract and independent expectations

For represented finite binary inputs, discounted price is the complete expression `c exp(-r t)`, with strictly positive cash flow and nonnegative years. Multiplication of rate and years and the exponential must not reject an otherwise finite final price. The helper now uses Section 8.1's existing complete scaled-PV implementation. Zero years returns cash; positive underflow reports zero; an unreportable final price raises ValueError. Input validation order remains cash, years, rate, followed by the domain check.

Normalized duration and convexity now explicitly refer to complete model prices, rather than a quotient of separately rounded binary price samples. With represented shifted rates `ru = float(r+h)` and `rd = float(r-h)`, set `u=exp(-t(ru-r))` and `d=exp(-t(rd-r))`. Duration is `-(u-d)/(2h)` and convexity is `(u-2+d)/h²`. Cash scale cancels before reporting. The denominator remains the requested represented h, not a substituted actual grid spacing. An asymmetric represented grid can produce a negative sampled curvature; the sampled result is not silently replaced by analytic t².

The positive reportable base-price gate remains first, followed by strict positive finite h and finite distinct represented r±h. Shifted absolute prices need not individually be reportable. Analytic curvature is the final report of exact represented t²; truly nonfinite final normalized or analytic outputs raise ValueError, while final underflow is allowed. Zero years retains duration -0.0 and convexity +0.0.

The source uses private 1600-digit Decimal arithmetic for normalized ratios and the existing 1300-digit scaled price helper. A growing normalized exponent above 10000 cannot yield a finite convexity even with the largest finite binary h; a decaying term below -10000 can be omitted at binary report precision under these finite-input bounds. These are scoped finite-binary range policies, not an arbitrary-precision API or a proof of every rounding boundary.

The new checker independently computes full absolute prices and shifted absolute prices using 1800 and 2300 Decimal digits, divides complete expressions before final binary reporting, and requires precision agreement. It does not call the source scaling or ratio implementations for expected values. Both implementations share Python's Decimal exponential backend: this is not an independent library certification. Relative tolerance is 4e-15 with no absolute floor; zero and zero sign are checked explicitly. Analytic references use the represented time and its exact Fraction square.

Coverage includes 38 named/seeded price cases, seven normalized five-field vectors, zero years, subnormal scales, finite results despite exponential/intermediate overflow or underflow, an unreportable shifted absolute price with reportable normalized results, asymmetric represented shifts, input-type/domain/order guards, collapsed and nonfinite shifts, zero base price and true final-range failures. The 84 predicates are not 84 independent methods, exercises, defects or coverage categories.

## Retained execution

- [Initial 79-predicate baseline](chapter-08-section-08-financial-initial79-baseline-expanded.json): 45 passed,34 mismatches; [corrected 79](chapter-08-section-08-financial-initial79-corrected.json):79 passed.
- [Expanded baseline](chapter-08-section-08-financial-baseline-expanded.json):45 passed,39 mismatches among84; [baseline replay](chapter-08-section-08-financial-baseline-expanded-replay.json) has identical observations. The five additional predicates cover an unreportable shifted absolute price.
- [Corrected expanded execution](chapter-08-section-08-financial-corrected.json):84/84 passed against the candidate source blob. The earlier [seven-probe screen](chapter-08-section-08-financial-baseline.md) is preserved separately.
- [Initial legacy-check failure](chapter-08-section-08-financial-legacy-initial.json) retains its actual traceback. Two old assertions were reconciled with the stated complete-price contract: huge negative discount exponents may legitimately underflow to zero, and final price overflow uses ValueError rather than leaking OverflowError. The latter was reviewed as an obsolete predicate, not claimed as a separately observed second failure. Other predicates are unchanged.
- [Chapter 8 scope](chapter-08-section-08-financial-scope.json):54 Python files compiled,44 check/test scripts passed,54 source hashes verified before and after execution. Actual per-script stdout/stderr and exact Git blob manifest are retained. [Runner](chapter-08-section-08-financial-scope-runner.txt).

Reproduce from repository root:

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_08_financial_range.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-financial-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-financial-observer.txt . baseline-expanded 39c3e62d59aade825ff6c414ba6bbbcd66666a90
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-08-financial-scope-runner.txt .
```

The observer retains failed baseline observations as data; inspect its failed count, not merely process exit. The scope runner asserts all actual script exits and preserves before/after hashes. It derives current inventory, which is not itself execution of every file.

## Limits and next item

Fresh candidate inventory:596 Python files,383 check/test scripts,597 required Python/fixture blobs. This batch executed Chapter 8 only. V-133 at `30fe802218e5ad9978031287330cd887ebbcf1dc` remains the latest full candidate Linux execution:595 compiled,382 scripts passed,596 required blobs verified. Thirty-five selected COV categories remain partially addressed; none closed. COV-51's independent suggested-step references, broader noise/conditioning/resource cases and independent acceptance remain open. Next substantive item: Section 8.8 suggested-step independent numerical references and input/scale/represented-grid contract. Book 1 has separate trackers and evidence.
