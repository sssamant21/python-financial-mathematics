# Chapter 2 Exercises 14–32 — reviewed answers

Reviewed 2026-10-29 at `9f792d034343fc946783af2036c2006a44e49235`. Function argument numbers below denote Decimal strings in actual execution. [reference.py](reference.py) contains supplemental teaching implementations; [review.py](review.py) executes them and the two original companion fragments.

## 2.13.14 — Annual contributions

annual_schedule(10000, 0, 2500, 5), using Decimal inputs, gives ending balances 12500, 15000, 17500, 20000, 22500. print_schedule labels and prints every year; exact expected stdout is checked. No return is assumed.

## 2.13.15 — Compound investment

annual_schedule(10000, .05, 0, 10) uses a for loop over years 1–10 and retains each balance. print_schedule prints each year and its two-decimal display; all ten internal balances are independently compared to 10000*(21/20)^n. The original companion loop is executed with documented balance/rate prerequisites; it did not itself include the requested printing.

## 2.13.16 — Contributions and return

End-of-year update: balance=balance*(1+rate)+contribution. Beginning-of-year update: balance=(balance+contribution)*(1+rate). Over five years from 10000 at 5% with contributions 2000, ending displays are 23814.08 and 24366.64. Beginning contributions receive one extra period of return. All five end-of-year balances and the beginning terminal value are independently checked. The exact original two-line end-of-year fragment is also executed once.

## 2.13.17 — Savings target

crossing_while(20000,0,5000,50000,20) first reaches 50000 in year 6. It checks period 0 before any update, increments years after updating, and stops at the first crossing or horizon. A target already funded reports year 0; a six-year horizon includes the crossing, while five years reports not reached. Raw balance is retained.

## 2.13.18 — Compound target

crossing_while(25000,.05,0,75000,30) first reaches the target in year 23; default-28-digit recurrence yields 76788.09389794523393896448224. The year-22 value remains below target. Exact Fraction closed-form balances establish the first crossing independently, and the published internal/display claims pass. Initial target attainment and failure within 22 years are checked.

## 2.13.19 — Bounded while

A loop without a horizon can stagnate at a zero balance, remain unchanged at a zero rate, or move away from a positive target at a negative return. Even positive growth does not imply attainment within the required horizon. Tests use finite horizons for zero principal, zero rate and -10% return; none reaches the selected target. Distinguish a financial horizon from an execution safety cap. No unbounded illustrative loop is executed.

## 2.13.20 — Cash-flow total

The arithmetic sum -10000+3000+3500+4000 is 500. It ignores cash-flow dates, discounting and rate conventions, so it is not a present value or an investment-return calculation.

## 2.13.21 — Sign counts

For the preceding cash-flow list, positive=3, negative=1, zero=0, total observations=4. A supplemental [-1,0,1] fixture confirms zero remains an observed classification. Counts reconcile to observation count, not monetary sum.

## 2.13.22 — Discounted cash flows

discounted_cashflows enumerates annual cash flows from period 1, uses effective annual 8% and retains each CF/(1+r)^period before summing. All three published Decimal values and their total 15330.48823858151704516587918 agree under the 28-digit context; the total displays 15330.49. Exact rational checks independently verify the three values and total within the stated bound. Matching annual periods and effective annual rate is required; period 0 would represent a different timing assumption.

## 2.13.23 — Year range

range(1,16) includes years 1–15; range(1,15) stops at 14 because the stop is exclusive. Tests verify both the inclusive intended sequence and the missing endpoint in the counterexample.

## 2.13.24 — Initial period

The executable review prints Period 0: initial state separately, then periods 1–10 as future states. The initial balance is measured before future updates; treating it as an extra future transition introduces an off-by-one financial period.

## 2.13.25 — Quarter ordinals

quarters(5) emits 20 entries, with ordinal periods 1–20. The numbers identify model periods rather than actual calendar dates; business calendars/day counts are not inferred.

## 2.13.26 — Scenario projections

scenario_projection loops through 3%, 5%, 7%; each call to annual_schedule initializes balance=10000 independently and records five years. First-year and terminal values match independent Fraction powers. Scenario balances must not carry from one assumed return into the next.

## 2.13.27 — Year and quarter

quarters(3) uses nested year 1–3 and quarter 1–4 loops with period=(year-1)*4+quarter. All 12 labels/periods are checked; the last is (3,4,12). These remain ordinal periods.

## 2.13.28 — State-reset defect

Initializing balance outside the outer scenario loop and reusing its mutated value contaminates later scenarios. The corrected scenario_projection resets through each annual_schedule call. Reverse-order tests yield identical values per rate; a deliberate shared-state counterexample produces a different terminal value. This counterexample is educational, not a manuscript runtime failure.

## 2.13.29 — First crossing with break

crossing_break(20000,.06,50000,30) checks period 0, updates one year at a time, and breaks at year 16; internal balance 50807.03369371342399599899208 displays 50807.03. Published claims and exact Fraction first-crossing benchmark pass. Tests also cover target already attained, horizons 15/16, and zero horizon.

## 2.13.30 — Missing observations

process_missing uses continue only after incrementing missing. The supplied list yields processed=3, missing=2 and sum=6000; processed+missing=5. An explicit zero is processed, not missing. Other invalid types/nonfinite cash flows require separate validation and are not silently treated as missing.

## 2.13.31 — Invalid scenarios

reject_scenarios validates representation, then finiteness, then supported r>-1. The supplied .05, NaN, -1.10, .08 list yields accepted .05/.08 and two rejection reasons (nonfinite and domain). continue preserves one disposition per observation; accepted+rejected equals supplied count. External strings/None are rejected by representation before Decimal methods run.

## 2.13.32 — Loop else

search_loop_else uses a 25-year for search, break on first crossing, and else only after normal exhaustion. Tests verify success at year 16, failure with zero growth, period 0, and success exactly at year 25. Period 0 is handled before the search; else is not a per-iteration branch and does not execute after break.

