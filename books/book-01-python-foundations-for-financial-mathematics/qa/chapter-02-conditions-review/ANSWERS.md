# Chapter 2 Exercises 1–13 — review and supplemental answers

Reviewed 2026-10-29 at `e0f9cfdd30ce42f576fee3760fc86254be2bbdb7`. Supplemental implementations are in [review.py](review.py); actual checks are in [results.json](results.json). No student submission or independent human/model acceptance is certified.

## 2.13.1 — Target Test

balance >= target gives False at 87,500 versus 100,000. Equality belongs to target reached. Boundary checks include immediately below, equal and above.

## 2.13.2 — Cash-flow signs

The published -2500 is negative: positive=False, negative=True, zero=False. Supplemental zero and positive cases preserve mutually exclusive classifications; known zero is not missing.

## 2.13.3 — Discount-rate domain

0 <= discount_rate <= .25 gives True at .08 and both endpoints; rejects values just outside. This interval is exercise-defined, not a universal discount-rate bound.

## 2.13.4 — Compound condition

investment > 0 and expected_return > 0 and years >= 5 gives True for 50000, .07, 8. Each failed conjunct was independently exercised.

## 2.13.5 — Missing versus zero

Use cash_flow is None. Decimal zero is falsy but is an observed zero, so if not cash_flow cannot distinguish missing from zero. Presence and truthiness were probed independently.

## 2.13.6 — Stable growth

discount_rate > growth_rate gives True for .09 > .03; equality .03 == .03 and .02 < .03 both fail. The companion only explicitly evaluated the first case; this supplement supplies the requested equality/lower cases. The selected formula requires strict inequality, not merely positive rates.

## 2.13.7 — Loan amount

Logical rule: loan_amount >= Decimal("1000") and loan_amount <= Decimal("500000"). Chained equivalent: Decimal("1000") <= loan_amount <= Decimal("500000"). Both accept 250000 and both endpoints and reject 999.99/500000.01. The companion supplied only the chained form.

## 2.13.8 — Short-circuit guard

Check presence, then isinstance(value, Decimal), then value.is_finite(). None/string/float/bool never receive a Decimal-only method call. Decimal NaN, signaling NaN and Infinity fail the finite check. Checking None alone does not protect arbitrary external types. This guard checks representation/finiteness, not rate domain.

## 2.13.9 — Return classification

The if/elif/else source classifies .06 positive, 0 zero and -.01 negative. These examples assume finite validated Decimals; the snippet is not a complete parser/domain validator.

## 2.13.10 — Liquidity classification

Use if ratio < .5, elif ratio < 1, else high. .5 is Moderate and 1 is High; .75 is Moderate. Thresholds are educational. Negative/nonfinite ratios require a separate input contract; these fixtures test the stated finite boundaries.

## 2.13.11 — Target classification

The supplemental target_classification implements Below target for balance < target, Exactly at target for equality, otherwise Above target. 102500 versus 100000 is Above target. The companion gives the published result but no implementation; all three finite branches are checked here.

## 2.13.12 — Investment screen

The supplemental screen implements investment > 0 and expected_return > 0 and years >= 5. A boundary horizon of 5 passes; zero principal/return and horizon 4 fail. Programmed rules omit liquidity needs, risk capacity, liabilities, taxes, uncertainty and suitability assessment; passing is not a recommendation. The companion explanation is retained and its requested implementation supplied here.

## 2.13.13 — Contribution rule

The supplemental contribution_rule returns Contribution required when balance < target and Target already funded for equality or above. Actual planning also needs liquidity, income, liabilities, taxes, risk, horizon, contribution limits and other goals. This is an educational rule, not an advice engine. The companion narrative is supplemented by code and all three boundary fixtures.

