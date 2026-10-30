# Section 6.9 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling files; aligned strictly increasing int64 periods and finite positive float64 prices. Caller establishes a consistently adjusted single asset, currency/unit, complete source history and abstract period origin/unit. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.9-E1

Add a final price of 100 at offset 5 and derive the final linked return from the original starting price.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Append price 100 at offset5. Intervals are (0,1),(1,3),(3,4),(4,5); the final linked gross telescopes to 100/100=1, so the final linked price-only return is 0. The last interval alone is 100/108.9−1=−89/1089, about −8.17%, not zero. The runner checks that ratio and final linked growth within absolute tolerance 1e−14 for this small fixture; binary64 108.9 is approximate. No initial interval or return is fabricated.

## 6.9-E2

Demonstrate a +20% followed by -20% path; explain why it does not finish unchanged.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Use prices [100,120,96] at offsets [0,1,2]. The gross factors are 6/5 and4/5; their product is24/25=0.96, so linked return is−1/25=−4%. The two simple returns +20% and−20% sum to zero, but the loss applies to the larger second-period starting value120. Absolute comparisons at1e−15 verify the small controlled path; adding simple interval returns is not the linked return.

## 6.9-E3

Add a test proving no artificial initial return is inserted.

**EXACT SOURCE N-MINUS-ONE/LABEL PROBES**. For N=4 prices, every returned array, including start/end labels, has shape(3,). The intervals are exactly (0,1),(1,3),(3,4), and the first simple return is the actual approximately0.10 rather than a synthetic leading0. A separate two-observation path at offsets4,9 yields exactly one labelled interval(4,9). A genuine constant-price interval may have a computed zero; that is distinct from inserting an extra observation.

## 6.9-E4

Design terminal-zero support while rejecting any subsequent division by zero.

**TERMINAL-EVENT DESIGN + ORIGINAL API REJECTION**. Keep return_path strictly positive. A separate terminal-event API could allow a single zero only as the final observation after a strictly positive prefix, require an explicit terminal/delisting/default event and price interpretation, and return last gross0, simple−1 and linked growth0. Reject any zero denominator, intermediate zero, subsequent price resurrection or continuation; do not silently divide by zero or replace the event with a tiny price. Define treatment of recovery/distributions separately and preserve interval labels and terminal status. The runner evaluates only the rational terminal equation and verifies the unchanged source rejects both [100,0] and [100,0,10]. New terminal support and its full schema/tests are not implemented.

## 6.9-E5

Propose a missing-middle-observation policy with explicit interval labels.

**MISSING-OBSERVATION DESIGN + CONTROLLED BRIDGE PROBE**. Default policy remains reject missing prices. If an explicitly approved endpoint-bridge analysis is required, retain the missing observation record/reason, create paired masks over periods/prices, flag the bridge as incomplete-observation history, and preserve the longer interval labels. For [100,missing,99,108.9] at offsets[0,1,3,4], controlled removal of only the marked missing observation produces intervals(0,3),(3,4), with the first endpoint ratio99/100. It does not recover an offset0-to1 return or imply the missing price was zero/unchanged. Source rejection of the NaN path and source calculation of the separately constructed bridge are retained. This controlled analysis explicitly relaxes observation completeness; general ingestion, approval workflow and metadata propagation remain designs.

## 6.9-E6

Explain the inputs needed to include a cash distribution in one interval without double counting adjusted prices.

**DISTRIBUTION DESIGN + SUPPLEMENTAL RATIONAL EXAMPLE**. For one interval require raw consistent same-currency per-unit prices, entitled distribution amount/unit, entitlement and payment timing, holding/ownership convention, splits/share-count changes, tax/fees and reinvestment assumptions. Under an explicit one-unit fixed holding and end-of-interval cash treatment without reinvestment, total return=(end_price+cash_distribution)/start_price−1. For start100,end95,cash10 this is5%, while source price-only return is−5%. Rational arithmetic and the unchanged price-only source illustrate the difference. If using a total-return-adjusted price/index already incorporating the distribution, do not add it again; inspect vendor adjustment methodology and maintain consistent adjustment basis. Split-only adjustment differs from total-return adjustment. A total-return API/data adapter is not implemented.

## 6.9-E7

Compare linked growth with the endpoint ratio on a longer deterministic path and document the comparison tolerance.

**EXACT SOURCE LONGER PATH + INDEPENDENT TELESCOPING ORACLE**. Use257 observations with price[i]=100+(17i mod31), i=0..256, at consecutive integer offsets. These exactly represented positive integer prices range100..130 and produce256 intervals. Derive each linked gross independently as Fraction(price[i],price[0]), rather than multiplying the tested ratios. Compare every source cumulative product against both these rational endpoint values converted to float and direct float endpoint division, with rtol=1e−12,atol=1e−14,NaNs disallowed. Actual maximum absolute error is 2.220446049250313e−16; the final exact growth is28/25=1.12. Labels are checked for all256 intervals. The tolerance is deliberately scoped to this moderate-magnitude, bounded-length deterministic fixture and is conservative relative to its observed rounding; it is not a universal error bound or financial materiality threshold. Extreme ratios, longer products, cancellation near zero returns and platform effects require their own policy and tests.

## 6.9-E8

Explain why three irregular interval returns do not establish an annual performance measure.

**TIMING/ANNUALIZATION DESIGN + EXACT SOURCE COMPARISON**. Three intervals with boundaries0,1,3,4 have durations1,2,1 abstract units. They do not establish calendar dates, a year fraction, observation frequency, or an annual horizon. Source returns remain unchanged when offsets are rescaled to0,10,30,40, with changed end labels10,30,40; it does no annualization. An annual measure requires a specified elapsed-time/year-fraction convention, positive linked growth and a declared formula/model, such as G^(1/T)−1 under a suitable geometric convention, together with price-only versus total-return and cash-flow/reinvestment assumptions. Do not take an unweighted mean of irregular returns or assume three observations mean a fixed fraction of a year. Annualization is a design explanation only, not an executed source capability.
