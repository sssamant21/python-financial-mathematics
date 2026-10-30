# Section 6.12 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling files; finite exact float64 square system/one-dimensional target within teaching bounds. Caller preserves state/instrument labels, payoff-per-unit conventions, currency and horizon. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.12-E1

Solve the supplied equations manually for target [80,120] and verify the result.

**EXACT SOURCE + MANUAL ELIMINATION**. For target [80,120], equations xA+xB=80 and xA+2xB=120 imply xB=40 by subtraction, then xA=40. The original guarded source returns these units and reconstructs both target payoffs within the declared small-fixture comparison tolerance. These are instrument units, not normalized allocation weights.

## 6.12-E2

Add a third independent equation/instrument with an obvious known solution.

**EXACT SOURCE + BLOCK-SYSTEM ORACLE**. Extend the supplied system to A=[[1,1,0],[1,2,0],[0,0,4]] and target [100,150,12]. The first two equations still give xA=xB=50, while the independent third equation gives xC=3. The diagonal block has nonzero coefficient 4, so the three columns are independent; source returns shape (3,) units [50,50,3] and reconstructs all three states. Caller labels must distinguish the added state and instrument; no new market-spanning claim follows.

## 6.12-E3

Permute rows and target entries consistently; verify that instrument units remain the same within tolerance.

**EXACT SOURCE ROW PERMUTATION + CALLER LABEL REVIEW**. Use the same A with target [80,130], giving deliberately unequal units [30,50]. Swap both rows and target entries with order [1,0] and preserve state labels as (STATE-2,STATE-1). The equations change order, not meaning, and source returns the same units within tolerance. Unequal units make the related column check informative. Labels are maintained in the QA caller; solve_payoffs itself accepts no labels and cannot verify their financial alignment.

## 6.12-E4

Permute columns and instrument labels consistently; verify that units follow the column order.

**EXACT SOURCE COLUMN PERMUTATION + CALLER LABEL REVIEW**. With target [80,130], swap A columns and instrument labels to (B,A). The source output follows that column order as [50,30]. Reapplying the inverse permutation restores [30,50] in original (A,B) order. A column permutation must not reorder target rows, which are a different axis. The runner verifies both numeric orders and the controlled label tuple; it does not infer labels from coefficients.

## 6.12-E5

Add a test for a nonfinite coefficient in A rather than only in the target.

**EXACT SOURCE NONFINITE-COEFFICIENT REJECTIONS**. Place NaN, positive infinity and negative infinity independently in A[0,1] with an otherwise valid system/target. All three original API calls raise ValueError before a solution is returned. Each rejected coefficient array remains byte-identical and the caller NumPy error policy is unchanged. These supplement the original target-focused nonfinite tests without editing that suite.

## 6.12-E6

Record absolute and normalized residuals for a deliberately rescaled system and explain the difference.

**EXACT SOURCE RESCALING + SUPPLEMENTAL EXACT REPRESENTED-INPUT DIAGNOSTICS**. Use intended decimal system A=[[0.1,0.2],[0.3,0.7]], b=[0.4,1.1]; decimal elimination gives units [6,−1]. Also multiply both arrays by 100000, staying within source magnitude bounds. This common scaling changes payoff units but not the intended unknowns or mathematical condition number. On this runtime, the first floating reconstruction residual is [0,0], normalized 0; the scaled residual has infinity norm 7.275957614183426e−12 and normalized residual 1.0247827625610471e−17, with scale approximately 710000. Both condition numbers are approximately 62.9841 and both pass the source gates. The runner independently rebuilds the diagnostic denominator with Python scalar arithmetic and checks the normalized formula with relative tolerance 1e−14 and zero absolute tolerance, treating zero exactly. It retains each coefficient, target, units and residual. Fraction arithmetic on the actually represented binary inputs and returned units produces additional nonzero exact arithmetic residuals even when the floating reconstruction reports zero; these are labelled separately, not substituted for the API diagnostic. Binary multiplication also makes the scaled target second entry 110000.00000000001, so last-bit differences need not obey exact scale invariance. Absolute error has payoff units; normalized error is dimensionless and does not establish financial materiality or forward accuracy. Nonuniform scaling can also change the reported condition number and requires an explicit transformation policy.

## 6.12-E7

Specify when a least-squares question would be appropriate instead of silently relaxing exact matching.

**LEAST-SQUARES DESIGN + SOURCE REJECTION + RATIONAL TOY**. Least squares is appropriate when the stated question is an approximate fit, often with more observations/equations than unknowns and a specified residual objective, rather than exact matching of every state. Specify observation/coefficient provenance, units/scaling, error assumptions, row weights, rank and singular-value cutoff, uncertainty/conditioning diagnostics, constraints and accepted approximation limits. An unweighted toy asks x≈1 and x≈2, minimizing (x−1)^2+(x−2)^2 at x=3/2 with objective 1/2. The runner checks that rational example and confirms the original square-only source rejects the rectangular (2,1) array; it does not call lstsq or implement a fallback. Rank-deficient minimum-norm selection, regularization or omitted equations would be different reviewed questions, never silent recovery from a failed exact-match solve.

## 6.12-E8

List the prices, constraints, and financial assumptions required before treating solved units as trade instructions.

**ECONOMIC/TRADE CONTRACT DESIGN ONLY**. Before using solved units operationally, supply tradable instrument identities, payoff definitions and common horizon/currency, current executable bid/ask prices and quantities, lot/minimum sizes, liquidity and market impact, budget and funding source, cash/borrowings/collateral, shorting/locate rules, financing and borrow costs, fees/taxes, settlement calendars and timing, corporate actions/default/recovery assumptions, legal/mandate and risk limits, input provenance/uncertainty and unrepresented-state exposure. Define an objective if optimality is required and an explicit feasibility/approval/execution policy. Source output contains units and numerical diagnostics only; it supplies no prices or orders. This answer is a conceptual contract review, not pricing, optimization, authorization, trade execution or independent model acceptance.
