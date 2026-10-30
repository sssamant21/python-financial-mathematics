# Section 6.10 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; exact float64 bounded nonempty vectors and unique tuple IDs. Caller establishes opening valuation time, complete comparable same-currency values, common return interval/convention, no trades/flows/fees/distributions/FX and long-only assumptions. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.10-E1

Change opening values to [500,400,100] and derive weights and the portfolio result for the same returns.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Values [500,400,100] sum to 1000, so opening weights are [1/2,2/5,1/10]. With returns [1/10,−1/20,0], contributions are [1/20,−1/50,0] and portfolio return is 3/100=3%. Ending values are 550,380,100, totaling 1030. Source weights/contributions/scalar match the rational expectations with absolute tolerance 1e−14, rtol=0 and NaNs disallowed; this is a small-fixture comparison policy.

## 6.10-E2

Give cash a supplied interval return of 0.002 and derive its contribution.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Keep original opening cash weight 1/10 and supply cash interval return 0.002=1/500. Its contribution is 1/5000=0.0002, or 0.02 percentage points of portfolio return. Add to original 0.045 to obtain 0.0452=113/2500, or 4.52%. This is a supplied common-interval cash-return assumption; no cash-rate/accrual model or annualization is inferred.

## 6.10-E3

Reorder both IDs and values consistently; show that aligned contributions reorder while the scalar result remains the same within tolerance.

**EXACT SOURCE PERMUTATION/IDENTITY PROBES**. Apply permutation [2,0,1] to IDs, values and returns: IDs (CASH,A,B), values [100,600,300], returns [0,0.1,−0.05]. Source produces weights [0.1,0.6,0.3], contributions [0,0.06,−0.015] and the same approximately 0.045 scalar within 1e−14 absolute tolerance. The runner separately confirms IDs-only mismatch is rejected. A matching ID tuple incorrectly attached to numbers remains an ingestion risk; shape/identity checks cannot establish provenance.

## 6.10-E4

Add a test for a unique instrument with zero opening value and an invalid supplied return.

**EXACT SOURCE ZERO-VALUE/INVALID-RETURN PROBES**. Append unique ID ZERO-D with opening value 0, producing a valid zero weight. Independently supply NaN, positive infinity and −1.01 for its return. The unchanged contributions API raises ValueError for every case despite zero exposure, and each rejected input remains byte-identical. Complete finite supported returns remain a whole-input requirement; do not replace missing data with zero merely because the current weight is zero.

## 6.10-E5

Derive closing weights for the example and show why substituting them for opening weights answers another question.

**EXACT SOURCE + INDEPENDENT RATIONAL CLOSING-WEIGHT ORACLE**. Original ending values are [660,285,100], total 1045. Closing weights are [132/209,57/209,20/209]. Supplying those with the original return vector computes 207/4180≈0.04952153 (4.952153%), versus the valid original interval result 9/200=0.045. Source correctly evaluates the supplied hypothetical; it cannot establish the weight valuation time. Closing weights already reflect the interval price changes, so substituting them answers a different weighted-average question and can introduce hindsight. They can serve as opening weights for a subsequent interval only under an explicitly defined holdings/cash-flow convention.

## 6.10-E6

Explain how excluding cash changes the denominator and report interpretation.

**EXACT SOURCE SUBSET DENOMINATOR + CONCEPTUAL REVIEW**. Removing cash leaves invested values [600,300] and denominator 900, so weights are [2/3,1/3]. Their weighted return is (2/3)(0.1)+(1/3)(−0.05)=0.05, or 5% of the invested subset. The full-portfolio gain is still 45 over 1000, or 4.5%, under zero cash return. Both arithmetic results can be valid under different stated denominators; label the subset and retain cash/account components rather than claiming that 5% describes the original whole portfolio.

## 6.10-E7

Specify the extra cash, liabilities, and financing rules needed for a signed-weight model.

**SIGNED-MODEL DESIGN + ORIGINAL LONG-ONLY REJECTION**. A signed-weight model must define equity/NAV versus net/gross exposure, explicit cash and borrowings, short-sale proceeds/collateral and rehypothecation, liabilities and mark conventions, borrowing/financing rates, stock-borrow costs, distributions owed, leverage/margin limits, zero/tiny/negative NAV handling, instrument types and horizon/currency/FX policy. Do not take absolute values or reuse a long-only positive denominator silently. A separate rational example long 120/short −20 has net exposure 100 and gross exposure 140; dividing by 100 gives signed weights 1.2 and −0.2, gross weight 1.4. That example is not a complete financed account. The runner confirms original weights_from_values rejects [120,−20]; a signed API and financing/accounting implementation remain designs only.

## 6.10-E8

Design a multi-interval holding/rebalancing contract before attempting to reuse this one-interval function.

**MULTI-INTERVAL DESIGN + CONTROLLED ONE-INTERVAL CALLS**. Define observation/valuation times, price/total-return conventions, holdings and cash ledger, external cash-flow timing, drift, target weights, rebalance decision/execution timing, transaction costs/fees/taxes/financing, currency treatment and portfolio return/linking rule. Weights for each interval must use information available at its start. Retain inputs and trade/cash records; never infer that reuse of fixed weights means unchanged holdings. With two assets opening at values [50,50] and returns [+10%,−10%] in each of two intervals, first total remains 100 and closing weights drift to [0.55,0.45]. Fixed holdings then earn 1% in interval two and end at 101; rebalancing to [0.5,0.5] between intervals with explicitly zero costs/external flows ends at 100. The runner checks separate source contributions calls and independent rational ending values. This is a controlled illustration, not a multi-interval holdings/rebalancing engine, performance attribution, or transaction implementation.
