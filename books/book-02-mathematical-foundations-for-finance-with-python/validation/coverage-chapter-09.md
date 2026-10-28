# Book 02 — Substantive Coverage: Chapter 9

**Date:** 2026-10-28  
**Inspected revision:** `44c136005d7c4ecbf3920f9d0b1128ec186dc7d4`  
**State:** Ten sections mapped; independent mathematical/financial review pending.

Inspected ten manuscripts, implementations, numbered scripts and scenario-revaluation regression. Mapping reaches95/215 sections (Chapters1–9). No new runtime execution occurred; [pinned full run](pinned-revision-runtime-validation.md) and [revaluation review](chapter-09-scenario-revaluation-review.md) retain their scopes.

## 9.1 Absolute/relative sensitivity
Source: [checks](../chapter-09/code/check_section_9_01.py).

E1 units/E2 exact vs local/E3 elasticity derivation manual. E4 zero-output normalization: portfolio zero-value and zero-cash inputs rejected, conceptual alternatives manual. E5 PV derivative/E6 duration:16 selected rate/time cases assert -tV and t. E7 matching10000/5/.04/1bp linear/exact changes. E8 demand elasticity-1.5 at four prices. E9 portfolio value2000/derivative20/elasticity.5 matching. E10 relative-percent vs percentage-point example not asserted.

## 9.2 Elasticity
Source: [checks](../chapter-09/code/check_section_9_02.py).

E1 derivation/E2 dimension cancellation manual. E3 demand exponent-2 not matching tested-1.5. E4 linear-demand elasticities-.25/-1/-4 matching. E5 revenue relation supported by selected derivative formulas, proof manual. E6 price25 slopezero with flanking signs, global max proof manual. E7 income.7/E8 rate elasticity-.2/E9 midpoint arc-11/15 and reversal invariance matching. E10 numerical hazards: invalid input/zero step sampled, near-zero baseline stability not established.

## 9.3 First-order Taylor
Source: [checks](../chapter-09/code/check_section_9_03.py).

E1 polynomial/E2 differentiability definition manual. E3/E4 square at3/h.2 matching10.2 and errorh². E5 Lagrange theorem manual. E6 discount formula/E7 matching10bp value change asserted. E8 portfolio duration derivation not in this script, related9.6. E9 revenue at105 matching linear3100/exact change97.5/error-2.5. E10 relative-error denominator: zero exact change returns None.

Step ladder has actual error-ratio check3.9–4.1 for halving h. This is useful sampled quadratic-error evidence, not a universal order proof.

## 9.4 Second-order Taylor
Source: [checks](../chapter-09/code/check_section_9_04.py).

E1 derivation manual. E2/E3 cubic linear1.2/quadratic1.26 changes and remainder.001 matching. E4 smoothness theorem manual. E5 derivatives/E6 duration5/convexity25 sampled across four rates. E7 matching h.001 correction is exercised through shock grid, not separately reported benchmark. E8 two-flow weighted duration/convexity and exact shock matching. E9 large-shock limits/E10 callable cash-flow assumption manual. Selected shocks improve quadratic vs linear error; no universal improvement established.

## 9.5 Remainder bounds
Source: [checks](../chapter-09/code/check_section_9_05.py).

E1 signed remainder/E2/E3 theorem assumptions manual. E4 cubic remainderh³ and quadratic absolute bound equality at five h values. E5 polynomial linear bound.063 not explicitly asserted. E6 exponential second/third derivative: matching first/second and independently expressed bound constants, derivation manual. E7 interval minimum-rate maximum supported by explicit worst-value formula. E8 matching10000/5/.04/.001 bound. E9 five portfolio shock bound checks, general sum proof manual. E10 economic-model distinction manual.

The bound_holds helper permits additional1e-9*max(1,baseline) rounding allowance. Tiny bounds can be dominated by that allowance, so passing does not show every bound is sharp or nonvacuous.

## 9.6 Discounted-value sensitivity
Source: [checks](../chapter-09/code/check_section_9_06.py).

E1/E2 derivatives and E4 duration/convexity sampled. E3 sign proof manual; positive-flow examples. E5 five-yearD5/K25 matching. E6 25bp conversion/E7 8000*4*.0025=-80 not matching inputs here. E8 cash-flow derivative exp(-5r) asserted. E9 two spot derivatives plus independent spot changes matching. E10 spot vs market key-rate distinction manual. E11 K>=D² asserted for one two-flow example; variance proof manual. E12 exact-revaluation rationale supported by shock comparisons, interpretation manual.

Weights sum1 checked. Cash-flow positivity assumptions matter: signed-net-value duration is not certified by these helpers.

## 9.7 Kinks/directional sensitivity
Source: [checks](../chapter-09/code/check_section_9_07.py).

E1 definition manual. E2/E3 call slopes/payoffs and E4 put slopes matching strike100. E5 centered.5 matching left0/right1. E6 cap slope/E7 floor-band slopes matching boundaries and selected values. E8 discounted slopes0/exp(-.08) and up/down exact scenarios matching. E9 call-put identity at98/100/102 matching; general proof manual. E10 pre-expiry delta distinction/E11 valid perturbation protocol manual. E12 offset kinks supported by payoff identity, not a general smoothness classifier.

## 9.8 Sensitivity reports
Source: [checks](../chapter-09/code/check_section_9_08.py).

E1 metadata requirements manual/partial schema. E2 +25/-50bp matching. E3 linear/quadratic and E4 stable exact-change expressions checked for five shocks. E5 zero row matching. E6 value8000/D4/-80 and E7 convexity18 correction use different report inputs, exact exercise absent. E8 signed error definitions indirectly used; no independent every-field schema. E9 relative denominator hazards manual. E10 two-spot bump matching. E11 market key-rate distinction/E12 contractual cap escalation manual.

Currency tolerance .25 pass flags are compared with absolute quadratic error. Large-shock tiny-positive exact-value stability fixed in9.9 is not automatically evidence for9.8's baseline+change valuation route.

## 9.9 Valuation report project
Source: [checks](../chapter-09/code/check_section_9_09.py), [revaluation regression](../chapter-09/code/check_scenario_revaluation.py).

R1 selected positive-flow/time/type/domain checks; R2 convention metadata inspected, not every field asserted; R3 bp conversion exercised; R4 baseline derivatives independently enumerated; R5 exact expm1 changes checked; R6 linear/quadratic estimates checked but error-field definitions only partial; R7/R8 bound flags checked without independent every-scenario numeric bound reconstruction here; R9 missing up/down/zero grids rejected; R10 JSON serialization succeeds, byte-for-byte deterministic repeated output not asserted; R11 numerical examples and errors present; R12 runtime/review flags explicitly False.

Questions Q1/Q2 derivatives manual plus numeric examples; Q3 -75bp exact input absent here; Q4 single time3 D3/K9 not matching time5 test; Q5 variance proof manual; Q6 +25bp absent project grid but related assessment; Q7 -50bp matching; Q8 interval supremum derivation not independently numeric-asserted here; Q9 interval hypothesis/Q10 zero rationale/Q11 model accuracy/Q12 certification evidence manual.

Five extensions (spot engine, kink, CSV, currency tolerance, evidence harness) are optional designs, not implemented acceptance failures. Boundary regression protects tiny-positive directly shocked value, zero shock and multi-flow references; exact_change can still suffer different cancellation/representation limits.

## 9.10 All twenty-five assessment items
Source: [checks](../chapter-09/code/check_section_9_10.py).

| IDs | Evidence / gap |
|---|---|
| E1 polynomial elasticity1.92/E2 exponential elasticity1/E3 zero output | No matching numerical examples; conceptual review |
| E4 sqrt first-order10.05/E5 second10.049875 | Not asserted |
| E6 cubic negative remainder/E7 linear.063/E8 inverse error budget | Related9.5 cubic sample, no matching full assessment error-budget assertions |
| E9–E13 single-flow value/sensitivities/shock/bounds | Matching in project/earlier section tests, not assessment's four-flow baseline |
| E14 two-flow portfolio/E15 variance proof/E16 payment derivative | Related9.6 samples; proof/manual |
| E17 call kink/E18 centered trap | Matching nondifferentiable flag and centered.5; left/right numeric fields not asserted here |
| E19 cap/floor | Matching9.7 evidence, absent here |
| E20 kink offset | Call-put identity at three spots asserted |
| E21 -75bp | Matching |
| E22 spot bumps/E23 error denominator/E24 certification | Related spot tests; explanations manual; assessment flags False |
| P25 applied project | Four-flow baseline/D/K, seven exact/linear/quadratic changes, signs and bound flags asserted; independent numeric M2/M3 fields and deterministic export not tested |

Project6 tasks: a baseline derivatives supported through reference calculation; b seven shocks; c three changes; d flags rather than independent interval-bound values; e universal-improvement explanation manual; f no repeated-output/export assertion here.

## Additional gap register

| ID | Gap | Next evidence |
|---|---|---|
| COV-52 | Bound flags can pass without independent bound-field or nonvacuity checks | Independent interval extrema and rounding-allowance analysis |
| COV-53 | Report determinism/metadata and exact-value stability vary across modules | Contract/repeated-output checks and cross-module large-shock cases |
| COV-54 | Relative elasticities/near-zero denominators only partly covered | Scale-aware domains and independent near-zero references |

These extend COV-01–COV-51. No new defect or independent sign-off is claimed. Next: Chapter10.
