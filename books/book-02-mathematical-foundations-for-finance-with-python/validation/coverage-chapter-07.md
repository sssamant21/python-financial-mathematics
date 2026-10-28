# Book 02 — Substantive Coverage: Chapter 7

**Date:** 2026-10-28  
**Inspected revision:** `ef1a3609fa46b2aa35de91a2ad107de54b5608cd`  
**State:** Ten sections / 109 numbered exercises and project questions mapped; independent review pending.

Read ten manuscripts, implementations, numbered checks and limit-boundary regression. Mapping reaches75/215 sections (Chapters1–7). No new runtime run is claimed; [pinned full run](pinned-revision-runtime-validation.md) and [limit review](chapter-07-limit-boundary-review.md) remain evidence for their scopes.

A sampled value supports a calculation; it does not prove a limit, continuity, unboundedness or theorem hypotheses.

## Section/exercise map

| Section / assertion source | Exercise evidence and gaps |
|---|---|
| 7.1 [checks](../chapter-07/code/check_section_7_01.py) | E1: modified value100 at2 vs nearby x+2, different exercise example conceptual. E2 limit2x+1 at3 absent. E3 removable quotient matching nearby values/exclusion. E4 one-sided criterion manual. E5 mismatch at1/value10 not matching modified-at2 example. E6 epsilon/delta proof manual. E7 zero annuity factor5 and near-zero direct sums. E8 finite-sampling limitation manual. |
| 7.2 [checks](../chapter-07/code/check_section_7_02.py) | E1 definitions manual. E2 step below/at/above5 and approach sides2/7 sampled. E3 nonexistence follows mathematically, no algorithm decides it. E4 matching-piecewise sides at2 sampled and value3. E5 quotient near3/exclusion sampled. E6 point-value/limit distinction manual. E7 sqrt right-limit0 absent. E8 fee5/10 around1000 sampled; continuity conclusion manual. |
| 7.3 [checks](../chapter-07/code/check_section_7_03.py) | E1 continuity definition manual. E2/E3 removable quotient and extension6 directly checked. E4 jump sides sampled. E5 reciprocal signs/value and pole rejection, not unboundedness proof. E6 oscillating(1) and zero rejection do not establish nonexistence; separate7.8 sequences support it. E7 kink values999/1000/1100, no one-sided derivative assertion. E8 annuity n5 zero extension checked. E9 relative-domain endpoint continuity manual. E10 operational-risk explanation manual. |
| 7.4 [checks](../chapter-07/code/check_section_7_04.py) | E1 3+8/x limit absent. E2 rational samples at ±1e100 approach2; proof manual. E3 reciprocal pole rejection/signs; E4 removable distinction related earlier modules, absent here. E5 log(x)/x proof absent. E6 fixed500 and long-horizon convergence sample. E7 repelling fixed-1000 checked; arbitrary-initial claim proof manual. E8 perpetuity2500/E9 matching n10 tail checked. E10 finite-large-input limitation manual. |
| 7.5 [checks](../chapter-07/code/check_section_7_05.py) | E1 periodic formula matching .06 examples. E2 continuous-limit proof manual; frequency grid only finite support. E3 .05 over3 factor not matching tested .06 over2. E4 continuous.04 to EAR absent exact input. E5 .05 effective-to-continuous matching. E6 PV500/.03/t2 matching. E7 annual.06/t2 and continuous values both checked, inequality comparison not explicit. E8 stable primitive rationale manual. E9 negative-rate factor/inverse grid supports selected cases. E10 convention interpretation manual. |
| 7.6 [checks](../chapter-07/code/check_section_7_06.py) | E1/E2/E3/E4 zero extensions1/1/7/1 and nearby samples asserted, general limits manual. E5 original0/0 vs extension interpretation manual. E6 small .001 log approximation not explicitly error-compared. E7 matching log(.98). E8 exact/linear-.005 separately checked; no approximation-error bound. E9 zero annuity12 matching. E10 primitive rationale manual. |
| 7.7 [checks](../chapter-07/code/check_section_7_07.py) | E1 IVT/continuity manual. E2 sqrt2 estimate/bracket/width asserted. E3 discontinuous sign-jump counterexample not executed. E4 uniqueness vs existence and E5 tangent root manual. E6 width8 after5 and E7 n9 halving bound absent exact assertions. E8 project root125 and original values checked. E9 bond residual at.05 and endpoint signs/bisection asserted. E10 strict monotonicity proof manual. |
| 7.8 [checks](../chapter-07/code/check_section_7_08.py) | E1 sampling not proof manual. E2 removable at1 excluded in raw/stable helpers, nearby x+1 checked. E3 two positive oscillation subsequences yield≈0/1 at n1/2/10/100, convergence-to-zero proof manual. E4 discontinuous bracket and E5 root-without-sign-change examples not asserted. E6 cancellation not directly compared with naive result; E7 extension1 asserted. E8 direct/logPV64-case grid. E9 bracket conditional guarantee manual. E10 test-plan assessment manual. |

Boundary suite [check_limit_boundaries.py](../chapter-07/code/check_limit_boundaries.py) checks power quotient at ±5e-324 and exponents±.5/0/1, polynomial value2.1 and empty/nonempty payment iterators. These support prior underflow/iterator fixes, not the full power-limit proof.

Approach functions compare floats around a point. Selected positive steps are tested; there is no general guarantee that arbitrary supplied steps change the represented input or remain inside a function's domain.

## 7.9 — Boundary and continuity investigation project

Source: [checks](../chapter-07/code/check_section_7_09.py).

Cases A–E: removable raw rejects3 while extension returns6; threshold fees match below/at/above1000; reciprocal samples show increasing magnitude/opposite signs for three decreasing distances;25 annuity factor/finite-sum cases; bond-yield bracket/residual/audit fields and selected errors asserted.

Project questions Q1/Q2 have matching values but require limit interpretation. Q3 unbounded asymptote and Q4 zero-extension derivations require proofs. Q5 primitive stability rationale manual. Q6 IVT continuity hypotheses and Q7 uniqueness cannot be inferred from a successful bisection. Q8 evidence-scope explanation manual.

The audit result's estimate, bracket, iteration count, width and residual are checked. This supports the reported computation, not automatic continuity verification or business approval.

## 7.10 — All twenty-five assessment problems

Source: [checks](../chapter-07/code/check_section_7_10.py).

| Problem IDs | Evidence / gap |
|---|---|
| P1 removable limit; P2 piecewise sides; P3 hole vs jump | Related earlier section examples; exact assessment statements/proofs not asserted here |
| P4 reciprocal pole5; P5 rational horizontal limit2; P6 x/exp(x) | No matching assertions |
| P7 exponential limit exp(.08) | No exact frequency/convergence input here |
| P8 log small-change1; P9 power limit6; P10 IVT | Related7.6 values/general theorem reasoning manual; power6 not matching tested limit7 |
| P11 discrete/continuous2500,.06,3 | Both matching formulas asserted; expected expression shares calculation primitive |
| P12 EAR from.05; P13 continuous from.08; P14 PV10000,.03,4 | Matching |
| P15 negative-.01/t2; P16 price100→103 | Matching |
| P17 shock at7/.001 | expm1 vs exp-minus1 identity only; first-order-.007/error comparison not directly asserted |
| P18 zero annuity10 | Matching plus finite-sum rate/count grid |
| P19 break-even200 | No matching project-profit assertion here (7.7 uses125) |
| P20 bond payments60/1060 yield.06 | Matching residual/sign bracket/estimate/width |
| P21 finite-sampling counterexample; P22 tangent root | Manual / no matching example |
| P23 seventeen-halving error bound | No exact assertion |
| P24 bond monotonicity/uniqueness; P25 stability/root conditioning | Manual proofs/interpretation |

The assessment is not a runner of earlier scripts. Many expected formula values reuse math.exp/log, so they are spot checks of translation/inputs, not independent transcendental accuracy references.

## Additional gap register

| ID | Gap | Next evidence |
|---|---|---|
| COV-46 | Continuity/IVT/uniqueness hypotheses not established by solver success | Manual theorem/domain/monotonicity review |
| COV-47 | Approach-step representability and exact bisection bound examples partly untested | Adjacent-float step cases and explicit width/error references |
| COV-48 | Limit/oscillation/asymptote samples do not prove the claims | Epsilon/delta, sequence and unboundedness arguments reviewed independently |

These extend COV-01–COV-45; exact-input and primitive-independence gaps also apply. No new defect or independent sign-off is claimed. Next: Chapter8.
