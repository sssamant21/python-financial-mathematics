# Book 02 — Substantive Coverage: Chapter 3

**Date:** 2026-10-28  
**Inspected revision:** `427db8f7abc06c79b3b3b3227300640ce450423b`  
**State:** Ten sections and 76 exercises/project questions/assessment problems mapped; independent review pending.

Inspected all ten manuscripts, nine implementations, ten numbered checks and check_exact_domain_boundaries.py. No new execution occurred; [pinned runtime](pinned-revision-runtime-validation.md) and [Chapter 3 source review](chapter-03-exact-domain-review.md) retain their scopes. Mapping reaches 45/215 sections (Chapters 1–4), not certification.

## 3.1 Inputs, outputs, domain and range

Source: [check_section_3_01.py](../chapter-03/code/check_section_3_01.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 square on [-2,3] | No matching range enumeration; continuous extrema proof manual |
| E2 5q-20 finite range | Other profit parameters/capacity enumerated; exact exercise range/-7 unattainability absent |
| E3 100/(1+r) range/output50 | Related signed PV and invalid rates; rate1/output50 absent |
| E4 reciprocal shifted pole | No matching helper/assertion; domain/range proof manual |
| E5 decreasing discrete range | Decreasing classification uses fixed60 rather than10; exact maximum absent |
| E6 transaction-count domain | Whole-quantity/fractional rejection; interpretation manual |

Worked profit84, zero-quantity loss-60, five finite profits and increasing/constant/decreasing classifications are asserted. Boundary suite separately tests a rational rate 10^-100 above -1. Classification metadata is not a proof of an unbounded range.

## 3.2 Graphs and financial interpretation

Source: [check_section_3_02.py](../chapter-03/code/check_section_3_02.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 price30/cost18/fixed90 | Checks use25/15/40; exact intercept/slope/root7.5 absent |
| E2 minimum integer8 | No matching whole-threshold assertion |
| E3 rows0,7,8 for same model | Other-model rows0,4,6 and row invariants; exact rows absent |
| E4 discrete graph excludes7.5 | Fractional capacity rejection is different from checking graph-domain membership |
| E5 axis rescaling | No rendered graph/axis test; manual interpretation |
| E6 parallel revenue/cost | Related equal-margin none case at10/10/fixed40; exact20/20/50 absent |

Baseline coordinates, all row differences, degenerate break-even cases and vertical-secant rejection are asserted. A table-row substring does not test graphical layout, scale, markers or interpolation semantics.

## 3.3 Composition

Source: [check_section_3_03.py](../chapter-03/code/check_section_3_03.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 affine/quadratic composition | Implemented compose examples use affine functions; exact exercise polynomial absent |
| E2 reciprocal composition excludes4 | No matching composed-domain assertion |
| E3 sqrt(9-x²) domain | No matching domain/assertion |
| E4 future fee on220/20 | Related110/10 yields1000/11; doubled exercise result absent |
| E5 immediate fee on220/20 | Related110/10 yields90; difference20/11 absent |
| E6 associativity at1 | Matching f/g/h and x=1 included in sampled identity |
| E7 nested reciprocals preserve2 exclusion | No matching domain assertion; symbolic reasoning manual |

Fee/discount timing, zero-fee/rate cases, noncommutativity and selected invalid domains have assertions. Generic compose delegates contracts to its operands; it does not compute symbolic composition domains.

## 3.4 Inverse functions

Source: [check_section_3_04.py](../chapter-03/code/check_section_3_04.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 affine slope5/intercept-7 | Other affine inverse value checked; both composition identities for exact parameters absent |
| E2 shifted square restriction | Unshifted restricted_square helper; shifted inverse domain not asserted |
| E3 8q-120 targets40/44 | Other profit model exercises unique/fractional/outside classifications |
| E4 future240/PV200 | Related110/100 and rate round trips; exact .2 case absent |
| E5 constant function many-to-one | affine_inverse all/none covers analogous degeneracy; injectivity proof manual |
| E6 nonnegative-rate PV range | Round-trip grid includes negative rates; constrained range proof manual |
| E7 x²=9 vs restricted inverse | Rational9/4 inverse and irrational2 classification; exact ±3 distinction absent |

Selected forward/inverse grids are mutually consistent. Boundary suite adds decreasing-profit inverse domain cases, zero and huge rational perfect-square inversions. Those do not turn a rational-perfect-square interface into a general exact real square-root implementation.

## 3.5 Piecewise functions

Source: [check_section_3_05.py](../chapter-03/code/check_section_3_05.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 threshold50 outputs3/7 | Helpers use threshold100 fees2/5; exact exercise absent |
| E2 marginal2%/3% threshold200 | Helper uses1%/2% threshold100; exact fee7 absent |
| E3 flat4/8 limits at100 | Helper uses2/5; neighbor values support a different jump; limit proof manual |
| E4 all-unit15/12 threshold5 | Helper uses12/10 threshold10; exact60/60/72 absent |
| E5 fixed-cost jump at21 | Helper threshold10 with costs40/70; exact130/89 absent |
| E6 need both sides of boundary | Matching helper below/at/above samples; general testing rationale manual |

Original parameter examples have exact checks. Boundary suite compares fee neighbors separated by 10^-100, preserving exact rational threshold behavior. It does not test all alternative exercise parameters or prove continuous limits.

## 3.6 Monotonicity and bounds

Source: [check_section_3_06.py](../chapter-03/code/check_section_3_06.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 4x+7 proof | Other finite increasing sequences; global real proof manual |
| E2 6q-25 capacity10 | Other positive-margin profit bounds; exact-25/35 absent |
| E3 -2q+15 capacity8 | Other negative-margin bounds; exact-1/15 absent |
| E4 constant5 on interval | Constant discrete sequence class tested; real-domain proof manual |
| E5 all-units9-to10 drop | Matching108>100; finite revenue sequence nondecreasing flag false |
| E6 1/x extrema/extended bounds | No matching helper; limit/attainment reasoning manual |
| E7 expansion jump vs margin | Related project/boundary examples; specific threshold11 conceptual argument manual |

Increasing/decreasing/constant finite bounds and all maximizing indices are asserted. Boundary suite explicitly verifies singleton strict monotonicity is vacuous and empty iterable rejection. Finite observations do not prove global/unbounded monotonicity; ordered indices are not automatically economic quantities.

## 3.7 Convexity and concavity

Source: [check_section_3_07.py](../chapter-03/code/check_section_3_07.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 quadratic3x²-2x+1 | Other chord/second-difference examples; exact polynomial proof absent |
| E2 -4x²+8x-1 maximum | No matching quadratic optimization example |
| E3 differences2,5,10,17,26 | Tests use0,1,4,9; same second difference, exact sequence absent |
| E4 profit -q²+12q-20 | Other cost/profit model with optimum5; exact optimum6/profit16 absent |
| E5 capacity4 maximum12 | Other-model capacity4 gives8; exact exercise absent |
| E6 chord x=0,y=4,t=.5 | Checked chord uses y=2; exact gap4 absent |
| E7 concavity vs decreasing | Other profit around optimum increases then decreases; conceptual explanation manual |

Quadratic chord gaps for positive/negative/zero coefficients and selected grid curvature are asserted. Equally spaced grid is an assumption: the API takes values only, so it cannot verify supplied x spacing. No finite sample proves convexity of arbitrary continuous interpolation.

## 3.8 Contracts and validation

Source: [check_section_3_08.py](../chapter-03/code/check_section_3_08.py).

| Exercise | Assertion evidence / gap |
|---|---|
| E1 PV preconditions/units | Nonnegative cash/rate>-1 tested; currency semantics manual |
| E2 losses vs invalid costs | Negative profit atzero and negative-cost rejection |
| E3 exact110/.1 PV100 | Matching exact assertion |
| E4 whole quantity boundaries | Zero, negative, fractional and positive integer cases |
| E5 profit invariant | p+40=10q and constant increments for20 quantities |
| E6 tests vs forecast accuracy | Manual model-suitability review |
| E7 rate10 intended10% | No exact rate10 counterexample here; caller-intent review manual |

PV inverse, zero-rate and additivity checks sample rational domains. Preconditions in software do not verify external currency/rate provenance.

## 3.9 Financial Function Explorer

Source: [check_section_3_09.py](../chapter-03/code/check_section_3_09.py).

Baseline rows0/4/8, break-even4, bounds, maximum/argmax, constant increments and both curvature flags are asserted. Stepped case tests rows5/6, jump-20, break-evens4/7, tied maximizers5/8 and neither global grid curvature. All row profit/difference invariants are checked. Constant/decreasing cases, capacityzero and selected invalid inputs are present.

| Project question | Evidence / gap |
|---|---|
| Q1 fixed50 break-even5 | No matching input assertion |
| Q2 profits5/6/7/8 | Rows5/6 directly; full table checked by assessment script |
| Q3 two break-evens | Exact4/7 reported; explanation manual |
| Q4 capacity6 optimum5 | Matching changed-capacity case absent |
| Q5 maximum vs argmax | Both fields/ties checked; units distinction manual |
| Q6 threshold alone insufficient | Boundary suite and rows5/6 check cross-threshold behavior |
| Q7 tests vs forecast | Manual suitability review |

Optional CSV, discount-pricing and repeated-expansion challenges are not implemented requirements. nonnegative_profit output exists but is not directly asserted by numbered project checks. Currency/row/schema validation is partial, and graph-ready tables do not supply visual graph validation.

## 3.10 Cumulative assessment

Source: [check_section_3_10.py](../chapter-03/code/check_section_3_10.py), reusing3.7/3.8/3.9.

| Problem | Evidence / gap |
|---|---|
| P1 range12q-30 | Full matching range asserted; extrema interpretation manual |
| P2 composition | Matching25/2 vs15 arithmetic asserted |
| P3 inverse targets24/20 | Exact8 vs15/2 arithmetic; whole-unit rejection not invoked here |
| P4 square restriction | No matching noninjectivity/inverse assertion |
| P5 inverse vs reciprocal | Manual conceptual answer |
| P6 marginal1%/3% fee | No matching fee formula/assertion |
| P7 all-units15/12 at10 | Matching135/120/132; monotonicity reasoning manual |
| P8 cost jump above5 | No matching0/-30/0 calculation here |
| P9 7q-21 extrema | No matching proof or endpoint values |
| P10 bounded quadratic optimum5 | Value5 atq5 only; no independent optimum/maximizer proof |
| P11 PV domain/invariant | Exact100 checked; broader invariant in3.8, not this script |
| P12 boundary test design | No literal cost50/90 threshold test family |
| P13 first/second differences | Convex flag for matching sequence; differences not explicitly asserted |
| P14 error categories | Selected domain/type rejections; classification prose manual |
| P15 integrated table | All nine exact rows, break-evens, maxima, monotonicity and row/difference invariants asserted |
| P16 revised price23 above7 | Not implemented/asserted; optional revised model and boundary design manual |

The assessment imports earlier helpers; it does not rerun all earlier scripts and is not independent duplication of their algorithms.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-36 | Many alternative exercise parameters absent despite matching worked-model checks | Exact exercise references or manual computation records |
| COV-37 | Generic composition/inverse domain claims not represented by helper samples | Symbolic/manual domain and injectivity review |
| COV-38 | Curvature helpers cannot verify grid spacing or continuous extensions | Explicit input-grid contract and manual curvature proof |
| COV-39 | Project/assessment some fields and revised models unasserted | nonnegative-profit/report contract checks and exact assessment cases |

These extend COV-01–COV-35; existing conceptual and independence gaps apply. No new implementation defect was established. Next: Chapter 5 mapping (Chapter 4 is already mapped). Independent review, final release/platform evidence and canonical approval remain pending.
