# Book 02 — Substantive Coverage: Chapter 8

**Date:** 2026-10-28  
**Inspected revision:** `110ea087e00668c1080f4a57d87a5a7f01fd8a02`  
**State:** Ten sections mapped; independent derivation and numerical accuracy review pending.

Inspected manuscripts, implementations, ten numbered checks and difference-denominator regression. Mapping reaches85/215 sections (Chapters1–8). No new execution occurred. [Pinned runtime](pinned-revision-runtime-validation.md) and [derivative boundary review](chapter-08-difference-denominator-review.md) retain their original scopes.

## 8.1 — Derivative definition
Source: [checks](../chapter-08/code/check_section_8_01.py).

E1 definition/nonzero h: zero steps rejected, proof/manual. E2 derivative4x+7: exact example absent. E3 x² derivation: centered and forward values at four points, symbolic limit manual. E4 x3 slope6: exact point3 not in grid(-3,0,2,10). E5 |x| kink: matching evidence in8.8/8.9, not here. E6 PV500/t2: grid uses cash0/100/1000 and times0/1/3/10, so exact input absent. E7 matching PV10bp approximation absent. E8 marginal12-.04q: value8 at100 checked. E9 tiny-step accuracy and E10 infinitesimal vs finite: manual; profit finite change7.98 contrasts derivative8.

Stable PV quotient checks use selected±1e-6 steps; they support a limiting calculation, not a proof or an optimal step-selection rule.

## 8.2 — Power/sum/constant rules
Source: [checks](../chapter-08/code/check_section_8_02.py).

E1 constant derivative0: matching constant and coefficient result. E2 7x^5: absent exact polynomial. E3 cubic4x³-6x+9: matching derivative grid. E4 quartic derivative199 at2: matching. E5 x^-2 and E6 sqrt(x): neither implemented by polynomial coefficient helper; domains/derivations manual. E7 revenue/marginal: matching values/grid. E8 marginal cost30 and E9 marginal profit30 at100: matching. E10 finite increment29.75: matching contrast, conceptual explanation manual.

Coefficient order/constant-zero behavior, revenue domain and malformed coefficients sampled. Finite derivative agreement does not establish a general power rule, particularly outside integer polynomial powers.

## 8.3 — Product/quotient rules
Source: [checks](../chapter-08/code/check_section_8_03.py).

E1 rule proof manual. E2 x²(3x+1) and E3 rational quotient: six-point comparisons to expanded derivatives; zero denominator rejected. E4 u'v' false rule: exact x*x counterexample not asserted. E5 R'=P+qP': matching revenue-specific expression and finite differences, derivation manual. E6 marginal revenue60 and E7/E8 average-cost derivative .05: matching. E9 coverage derivative: matching time grid. E10 discounted C(t) product: analytic/finite difference at positive times; t0 finite difference deliberately skipped because central negative-time perturbation is outside its domain.

Domain-aware one-sided checks at endpoints are not thereby established.

## 8.4 — Chain rule
Source: [checks](../chapter-08/code/check_section_8_04.py).

E1 definition proof/manual. E2 (2x+1)^5 absent. E3 (3x²+2)^4: matching explicit derivative, generic chain helper and finite difference. E4 exp(-3x²)/E5 log(1+x²): exact functions absent. E6/E7 constant/variable-rate PV: finite-difference grid of variable-rate function, derivation manual. E8 matching -8exp(-.128). E9 nominal rate as function: finite-difference model at selected years/shocks; domain cases sampled. E10 log price derivative: matching price/time samples.

Callable/type validation sampled. Finite-difference comparisons may share model-function/convention errors with analytic functions.

## 8.5 — Exponential/log derivatives
Source: [checks](../chapter-08/code/check_section_8_05.py).

E1 derivative definition proof manual. E2 7exp(3x): matching derivative/finite differences. E3 5exp(-.3x²) absent. E4 log(1+2x): matching values and domain boundary-.5. E5 log10 derivative absent. E6 accumulation time/rate sensitivities: matching r*A/t*A grid. E7 accumulation1000,.04,5 checked; matching time derivative is outside rate/time grid and not separately benchmarked. E8 PV sensitivity/1bp: derivative and exact shock change at1e-4 checked; error of linear approximation not explicitly bounded. E9 prices100→103 and E10 elasticity1.5: matching values.

Stable exponential quotient reference reuses exp/expm1; it is a translation identity, not an independent high-precision primitive oracle.

## 8.6 — Higher derivatives/curvature
Source: [checks](../chapter-08/code/check_section_8_06.py).

E1 first/second/third polynomial coefficient tuples: matching. E2 x³ concavity/E3 x^4 counterexample: manual, no matching sign-change assertion. E4 cost curvature.1 absent explicit test. E5 profit maximizer160: slope0/curvature-.5 and two comparison points; global feasible-domain proof manual. E6 PV second derivative: value grid plus centered-second check; proof manual. E7 matching204682.688... input in grid. E8 second-order shock improves selected.01 example, not universal error guarantee. E9 nonnegative-flow curvature: two positive cash flows have positive d2, negative-flow example negative; all-flows proof manual. E10 small h cancellation manual.

## 8.7 — Implicit derivatives
Source: [checks](../chapter-08/code/check_section_8_07.py).

E1 circle(3,4) slope-.75 and finite difference: matching. E2 vertical point(5,0) rejected; branch interpretation manual. E3 xy+y² derivative and E4 general implicit theorem: manual/no matching function. E5 ellipse(0,2): exposure helper tested different inputs; exact point absent. E6 break-even derivative formula sampled; E7 price50/cost20/fixed1200 included grid, explicit q40 follows original equality but not separate known-value tuple. E8 bond derivatives negative on positive-flow grids and reciprocal sensitivity product1. E9 one-period payment105 gives sensitivity-.0105 matching. E10 branch switching/near-singularity hazards not directly simulated.

## 8.8 — Numerical steps
Source: [checks](../chapter-08/code/check_section_8_08.py).

E1 forward/backward/center formulas: matching cubic12.61/11.41/12.01. E2 truncation expansion proof manual. E3 cubic centered12.01 matching. E4 second quadratic2 checked. E5 roundoff mechanism manual. E6 suggested first/second steps positive/representable with second>first, but actual epsilon exponents not independently asserted. E7 duration5/E8 convexity25 matching. E9 Richardson12 matching. E10 kink centered0 vs forward1/backward-1 matching, differentiability explanation manual.

## 8.9 — Derivative comparator project
Source: [checks](../chapter-08/code/check_section_8_09.py).

R1 callable first/optional second: correct analytic results and invalid callable sampled, no complete no-second output contract assertion. R2 finite positive steps: zero/unchanged/type/nonfinite rejection plus boundary suite. R3 four first estimates and R4 second: matching cubic known values. R5 signed/absolute errors: estimates/pass flags asserted, error field definitions not independently asserted. R6 configurable tolerances/step ladder: forward fails/center passes at selected tolerance; four model factories produce three-step reports, middle step passes. R7 invalid ratio perturbation and kink disagreement: visible evidence, no automatic proof of nonsmoothness or generic branch consistency. R8 four financial factories exercised. R9 standard-library design inspected. R10 evidence-status separation manual.

Eight review statements about error order, noise, stationary points and independent references are not proved by three returned reports. No ratio-of-errors convergence order or intentionally wrong analytic derivative test is asserted.

## 8.10 — All twenty-five assessment problems
Source: [checks](../chapter-08/code/check_section_8_10.py).

| IDs | Evidence / gaps |
|---|---|
| P1 definition/x²; P2 polynomial; P3 product; P4 quotient; P5/P6 chain/exponential; P7 log domain | Related earlier checks, not matching assessment expressions/proofs |
| P8 profit125 | Slope0 and profit higher than100/150; global curvature/uniqueness proof manual |
| P9 accumulation2500,.06 and second derivative | No matching assessment assertion |
| P10 PV first/second; P11 Taylor shock | Matching numeric fields and second-order error improvement |
| P12 price80→84 | Matching log return; simple.05 not separately asserted |
| P13 demand elasticity-1.5 | No matching negative-elasticity assertion |
| P14 break-even45/15/900 | Matching q30/derivative-1 |
| P15 payment110/price100 | Matching yield.1 and inverse sensitivity-.011; dP/dy value not explicit |
| P16 cubic concavity; P17 x^4 counterexample | No matching sign-change assertions |
| P18 cubic finite differences | Centered12.01 only here; forward/backward values in8.8 |
| P19 quadratic second difference2 | Matching |
| P20 Richardson proof | Related8.8 example, derivation manual |
| P21 kink | Related8.8/8.9 values; conceptual conclusion manual |
| P22 three epsilon heuristics | Not explicitly asserted; optimality qualifications manual |
| P23 three cash-flow derivatives | Related8.6 uses different two-flow schedule |
| P24 derivative units/bp conversion | Shock computations related; units interpretation manual |
| P25 verification protocol | Requires manual test-design assessment |

Assessment report only asserts a required-key subset, not every output's schema/value. The revised centered-second test h=2e-4 has a stated relative truncation rationale; it is stronger than simply widening tolerance to suppress a failure.

## Boundary regression and gaps

[Difference-denominator suite](../chapter-08/code/check_difference_denominators.py) verifies h² underflow/overflow rejection in three modules, comparator underflow, unchanged shifts, normal quadratic2 and centered-first denominator overflow in8.8. This does not establish consistent guards in every earlier first-difference helper.

| ID | Gap | Next evidence |
|---|---|---|
| COV-49 | Derivative accuracy/convergence order not established by selected passing steps | Independent reference/error-ratio ladders and noisy/wrong-reference cases |
| COV-50 | Comparator error fields/tolerance acceptance not fully asserted | Independent signed/absolute error and boundary gates |
| COV-51 | Implicit branch/domain and first-difference guards vary | Endpoint/near-singularity and representability review across helpers |

These extend COV-01–COV-48. No new implementation defect or independent sign-off is claimed. Next: Chapter9.

## Subsequent COV-49 accuracy follow-up

The [second-difference record](chapter-08-difference-order-followup.md) adds exact polynomial error ladders, a special vanishing-coefficient case and a representable-step cancellation example. Two faulty formula variants were detected. All 21 chapter sources compiled and 11 scripts passed; algorithm unchanged. Other helper/noise/reference/range and independent-review obligations remain open.

## Subsequent COV-50 comparator follow-up

The [comparator audit](chapter-08-comparator-audit-followup.md) adds exact error-field/tolerance-boundary and wrong-reference cases, retains tolerance metadata and rejects nonfinite computed estimates/errors to prevent false passes. All 21 chapter sources compiled and 11 scripts passed. Broader comparator/reference and independent-review obligations remain open.

## Subsequent COV-51 helper-guard follow-up

The [helper guard record](chapter-08-helper-guards-followup.md) rejects nonfinite returned estimates and avoids a Richardson intermediate overflow. Selected invalid controls are checked before callbacks, with denominator and half-step cases. All 21 chapter sources compiled and 11 scripts passed. Earlier copies, implicit domains/ranges and independent review remain open.
