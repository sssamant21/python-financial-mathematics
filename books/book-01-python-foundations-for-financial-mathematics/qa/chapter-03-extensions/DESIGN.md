# Extension contracts and packaging plan

## 1 — Signed cash flows

signed_present_value discounts one finite signed Decimal period-n flow to period0. Positive means receipt and negative payment from the same owner's perspective. Currency and matching effective-period meaning are caller metadata. Delegate absolute-value valuation to the unchanged canonical nonnegative function, then restore the sign. Negative zero normalizes to positive zero. The canonical function continues rejecting negative amounts. Its count/rate domains, fixed context, propagated exceptions and numerical limitations remain applicable. No intermediate flows or currency conversion are added.

## 2 — Finite positive growth underflow

Construct rate exactly as minus2000 nines after the decimal point using the Decimal tuple constructor, avoiding an ambient-context subtraction that would round it to−1. Then1+r=10^-2000, a finite positive representable base; the exact1000-period factor is10^-2000000. Under the fixed policy it becomes0E-1000038 with Underflow/Inexact flags. The source positive-factor guard raises ArithmeticError. This is selected evidence of a documented numerical limitation, not a newly discovered source defect or proof of all extreme inputs.

## 3 — Explicit currency posting

post_usd_cents posts a final USD valuation once with quantum.01 and ROUND_HALF_UP. It accepts finite signed Decimal magnitude<=1e24, operates in a local fixed40-digit context and leaves raw input unchanged. Wrong representation raises TypeError; unsupported value raises ValueError. This choice is an educational posting policy, not a universal accounting rule. Later calculations use the posted value only if the business model explicitly chooses it. The1.005 half-cent fixture demonstrates that posting before doubling changes2.010 into2.02. Canonical valuation remains unquantized.

## 4 — Equivalent effective annual conversion specification

Before implementation, define annual_effective_to_periodic(annual_effective:Decimal,*,periods_per_year:int)->Decimal as (1+annual_effective)^(1/m)-1. Annual input is effective, not a nominal quotation; r must be finite and>-1, m an integer1..366 excluding bool. Output is dimensionless effective rate per equal subdivision of that annual period. No fees, day-count/calendar conversion or regulatory APR interpretation is implied.

A future implementation must specify its fractional-power algorithm and complete context, factor/result guards, cancellation/underflow behavior near−1 and0, exception classes and tolerance/error analysis. Validate all inputs even for m1; check zero, negative rates, m1, upper frequency and independently known annual/periodic pairs such as quarterly.02 yielding annual.08243216. Verify caller-context isolation and original/effective metadata. No fractional-power implementation is added in this review: the task explicitly asks to document before adding it. Passing the known-pair check alone does not validate a general root algorithm.

## 5 — Scenario report

scenario_report emits one row per supplied nominal annual quotation with original quotation, effective periodic rate, frequency, period count, period0 principal, future valuation period, numeric future amount, currency label, assumptions and policy. Values stay numeric until JSON serialization; no ranking/probabilities are inferred. Canonical exceptions propagate. The report assumes one constant rate and no intervening flows/fees/tax/inflation/conversion; currency is an explicit label, not inferred/validated monetary metadata. The helper is not persistence or an arbitrary external-data parser.

## 6 — Chapter5 packaging migration plan

1. Preserve the existing public signatures, keyword-only requirements, amount/rate/count domains, exception classes, fixed context and valuation staging as the compatibility baseline.
2. Place the existing module under a src-layout package; export the same public functions through a documented package interface. Keep internal helpers private and migrate imports deliberately.
3. Add pyproject metadata with a reviewed build backend, declared Python compatibility and standard-library-only runtime requirements. Keep checker/test tools in development dependencies rather than runtime dependencies.
4. Move source tests to a tests directory; run known values, domains, context preservation, mutation detection and demo assertions against the installed package, not an accidentally importable checkout.
5. Build wheel/sdist in isolated tooling; install the wheel into a fresh environment; verify import origin and silent import, run the unchanged acceptance suite, and compare demo output. Review Windows/macOS separately.
6. Version any numerical-policy or sign/currency extension separately; do not weaken the old nonnegative contract. Record source/build hashes, exact runtime/tool versions and test evidence. Document migration/deprecation if old module imports change.

This is a plan, not an executed build/install result. Chapter5 packaging evidence remains separate.
