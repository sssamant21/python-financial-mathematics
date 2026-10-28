# Book 02 — Substantive Coverage: Sections 4.9–4.10

**Date:** 2026-10-28  
**Inspected revision:** `839bb2d6980ac6f6f2cf9925bf0f8d96db606a05`  
**State:** Chapter 4 mapping complete, substantive gaps and independent review pending.

Inspected both manuscripts, both implementations, their numbered checks and the growth-recovery boundary checks. This completes mapping for 10/215 book sections, not validation or certification of those sections. Earlier slices: [4.1–4.6](coverage-sections-04-01-06.md), [4.7–4.8](coverage-sections-04-07-08.md).

Existing [pinned runtime evidence](pinned-revision-runtime-validation.md) includes these scripts. No new runtime test execution is claimed in this mapping pass.

## 4.9 requirements and worked scenario

Assertion sources: [project checks](../chapter-04/code/check_section_4_09.py) and [recovery checks](../chapter-04/code/check_growth_recovery_boundaries.py).

| Requirement | Assertions present | Remaining coverage |
|---|---|---|
| R1 principal/nominal/frequency/period inputs | Worked periodic_result; valid periodic CLI invocation; invalid principal, frequency and negative periods | Fractional/bool counts, parser missing/bad argument cases not asserted here |
| R2 periodic FV/PV/EAR/equivalent rate | 10000 at .06, monthly, 36 periods; FV direct-power reference; recovered PV and EAR; equivalent continuous FV | Complete output schema/types/units not asserted |
| R3 continuous rate and real horizon | Continuous scenario at three years; valid CLI at two years; negative horizon rejection | Noninteger positive horizon not directly exercised |
| R4 continuous FV/PV/EAR | FV and recovered PV asserted | Continuous report EAR field not directly asserted |
| R5 EAR-to-nominal conversion | Five frequencies by five EARs through round trips | Same implementation family; independent oracle and tiny-signal tolerances needed |
| R6 rate sensitivity | Three-year first-order .003 and exact expm1(.003) fields | Negative perturbations and approximation error bound absent |
| R7 invalid domains/range | Selected ValueError cases, bool/NaN validator rejection, two underflow exceptions | Infinity and field-specific nonfinite coverage, CLI error exit/stderr not asserted |
| R8 reproducible positive/zero/negative cases | Numeric grid, periodic zero rate, continuous negative rate, three CLI success paths | main(argv) is called in-process; installed/subprocess command behavior not established |

The worked monthly scenario matches the numerical assertions. The continuous CLI example in the manuscript uses principal 10000, rate .06, years 3; the CLI assertion instead uses 1000, .05, years 2. This is related behavior, not exact example execution.

Recovered PV is a division of the generated FV by the same factor. It tests mutual consistency but is not an independently supplied future-cash-flow valuation benchmark.

Recovery checks assert continuous/periodic factor-underflow rejection, zero horizon, a 25% one-period known value and zero principal at an ordinary factor. Partial monetary underflow, full CLI presentation and extreme conversion ranges remain open.

### Review questions and optional extensions

| Item | Evidence disposition |
|---|---|
| Q1 positive factor | Invalid factor rejection supports the domain; logarithm/model explanation needs manual review |
| Q2 nominal vs EAR | Conversion/known-value assertions; interpretation manual |
| Q3 completed periods | Integer validators exist; parser success uses integers; posting convention manual |
| Q4 meaning of round trip | Conceptual answer/manual review; mutual consistency is not model suitability |
| Q5 precision vs omissions | Manual model-assumption review |
| Q6 30-year 10bp first-order 3% | Project assertion uses three years/.003; thirty-year assertion elsewhere is cross-section evidence, not this script |

Extensions 1–6 (frequency comparison command, implied-rate command, whole-period threshold command, perturbation table, day-count convention and Decimal rounding) are optional student work, not claimed implemented requirements. They are not counted as failed mandatory acceptance criteria.

## 4.10 assessment: all 24 problems

Assertion source: [assessment checks](../chapter-04/code/check_section_4_10.py), inspecting answers() outputs as well as direct function calls.

| Problem | Executable evidence / remaining review |
|---|---|
| P1 continuous-growth derivation/units | No proof assertion; separation argument and units require manual review |
| P2 log domains/rewrite | No negative-x rewrite example in this script; manual domain review |
| P3 periodic derivation/postings | Sample FV values and invalid counts; general derivation/convention manual |
| P4 continuous limit | No convergence sequence or proof assertion; manual review |
| P5 EAR/equivalent continuous derivation | EAR check and equivalent one-year grid; derivation manual |
| P6 inverse growth/domains | Implied rate and zero-time rejection; full identifiability cases not covered here |
| P7 time vs portfolio aggregation | Cumulative return checked; portfolio contrast absent here, present at different inputs in Section 4.6 |
| P8 stable primitives/conditioning | Formula uses inspected primitives; no conceptual proof or direct fsum advantage check |
| P9 quarterly FV/EAR | Both answers() values checked against direct powers at matching inputs |
| P10 PV 1210 at .10 over two years | Answer checked against 1000; implementation and answer expression closely related |
| P11 .07 EAR conversion | Rate checked against log1p(.07); one-year accumulation grid includes .07 |
| P12 doubling at .06 | Real period count checked; ceil gives 12; independent adjacent inequality/minimality check absent |
| P13 1000-to-1250 in four years | Rate checked against log(1.25)/4 |
| P14 +15%,-10%,+5% | Simple answer checked against product; log checked separately against log(product) |
| P15 30% loss recovery | Answer equals 1/.7-1; cumulative recovery close to zero; answer equality reuses same expression |
| P16 .4/.6 portfolio returns | No matching assertion or answers() field; Section 4.6 uses .5/.5 and different returns |
| P17 20-year 15bp sensitivity | Exact expm1(.03) answer checked; first-order .03/error comparison absent |
| P18 tiny 1e-16 return | No tiny-rate assertion in assessment; Section 4.7 has the matching tiny input |
| P19 deposit-only balance change | Manual interpretation; no external-flow calculation asserted |
| P20 unreachable target at -.02 | No matching inversion/reachability assertion in assessment |
| P21 equal endpoints/zero-rate time ambiguity | Zero-rate forward invariants checked; solution-set explanation untested |
| P22 fractional monthly postings | Counts validated in implementation; no 5.5 rejection assertion here |
| P23 precision vs model omissions | Manual assumptions/source review |
| P24 independent verification plan | Script provides examples, not an assertion that a student's plan is independent or adequate |

No direct imports from earlier section modules are used by the two implementations; they contain parallel formula implementations. The assessment script is not a chapter aggregate that invokes all prior checks. Cross-section evidence can support a concept but must not be counted as the exact assessment input, a proof, or independent review.

## Additional gap register

| ID | Gap | Proposed evidence |
|---|---|---|
| COV-14 | CLI success only, in-process | Subprocess success/error paths with exit status, stderr and JSON output contract |
| COV-15 | Report schema and some output fields unasserted | Validate units/conventions, expected keys/types and continuous EAR independently |
| COV-16 | Noninteger continuous horizon and exact CLI examples not exercised | Matching worked-example and fractional-horizon cases |
| COV-17 | Integrated assessment omits several numbered inputs/concepts | Targeted numerical references plus manual conceptual-answer review |
| COV-18 | Parallel implementations can drift | Document contracts and independent cross-implementation/reference checks |

These extend COV-01–COV-13. They describe evidence gaps, not demonstrated implementation defects. No low-value mirror tests were added merely to raise a count.

Manuscript runtime notes now refer to the existing pinned evidence. The Chapter 4 checklist item “all chapter labs executed” remains unchecked: successful reference scripts do not prove that every printed lab command or interactive extension was executed. Independent review and canonical approval remain pending.

Next: substantively map Chapter 1 in sequence, keeping the Chapter 4 gaps open for a separate remediation/review pass.
