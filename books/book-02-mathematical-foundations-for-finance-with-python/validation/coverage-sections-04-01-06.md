# Book 02 — Substantive Coverage: Sections 4.1–4.6

**Date:** 2026-10-28  
**Inspected revision:** `64c07154ec10eecb73c805de80a39da35e26dad2`  
**Status:** Six sections and their 46 numbered exercises mapped; partial executable evidence, independent review pending.

Read the six manuscripts, implementations and numbered check scripts. Assertions below are in each check script's run() function. Runtime evidence is the earlier [pinned full run](pinned-revision-runtime-validation.md), not a new execution. Spot checks do not prove identities or validate exercise reasoning. Existing [4.7–4.8 mapping](coverage-sections-04-07-08.md) brings substantive mapping to 8/215 numbered sections, not eight certified sections.

## 4.1 — Exponential Growth and Decay

Assertion source: [check_section_4_01.py](../chapter-04/code/check_section_4_01.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 recurrence to three-period formula | Forward values at n=0,1,2,3 and inverse grid | Induction/repeated-substitution proof needs manual review |
| E2 200 at 10% for four periods | Related 100-at-10% cases only | Exact 292.82 exercise input not asserted |
| E3 1000 declining 10% twice | Related 500 declining 20% three times | Exact 810 and 19% exercise results not asserted |
| E4 linear vs exponential at 5%, n=3 | linear_value(100,10,2)=120 and growth 121 | Exercise pair 115 vs 115.7625 not asserted |
| E5 100 to 121 in two periods | Exact inferred rate 1/10 | Positive-factor uniqueness reasoning manual |
| E6 irrational doubling factor | Doubling over two periods classified not_rational | Irrationality explanation manual |
| E7 monthly/year units | No unit-aware assertion | Manual specification/example review |

Worked annual-growth and decay examples have exact Fraction checks: 9261/8 and 256, and cumulative changes 1261/8000 and -61/125. Zero principal, zero periods, growth/decay/zero-rate inverse cases and type/domain rejections are asserted. Monotonicity across arbitrary horizons and financial model limitations are not proved by that grid.

## 4.2 — Natural Exponential and Logarithm

Assertion source: [check_section_4_02.py](../chapter-04/code/check_section_4_02.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 exponential invertibility and domain | Growth and rate-conversion round trips | Strict monotonicity/range proof manual |
| E2 derive time inversion | Doubling at .06, halving at -.06, unchanged target | Derivation/domain reasoning manual |
| E3 doubling in ten years | Related doubling-time and rate examples | ln(2)/10 exercise value not directly asserted |
| E4 PV of 500 after four years at .03 | PV of 1000 after three years at .05 | Exact exercise inputs not asserted |
| E5 continuous ln(1.05) to 5% effective | effective_rate(log1p(.05)) close to .05 | Identity proof manual |
| E6 invalid ln(0), ln(-2) | Selected invalid inverse inputs | No paired explicit zero/negative logarithm-domain demonstration |
| E7 zero-rate inversion | Unequal-target zero-rate rejection | Equal-target zero-rate nonuniqueness not directly asserted here |

Worked doubling, continuous-rate and PV examples have matching checks. Forward/PV round trips cover negative/positive rates and zero time; conversion round trips include 1e-12. Continuous-limit and exponential-law explanations, contractual conventions and precision limitations require manual review.

## 4.3 — Logarithm Rules and Their Domains

Assertion source: [check_section_4_03.py](../chapter-04/code/check_section_4_03.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 ln4+ln5-ln2 | Product(4,5), quotient(20,2) spot checks | Combined expression not explicitly asserted |
| E2 power/quotient proof | Power(5,3), quotient spot checks | General proof and negative exponent branch manual |
| E3 domain ln(x-5) | Positive-input validation only | Shifted boundary x=5 not represented |
| E4 domain log rational expression | No sign-chart assertion | Both x<-2 and x>5 branches and poles need review |
| E5 ln(x²) domain-preserving rewrite | No negative-x comparison | Counterexample and absolute-value identity untested |
| E6 prices 100,110,105 | Cumulative log log(1.05) and simple .05 | Written telescoping explanation manual |
| E7 invalid logarithm-of-sum expansion | Explicit log(2+3) differs from log2+log3 | General nonidentity explanation manual |
| E8 tiny return conversion | 1e-12 log/simple checks | Absolute tolerance 1e-12 is comparable to signal; does not establish relative accuracy |

Worked factor, price-change and telescoping examples have numerical assertions. Multiple paths are compared with endpoint log_return, which is another implementation routine rather than a wholly independent oracle. The stable log1p discussion does not establish recovery of precision lost before input conversion.

## 4.4 — Discrete and Continuous Compounding

Assertion source: [check_section_4_04.py](../chapter-04/code/check_section_4_04.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 quarterly EAR derivation | Quarterly FV at nominal .12; EAR monthly | General derivation/manual review |
| E2 .08 semiannual over three years | Other semiannual case at .12 for one year | (1.04)^6 not directly asserted |
| E3 .10 annual vs monthly | Frequency examples use .12 | Exercise comparison not directly asserted |
| E4 .05 EAR to continuous | Conversion round-trip grid includes .05 | No independent direct ln(1.05) assertion for this input |
| E5 .10 EAR equivalence over two years | Both PV routines yield 1000 for 1210 | Accumulation identity derivation manual |
| E6 completed-period integer convention | Fractional count and bool rejected | Financial posting interpretation manual |
| E7 omitted real-world features | No suitability assertion | Manual assumptions review |
| E8 nominal quotation needs frequency | Annual/semiannual/quarterly/monthly .12 FV values | Interpretation and general frequency ordering manual |

Frequency table values, monthly EAR and worked equivalent PV have numerical spot checks. Conversion grid covers five frequencies and five EARs; round trips can share implementation errors. Continuous-limit convergence is not tested as a sequence. Absolute tolerance 1e-11 exceeds the 1e-12 tiny-rate signal.

## 4.5 — Solving for Time and Growth Rate

Assertion source: [check_section_4_05.py](../chapter-04/code/check_section_4_05.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 derive real period count | Inverse grid reconstructs n | General derivation/manual review |
| E2 doubling at .05; first whole n=15 | Direct real-time formula and integer result | Explicit adjacent inequality checks not in test oracle |
| E3 200 to 242 over two periods | Direct rate close to .1 | Written derivation manual |
| E4 continuous 100 to 150 in five years | Direct ln(1.5)/5 and time inverse | Derivation manual |
| E5 declining target at positive rate | periods_to_target(100,80,.05) rejects | Reachability proof manual |
| E6 zero rate, unchanged target | periods_to_target(100,100,0) rejects | Rejection does not describe the full solution set |
| E7 monthly nominal and EAR | Nominal .12 checked at exact generated endpoint | EAR result not directly asserted in this script |
| E8 crossing vs equality | 100 to 115 at .1 returns period 2 | No assertion of non-equality or prior-period minimality |

Worked doubling and continuous inversion match test inputs. Monthly example uses an endpoint generated by 1.01**12 rather than the manuscript's rounded decimal observation. The rate grid (-.4,-.1,.01,.1) is not a near-zero-rate grid; manuscript coverage wording was narrowed accordingly. Negative-rate, zero-time/rate and invalid-input cases are sampled, not exhaustive.

## 4.6 — Products and Additive Log Changes

Assertion source: [check_section_4_06.py](../chapter-04/code/check_section_4_06.py).

| Exercise | Existing evidence | Gap / review |
|---|---|---|
| E1 three-factor cumulative formula | Three-return known value .1286 | General derivation/manual review |
| E2 +10%,-5%,+8% | Simple .1286 and log(1.1286) | Numerical spot check present |
| E3 telescoping | Price path 100,110,105 gives log(1.05) | General proof manual |
| E4 loss/recovery asymmetry | (-.2,.2) gives -.04; (-.2,.25) gives zero | Written financial explanation manual |
| E5 -100% log domain | -1 and -1.2 rejected | Domain reasoning manual |
| E6 portfolio vs weighted logs | Simple .05; log1p(.05); explicit weighted-log inequality | Broader weight/input cases and derivation manual |
| E7 deposit-only balance increase | No external-flow example asserted | Manual performance/cash-flow distinction |
| E8 stable tiny changes | log1p(1e-12) comparison and two tiny returns | Same primitive reused; abs_tol=1e-11 exceeds signal, naive expected formula can lose precision |

Main worked return, loss/recovery and portfolio examples match assertions. Empty-return sequences, nonpositive price and portfolio weight/length/domain cases are sampled. No input validator can establish that the supplied price path has been correctly adjusted for external flows.

## Additional coverage gaps

| ID | Finding | Proposed evidence |
|---|---|---|
| COV-08 | Some exact numbered-exercise inputs absent | Add independently computed expected values where useful |
| COV-09 | General domains/identities represented only by numerical samples | Named manual derivation/domain review, including sign charts |
| COV-10 | Tiny-signal absolute tolerances can admit zero or large relative errors | Design scale-aware checks with independent high-precision references |
| COV-11 | Threshold results do not independently assert minimality | Check preceding/current growth inequalities with an independent oracle |
| COV-12 | Rate/time units and external-flow interpretation unverified | Manual scenario review with explicit conventions |
| COV-13 | Near-zero inversion accuracy not demonstrated by Section 4.5 grid | Add justified near-zero input grid and oracle |

These extend COV-01–COV-07 from the first mapping slice. They are coverage findings, not demonstrated implementation defects. No new test execution or independent reviewer sign-off occurred in this mapping pass.

The six manuscripts now link their scoped historical runtime evidence and this map. Mathematical/editorial review and canonical approval remain pending. Next: Sections 4.9–4.10 project/assessment coverage and cross-section evidence.
