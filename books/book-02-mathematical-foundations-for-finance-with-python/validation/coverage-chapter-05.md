# Book 02 — Substantive Coverage: Chapter 5

**Date:** 2026-10-28  
**Inspected revision:** `c2026760ba7da0610f3cb13eba83bcd0591170b9`  
**State:** Ten sections / 92 numbered exercises and project questions mapped; independent review pending.

Read manuscripts, implementations, ten numbered checks and recurrence boundary regression. Mapping now covers 55/215 sections (Chapters 1–5). No new runtime execution occurred; [pinned full-run evidence](pinned-revision-runtime-validation.md) and [recurrence review](chapter-05-recurrence-boundary-review.md) remain separately scoped. Assertions reside in each numbered check's run(); the boundary suite uses unittest methods.

## 5.1 — Sequences and time indexing

Source: [checks](../chapter-05/code/check_section_5_01.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 balance sequence/initial condition | Path begins at1000, length3; meaning/manual definition |
| E2 grid24 monthly intervals | Matching length25 |
| E3 monthly t9 | Matching .75 |
| E4 end-flow recurrence | Matching path values; derivation manual |
| E5 two end deposits | Matching1110/1221.1 |
| E6 beginning deposits | Matching1111/1223.11 |
| E7 one-period PV500/.05 | Matching direct quotient |
| E8 payments[n-1] | First/third payment lookup and invalid index; general label argument manual |

Empty paths/grids, zero rates and selected input boundaries are checked. Grid precision and arbitrary-unit compatibility remain outside finite examples.

## 5.2 — Arithmetic and geometric sequences

Source: [checks](../chapter-05/code/check_section_5_02.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 arithmetic term19 | Matching value |
| E2 arithmetic sum140 | Matching value |
| E3 geometric term100*1.05^4 | Matching direct-power reference |
| E4 finite geometric proof | Values/sum-of-terms grid; proof manual |
| E5 four-term sum45 | Matching value |
| E6 deposits FV331 | Matching value |
| E7 zero-rate FV300 | Matching value |
| E8 tiny-rate stable formula | No near-zero accuracy assertion in this script |

q=-2,0,1, empty sums, negative deposit-model rates and count/type/domain rejections are sampled. Same term helpers used in sum reference checks can share formula errors. General algebraic q domain is broader than positive-factor financial domain.

## 5.3 — First-order balance recurrences

Source: [checks](../chapter-05/code/check_section_5_03.py), [boundary regression](../chapter-05/code/check_recurrence_boundaries.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 need initial condition | No explicit two-initial-path comparison; conceptual reasoning |
| E2 recurrence derivation | Matching updates/invariants, derivation manual |
| E3 first balances1120/1242.4 | Matching path |
| E4 beginning balance1122 | Matching balance and interest22 |
| E5 withdrawal ending-90.8695 | Matching unrestricted path and restricted rejection |
| E6 varying rates/flows final1070.434 | Matching full path |
| E7 telescoping identity | reconcile outputs agree on several schedules; mathematical vs rounded ledger distinction |
| E8 three-period expansion | Related closed-form checks in5.4, proof manual |

Empty/zero-rate schedules, unequal lengths and invalid types/domains are sampled. Boundary regression verifies growth-factor evaluation at nextafter(-1,0), nonzero rounding_adjustment, correct available-balance rejection and beginning-flow order. It does not independently specify every ledger field or adjustment sign/range.

## 5.4 — Closed forms

Source: [checks](../chapter-05/code/check_section_5_04.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 B2/B3 substitution | Numeric recurrence comparisons, symbolic expansion manual |
| E2 induction | No test can replace induction; manual |
| E3 end B3=1367.248 | Matching value |
| E4 begin B3=1373.3688 | Matching value |
| E5 zero-rate B0+nC | Matching1300 for both timings |
| E6 fixed-rate varying-flow formula | Variable-form comparison at selected rates/flows; exact expression proof manual |
| E7 two-period variable expansion | No matching symbolic assertion; general variable schedule spot check |
| E8 stable tiny-rate expression | Grid includes1e-12, compared to float recurrence; independent high-precision error reference absent |

120 constant-schedule grid cases compare n0..11, five rates and both timings; empty/single-variable schedules and selected errors are checked. Moderate-value agreement is not extreme-range or relative tiny-signal evidence.

## 5.5 — Fixed points

Source: [checks](../chapter-05/code/check_section_5_05.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 fixed-point definition | Constant path at5000 checked; definition manual |
| E2 derive -C/i | Matching numeric equilibria; algebra/manual |
| E3 equilibrium5000 | Matching |
| E4 repelling classification | Matching |
| E5 B4=3917.56784 | Matching |
| E6 negative-rate equilibrium500 attracting | Matching |
| E7 zero-rate all/none | Matching labels and paths |
| E8 beginning equilibrium | Matching5100 for selected inputs; proof manual |

Fifty recurrence/deviation comparisons and selected domain/type checks support examples. Financial admissibility of an algebraic equilibrium and real sustainability remain separate.

## 5.6 — Convergence and stability

Source: [checks](../chapter-05/code/check_section_5_06.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 epsilon convergence definition | Manual |
| E2 deviation q^n e0 | Numeric deviations only; proof manual |
| E3 q=.9,1.1,-1 | Matching attracting/repelling/oscillatory labels |
| E4 B*=500/B3=208.4 | Equilibrium500 and deviation-400*.9^3 separately checked; summed B3 not explicit |
| E5 first tolerance period36 | Matching integer; adjacent minimality inequality not separately asserted |
| E6 half-life | Same logarithmic reference expression; independent benchmark absent |
| E7 path difference6.5536 | Matching |
| E8 shock106.1208 | Matching plus pre-shock/at-shock cases |

q0 special tolerance step and q1 neutral/no-fixed-point branches are sampled. Full mathematical multiplier classification and near-|q|=1 conditioning are not proved by returned labels.

## 5.7 — Variable rates and schedules

Source: [checks](../chapter-05/code/check_section_5_07.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 recurrence | Numeric schedule, derivation manual |
| E2 two-factor expansion | General product/sum comparison; exact symbolic identity manual |
| E3 final-flow factor1 | No isolated matching assertion; timeline reasoning |
| E4 end first balance1120 | Matching |
| E5 begin first1122 | Matching |
| E6 final1090.564 | Matching both timing paths |
| E7 reconciliation | Matching numeric interest/flow reconciliation |
| E8 rate-order effects with intervening flows | No explicit swapped-rate comparison |

Zero-rate/empty schedules, length/timing/rate and no-overdraft failures sampled. Similar helpers recur across modules; agreement alone does not establish an independent financial specification.

## 5.8 — Withdrawal boundaries

Source: [checks](../chapter-05/code/check_section_5_08.py).

| Exercises | Evidence and gaps |
|---|---|
| E1 end feasibility | Selected withdrawals original availability; general inequality manual |
| E2 begin feasibility |105 fails before growth but succeeds after growth |
| E3 zero-rate first fail3 | Matching |
| E4 partial final withdrawal100 | Matching paid100/closing0 |
| E5 .01 first fail3/available109.1305 | Matching |
| E6 withdrawal equilibrium W/i | Related5.5/5.6 examples; derivation manual |
| E7 exact exhaustion four, failfifth | Matching including feasible equality atzero |
| E8 real sustainability | Manual model-assumption review |

Reject vs partial policies and empty schedule are sampled. Continuation/retry after rejection, partial-payment rule under varied rates, near-boundary exact comparisons and all ledger fields are not covered exhaustively.

## 5.9 — Recurrence engine

Source: [checks](../chapter-05/code/check_section_5_09.py).

Required Period/EngineResult records are consumed, but full field/type schema is not independently asserted. End/begin numerical examples, product/sum reference, reconciliation, no-overdraft rejection, applied0/acceptedFalse, exact exhaustion, empty input and selected invalid Period/timing/type cases are asserted.

| Project question | Evidence and gaps |
|---|---|
| Q1 add last contribution50 ->1140.564 | No matching modified scenario |
| Q2 product/sum reference | Matching unrestricted end/begin scenario |
| Q3 reconciliation proof | Helper agreement; telescoping/rounding semantics manual |
| Q4 requested vs applied | Rejected applied0 and reconciliation; altered requested ledger invariance not independently tested |
| Q5 first fail3 | Matching |
| Q6 begin/end liquidity | Matching105 rejected before growth, accepted after |
| Q7 partial withdrawal extension | Optional design, not engine feature; distinct5.8 policy exists |
| Q8 three further real-money tests | Manual test-plan assessment |

Rejected scenarios fail on their last supplied period, so they do not alone demonstrate that later scheduled periods are not processed. The boundary regression also supplies only one period. Product/sum reference is specified for unrestricted schedules, not requested flows after a rejection.

## 5.10 — All twenty assessment problems

Source: [checks](../chapter-05/code/check_section_5_10.py), assessment_values and engine imports.

| Problem | Evidence and gaps |
|---|---|
| P1 arithmetic path100..200 | Not in assessment_values or numbered assertions |
| P2 geometric562.432 | Matching fixed expected |
| P3 first/second balances | Matching1120/1242.4 |
| P4 closed-form proof/zero multiplier case | No proof assertion; related5.4 evidence |
| P5 timing1150/1155 | Matching |
| P6 unstable equilibrium5000 | Not among returned expected fields; related5.5 |
| P7 stable500 and full path | Equilibrium500 checked; full expression proof manual |
| P8 tolerance36 | Matching, minimality proof/manual |
| P9 sensitivity6.5536 | Matching |
| P10 shock106.1208 | Matching |
| P11 variable ledger | Final plus engine/reference/reconciliation; full interest breakdown via5.7 |
| P12 begin schedule | Matching final and reference/reconciliation |
| P13 zero-rate fail3 on500/200 | Not directly this assessment;5.8 supports exact input |
| P14 .01 depletion | Matching fail3/109.1305 |
| P15 exact exhaustion/fail5 | Matching fourth closing0 accepted and fifth rejected |
| P16 begin/end105 | Not here; matching5.9 assertions |
| P17 applied-flow identity | Rejected engine reconcile; mathematical explanation manual |
| P18 two-period expansion | No exact symbolic proof assertion |
| P19 four invalid-input conditions | Not directly here; helper tests elsewhere |
| P20 sustainability critique | Manual |

The assessment reuses the engine and related formulas; it does not invoke all ten scripts. Fixed expected dictionary keys assert eleven computational outputs, not twenty complete written solutions.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-40 | Reject-and-stop not exercised with subsequent scheduled periods | Multi-period suffix after early rejection, assert ledger/closing/timing |
| COV-41 | Rounding adjustment only partly independently specified | Reference field values and mathematical/numerical reconciliation review |
| COV-42 | Rate ordering, tolerance minimality and selected assessment inputs unasserted | Independent exact/Decimal scenarios and adjacent-period checks |

These extend COV-01–COV-39. Existing proof, tiny-signal and contract gaps apply. No new defect or independent sign-off is claimed. Next: Chapter6.
