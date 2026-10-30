# Section 6.11 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; exact float64 finite two-axis arrays, matching unique tuple instrument identities/order and labelled scenario/portfolio axes. Caller establishes common one-interval price returns, long-only opening weights, complete cash/denominator and compatible currency/unit conventions. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.11-E1

Add a third portfolio with weights [0,0,1] and derive its three scenario results.

**EXACT SOURCE + INDEPENDENT RATIONAL CELL ORACLES**. Append portfolio P3-CASH with weights [0,0,1]. Its UP, DOWN and CASH-YIELD results are [0,0,0.002], since only the cash column contributes. The resulting scenario-by-portfolio table has shape (3,3), with original two portfolio columns unchanged and the third labelled P3-CASH. The runner derives every cell using Fraction return/weight inputs independently of matrix multiplication, and verifies labels and values. Comparisons use rtol=1e−12, atol=1e−14 with NaNs disallowed for these small fixtures.

## 6.11-E2

Add a fourth scenario [0.05,0.05,0] and compute every portfolio result by hand.

**EXACT SOURCE + INDEPENDENT RATIONAL CELL ORACLES**. Append scenario BROAD-UP with returns [0.05,0.05,0]. For original P1, result is (3/5)(1/20)+(3/10)(1/20)=9/200=4.5%; for P2 it is (1/5)(1/20)+(3/10)(1/20)=1/40=2.5%. For the added all-cash P3 it is zero. This composed extension has four scenarios and three portfolios, shape (4,3). The runner checks all three hand-derived cells and the new scenario label without changing the original fixture.

## 6.11-E3

Reorder scenario rows and labels consistently; verify the corresponding output row permutation.

**EXACT SOURCE ROW/LABEL PERMUTATION + LIMIT PROBE**. Use row order [2,0,1] and apply it to both return rows and scenario labels. Output rows become CASH-YIELD,UP,DOWN in that order while portfolio columns stay P1,P2. Numerical results match the corresponding original output permutation within the stated tolerance. A separate stale-label probe deliberately reorders labels alone: source still accepts unique correct-length labels and leaves numbers unchanged. This demonstrates the caller alignment responsibility, not a source validation defect; a numeric matrix cannot infer which scenario name belongs to a row.

## 6.11-E4

Add a test that a duplicate portfolio label fails even when weight rows are numerically valid.

**EXACT SOURCE EXPECTED REJECTION**. Pass original numerically valid weight rows with duplicate portfolio labels (P1,P1). The unchanged source raises ValueError through label_axis before multiplication. Distinct valid allocations do not make duplicate identities acceptable; both label count and uniqueness are required. Expected traceback is retained separately from unexpected failures.

## 6.11-E5

Derive the shape and element payload of a 1000-scenario, 200-portfolio result table.

**INDEPENDENT INTEGER PAYLOAD + BOUNDED EXACT SOURCE ALLOCATION**. A result with 1000 scenarios and 200 portfolios has shape (1000,200), 200,000 float64 cells and 1,600,000 element bytes =1.6 decimal MB =1.52587890625 MiB. This is output payload only, not peak RSS or an OS reservation. A feasible controlled source run with three instruments, 1000 all-zero return rows and 200 all-cash portfolios actually allocates this output and confirms shape/dtype/nbytes/zero values at max_cells=200000. Return input has 3000 cells and weights 600, so max_cells=199999 fails specifically on the output size while both inputs are below it. Existing source checks each individual matrix, not their combined process footprint; internal workspace and validation temporaries are not measured.

## 6.11-E6

Compare one portfolio's result column with the elementwise weighted sum from Section 6.10.

**CROSS-SECTION EXACT SOURCE FUNCTION CALLS + RATIONAL ORACLE**. Load the unchanged first Python listing of Section 6.10, with its file/listing hashes retained. For each original portfolio weight row and every scenario, call its contributions function on the aligned return row. Both columns match the Section 6.11 matrix result and independently derived rational cells: P1 [0.045,−0.09,0.0002], P2 [0.005,−0.01,0.001]. This is exact-source function-call agreement under shared one-interval assumptions; it is not a rerun of the Section 6.10 unittest suite, not independent model acceptance, and not proof for arbitrary data.

## 6.11-E7

Specify the additional conventions needed to interpret rows as successive periods instead of alternatives.

**CONCEPTUAL SUCCESSIVE-PERIOD CONTRACT REVIEW**. Before interpreting rows as time, define chronological interval start/end labels, shared observation frequency or irregular duration treatment, beginning holdings/NAV, cash and liabilities, external cash-flow timing, total-versus-price-return conventions, corporate actions, FX, fees, financing and taxes. Decide whether each portfolio is fixed holdings with drifting weights or rebalanced to targets; state decision/execution timing, transaction costs and information availability. A constant W across historical rows generally describes repeated target-weight reuse, not fixed holdings. A drifted W_t may require per-period weighted sums rather than one fixed matrix product. Link compatible interval portfolio gross returns under an explicitly defined performance methodology; do not sum alternative scenario rows or assume a numerical table is a realized account path. This batch records the design and the unchanged output-axis contract only; no holdings/rebalancing/time-path engine is implemented or executed.

## 6.11-E8

Describe why a matrix of numerical results is not automatically a calibrated risk model.

**CONCEPTUAL MODEL-CALIBRATION LIMIT REVIEW**. Matrix multiplication applies supplied allocations to supplied returns; it provides no evidence that the scenarios are exhaustive, calibrated, probable, representative, independent, stationary or appropriate for a decision. Retain horizon, units, valuation/data lineage, model assumptions, calibration method/data window, dependence/tail behavior, scenario selection and probability/weight rationale if used, missing-data policy, uncertainty/sensitivity checks and validation/monitoring criteria. Distinguish realized observations from hypothetical stresses and explicitly model omitted costs/flows/FX/financing as required. This source returns scenario/portfolio labels, numerical returns and observed weight sums, with no probabilities. Shape, finite-value and algebra checks support implementation claims only; distributional calibration, risk measures, backtesting and independent acceptance remain unexecuted. A numerical output alone is not a calibrated risk model.
