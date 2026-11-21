# V-227 — Section 10.2 polynomial contracts and partial lab checkpoint

Baseline: `4e4dba9e89d0448ab378b6c6a1d8735bec198942`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected run](first.json), [corrected replay](replay.json), [candidate source verification](candidate-verification.json), [latest full-run delta](runtime-delta.json).

Per-file Git blob SHA and SHA256 values identify the tested candidate files. The baseline revision itself does not contain the fixes.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-polynomial-2026-11-21/review.txt first --chapter
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-polynomial-2026-11-21/review.txt replay
```

Append `--baseline` to read the immutable original sources. Both baseline runs preserve **23 passes and ten failures**: nine iterator, cancellation, primitive-range or reporting predicates and one escaped-markup check. Ordinary CLI fields and selected exercises already passed. Three selected finite-result support cases are labeled as extensions rather than retroactive universal range requirements. These are failed predicates, not a count of independent financial-model bugs.

## Source correction and actual checks

The polynomial helpers now consume coefficients once and apply the existing finite-float conversion. They combine exact `Fraction` expressions of the represented inputs before one final float report. Antiderivatives include the integration constant before rounding. Definite integrals use complete endpoint-power differences without requiring each primitive to fit in a float.

This fixes one-pass coefficient use and preserves small differences between large endpoint values. Selected cases cover zero coefficients, signed-term/constant cancellation, a small coefficient times a large power, zero-width integrals and finite definite results with unreportable individual primitives. Empty coefficients remain rejected, including for zero-width integrals. True final overflow raises `ValueError`; final underflow to zero remains allowed. No signed-zero rule is added. Exact powers can increase integer bit lengths and resource costs; arbitrary-degree or arbitrary-length resource acceptance remains open.

Both corrected runs pass **33 predicates** with identical rows:

| Scope | Predicates |
|---|---:|
| Complete ordinary CLI: 12 numeric fields and six schemas | 18 |
| Exercise source calls/caller composition | 4 |
| Polynomial iterator, numerical and reporting contracts | 10 |
| Runbook markup | 1 |

The native checker gains nine polynomial regression cases. All 21 Chapter 10 Python files compile and verify; all eleven checkers and ten CLI labs pass, giving 22 first-run command records. The scoped replay has three commands; it does not repeat the whole chapter. Source blob identities verify after execution.

Ordinary exponential and midpoint CLI expectations use an independent 140-digit, 120-term exponential series. This does not validate their extreme ranges. Closed-form constant/linear references check cancellation without reusing the actual primitive outputs. Numeric comparisons use rtol 5e-14 and atol 1e-12; zero, exception and schema checks are exact. Ten escaped backticks are repaired, and the manuscript's scoped runtime status explicitly retains unfinished functions and independent/canonical gates.

## Lab and exercise alignment

Six review units cover constants/antiderivatives, oriented signed amounts, ordinary exponential cash flow, midpoint approximation, starting-balance caller composition, and units/evidence. They are review units, not additional tests.

The fourteen exercise dispositions remain distinct: polynomial antiderivatives (1–2), native integral 240 (3), constant-family concept (4), signed cancellation (5), oriented −8 (6), zero-width exponential identity (7), exponential antiderivative (8), nonpolynomial logarithm (9), constant-rate accumulation (10), caller balance 500+240 (11), additivity (12), native quadratic 1/3 (13), and undiscounted accumulation versus present value (14). Conceptual antiderivatives are not claimed as implemented symbolic-integration APIs.

## Explicitly unfinished work

**Section 10.2 remains in progress.** `exponential_definite` and `midpoint_sum` are unchanged. Their complete-expression/range, callback/preflight, zero-width, rounding, iteration and reporting contracts remain separate unfinished work. Resume those obligations next; do not advance to 10.3 from this partial pass.

The candidate inventory remains 642 Python files, 429 check/test scripts and 643 required blobs. Of these required blobs, 641 match V226 at `ad0f11b8eb295b0c062256a47d869044b874aa77`; only the 10.2 source and checker differ. The companion checker is the only direct importer of these polynomial helpers, and the Chapter 10 support run passes. Latest full-book execution remains V226 at its recorded pin. Refresh after the coherent remaining 10.2 code/check batch before advancing to 10.3.

All 38 selected COV categories remain partial; none is closed. Broader resource, provenance, model, platform, release, independent and canonical gates remain open. Book 1 has separate trackers.
