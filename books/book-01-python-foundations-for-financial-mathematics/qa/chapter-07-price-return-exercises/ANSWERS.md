# Section 7.15 — Worked answers

**7.15-E1. Reproduce +10%, −10% and the linked −1% by hand.**

From 100 to 110 the gross ratio is 11/10; from 110 to 99 it is 9/10. Subtract one for +10% and −10%; multiply gross ratios to get 99/100, or −1% linked. Adding the two simple returns incorrectly gives zero.

**7.15-E2. Explain why the first interval return is missing while the first cumulative baseline return is zero.**

There is no preceding supplied price at the first observation, so the interval fields are undefined. The cumulative baseline compares 100 with itself: 100/100 − 1 = 0. Subsequent returns are labeled by their ending observations and carry their actual starts and elapsed times.

**7.15-E3. Change the final price to 121 and compare direct endpoint and compounded results.**

With terminal price 121, both gross ratios are 11/10. Linking yields 121/100 − 1 = 21%, identical to the direct endpoint. Adding the two simple returns gives 20%.

**7.15-E4. Replace the middle price with NaN and contrast rejection, no filling, forward filling and dropping the row.**

The public transform rejects a missing middle price. Unfilled raw pct_change yields three missing values because each adjacent pair includes the missing observation. Forward filling creates prices 100, 100, 99 and fabricates a zero first interval, followed by −1%. Dropping the missing row instead gives one −1% interval spanning four days; the intervals and their meanings differ.

**7.15-E5. Verify that multiplying every price by a common positive scale leaves fixture returns unchanged.**

For k > 0, (k P_end)/(k P_start) = P_end/P_start in exact arithmetic. The fixture scaled by 10 preserves simple, gross, log and cumulative results within the stated tolerance; extreme rescalings can still hit float limits.

**7.15-E6. Explain why a constant-currency scale is different from changing FX rates across observations.**

With target currency units per local currency unit, the converted gross ratio equals the local price ratio times FX_end/FX_start. A flat 100 local price at FX 1, 1.1, 1.2 gives converted prices 100, 110, 120, with simple returns 10% and 1/11. A fixed FX scale cancels; varying FX needs aligned quotes and an explicit convention. The source has no FX API.

**7.15-E7. Describe a separate simple-return-only contract that allows a terminal zero price without claiming finite log returns.**

A simple-only API could allow a final zero after a strictly positive starting price for that interval, giving gross zero and simple −100%. Reject any zero denominator and omit log output; log(0) is not finite. Define zero provenance so a missing quote cannot masquerade as loss. The combined API rejects a terminal zero.

**7.15-E8. List source metadata needed before interpreting a price series as a total-return or adjusted-price series.**

Record instrument and field identity, currency and units, vendor and dataset version, observation convention, split and distribution adjustment policy, and whether, when and at what prices distributions are reinvested. Document gross/net tax treatment, methodology revisions and effective dates; an adjusted-price label alone does not establish total return.
