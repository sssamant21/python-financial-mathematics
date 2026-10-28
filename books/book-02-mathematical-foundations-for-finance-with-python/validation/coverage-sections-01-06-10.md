# Book 02 — Substantive Coverage: Sections 1.6–1.10

**Date:** 2026-10-28  
**Inspected revision:** `0dac315c88b081bae421807b5102422e08036b4e`  
**State:** Five sections and 30 practice problems mapped; independent content review pending.

Inspected manuscripts, implementations and numbered check scripts. Mapping now covers 20/215 numbered sections: all Chapter 4 and Sections 1.1–1.10. Counts measure mapping, not validated chapters or closed findings. Assertions execute at module level in these scripts. Existing runtime evidence remains the [pinned full run](pinned-revision-runtime-validation.md); no new runtime run is claimed here.

## Assertion sources

- [check_section_1_06.py](../chapter-01/code/check_section_1_06.py): `37abb59872f660390c8f2776e415a26898a3bcc7`.
- [check_section_1_07.py](../chapter-01/code/check_section_1_07.py): `5c6104a69df590ef0658069f44a5f3a630267c87`.
- [check_section_1_08.py](../chapter-01/code/check_section_1_08.py): `935b74570e75cb3c942685fe11a842b81b491f89`.
- [check_section_1_09.py](../chapter-01/code/check_section_1_09.py): `e95af9a4b443efc6d55e75517a94734b360b55a1`.
- [check_section_1_10.py](../chapter-01/code/check_section_1_10.py): `35c73df80da18b56e765d52872dfa0b760cf29c4`.

## 1.6 — Expressions, Equations, and Identities

| Practice problem | Existing assertion evidence | Remaining review |
|---|---|---|
| P1 classify expression/equation/identity at principal 200 | Analogous principal-100 rate equation and exact expansion samples | Exact principal-200 input and classification language not asserted |
| P2 unique/all/none linear equations | All three matching coefficient cases asserted | General real-solution-set reasoning manual |
| P3 division loses zero root | Sampled original equation identifies [0,2] | Completeness proof and division restriction manual |
| P4 radical extraneous candidate | Squared candidates [0,3]; original rejects zero and accepts three | Domain x>=1 and general equivalence reasoning manual |
| P5 cleared denominator candidate | Linear candidate one, zero denominator, and original_quotient exclusion checks | Original rational equation has no dedicated solver; reasoning manual |
| P6 residual scaling | Exact -1/100 and -1/10000 asserted | Units, scale and tolerance interpretation manual |

625 small coefficient cases distinguish unique/all/none and substitute into the original equation. Fifty-five rational expansion samples and five quotient samples support identities without proving them. Fourteen rejection cases preserve input contracts and the excluded point. A tiny exact nonzero coefficient yields 10^30 rather than being thresholded to zero.

Lab investigations have matching expression/rate examples, domain removal of rate -1, quotient exclusions, radical candidates and tiny-coefficient checks. Some lab coefficient examples differ from the named checks, although the grid contains their small-coefficient analogues. Finite candidate enumeration is not a general symbolic solver or proof of all real cases.

Cross-section note: this supplies related original-domain evidence for the Section 1.4 excluded-point discussion, but not the exact pole at .03 or its full sign-domain derivation.

## 1.7 — Inequalities and Financial Constraints

| Practice problem | Existing assertion evidence | Remaining review |
|---|---|---|
| P1 solve -3x+6<=0 | Sign-sensitive grid includes negative coefficients but not constant 6 | Exact permitted/excluded example not directly asserted |
| P2 fee 4+.02x, budget 14, cap 400 | Matching maximum 400 and slacks 2/0 | Full feasible-interval derivation manual |
| P3 zero proportional fee, cap 100, budget 5, fixed 4/5/6 | Below/equal/above cases use other policy values | Matching exercise inputs not asserted |
| P4 .95 target, .1 band, long-only | .95 band grid includes .85,1,1.05 and interval-reference comparison | Continuous interval argument manual |
| P5 incompatible band/cap | Exact max-lower > min-upper conflict assertion | Why clipping fails and appropriate policy response manual |
| P6 strict bound below 1000 | Exact boundary exclusion asserted | No-largest-real-value/supremum proof manual |

180 policy cases and 1,080 proposals compare direct inequalities, slacks and the returned maximum; 150 band cases compare interval intersections; 225 sign cases handle positive/negative/zero coefficients. Maximum+0.01 infeasibility is a finite local check, not by itself a proof of global maximality. The algebraic derivation remains required.

Zero maximum is distinguished from None; fixed-fee zero-transaction treatment belongs to this model and must not be silently substituted for the Section 1.11 no-transfer fee exemption. The two-weight lab extension is not implemented by a one-weight membership helper.

## 1.8 — Logic, Assumptions, and Implications

| Practice problem | Existing assertion evidence | Remaining review |
|---|---|---|
| P1 acceptance conjunction/negation | Exhaustive Boolean rows include both De Morgan identities | Financial predicate translation manual |
| P2 positive interest converse counterexample | Exact (-100)*(-.1)>0; sign grid with principal-positive equivalence | Quantifier/domain argument manual |
| P3 “accepted only if checks pass” | Implication truth table asserted | Necessary vs sufficient language not machine-established |
| P4 negate universal positive payments | [1,0,3] all/any checks | Existential interpretation and remaining-payment signs manual |
| P5 empty observations | all([]), empty/missing/extra/duplicate schema rejection; Boolean-type checks | Schema adequacy relative to real required observations manual |
| P6 principal 500, rate -1, periods True | Analogous domain grid includes rate -1 and True periods with principal 1000 | Exact principal-500 record not asserted; failure explanation manual |

Four Boolean rows exhaust the declared two-valued domain. Eight three-check combinations exhaust that schema's results. The 432 input cases and 25 rational sign cases are finite samples, not exhaustive real inputs. Fifteen rejected calls cover schema/interface errors.

Truth tables are exhaustive for their stated finite Boolean inputs; no violation among financial samples proves a universal real-valued proposition. Unsupported observations yield failed predicates rather than a claim that the unknown underlying quantity is negative. The lab validates inputs; it does not compute growth or approve a model.

## 1.9 — Definitions, Propositions, and Counterexamples

| Practice problem | Existing assertion evidence | Remaining review |
|---|---|---|
| P1 effective-fee definition/domain | Zero/negative amount rejected; positive exact fee/effective pairs | Definition and zero-extension reasoning manual |
| P2 fixed 3, rate .02, amounts 100/300 | Matching 300 case is asserted (9,3%); no matching 100 case | Five-unit fee, 5% and two-percentage-point comparison not directly asserted |
| P3 strict-decrease counterexample at fixed zero | Returned witnesses validated for fixed-zero search grid | Exact 100/200 witness differs from grid's first .5/1 witness; assumptions/manual explanation |
| P4 total-fee nondecrease and strictness | Difference identity and sign conditions asserted on 54 pairs | General proof manual |
| P5 candidate list 1,2,3 | Search grid uses four amounts and six pairs | Exact three-pair list/count and finite-vs-universal explanation not asserted |
| P6 invalid negative-fixed-fee witness and repaired claim | Negative fixed fee rejected; nonstrict/strict outcomes tested | Valid repair argument and quantifiers manual |

Eighteen searches assert pair count, presence/absence of a witness and returned witness validity. Search count includes every pair rather than terminating after its first witness. One sentence saying the search returns its first witness does not imply it stops enumeration early.

The direct fee-difference formulas give an alternative reference for selected exact pairs; they still require proof over the general domain. Returned scope text is present in implementation but is not asserted by the numbered script.

## 1.10 — Units, Dimensions, and Financial Conventions

| Practice problem | Existing assertion evidence | Remaining review |
|---|---|---|
| P1 75 shares at USD18 | No matching position-value assertion | 1350 and unit cancellation/manual invalid-addition review |
| P2 3% to 3.5% change | Decimal/percent/bp normalization grid | .5 percentage point, 50bp and relative 1/6 not directly asserted |
| P3 million/thousand scaling | No scale-normalization assertion | Exact USD1,550,000 and 1.55 million/manual units |
| P4 12000 at 5% for 90 days | Accrual grid uses other principals/rates/day intervals | Matching 150 and 10800/73 exercise values absent |
| P5 2024 leap interval ACT/365F | Exact matching two-day fraction 2/365 asserted | Fixed-denominator interpretation manual |
| P6 decimal 5 means 500%, not quoted 5% | Decimal 5 and percent 5 normalization assertions | Caller intent cannot be established by dimensional analysis |

Fifteen representation cases, eighteen calendar cases, 162 accrual cases and two additivity cases cover fixed-denominator conventions. Known calendar lengths include 1900/2000 century leap rules, zero days, year transitions and leap/nonleap years. The worked 10000-at-6%-for-30-days example is checked under both conventions.

Sixteen rejection cases exclude timestamps, unsupported dates/conventions and invalid currency labels. Currency syntax is not registry validation. Constant principal/rate and fixed denominators are required for the additivity example; tests do not establish which day-count convention a real contract uses.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-23 | Finite equation/sign grids do not prove full solution sets or extremal claims | Manual derivations, exclusions and supremum/maximality arguments |
| COV-24 | Counterexample search count/scope and exact exercise list partly unmatched | Explicit finite-list/count/scope assertions where useful, plus quantifier review |
| COV-25 | Units/scale and some accrual exercise inputs not asserted | Independent exact benchmarks and manual convention/source review |

These extend COV-01–COV-22; existing conceptual/input-mismatch categories also apply. No implementation defect is established, and no algorithm, manuscript answer or numerical test was changed in this mapping pass.

Next: Sections 1.11–1.15, including project batch evidence and chapter-wide exercises. Independent mathematical/editorial review, supported-platform checks and canonical approval remain pending.
