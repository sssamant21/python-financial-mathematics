# Book 02 — Substantive Coverage: Sections 2.6–2.10

**Date:** 2026-10-28  
**Inspected revision:** `a6357fa910cf5d76e55956d78124febf87c10091`  
**State:** Chapter 2 mapped; independent review and coverage remediation pending.

Read the five manuscripts, implementations and numbered checks. Mapped 18 section exercises, six project extensions, twenty assessment exercises/applications and seven mini-case tasks. The book now has 35/215 numbered sections mapped (Chapters 1, 2 and 4). No new execution or correctness certification is claimed; [pinned runtime evidence](pinned-revision-runtime-validation.md) is separate.

## 2.6 — Inequalities and Absolute Values

Source: [check_section_2_06.py](../chapter-02/code/check_section_2_06.py).

| Exercise | Evidence / remaining review |
|---|---|
| P1 negative coefficient and nonnegative intersection | Matching final intersection; original strict -2 boundary/neighbor checks are on other grid inputs; derivation manual |
| P2 absolute band and strict cap | Matching [1,4) intersection asserted |
| P3 outside union/zero bands | General inside-band grid and zero singleton/empty cases; specific outside |x-5|>2 union not asserted |
| P4 positive quadratic profit with cap | Original polynomial/price/cap vs (20,60] checked at 127 probes |
| P5 rational sign inequality | Non-strict union checked at 26 probes; strict zero exclusion not separately asserted |
| P6 band/cap/conflicting floors | Matching [.45,.7], empty and singleton outcomes asserted |

54 linear solutions/486 memberships, 72 absolute-band solutions/648 memberships, 100 interval pairs/900 memberships and endpoint-neighbor checks support exact boundaries. Eleven invalid calls cover selected types. Direct original-expression checks are useful evidence; finite probes do not prove sign-chart completeness. Arbitrary unions and general polynomial/rational inequalities are not implemented by the interval helpers.

## 2.7 — Simultaneous Equations

Source: [check_section_2_07.py](../chapter-02/code/check_section_2_07.py).

| Exercise | Evidence / remaining review |
|---|---|
| E1 substitution | Matching (7,11) asserted; steps manual |
| E2 exposure/budget | Matching (25/2,9); units/whole-unit feasibility manual |
| E3 singular systems | All four matching classifications; line parameter samples checked |
| E4 allocation targets100/150 | Matching (1000,1000),(-250,2250); exact [60,140] target interval not directly asserted for these rates |
| E5 equal rates with cap200 | Target21 infeasible asserted; exact target20 line and added cap200 not directly exercised |
| E6 zero row/invariance/residual | Matching residual(2,0); general row-swap/scale grid; specific free-x line/scaled residual-6 not directly asserted |

729 small systems are compared with separately implemented row reduction instead of determinant formulas, with swap/scale classifications and 480 line-member samples. 1,488 planted unique points and 240 allocation boundary cases supply additional evidence. Eleven rejections sample interfaces. Parametric-line completeness and financial-unit interpretation still require derivation review.

## 2.8 — Scaling and Algebraic Validation

Source: [check_section_2_08.py](../chapter-02/code/check_section_2_08.py).

| Exercise | Evidence / remaining review |
|---|---|
| E1 scale 5x-10 by -7 | Other row scaled by -7; matching x=2 example absent |
| E2 multiply by x-2 introduces root | No matching transformed equation assertion |
| E3 revenue price8/fee40/target360 | Other cash_flow_balance case (12,100,50,1150); exact exercise absent |
| E4 raw/normalized residual at origin | Matching normalized1, scale invariance and raw scaling; scaled -13/1000 follows from assertions |
| E5 zero coefficient with integer domain | solve_one all/none samples; full nonnegative-integer interpretation manual |
| E6 tiny residual with variable error1 | No matching tiny-coefficient counterexample |

Three nonzero factors and three points test raw residual scaling and normalized invariance. Zero denominator normalizer returns0 for the zero equation. Zero scale, float and bool rejection are checked. These exact-arithmetic checks are not evidence of conditioning or forward-error guarantees for general float solvers.

## 2.9 — Break-Even and Formula Rearrangement Analyzer

Source: [check_section_2_09.py](../chapter-02/code/check_section_2_09.py).

The eight core contract areas have evidence as follows: exact rational type rejection; nonnegative model input checks sampled for price; quantity equality at120; fractional145.5 equality vs whole-unit rejection; minimum146 with previous145 infeasible; price25 inverse; zero/negative margin and zero-quantity classifications; original-profit substitution on unique results across a nine-model grid. Full negative-input-field combinations, Boolean whole_units policy and output-schema consistency are not exhaustively asserted.

| Extended exercise | Evidence / remaining review |
|---|---|
| X1 price40/cost28/fixed960 break-even80 | No matching input assertion |
| X2 minimum91 for profit125 | No matching input assertion; analogous146 threshold has adjacent check |
| X3 rearrange fixed cost | No dedicated inverse-fixed-cost function/assertion |
| X4 zero margin/fixed50 targets-50/0 | Analogous zero-margin cases at fixed0/100; matching pair absent |
| X5 equality vs rounding | Matching145.5/no-integer/146 distinction asserted |
| X6 currency-scaling and substitution properties | Unique-result substitution grid present; full currency-scaling property absent |

The project has no CLI/parser acceptance contract; its main demonstration is distinct from a subprocess test. Optional extensions are not counted as implemented mandatory features. Financial scope and real-versus-whole-unit interpretation require manual review.

## 2.10 — Core assessment, applications and mini-case

Source: [check_section_2_10.py](../chapter-02/code/check_section_2_10.py), importing Section 2.9 helpers.

| Item | Assertion coverage |
|---|---|
| E01 equivalent forms | Matching substitution at -2; not general equivalence proof |
| E02 linear equation | Matching original substitution at5 |
| E03 rational equation | Candidate7/2 original ratio asserted; excluded2 reasoning manual |
| E04 square equation | Both real candidates verified; nonnegative filter not explicitly asserted |
| E05 fractional exponent | 9^3=27^2 asserted; original fractional-root/domain verification manual |
| E06 quadratic | Both3,4 satisfy original; factoring/completeness manual |
| E07 no real roots | Positivity at -2,0,2 only; discriminant/general proof not asserted |
| E08 inequality | Boundary4 and point5 checked; entire x<=4 solution/manual sign reasoning |
| E09 absolute tolerance | Both95/105 boundaries checked; interior/outside classification absent |
| E10 system | Matching20/30 both equations asserted |
| E11 singular system | No matching line/contradictory-system assertion in this script |
| E12 allocation | Matching-50/150 equations asserted; nonnegative rejection not explicit |
| A01 revenue/units | Matching1150 arithmetic; units manual |
| A02 break-even | Matching120 through project helper |
| A03 integer threshold | 146, previous145 inequality and no exact integer equality asserted |
| A04 inverse price | Matching25 asserted; original-price substitution not separate here |
| A05 zero margin | Matching target0 none at fixed100; target-100 all not asserted here |
| A06 residual scale | Exact-13 and-13/1000 asserted; interpretation manual |
| A07 extraneous root | No matching x=4 multiplied-by-(x-2) assertion |
| A08 inverse revenue price | No matching pq-F=T helper/zero-q classification; profit-price helper is related but distinct |

Mini-case tasks1–7: the model supplies contribution6 (not directly asserted); matching break-even150, minimum171, adjacent profits120/126, inverse price18 and zero-margin none are asserted. The request for two business assumptions requires manual assessment. Tests are computational examples, not grading the written solutions.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-33 | Assessment “no real roots” represented by only three positivity probes | Explicit discriminant/reference argument and manual proof review |
| COV-34 | General inequality sets/unions broader than interval/probe support | Full sign/domain derivation and exact strict-endpoint examples |
| COV-35 | Project extension/scaling and several assessment cases lack matching assertions | Independent targeted benchmarks or documented manual evidence |

These extend COV-01–COV-32; earlier conceptual/input-mismatch categories also apply. They are coverage gaps, not demonstrated new defects. No manuscript or code changed during this mapping slice.

Next: Chapter 3 mapping, Sections 3.1–3.5. Independent review, final release validation and canonical approval remain pending.
