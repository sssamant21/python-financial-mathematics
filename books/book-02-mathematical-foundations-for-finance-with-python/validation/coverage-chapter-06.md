# Book 02 — Substantive Coverage: Chapter 6

**Date:** 2026-10-28  
**Inspected revision:** `83ed0354c828485e4b4c68cd3eba6bf8dbf81f9a`  
**State:** Ten sections mapped; formula derivation, independence and numerical-range review pending.

Inspected ten manuscripts, implementations, ten numbered checks and the series-boundary regression. This covers 92 numbered exercises/project extensions plus six capstone tasks. Mapping reaches65/215 sections (Chapters1–6). No new runtime run occurred; [pinned evidence](pinned-revision-runtime-validation.md) and [series review](chapter-06-series-boundary-review.md) remain scoped records.

Each table lists all exercise IDs; grouped IDs share an evidence disposition, not a claim of identical coverage.

## 6.1 — Summation/product notation
Source: [checks](../chapter-06/code/check_section_6_01.py).

| IDs | Evidence / gaps |
|---|---|
| E1 odd-number sum16; E2 product24 | Neither exact expression asserted |
| E3 empty sum/product | Matching0/1 assertions |
| E4 reindexing | Manual index/domain proof |
| E5 flow120; E6 factor1.040094; E7 balance1040.094; E8 balance1058.8 | Matching values; product/sum vs iterative route for E8 |

Eight generated moderate schedules compare recurrence and weighted sums. Length, factor/type/nonfinite errors sampled. Mathematical notation and units remain manual.

## 6.2 — Finite geometric sums
Source: [checks](../chapter-06/code/check_section_6_02.py).

| IDs | Evidence / gaps |
|---|---|
| E1 sum31; E3 q1 sum4; E4 q.5 sum1.75; E5 q1.02 sum3.0604 | Matching values |
| E2 general derivation | Finite examples do not prove identity |
| E6 end1367.248; E7 begin1373.3688 | Matching |
| E8 stable near-one expression | Rate1e-12 grid and factor≈100; independent accuracy analysis pending |

Sixty rate/count/timing combinations compare closed and iterative balances. Separate boundary suite tests q=1e-100, nextafter(1,+inf), and .5 known sum. q0/negative branches are examples, not universal range certification.

## 6.3 — Infinite geometric series
Source: [checks](../chapter-06/code/check_section_6_03.py).

| IDs | Evidence / gaps |
|---|---|
| E1 convergence definition | Manual |
| E2 ratio.6 sum2.5 | Matching |
| E3 q=-1 divergence | API rejects; partial-sum oscillation proof not asserted |
| E4 .8 first4/tail | Matching2.952/2.048 and reconciliation |
| E5 ordinary2000; E6 due2100 | Matching |
| E7 tail derivation | Tail n0/10 and finite+tail identity; proof manual |
| E8 zero-rate divergence | API rejection; unbounded partial-sum proof manual |

Zero-amplitude geometric series permits a zero result outside ordinary nonzero convergence range. Positive-payment financial convergence and algebraic signed/alternating series must retain separate domains.

## 6.4 — Annuities
Source: [checks](../chapter-06/code/check_section_6_04.py).

| IDs | Evidence / gaps |
|---|---|
| E1 payment times | Direct enumerator comparison exercises timing, but explicit time-array contract not asserted |
| E2 FV derivation; E3 PV derivation | Manual geometric proofs |
| E4 FV306.04; E5 due312.1608; E6 zero-rate300 | Matching values |
| E7 FV/PV identity | Matching three-period identity plus grid |
| E8 payment inverse | Six rate/timing round trips to PV1000; independent payment benchmark/manual algebra |

120 value-grid cases compare direct enumeration with closed forms. Empty count, invalid conventions/rates and zero-period payment solving sampled. Extreme FV may overflow an intermediate PV despite a representable final answer; scoped runtime does not close that previously recorded range concern.

## 6.5 — Growing streams
Source: [checks](../chapter-06/code/check_section_6_05.py).

| IDs | Evidence / gaps |
|---|---|
| E1 payments100,102,104.04,106.1208 | Exact listed growth.02 sequence not asserted |
| E2 formula derivation | Manual |
| E3 PV100/1.05+103/...; E4 correspondingFV | Matching explicit payments and accumulation |
| E5 equal-rate proof; E6 PV300/1.04 | Value asserted; proof manual |
| E7 timing shift | DuePV compared with ordinary*1.05 and broad grid |
| E8 nonzero convergence r>g | Equal/greater-growth perpetual cases rejected; proof manual |

96 grid cases include near equal growth/rate and negative rates. The enumeration and formula share primitives; a broad float grid is not a high-precision error bound near cancellation.

## 6.6 — Perpetuities/tails
Source: [checks](../chapter-06/code/check_section_6_06.py).

| IDs | Evidence / gaps |
|---|---|
| E1 level derivation | Manual |
| E2 ordinary2000; E3 due2100; E4 deferred2000/1.05^3 | Matching |
| E5 convergence | Nonzero equal/greater-growth rejection, zero-payment exception; proof manual |
| E6 growing100/.03 | Matching |
| E7 growing-tail derivation | Tailn5 and five finite+tail cases; proof manual |
| E8 finite value when r<=g | Related finite grids in6.5/6.8; conceptual distinction manual |

Deferred/growing/level formulas have selected matching checks. Tail+finite=total is related-formula consistency; it does not by itself independently validate every timing exponent.

## 6.7 — Truncation error
Source: [checks](../chapter-06/code/check_section_6_07.py).

| IDs | Evidence / gaps |
|---|---|
| E1 error definitions; E2 exact-tail derivation | Manual definitions/proof |
| E3 sum5; E4 partial2.952/tail2.048; E5 relative.4096 | Matching |
| E6 minimum relative horizon | q/tolerance grid checks n and n-1 with numerical slack |
| E7 perpetuity95 periods | Matching returned integer; original-tail minimality not separately asserted for this case |
| E8 truncation vs model error | Manual |

Thirty partial+tail cases and twelve horizon cases include alternating/zero ratios. Adjacent n checks support discrete minimality at sampled inputs, unlike a ceiling-only assertion. Absolute-error horizon derivation is in prose but lacks a corresponding absolute-horizon implementation/check here.

## 6.8 — Zero rates/verification
Source: [checks](../chapter-06/code/check_section_6_08.py).

| IDs | Evidence / gaps |
|---|---|
| E1 removable0/0; E2 zero-rate limit | Finite zero cases asserted; limit proof manual |
| E3 PV2000; E4 dueFV2000 | Matching |
| E5 growingzero-discount306.04 | Matching |
| E6 positive level zero-rate divergence | No matching rejection in this script; earlier perpetuity rejection evidence is related |
| E7 zero discount/negative growth perpetual1000 | Matching project assertion in6.9, not here |
| E8 independent methods | Closed/enumerated values and timing/PV-FV checks; independence analysis manual |

384 growing-stream and96 level-stream grid comparisons cover signed growth/discount regimes and g=r. Those grids are evidence for stated finite domains, not for nonzero perpetuities or every near-zero condition.

## 6.9 — Verification engine
Source: [checks](../chapter-06/code/check_section_6_09.py), [boundary suite](../chapter-06/code/check_series_boundaries.py).

Acceptance1 finite/type/count/conventions has selected rejection assertions. Acceptance2 empty streams is in the grid. Acceptance3 formula/direct agreement and4 time-n FV are enforced inside verify() for both kinds across168 scenarios; the outer script additionally asserts PV against direct_sum. Acceptance5 r0/g=r appears in the grid and known values. Acceptance6 invalid nonzero perpetual growth rejected. Acceptance7 five finite+tail reconciliations. Acceptance8 accurate limitations requires manual review.

| Extension IDs | Evidence disposition |
|---|---|
| X1 JSON-lines; X2 seeded random matrix; X3 irregular times; X4 absolute horizon | Not implemented/claimed mandatory; design tasks |
| X5 payment scaling | Signed first values sampled, but no explicit scale relation assertion |
| X6 negative payment | first=-100 grid cases present |
| X7 sum vs fsum sensitive benchmark | Not asserted |
| X8 reviewer checklist | Manual |

Boundary suite rejects nonfinite/negative tolerances and Boolean tolerance, and checks zero-rate values. Accepted huge finite tolerance can weaken verification by policy; appropriateness is not established by input validity. verify() must itself remain trustworthy; monkeypatched disagreement/false-report paths are not tested.

## 6.10 — All twenty assessment problems
Source: [checks](../chapter-06/code/check_section_6_10.py).

| IDs | Evidence / gaps |
|---|---|
| P1 explicit four payments/third term | Exact206.0804/52.02 not asserted |
| P2 geometric derivation | Manual |
| P3 sum480 | No matching generic infinite-series input here |
| P4 q1.01 divergence | No matching partial-sum proof here; perpetual domain checks are related |
| P5 ordinaryPV; P6 FV315.25; P7 dueFV331.0125 | Matching ordinaryPV/dueFV; duePV factor not independently asserted as an explicit known value |
| P8 twelve80 zero-rate960 | Other input250/eight→2000 tested; exact exercise absent |
| P9 growing100/103/106.09 | Matching g.03/r.05/n3 in grid |
| P10 equal-rate five payments | Matching500/1.04 |
| P11 growth.08/rate.03/n4 | Grid has same rates but count0/1/3/10, not4 |
| P12 rate-.02 | Grid uses negative discount-.01; exact-.02 example absent |
| P13 level2500; P14 growing3750 | Matching |
| P15 deferred2500/1.06^3 | No matching deferred assertion |
| P16 growing tail3750*(1.02/1.06)^5 | Other payment/rate tail cases; exact exercise absent |
| P17 relative.8^10 | Not directly asserted |
| P18 horizon21 | Matching |
| P19 three-check design; P20 model-risk critique | Manual |

192 finite valuation scenarios compare analytic/enumeratedPV and FV/PV. Applied capstone a–f: same1000/.03/.05/n10 lies in grid (both due modes); contributions not explicitly listed/asserted, and due-to-ordinary factor not separately asserted. Infinite50000 and finite+tail identity at n10 are checked through other tail loop references. Explanations of convergence, assumptions and finite/infinite distinction remain manual.

## Additional gap register

| ID | Gap | Next evidence |
|---|---|---|
| COV-43 | Many finite/tail oracles share primitive formulas | Independent exact/Decimal or recurrence references and exponent/timing review |
| COV-44 | Absolute-horizon design and verification-failure paths absent | Targeted error-budget and intentionally inconsistent-reference cases |
| COV-45 | Extreme finite FV/near-equal-rate accuracy not certified | Scale-aware reference cases, including finite-result/intermediate-overflow scenarios |

These extend COV-01–COV-42. No new implementation defect or independent sign-off is claimed. Next: Chapter7.
