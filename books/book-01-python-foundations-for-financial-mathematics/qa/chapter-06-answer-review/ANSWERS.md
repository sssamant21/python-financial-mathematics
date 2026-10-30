# Chapter6 — prompt-aligned review of20 chapter-wide answers

This review combines original-source test observations, independent rational/Decimal arithmetic and conceptual/design review. These are separate evidence routes; all20 passing reference methods do not establish complete prose alignment or independent acceptance. The missing callable functions for Problem18 were corrected under F35.

## 6.17-01 — Array contract

**Prompt:** Create a float64 array from [100, 102, 99]. Report its shape, dimension, and dtype. Explain why the values alone do not specify financial units.

Observed float64 shape(3,),dimension1 and values. Units/currency/instrument/time are separate semantic inputs; source test alone cannot validate their provenance.

## 6.17-02 — Integer truncation

**Prompt:** Assign 1.75 into the first element of an integer array [1,2]. Explain the result and supply a floating alternative.

Observed integer array becomes[1,2]; floating alternative becomes[1.75,2]. Casting the truncated result afterward cannot recover the fraction. This is representation behavior, not rounding policy.

## 6.17-03 — Slice ownership

**Prompt:** Slice elements 1 onward from [100.,101.,102.], change the slice first element to zero, then repeat using copy. Identify the source changes.

Observed view changes original to[100,0,102]; copied view then changes to[9,102] without changing that source. Supplemental fresh-repeat copy exactly follows prompt: fresh source remains[100,101,102], copied slice becomes[0,102]. Distinguish the source test sequence from this separate repeat.

## 6.17-04 — Fixed-quantity P&L

**Prompt:** For quantities [10,-5,0], opening prices [100,80,50], and closing prices [105,76,52], calculate price-only P&L. State the assumptions.

Independent Fraction calculation10*(105-100)=50,-5*(76-80)=20,0*(52-50)=0 currency units. Positions unchanged, common quote units/currency/interval; signed short quantity excludes trading, distributions, borrow fees and FX.

## 6.17-05 — Broadcasting direction

**Prompt:** For closing prices [[110,95],[80,105]] and opening prices [100,100], calculate asset returns. State the input and output shapes.

Rational ratios give[[1/10,-1/20],[-1/5,1/20]]. Closing shape(2,2), opening shape(2,),result(2,2); columns identify assets, rows scenarios. Equal axis lengths do not prove correct alignment.

## 6.17-06 — Aggregation axes

**Prompt:** For return matrix [[.10,-.05],[-.20,.05]], find row means and column means. Explain why neither is automatically an expected portfolio return.

Exact means: rows1/40,-3/40; columns-1/20,0. Axis1 averages assets equally, axis0 scenarios equally. Neither establishes portfolio weights or scenario probabilities without those assumptions.

## 6.17-07 — Cash-flow vector

**Prompt:** Discount cash flows [100,100,1100] at times [1,2,3] using annual effective rate .05. Compare a vector expression with scalar arithmetic.

Independent rational sum100/(21/20)+100/(21/20)^2+1100/(21/20)^3 gives1136.1624014685239 approximately. Source scalar/vector agree with rational benchmark within1e-10; printed1136.162401469 within1e-9. Same-currency deterministic promised flows at years1,2,3 under annual effective5%; no timing/credit/curve model inferred.

## 6.17-08 — Successive returns

**Prompt:** Prices [100,110,99] are consecutive observations of one asset without distributions. Calculate simple interval returns and cumulative return.

Rational successive returns1/10 and-1/10; endpoint ratio99/100-1=-1/100. Multiplication telescopes under same time path/no distributions; adding to0 loses compounding. Not independent scenarios.

## 6.17-09 — Opening weights

**Prompt:** Given common-currency opening values [600,300,100], derive weights and combine asset returns [.10,-.05,0]. Explain the weighting date.

Opening total1000 gives exact weights3/5,3/10,1/10. Weighted return9/200=.045. Weight date is opening; using closing weights silently changes the question.

## 6.17-10 — Multiple portfolios

**Prompt:** Use R=[[.10,-.05,0],[-.20,.05,0]] and W=[[.6,.3,.1],[0,1,0]]. Calculate R @ W.T and label its axes.

Scalar rational products give[[9/200,-1/20],[-21/200,1/20]]; result shape2scenarios by2portfolios. W rows are portfolios, so transpose exposes common asset axis. No sum over scenarios.

## 6.17-11 — Linear system

**Prompt:** Solve 2x+y=5 and x+3y=5 with np.linalg.solve. Verify the residual rather than forming an inverse.

Exact elimination/determinant5 gives x2,y1, and equations4+1=5,2+3=5. Observed solver/residual checks agree. Residual tolerance is fixture-specific and does not establish conditioning generally.

## 6.17-12 — Singular model

**Prompt:** Attempt to solve [[1,2],[2,4]] x = [3,6]. Explain why a unique answer is unavailable.

Exact determinant1*4-2*2=0,second RHS6=2*3. Infinite solutions x+2y=3,not a unique solution. Source explicitly expects LinAlgError. No least-squares substitution.

## 6.17-13 — Random protocol

**Prompt:** Create two fresh Generator(PCG64(42)) instances and draw five standard normals from each. Then draw another five from the first. State what the seed does and does not establish.

Fresh Generator(PCG64(42)) calls produce equal five-element arrays in the actual runtime; source checks the next call differs. This is protocol repeatability, not independent distribution validation, historical forecasts or cross-version bitstream promise. Record generator,version,seed,call order and environment.

## 6.17-14 — Tiny linked changes

**Prompt:** Link three returns of 1e-17 using both prod(1+r)-1 and expm1(sum(log1p(r))). Compare with 3e-17 and explain the loss.

Independent precision80 Decimal expression(1+1e-17)^3-1=3e-17+3e-34+1e-51. float64 1+1e-17 rounds to1 so product route gives0; log1p/expm1 result agrees with high-precision expression within1e-31. Relative-to-scale tolerance differs from usual1e-12 fixture checks; no universal accuracy ranking.

## 6.17-15 — Tolerance and shape

**Prompt:** Show that allclose may accept shapes (2,1) and (2,) through broadcasting. Explain a safer result-comparison contract.

Observed ones(2,1) versusones(2,) allcloseTrue while shapes differ. Require exact shape/axis/identity contracts, finite values and a justified rtol/atol before numerical comparison. Identity is not established by shape equality.

## 6.17-16 — Finite input gate

**Prompt:** Build a finite-value check for [1,nan,inf]. Explain why replacing invalid observations with zero changes the financial model.

isfinite gives[True,False,False]; complete gate allFalse. Reject or route unavailable/invalid observations under explicit policy. Zero price/return is a substantive economic assertion, not a neutral missing-data repair.

## 6.17-17 — Payload budget

**Prompt:** Calculate float64 payload bytes for a (1000,20) matrix. Does this establish peak process memory?

Payload formula1000*20*8=160000bytes agrees with observed nbytes. Does not include Python objects, temporaries, other arrays, conversion or library process memory; no peak-memory measurement is claimed.

## 6.17-18 — Benchmark boundary

**Prompt:** Write equivalent list-to-list Python and NumPy P&L functions for the fixed-quantity fixture in Problem 4. Verify agreement before timing. Explain a fair measurement protocol.

INITIAL ALIGNMENT FAIL: source had inline expressions only despite requiring functions. F35 adds python_pnl/numpy_pnl with same list-to-list arithmetic boundary and unequal-length rejection. Both return[50,20,0] lists against the rational benchmark; twenty-method suite updated without adding methods. Assumes aligned finite numeric lists from this fixture contract,not a general validated API. Fair future timing: identical data/input-output boundaries, check equality first, warm both, repeat in balanced order, record raw samples/runtime/hardware and exclude setup equally. No timing run or speed claim.

## 6.17-19 — Project reconciliation

**Prompt:** Independently value holdings [6,3,1] opened at [100,100,100] under closing rows [[110,95,100],[80,105,100],[100,100,100]]. Reconcile direct P&L with opening-weight returns.

Independent direct holdings valuation yields1000opening;1045,895,1000ending;45,-105,0P&L;9/200,-21/200,0returns. Observed weighted reconstruction agrees within specified fixture tolerance. Rows are alternatives,not compounded. Section6.16 project validation remains a separate workflow.

## 6.17-20 — Identity and permutation

**Prompt:** For returns [.10,-.05,0] and weights [.6,.3,.1], show that permuting both together preserves return, while permuting only weights gives a different result. State how production code prevents this mistake.

Rational aligned return9/200 remains unchanged under joint[2,0,1] permutation. Reversing weights alone gives-1/200. Labels/order must be checked at ingestion; use exact ordered identity or a validated explicit alignment adapter,not mere equal dimension. No production adapter integration is claimed.
