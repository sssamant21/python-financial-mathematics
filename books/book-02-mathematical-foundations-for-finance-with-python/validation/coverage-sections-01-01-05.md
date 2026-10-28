# Book 02 — Substantive Coverage: Sections 1.1–1.5

**Date:** 2026-10-28  
**Inspected revision:** `5f73dc91ef6fa433aff31bdff69216f9b31e8ffb`  
**State:** Five sections and 29 practice problems mapped; conceptual review remains pending.

Read the five section manuscripts, implementations and numbered check scripts. This extends substantive mapping to 15/215 numbered sections: Chapter 4 plus Sections 1.1–1.5. It is not a validated-section count. Existing runtime results are recorded in the [pinned full run](pinned-revision-runtime-validation.md); no new test execution occurred in this mapping pass.

## Assertion sources

- [check_section_1_01.py](../chapter-01/code/check_section_1_01.py): `5982d9f76c65268e8547b9c83f8e2aaa626fd2a2`.
- [check_section_1_02.py](../chapter-01/code/check_section_1_02.py): `01158df95012498fd1a16806daf310ee17efdb34`.
- [check_section_1_03.py](../chapter-01/code/check_section_1_03.py): `e139ceca9e638bbd6c26ffabbd435a5463140f0a`.
- [check_section_1_04.py](../chapter-01/code/check_section_1_04.py): `29a93022349b01b2e7a7369dbcf597f2591e8fb8`.
- [check_section_1_05.py](../chapter-01/code/check_section_1_05.py): `e9936bfa5bc75d730eea14a1fc2139ad80da3fe9`.

These checks execute assertions at module level. Named check labels below identify actual assertions, not inferred coverage from function names or imports.

## 1.1 — Why Mathematical Foundations Matter in Finance

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 2000 at .03 for two periods | Known case equals 2121.8 | Derivation, reinvestment and units manual |
| P2 upfront/end fee on 500 at .04 | 514.8, 515 and difference .2 asserted | Timeline interpretation manual |
| P3 discount 121 and wrong-date accumulation | Direct expressions checked against 100 and 146.41 | Explanation of the year-four valuation date manual |
| P4 +10% then -10% counterexample | 100*1.1*.9 close to 99 | General explanation manual |
| P5 review account assumptions | No machine assertion of actual contract suitability | Named manual review |

Known-value cases cover the opening growth example, zero periods/rate, negative rate and entering 5 instead of .05. Thirty-six moderate scenarios compare the closed form with iterative multiplication and recover principal. Thirteen invalid/range cases include bool/nonfinite inputs and over/underflow. Recurrence is an alternative evaluation order, not an independent specification of the rate convention.

Six hands-on investigations are partly represented: zero/negative rates and invalid inputs have assertions; five-period recurrence comparisons are in the grid; fee exercise checks use fee 5 rather than the requested fee-20 investigation; percentage-input mistake has the matching 6000 result. Student predictions, explanations and restoring demonstration inputs are not automated evidence.

## 1.2 — Mathematical Objects and Number Systems

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 classify number systems | Binary eighth and rational float sqrt approximation checks | Complete classification of 0,-3,7/20 and exact sqrt(2) is conceptual |
| P2 1.25% exact rate on 800 | Fraction('0.0125')==1/80 and ending value 810 | Unit/rate interpretation manual |
| P3 Decimal precision does not make 1/3 exact | Decimal context quotient converted to Fraction differs from 1/3; exact decimal sum | Precision 50 example not literally used; general argument manual |
| P4 split 101 between four | Exact [26,25,25,25] plus conservation grid | Divisibility/necessity proof manual |
| P5 float-to-Decimal preserves approximation | Decimal(.1)!=Decimal('.1') | Original-source intent cannot be inferred by test |
| P6 portfolio objects/alignment | Aligned value 80 and list concatenation asserted | Labels, currency, valuation time and semantic alignment manual |

Representation assertions cover exact thirds/sevenths, quoted decimal conversion, half-even/up rounding, finite values and local-context restoration. The 408 small allocation scenarios check conservation, shape, integer/nonnegative amounts, spread and the stated remainder rule. The remainder expected-value expression resembles the implementation; conservation and balance supply complementary properties, not a proof for all integers.

Lab extensions and selection of a representation appropriate to a real contract require manual judgment. Computational representations do not establish mathematical classification of an exact irrational constant.

## 1.3 — Variables, Constants, and Parameters

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 variable/parameter roles in 500(1+r)^3 | Scenario grids vary rates/principals/horizons | Symbol roles and non-random interpretation manual |
| P2 time study 500(1.04)^n | Grid includes principal 500, rate .04, horizons 0,1,2,5 | General domain/formulation manual |
| P3 target principal for 1210 | 1210/(1.1**2) close to 1000 | Unknown-vs-parameter distinction manual |
| P4 zero principal/horizon identifiability | Multiple rates give zero/unchanged value | Finite sample does not prove full solution set |
| P5 uppercase BASE_RATE convention | No rebinding/immutability assertion | Python naming policy/source review |
| P6 50bp move at 500,.04,n=2 | Direct difference 5.2125 and independent Fraction benchmark | Expanded identity/general derivation manual |

Named assertions include preservation/order/duplicates of scenario inputs, generator acceptance, empty scenarios, basis points, joint-change path decomposition and negative rates. Sixty-four scenarios compare recurrence/scaling; 36 compare finite-change expansion. The exact rational benchmark strengthens the one worked finite change.

Empty scenarios explicitly bypass row validation even for invalid principal/horizon; this is asserted as the documented contract, not global parameter validation. A passed empty result must not be interpreted as validation of absent rows or general model suitability.

## 1.4 — Sets, Intervals, and Financial Domains

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 [-.02,.10) endpoints | Four endpoint conventions tested on [0,1] | Exact stated interval not directly asserted |
| P2 policy/model intersection | -1 exclusion, negative admitted rate, named lower-exclusion comparison | Full (-1,.15] boundary/intersection evidence incomplete |
| P3 excluded .03 pole and cancelled quotient | No direct quotient/pole assertion in this script | Manual domain derivation; possible cross-map to 1.6 later |
| P4 coupled weight pairs | Endpoint pairs; .8/.8 and 1.1/-.1 rejection; rational weight grid | Full-investment interpretation manual |
| P5 complete loss vs discount-rate boundary | Exact -1 simple return and discount rejection | Different model domains manual |
| P6 empty/singleton and reversed bounds | Named empty/singleton examples; equal-bound conventions; reversed-bound exception | Mathematical set vs API error explanation manual |

Assertions cover set operations, 40 interval cases, 60 product-domain cases, 225 coupled weight cases and 11 invalid configurations. Adjacent representable floats around -1, 0 and 1 are exercised. The float-conversion limitation at 2**53+1 is intentionally asserted; membership reflects converted floats, not arbitrary exact integer membership. Budget tolerance relaxes the sum check, not component bounds.

Named rational-reference comparisons strengthen finite samples; they do not certify every possible tolerance boundary or input subclass.

## 1.5 — Mathematical Notation and Indexed Quantities

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 relabel 20,30,40 | One-based enumerate tuples asserted | Relabeling vs financial-time interpretation manual |
| P2 inclusive sum t=0..4 | tuple(range(5)) asserted | Summation notation explanation manual |
| P3 record 2 paid at time 5 | Matching period-five PV vs 100/1.1**5 | Oracle reuses direct formula; label explanation manual |
| P4 repeated-date aggregation | Matching schedule at rate .05 vs aggregated equivalent | General linearity and same-currency assumptions manual |
| P5 multi-index flows | 40, 440 and zero-rate PV 480 asserted | General indexed-sum interpretation manual |
| P6 ordinary zip data loss | Strict mismatch both directions and consumption-time exception | No explicit ordinary-zip truncation assertion; missing-data intent manual |

Two-payment timing examples use exact Fraction reference values. Repeated and identical records, signed/time-zero payments, empty schedules, generator inputs, re-pairing and irregular schedules are asserted. Fifty-four schedule scenarios use scaling, date shifts and rational PV references; 24 whole-record permutations preserve PV. Label-order permutations yield 80 while wrong positional pairing yields 70.

Twenty invalid/range cases plus strict-zip consumption cover selected interface failures. A source's completeness, currency or duplicate-asset-label policy is not validated by those tests. The lab is for finite schedules, not unbounded streams.

## Additional gap register

| ID | Finding | Required next evidence |
|---|---|---|
| COV-19 | Conceptual answers not established by numerical matches | Manual review of units, roles, derivations and exact-vs-represented objects |
| COV-20 | Some exercise/lab inputs differ from asserted inputs | Preserve exact input mapping; add independent cases where material |
| COV-21 | Set/domain descriptions broader than finite samples | Review sign/exclusion reasoning and API-vs-mathematical semantics |
| COV-22 | Real data alignment/completeness outside helper contracts | Manual input-specification review; do not infer source validity from shape checks |

These extend the eighteen Chapter 4 categories. No implementation defect is established by these gaps. No source algorithm, exercise answer or numerical test was changed. Existing manuscript evidence claims were retained with their recorded scope; independent mathematical/editorial review and canonical approval remain pending.

Next mapping slice: Sections 1.6–1.10.
