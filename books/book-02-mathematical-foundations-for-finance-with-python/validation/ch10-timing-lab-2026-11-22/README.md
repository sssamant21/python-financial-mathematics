# V262 — Section10.8 timing/limit/units/applied-lab crosswalk

Source pin: `d70076db68175154442acfeb934c721bd438d6ab`. [Runner](review.txt), [first](first.json), [replay](replay.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-timing-lab-2026-11-22/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-timing-lab-2026-11-22/review.txt replay
```

**152 predicates pass twice**,identical rows and external applied tables. Native CLI/compile execute each run:four command records. Source/dependency hashes,all outputs,1600-digit independent references and scope retained. No source numerical failure/change. V258–261 baseline failures,policy probes,observer/interim records and corrected18/39/27/79 predicates remain separate. This batch adds no answer/workflow counts.

| Predicates | Actual execution and independent checks |
|---|---|
|120 |Twelve applied rows:four frequencies n2,8,24,730 at rates.06,0,−.02,plus four global predicates per rate. Continuous/direct geometric references use independent1600-digit Taylor exponentials;nominal totals2400 and paymentsCT/n checked;all three PV/signed-difference fields and timing order checked. |
|30 |For rates.06 and−.02,begin/end relative errors show selected first-order doubling ratios≈2;midpoint shows second-order≈4 at n16,32,64,128,256. Signed leading coefficients at n256 agree with+.5,−.5,−1/24 within.001 relative;doubling ratios within.02. These grids are away from the observed float rounding floor,not a universal asymptotic/resource certificate. |
|2 |Exercise4 payment500 derived from1000*2/4;Exercise5 explicit source schedule at.5,1,1.5,2 years agrees with the source equal-payment formula. This is labelled cross-API integration,not the independent oracle. |

The native comparison report contains signed differences only. Absolute and signed/absolute relative differences required by the applied assessment are **external report assembly** in JSON,derived from actual native fields and the nonzero continuous reference. No new native relative-difference field is invented. At C1200,T2 all three required rates have nonzero continuous PV;zero denominators elsewhere require a separate policy. n730 is a uniform365-day-year approximation,not validated business-day/calendar conventions.

## Timing and limit derivations

For x=rT/n and a constant positive payment rate,the source timing factors have series:
`end=1−x/2+x²/12+O(x⁴)`, `begin=1+x/2+x²/12+O(x⁴)`, `mid=1−x²/24+O(x⁴)`.
They follow by expanding exponentials and dividing their convergent series near0;the midpoint factor x/(2sinh(x/2)) is even. This explains first-order begin/end and second-order midpoint relative bias,with signs normalized by x or x² in the actual checks. It is a local series argument,not a global fixed-n guarantee.

For fixed finite r,T,individual paymentCT/n shrinks as n grows,keeping totalCT;the timing factors tend to1 as x→0. More generally,continuous c(t)exp(−rt),or a Riemann-integrable bounded integrand,admits the stated Riemann-sum limit. Fixed-size payments instead increase total payments and are not that approximation. Positive C,T,r give begin>mid>end;negative r reverses the order for positive C. With negative C,inequalities reverse again. Convex exponential discounting makes midpoint underestimate the positive-stream integral for either nonzero rate. Actual contractual schedules are valued at actual dates;their difference from a continuous stream is a model difference,not automatically error.

Ratios of PVs require a **nonzero continuous PV**. At C0 or T0,both PVs may be0,so an observed0/0 quotient is undefined even if the analytic timing factor has a continuous extension. The manuscript qualification is clarified;native timing_ratio remains an analytic factor depending on r and T/n,not an instruction to divide zero PVs.

## All14 exercises and applied assessment

| Exercises | Disposition |
|---|---|
|1–3 |Discrete amounts are currency;continuous rates currency/year multiply years;flat rate1/year,times years. Exact sums/integrals and unit cancellation reviewed conceptually. No actual curve/day-count/source approval. |
|4–5 |500 per payment and explicit end times.5,1,1.5,2 checked as above. |
|6–8 |Source timing order at all required rates/resolutions and exact zero-rate total2400 verified;C,T sign assumptions explicit. |
|9–10 |Finite geometric sum q(1−q^n)/(1−q) and exact nonzero-PV ratio derived;zero-rate continuous extension separated from0/0. Prior range oracles retained. |
|11–12 |Signed small-step coefficients and selected observed first-/second-order errors checked;roundoff/extreme ranges retain declared limits. |
|13–14 |Shrinking payment versus fixed amount and actual contractual versus continuous model interpretations reviewed;no invented payment calendar or accepted economic substitution. |

Applied assessment now has all three rates,four frequencies,three timing PVs,continuous PV,nominal totals and externally assembled absolute/relative differences. All earlier support limits remain:equal/ratio4096-bit counts,schedule10000 rows,800/2000-digit contexts,growth/decay cutoffs,final-underflow0 and unresolved signed-cancellation rejection. No exhaustive resource/precision/financial model proof or independent acceptance.

**Checkpoint:** Selected10.8 source/report/proof/14-exercise/applied-lab crosswalk recorded. Next V263 full pinned runtime and unchanged executable-identity verification before10.9. All38 selected COV categories partial,none closed;not defect counts/percentages. Book2 IN PROGRESS;broader data/model/platform/reviewer/release/canonical gates open. Book1 separate.
