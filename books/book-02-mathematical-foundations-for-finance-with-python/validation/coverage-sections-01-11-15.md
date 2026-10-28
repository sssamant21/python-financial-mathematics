# Book 02 — Substantive Coverage: Sections 1.11–1.15

**Date:** 2026-10-28  
**Inspected revision:** `ade78ec348baff263a3877d82c6b1b3540f2ea4f`  
**State:** Chapter 1 mapping complete; substantive evidence gaps and independent review remain open.

Inspected five manuscripts, their implementations/checks and check_chapter_01.py. Mapped 18 section practice problems, six project challenges and twenty chapter-wide problems. Together with earlier slices this covers 25/215 numbered sections: all Chapter 1 and Chapter 4. Mapping is not certification. No new runtime execution occurred; the [pinned full run](pinned-revision-runtime-validation.md) retains its original revision and scope.

Companion walkthrough/solution manuscripts were linked but were not independently audited in this slice. The chapter problem mapping compares the problem statement, reference implementation and assertion, not the completeness of those separate solution documents.

## 1.11 — Translating Financial Questions into Mathematics

Assertion source: [check_section_1_11.py](../chapter-01/code/check_section_1_11.py).

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 decision, balances and objective | Fee, both balances, original constraints and conservation checked | Mathematical formulation/objective explanation manual |
| P2 800/100 reserve200 target500 | Matching transfer400, fee12, source388; target follows from accounting | Full written constraint/minimality argument |
| P3 target700 infeasible | Matching exercise transfer None | Exact upper bound 29800/51 and reserve deficit16 not directly asserted |
| P4 no action at equal balances | Source=reserve, destination=target zero-action boundary asserted | Alternative fee-at-zero contract not implemented; comparison manual |
| P5 initially deficient reserve | Explicit deficient-source boundary plus grid | General impossibility proof manual |
| P6 cap250 | No cap parameter in this model | Proposed extension/domain intersection requires manual review |

324 scenario cases use an independently rearranged positive-transfer upper bound; 1,296 proposals check conservation and original constraints. A smaller gap/2 proposal fails the target, but general minimality relies on the formulation. Six boundaries include exact fee affordability and just-insufficient source. Thirteen invalid-input cases exercise selected contracts.

The model's zero-transfer fee exemption differs deliberately from the affine transaction-fee model in Section 1.7.

## 1.12 — Translating Mathematical Expressions into Python

Assertion source: [check_section_1_12.py](../chapter-01/code/check_section_1_12.py).

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 grouped quotient, power, absolute band | Grouped quotient and growth grid; no matching absolute-band translation here | Syntax/domain interpretation manual; cross-section band evidence is distinct |
| P2 unary minus/power/XOR | Matching -9,9,1 assertions | Operator meaning/source explanation manual |
| P3 zeros preserve period-two payment | Matching 100 vs110 values | Index/time explanation manual |
| P4 200 declining10% twice | Matching exact162; -1/-2 rejected | Financial domain interpretation manual |
| P5 (-50,55) at .10 | Exact zero PV asserted | Sign/timeline explanation manual |
| P6 empty, float and bool contracts | Matching rejection categories | Distinction from mathematical impossibility manual |

Sixty growth cases compare with additive-interest recurrence. 360 signed schedules compare with backward nested discounting, an alternative evaluation structure. Time-zero terms, input preservation, exact discounted terms, power associativity and invalid domains are asserted. Copying this exact interface does not extend the Section 1.5 empty-schedule or generator contract; these interfaces intentionally differ.

## 1.13 — Checking Mathematical and Computational Results

Assertion source: [check_section_1_13.py](../chapter-01/code/check_section_1_13.py).

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 candidate210 vs220.5 | Matching discrepancy -10.5 asserted | Weak-bound result for this input is not explicitly checked (related 100/110 example is) |
| P2 copied formula vs recurrence | Recurrence references and exact audit grid | Shared convention errors/manual independence review |
| P3 1e-8 vs zero tolerance | Both matching tolerance outcomes and reversed comparisons asserted | Materiality/tolerance justification manual |
| P4 numerical tolerance vs reserve waiver | No transfer-policy test in this script | Manual separation of policies |
| P5 always-zero function counterexample | Positive known values and deliberately wrong candidates | No literal mutant always-zero implementation tested |
| P6 preserve failure evidence | No evidence-capture procedure assertion | Manual review of reproducibility and tolerance-change rationale |

Sixty exact audits check correct and unit-perturbed candidates; 72 property cases check staging/scaling; five deliberate errors are rejected. Thirteen tolerance examples include dyadic exact boundaries, and sixteen rejections enforce comparison domains. The candidate110 at principal100 still passes weak bounds, demonstrating their insufficiency. Properties and inverse checks share the model's convention and cannot establish external suitability.

## 1.14 — Financial Formula Validation Toolkit

Assertion source: [check_section_1_14.py](../chapter-01/code/check_section_1_14.py).

| Contract/milestone | Existing evidence | Remaining review |
|---|---|---|
| Three models and PASS/FAIL/INVALID | Eight-case fixture with exact ordered statuses, counts4/2/2 and named reserve failure | Model suitability remains external to dispatcher |
| Exact-key and identity rules | Required-key removal/extra keys across model inputs; malformed envelopes and duplicate IDs | Full envelope/case field/type boundary combinations not exhaustive |
| Exact growth and rate normalization | 27 recurrence cases; 3 quotation equivalents; observation+1 must FAIL | Horizon120 accepted endpoint not directly exercised |
| Accrual | ACT/365F exact3600/73; wrong50 fails; leap interval example | All date/currency/source meanings not established by syntax |
| Transfer accounting and constraints | Each observed field perturbed; source breach isolated; zero-action fee case | Proposed transfer validation is not minimum-transfer optimization |
| Serialization/report | Strict JSON serialization, exact discrepancy string, invalid details/checks, CLI report equality | Every metadata/schema/type field not independently asserted |
| CLI exit/report behavior | Twelve subprocess cases; success0, mixed1, input errors2; report writing and overwrite prevention | Windows/environment matrix still pending |
| Loader limits | Duplicate keys, NaN/Infinity, malformed/invalid UTF-8, missing file, 1,000,001 bytes rejected | Exactly1,000,000 bytes and 100-case positive boundaries not established |

Fixture immutability is directly asserted. Subprocess checks are materially stronger than in-process main() success calls. No test establishes that a declared currency, rate representation or date convention matches an external source.

### Six project challenges

| Challenge | Evidence / gap |
|---|---|
| C1 correct missing-period observation and recompute whole-batch counts | Correct/incorrect growth observations checked; exact modified eight-case counts not asserted |
| C2 replace convention with ACT/365F | Exact3600/73 passes and observation50 fails |
| C3 repair target700 and transfer500 | Valid fixture transfer and chapter-wide repaired batch support accounting; challenge-specific full report review pending |
| C4 zero action at source=reserve/destination=target | Matching scenario passes with fee0; wrong fee5 fails |
| C5 decimal/percent/bp equivalence | All three produce reference121 and PASS |
| C6 invalid case vs malformed batch | INVALID rows coexist with valid records; malformed batch/CLI errors exit2 |

## 1.15 — All twenty chapter-wide problems

Assertion source: [check_section_1_15.py](../chapter-01/code/check_section_1_15.py). Each reference_results() entry is compared with a fixed expected JSON-ready value, plus structural assertions.

| Problem | Computational evidence / remaining written review |
|---|---|
| P01 allocation | [26,25,25,25], sum101/spread1; domains/divisibility rationale manual |
| P02 fixed-parameter scenarios | Exact520.2 and540.8; variable/decision distinction manual |
| P03 interval | True,True,False,False at specified values; notation/domain explanation manual |
| P04 indexed schedule | Exact total0; sum notation, signs and risk interpretation manual |
| P05 equations | unique5/all/none and original residual; later financial-domain interpretation manual |
| P06 fee budget/cap | Maximum500, slacks0/-.1; affine-at-zero specification manual |
| P07 inequality | False,True,True at2,3,4; strict-boundary extension manual |
| P08 revenue/profit | Profit-20 and false implication; converse/contrapositive prose manual |
| P09 quantifier negation | Witness indices[1,2]; universal/empty-domain interpretation manual |
| P10 strict fee claim | Both rates1/200; general nonstrict/strict proof manual |
| P11 units/rate changes | Value1000, .75pp,75bp, relative1/4; units and invalid addition manual |
| P12 leap accrual | Exact2 and144/73; day-count/rounding interpretation manual |
| P13 minimum transfer | Transfer500, fee16, balances684/650, higher-target None; conservation also asserted; formulation/manual proof |
| P14 grouping/operators | Correct125, wrong10000, power8/XOR1; translation reasoning manual |
| P15 cash-flow timing | Totals0,62/5,100,110; deleting-zero interpretation manual |
| P16 tolerance/policy | False/True closeness outcomes; reserve waiver not decided by test |
| P17 missing-period audit | Reference363, discrepancy-33, relative1/11 and weak checks; absolute-error field not separately asserted |
| P18 mixed batch | Counts1/1/1 and failure constraint isolated; exact exercise CLI exit not separately invoked |
| P19 repaired copy | Counts3/0/0, success, original batch unchanged; exact exercise CLI exit not separately invoked |
| P20 meaningful checks | Exact scale4 relation, missing-period rejected and selected invalid inputs; student's test plan/evidence interpretation manual |

No test automatically awards the manuscript's five-point reasoning rubric or audits the separate companion solutions. Fixed expected values supply concrete numerical references; imported helpers and repeated expressions are not twenty independent model implementations.

## Aggregate and dependency scope

check_chapter_01.py runs only the fifteen numbered scripts in subprocesses. It does not run check_foundation_boundaries.py, added later. Its declared fifteen-script scope is accurate, but it must not be described as every current Chapter 1 check. The full pinned book run separately included both the aggregate and the boundary suite; aggregate results duplicate numbered checks.

The aggregate hashes all code/JSON fixture files after execution. Hash presence does not prove a file was exercised, and the runner itself does not pin a Git revision or place a timeout on each child. Evidence still needs an external snapshot/command record. No runner change or new execution was made here.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-26 | Chapter runner omits later boundary suite | Decide intended runner scope; keep aggregate duplication explicit |
| COV-27 | Project positive size/count/horizon boundaries not fully exercised | Meaningful accepted-boundary and adjacent-rejection cases |
| COV-28 | Report metadata and every output field not independently asserted | Specify and test consumer-visible report contract |
| COV-29 | Companion walkthrough/solutions and prose rubric not audited | Named independent content review tied to revision |

These extend COV-01–COV-25. Existing exact-input, conceptual and independence categories also apply. They are evidence gaps, not demonstrated implementation defects.

Chapter 1 is now fully mapped, with gaps open. Next: Chapter 2 substantive coverage mapping, starting Sections 2.1–2.5. Independent review, supported-platform testing and canonical approval remain pending.
