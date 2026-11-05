# Chapter 8 — Twenty worked-answer reviews

**8.14-P1 — Same endpoint, different paths**

Both finish at index 120 and return 20%. At the middle observation A is 110 while B is 80. Equal endpoint growth does not imply equal interim experience.

QA review: Independent indexed matrix [[100,100],[110,80],[120,120]] matches source.

**8.14-P2 — Figure, Axes, Axis, and Artist**

The axes array has shape (2, 1). axes[0, 0] belongs to fig; its yaxis belongs to that Axes; the returned Line2D is the first element of its lines collection.

QA review: Ownership verified on exact Figure/Axes/Axis/Line objects; supplemental QA export labels the figure.

**8.14-P3 — Coordinate order and elapsed spacing**

The numeric gaps are 1 and 3 days. The alternative order is not strictly increasing. A line follows supplied order; it does not sort observations for the author. Equal category spacing would conceal the longer interval.

QA review: Artist x spacings are 1 and 3; unsorted [0,4,1] reverses the last segment.

**8.14-P4 — A missing point and a dropped point**

Retaining NaN preserves a break. Dropping the missing point leaves coordinates [0, 1, 3], which permits a direct connection from day 1 to day 3. Neither operation supplies evidence about the missing value.

QA review: Supplemental QA legend distinguishes the retained-gap line from the dropped-row connection; no value is imputed.

**8.14-P5 — Effective position states**

The held states are 10 and 12. Initial vertices are (0, 10), (1, 10), (1, 12). At day 3 the state becomes 8; the fixture supplies no later end date. Straight interpolation would invent gradual position changes.

QA review: First three path vertices and persistence intervals verified. No state after the last supplied update is modeled.

**8.14-P6 — Repeated local clock hours**

The labels are 01:30 EDT -0400 and 01:30 EST -0500, one elapsed hour apart. UTC coordinates distinguish the instants; local clock text alone does not.

QA review: UTC elapsed time is independently one hour. The repeated local clock labels retain offsets.

**8.14-P7 — Expected rows and expected cells**

Source-row presence is [True, False, True]. Observed counts by date are [2, 0, 1], or 3 of 6 expected cells. The January 3 row exists even though one of its cells is missing.

QA review: Presence and observed-cell counts differ as required: three observed cells across six expected slots.

**8.14-P8 — Simple, log, and compounded returns**

Simple returns are +10% and −10%; their sum is zero. Compounding gives 1.1 × 0.9 − 1 = −1%. Summed log returns recover the same −1% through expm1. An arithmetic sum of simple returns is not the compounded result.

QA review: Ratios 11/10 and 9/10 give zero simple-return sum but linked −1%; log reconstruction agrees.

**8.14-P9 — Strict linkage and an observed zero**

Adjacent returns are undefined at the first point, then +10%, −10%, unknown, unknown, and 0%. Strict linkage becomes unknown at the gap and stays unknown. The separately calculated endpoint ratio is +8%; it does not reconstruct the missing intervals.

QA review: Full strict path [0,.1,−.01,NaN,NaN,NaN] verified; endpoint-only +8% is distinct.

**8.14-P10 — Histogram edges and exact zeros**

Counts are [2, 2, 3, 4]. Binning the edges gives [1, 1, 1, 2]. Bins include their left edge and exclude their right edge except the last, which includes both. Exact zero belongs to the bin starting at zero.

QA review: Integer scalar assignment yields [2,2,3,4]; the separate edge sample is [1,1,1,2].

**8.14-P11 — Density area and unit changes**

Shares are counts/11 and sum to one. Density is share/width; its area sums to one although heights need not sum to one and may exceed one. Multiplying widths by 100 requires dividing density heights by 100, preserving every bin area.

QA review: Densities are [25/11,100/11,150/11,50/11] per unit decimal return; dividing by100 changes to per-percentage-point units.

**8.14-P12 — Scatter alignment by interval label**

Retained dates are January 1, 3, and 4: (.01, .015), (0, 0), and (−.01, −.02). Coverage is 3/4 expected pairs. Independent dropna calls followed by positional pairing would not establish label alignment.

QA review: Manual label map yields Jan1 (.01,.015), Jan3 (0,0), Jan4 (−.01,−.02).

**8.14-P13 — Correlation, slope, and equality**

Correlation is +1, but the line has slope 2 and intercept .01 rather than the equality reference slope 1 and intercept 0. A constant coordinate has zero centered sum of squares, so the correlation denominator is zero; report the statistic as unavailable.

QA review: The specified affine output is [−.03,.01,.03,.07]. Correlation+1 does not make slope1 or intercept0; constant-input denominator is zero.

**8.14-P14 — Signed weights and absolute composition**

Net value is 1,000 and total absolute value 1,400. Signed weights are [.6, .4, −.2, .2]; absolute shares are [3/7, 2/7, 1/7, 1/7]. Both sums equal one for different reasons. Risky gross exposure is 1,200/1,000 = 120%, excluding cash. These are exposure measures, not risk contributions.

QA review: All four signed and absolute components and the cash-excluded risky numerator are reconciled independently.

**8.14-P15 — Payoff, profit, and contract scaling**

Call profits are [−600, −600, −600, 0, 1,400]; put profits are [9,600, 0, −400, −400, −400]. Break-even prices are 106 and 96. Call payoff minus put payoff equals 100(S − 100). This terminal identity is not a claim about current option prices.

QA review: Call payoffs [0,0,0,600,2000] and put payoffs [10000,400,0,0,0] are explicitly reconciled; subtract600/400 for profits.

**8.14-P16 — Equal numeric rates and equivalent rates**

Using the same numeric nominal 5% with monthly compounding produces a larger balance than annual 5%. Equivalent nominal annual rate is 12[(1.05)^(1/12) − 1]; equivalent continuous rate is log(1.05). Applying these equivalent rates reproduces 1,000(1.05)^20 within floating-point tolerance.

QA review: Independent 60-digit Decimal nominal/continuous equivalents and endpoint balances retained in results; no universal accuracy claim.

**8.14-P17 — Scenario orientation and a reference case**

The grid shape is (5, 4); cell [2, 1] equals 1,000(1.05)^10. The joint case exceeds the reference by approximately 623.30 currency units. Both inputs change, so this difference is not a one-factor sensitivity. Scenario cells do not supply probabilities.

QA review: All twenty rate/horizon cells checked against independent rational powers, not just the interior reference.

**8.14-P18 — Zero, omission, units, and sign cues**

The order is D, A, C, B; E is explicitly omitted, leaving coverage 4/5. C remains an observed zero-width bar, not missing data. PercentFormatter(xmax=1) displays .025 as 2.5%; a hatch on B supplements its sign and position. Object checks do not certify legibility or accessibility.

QA review: Exact source bar ordering/hatch checked; the supplemental QA display additionally makes the zero and signed labels visible.

**8.14-P19 — Export and resource checks**

The line retains the three specified balances. PNG signature and SVG XML checks establish limited format evidence. Closing the Figure restores the prior open-figure set. These checks do not demonstrate that labels are readable; the temporary files are removed automatically.

QA review: Source line and cleanup checked. QA re-export adds constrained layout for visual review; original temporary export checks remain structural.

**8.14-P20 — Dashboard coverage and evidence**

There are 5/6 price cells and 1/2 jointly complete adjacent-return pairs. A’s final strict return is unknown and serializes as null. Strict JSON rejects NaN; replacing LF with CRLF changes the input hash. A hash records byte identity, not economic truth. The small reference check covers these semantics only; it does not replace the sixteen acceptance tests or visual review in Section 8.13.

QA review: Mini-case accounting is separate from the explicitly rerun original sixteen-method project integration suite.
