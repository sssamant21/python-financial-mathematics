# Sections3.10–3.13 —36 exercise answers

Scoped technical review on2026-10-29. Exact source calls, temporary policy/mutation copies and conceptual proposals are distinguished below.

## 3.10-E1

Nominal annual8% convertible quarterly gives effective quarterly .08/4=.02; exact source conversion agrees.

## 3.10-E2

Effective annual=(1+.02)^4−1=.08243216. The expected Fraction(51,50)^4−1 is independent of the source implementation.

## 3.10-E3

One-period discount factor at25% is1/1.25=.8; exact source agrees.

## 3.10-E4

A supported−10% periodic rate has factor1/.9>1. Forward decline makes a future positive amount worth more at the earlier time under that scenario.

## 3.10-E5

Boolean horizon and fractional frequency raise TypeError; infinite rate raises ValueError. Exact source functions were exercised separately.

## 3.10-E6

j/12 converts a nominal annual quotation convertible monthly. An effective annual rate instead requires(1+r_month)^12=1+r_annual; dividing it by12 generally does not satisfy that relationship.

## 3.10-E7

At precision3, direct2/3=.667 while2*(1/3)=.666 because the reciprocal is rounded before multiplication. The initial100/7 fixture happened to agree; its failed distinguishing predicate is retained as a harness error, not a source defect.

## 3.10-E8

Proposed equivalent-effective conversion: r_period=(1+r_annual)^(1/m)−1, finite effective annual r>-1, positive integer m with explicit cap, matching equal periods, dimensionless output. Specify Decimal fractional-power algorithm/context, precision/error bounds, signals and near−1 behavior before implementation; do not silently reuse nominal j/m.

## 3.10-E9

Precision2 with Inexact trapped raises Inexact in the chosen accumulation fixture. localcontext restores caller settings/flags/traps. This is selected signal behavior, not exhaustive extreme-domain certification.

## 3.11-E1

Nested apply_factor(amount, factor=discount_factor(periodic_rate_from_nominal(j,...),periods=...)) matches the staged wrapper within1e−24 for this fixture. Staging is easier to inspect. Python evaluates argument expressions before the outer call, so the nested expression can validate rate conversion before outer amount validation; the canonical wrapper validates amount first.

## 3.11-E2

104.04 due after two quarters at nominal8% quarterly: periodic .02 and PV=104.04/1.02^2=100. Exact source wrapper agrees with the hand-checkable benchmark.

## 3.11-E3

Treating nominal annual12% as monthly12% compounds1.12 twelve times instead of the convertible-monthly1.01 factor. The factors differ; units/convention are part of the contract.

## 3.11-E4

Exact wrapper rejects infinite amount(ValueError), fractional frequency(TypeError), and negative horizon(ValueError). These are distinct fixture calls.

## 3.11-E5

For a fixed positive future amount, supported negative nominal−12% convertible monthly implies−1% monthly and a larger PV than zero rate for a positive horizon. The selected source call confirms that inequality.

## 3.11-E6

Early cents rounding changes later calculations:1.005 doubled raw is2.010, whereas cent-quantizing first under the active half-even context yields1.00 then2.00. The declared quantization rule and stage must accompany any posted result.

## 3.11-E7

Nested/staged agreement shares helpers and may reproduce their defect. Use independently derived expected values and financial convention checks; composition agreement alone is not validation of components.

## 3.11-E8

A future wrapper should record original nominal/effective quote, conversion frequency, effective periodic result, units, horizon, timeline, data/code revision and numerical policy/staging. Preserve original/effective inputs if policy changes them. This is a proposed metadata contract, not implemented persistence.

## 3.11-E9

A print-only helper returns None; adding it to a Decimal amount raises TypeError. Separate numeric returns from presentation. The probe captures printed output and verifies the failure.

## 3.12-E1

An ambient calculation reading a mutable market-rate global changes output for identical explicit principal arguments when the global changes. The fixture switches5% to10%; explicit argument identity is insufficient.

## 3.12-E2

Printing deterministic text is an observable effect and ordinarily returns None. A calculation-only function returns its numeric result; deterministic output alone does not imply purity.

## 3.12-E3

The exact fixed-policy function returns its known reference result with caller precision6,ROUND_DOWN and a preexisting Inexact flag; all caller settings/flags/traps remain unchanged.

## 3.12-E4

A NaN-rate validation failure raises ValueError while preserving the same full caller context snapshot. Failure-path context isolation is checked explicitly.

## 3.12-E5

An in-memory policy copy changes precision40 to6; the selected1234.56/.037/17 valuation changes. A real policy revision needs before/after results, error-bound justification, updated contracts/tests/source hashes and compatibility review. Canonical policy remains40.

## 3.12-E6

Precision is only one context field: rounding, Emin/Emax, clamp, capitals, traps and existing flags also matter. Copying only precision does not define or isolate a complete arithmetic policy.

## 3.12-E7

Reproduction from external data needs authorized dataset identity/hash/version and retrieval/as-of time, schema/unit/currency/timezone conventions, cleaning/missing-data policy, exact inputs, code/dependency/runtime revision, complete arithmetic context and rounding/reporting policy, expected values/tolerances and actual output. No external dataset is consumed by this batch.

## 3.12-E8

A local list parameter aliases the caller object and can append without rebinding any outer name. The executed probe mutates the caller-visible list; local names do not promise ownership isolation.

## 3.12-E9

A fixed random seed controls one source of randomness; fixed precision controls one numerical setting; repeatable output establishes neither appropriate financial assumptions nor correct units/data/formula. Reproducibility and model validity need distinct evidence.

## 3.13-E1

Known independent PV:144/(1.2*1.2)=100. The exact fixed-policy function agrees, rather than computing an expectation through the same helper.

## 3.13-E2

The validation-failure preservation check in3.12-E4 also supplies this exercise: invalid NaN at zero horizon raises ValueError and leaves caller settings/flags/traps intact.

## 3.13-E3

At r=−.99,n=2,amount1, growth=.01^2=.0001 and PV=10000. This small-horizon fixture is supported; behavior arbitrarily close to−1 still requires numerical-range/error analysis.

## 3.13-E4

A temporary source copy changes growth exponent n to n+1. The isolated published test_known_values returns exit1 and reports failure. Complete transcript retained; canonical source is unchanged. This is one mutation, not a complete mutation campaign.

## 3.13-E5

At rate0, multiplication and division by(1+0)^n both preserve the amount. Zero-rate cases cannot distinguish accumulation from discounting; include nonzero independent known values.

## 3.13-E6

Check type(result) is Decimal or isinstance according to the intended subclass contract; Decimal(100)==100 alone is insufficient. The actual fixed-policy return type is recorded as Decimal.

## 3.13-E7

All12 published methods run individually in fresh subprocesses and pass. This supports independence for those methods in this environment; it does not prove every future test order or concurrency behavior.

## 3.13-E8

Proposed rule: |actual−expected|<=max(abs_tol,rel_tol*|expected|), with abs_tol tied to meaningful amount scale near zero and rel_tol justified by error analysis over supported magnitudes. Test small/zero/large references and rounding boundaries; do not choose tolerances merely to pass. No universal finance tolerance or completed error-bound certification is asserted.

## 3.13-E9

A numerical suite cannot establish that a supplied discount rate is economically appropriate for the cash flow or that external data is accurate. Those require independent financial/data review beyond finite arithmetic fixtures.

