# Section18.4 — Simulating financial outcomes: scoped review

Reviewed 2026-11-08 by Codex, not an external independent reviewer. Baseline `24957071300057f05fe26ed816c9135f906d3640`; [source](../../chapter-18/18.04-simulating-financial-outcomes.md). One workflow, forty local answers, twelve lab steps. No new historical unique methods.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-outcomes-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-outcomes-review/review.py 24957071300057f05fe26ed816c9135f906d3640
```

The baseline command intentionally exits1; it requires the baseline git object. [Baseline](baseline.json) retains eleven failed supplemental predicates; [final results](results.json) retains three passing exact-source commands and75 passing supplemental predicates. The reference demo invokes ten existing unittest methods; import is silent and compilation passes. Commands, predicates, answers, workflow/step records and unique methods remain separate inventories. Python3.12.14/Linux, local random.Random/Mersenne Twister, source and listing SHA256 are in JSON.

## Finding F176 and observer correction

Original fee arithmetic loses integer identity with fee `10**18+1`; discounting by rate0 loses integer identity. A large terminal mean can obscure profit through cancellation (seed43's true sample profit.002 reported .001999999999995339). Unreportable mean profit can return infinity; a nonzero discounted subnormal can return zero. Huge finite-integer inputs leak OverflowError; malformed noniterable samples leak TypeError. Calculating SD before SE can overflow even when the required SE is finite.

The source now uses explicit displayed-decimal float and exact integer arithmetic for model/report quantities, enforces finite int/float inputs within finite float range (no booleans), normalizes invalid/unreportable cases to ValueError, preserves exact whole-number reports, calculates profit before rounding its mean, and calculates SE directly from rational variance/N with Decimal square root. Signed observations and cost/threshold remain permitted by summarize; it does not implement a simple-return API. True zero stays valid, while nonzero report underflow raises. Fees are terminal and paid once; they may make outcomes negative. Original ten methods remain unchanged and pass.

The first observer incorrectly expected rejection for two observations ±1.79e308: their sample SD is too large for float, **but SE is1.79e308 and reportable**. [Initial observer baseline](initial-observer-baseline.json) and [initial corrected-source run](initial-corrected-source.json) retain the mistaken predicate and corrected source's failed expectation. The observer was corrected to require the finite SE, then rerun on both original and final sources. Original source still fails by overflowing intermediate SD. Final counts75 and eleven baseline failures come from the final observer; the earlier71-predicate inventories are transitions, not additional methods/failures. This QA error is not counted as a manuscript defect or independent acceptance.

## Analytical expectations and execution boundaries

Exact-source execution consists of the complete verbatim reference fence, demo/tests, quiet import and compile, extracted to a fresh temporary module. All additional function calls and controlled boundary injections are supplemental probes. The injected fixed generator only supplies [0,nextafter(.25,0),.25,nextafter(.75,0),.75,nextafter(1,0)]; source mapping returns [80,80,100,100,120,120]. It does not test random quality, and the original generator class is restored even on failure.

Independent Fraction/Decimal derivations use probabilities[1/4,1/2,1/4] and values[80,100,120]. Probability sum1; E[V]=100; profit mean0; Var(V)=200; SD=sqrt200; SE at10000=sqrt(200/10000)=.1414213562…. Loss V<100 has probability1/4, whereas V≤100 has3/4. Loss indicator SE=sqrt((1/4)(3/4)/10000)=.004330127…. Rounded values14.1421,.14142,.00433 are explicitly checked. Sample[80,100,120,100,80] has mean96, profit−4, loss count2/5, unbiased variance280 and SE=sqrt56. Terminal fee2 gives[78,98,118], expected98 and strict loss probability3/4. Constant effective discount5% gives expected PV2000/21≈95.2381; the displayed rounding is checked.

For observed state counts kd,kf,ku, the supplemental reference calculates mean=(80kd+100kf+120ku)/N−fee, variance=sum(kj(vj−fee−mean)²)/(N−1), and SE=sqrt(variance/N); loss is counted after fee against100. The count reference replays **the same RNG**: independent summary algebra does not independently validate distribution or stream independence. Arithmetic comparisons use rtol1e-12,atol0; integer identity uses exact equality. These are numerical predicates, not statistical acceptance bands. No requirement for every larger sample to be closer and no rare-event/coverage certification.

## Twelve lab-step contracts

Prerequisite: Python standard library, save exact reference as financial_outcomes.py, preserve local generator/seed/count, distinguish fee timing and strict threshold. Model: fictional currency; cost100 at time0, one-year terminal values, simple returns, no taxes/costs except stated terminal fee. No external market data/date or calibrated real-world/risk-neutral measure; discount arithmetic is not a market-price claim.

| Step | Actual review/execution record |
|---|---|
| 1 | Cost100, one-year horizon, values80/100/120 and probabilities.25/.5/.25 recorded above and in JSON. |
| 2 | Exact rational sum equals1. |
| 3 | Independent expected terminal100 and profit0. |
| 4 | Strict-loss probability.25; nonpositive-profit probability.75 separately checked. |
| 5 | Independent variance200, theoretical SE.141421… and indicator SE.004330…; printed rounding checked. |
| 6 | Exact reference demo/tests run; N10000,seed42, Python/version/source hashes retained. |
| 7 | Seed42 counts[2481,5058,2461], mean99.96, SE.1406051812050259, loss.2481. Compared descriptively with100/.25; no deterministic statistical pass threshold. |
| 8 | Seed43 counts[2454,5091,2455], mean100.002, profit.002, SE.14013551796864218, loss.2454. Differences observed, not independence certification. |
| 9 | Fee2,seed42: same state counts, net mean97.96, profit−2.04, loss.7539; analytical targets98/.75. Paired source fee shift checked. |
| 10 | Source discount100 at.05 compared with independent2000/21; stated probabilities/constant discount rate only. |
| 11 | Ten original methods and invalid-input probes run; eleven original failures and corrected rerun retained. |
| 12 | Contract/units/timing/source/environment/results retained. Platform, statistical and model acceptance explicitly open. |

## Forty prompt-to-answer alignment records

All forty local prompts and answers were read in order. Conceptual reviews below are not counted as executed callable exports.

| Answer | Derivation, check or scoped limit |
|---|---|
| 1 | .25+.5+.25=1, exact rationals. |
| 2 | Down profit−20, direct subtraction. |
| 3 | Flat profit0, direct subtraction. |
| 4 | Up profit20, direct subtraction. |
| 5 | Down return−20/100=−.2. |
| 6 | Up return20/100=.2. |
| 7 | Expected terminal100, independent weighted sum. |
| 8 | Expected profit0, expected terminal minus cost. |
| 9 | V<100 probability.25, strict state selection. |
| 10 | V≤100 probability.75, different inequality. |
| 11 | Known sample mean96, source compared with exact sum/5. |
| 12 | Known sample profit−4, source compared. |
| 13 | Known sample loss.4, source count/frequency. |
| 14 | Population variance200, weighted squared deviations. |
| 15 | SDsqrt200≈14.1421, Decimal root and rounding. |
| 16 | SE at10000≈.14142, independent sqrt variance/N. |
| 17 | Loss indicator SE≈.00433, independent Bernoulli formula. |
| 18 | Fourfold N halves theoretical SE under IID/same variance; algebraic factor checked. |
| 19 | Seed helps compatible replay; source list equality checked. |
| 20 | More paths do not fix wrong model: correct conceptual distinction. |
| 21 | 5% PV≈95.2381, source versus2000/21. |
| 22 | Fee down value78, controlled source mapping. |
| 23 | Fee flat value98, controlled source mapping. |
| 24 | Fee up value118, controlled source mapping. |
| 25 | Expected net98, exact weighted fee outcomes. |
| 26 | Strict net loss versus100 probability.75, exact state selection. |
| 27 | Fee timing prevents applying twice: correct design requirement; no time-zero-fee API claimed. |
| 28 | U=.25 maps flat, actual source under injection. |
| 29 | U=.75 maps up, actual source under injection. |
| 30 | Negative probability invalid: correct probability axiom; source fixes probabilities, has no general probability validator. |
| 31 | Exclusive/exhaustive model probabilities sum1: correct finite-model requirement. |
| 32 | Real-world not automatically risk-neutral: correct measure distinction; no calibration executed. |
| 33 | Deterministic stress need not have probability: correct scenario distinction. |
| 34 | Zero observed events do not prove zero probability: correct statistical limit; no rare-event interval implementation claimed. |
| 35 | Simple return undefined at zero cost: correct denominator condition; summarize can still use zero threshold because it computes profit, not return. |
| 36 | Terminal value differs from profit after cost conventions: source report separates the two. |
| 37 | Real outcome may fall outside finite model: correct model limit. |
| 38 | Agreement with100 supports a basic estimator check, not model validation: correct evidence interpretation. |
| 39 | Generator/version/inputs/draw order also matter: local state and metadata retained; no cross-version guarantee. |
| 40 | Output guarantees no future outcome: correct simulation interpretation. |

## Remaining scope / resume

Next: **Section18.5 — Return Simulations**. Chapter18 now has four scoped workflows and160 local answers, not full chapter acceptance. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, rare-event/statistical/model checks, broader branch/input coverage, editorial/copyright and external independent acceptance remain open. No production/external messaging actions.
