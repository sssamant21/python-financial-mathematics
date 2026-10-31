# Section 7.14 — Eight scoped local answers

Unchanged trailing/expanding source is separate from supplemental time-window and scalar arithmetic. Independent rational prefix sums verify every expanding mean;sample/population dispersion and future perturbations are checked without claiming a trading strategy. E7 publication-time rules remain design. Full console expectations are transcribed from the published table and formulas.

## 7.14-E1

**Prompt:** Compute the final rolling and expanding means by hand.

**Scope:** SOURCE + RATIONAL ORACLE

Final three-observation mean=(104+106+108)/3=106. Final expanding mean=(100+102+104+106+108)/5=104. Both include the current supplied row;one uses the latest3observations and the other all5. Equal observation weighting is not elapsed-time weighting.

## 7.14-E2

**Prompt:** Explain the two leading rolling NaNs and three leading prior_mean NaNs.

**Scope:** SOURCE WARM-UP

min_periods3 requires three observed source prices,so rolling mean/std areNaN for the first2rows. prior_mean shifts that computed rolling mean one row,creating3leadingNaNs;its first mature value at15:00 is102 from14:40. These are defined warm-up states,not missing input or observedzero. No filling is authorized.

## 7.14-E3

**Prompt:** Compare the thirty-minute and three-observation populations at 14:40.

**Scope:** SOURCE + EXPLICIT WINDOW POPULATIONS

At14:40,the right-closed30minute interval is(14:10,14:40],so the14:10 observation is excluded and only104 remains. The three-observation window contains100,102,104 and averages102. Irregular timestamps mean time windows and observation-count windows need not use the same population.

## 7.14-E4

**Prompt:** Change only the final price and verify earlier results remain unchanged.

**Scope:** EXACT SOURCE FUTURE PERTURBATION

Change final108 to1000. All earlier output rows remain equal;final rolling mean becomes(104+106+1000)/3=1210/3,final expanding mean1512/5=302.4,while final prior_mean remains104. This checks trailing alignment on the fixture,not whether the underlying prices were historically available or revised.

## 7.14-E5

**Prompt:** Compare ddof=0 and ddof=1 for [100,102,104] and state their units.

**Scope:** SOURCE/SCALAR DISPERSION

For100,102,104,mean102 and squared deviations4+0+4=8. ddof0 gives variance8/3,stdsqrt(8/3)≈1.632993;ddof1 gives variance4,std2. Both standard deviations have price units and neither is annualized return volatility. The convention must follow the intended statistical question,not a desired number.

## 7.14-E6

**Prompt:** Explain why shifting one row is not the same as shifting thirty elapsed minutes.

**Scope:** SOURCE INDEX ALIGNMENT

shift1 withoutfreq moves feature values one row while retaining output labels. At15:00,the prior feature comes from14:40,20minutes earlier;at15:10 it comes from15:00,10minutes earlier. It is neither a uniform30minute delay nor a trading-day convention. A required elapsed-time lag needs a separately defined temporal alignment policy.

## 7.14-E7

**Prompt:** Propose an explicit publication-time contract before using prior_mean as a historical feature.

**Scope:** PUBLICATION-TIME DESIGN — NOT IMPLEMENTED

Require source observation,event/publication/ingestion and revision-availability timestamps,plus decision cutoff,instrument/context,calendar and allowed quote age. Build each historical feature only from the version of each observation actually available by that cutoff;define ties,late arrivals and corrections explicitly. A prior-row feature may still contain unavailable or revised data,so rowshift alone cannot prevent look-ahead bias. Proposed checks include late publication,post-decision revision,missing eligibility metadata and future-price perturbation;only the latter numerical fixture check executed here. No point-in-time feature engine/backtest was implemented.

## 7.14-E8

**Prompt:** Add an independent expanding-mean scalar check for each row without copying the pandas expression.

**Scope:** INDEPENDENT PREFIX-SUM ORACLE

Maintain a Python Fraction running sum and divide by the number of supplied observations at each row,rather than copying pandas.expanding. Prefixes100,202,306,412,520 divided by1,2,3,4,5 give100,101,102,103,104. All five original source expanding values match these exact expectations. This verifies the small complete fixture,not arbitrary-scale numerical error bounds.

Original demo/discovery/compileall pass with FutureWarning as error. First-run outputs and expected rejection traces retained; no unexpected failure or manuscript defect. F28/F32 and F37 history remain intact; no independent acceptance or new historical unique methods/workflow cases are inferred.
