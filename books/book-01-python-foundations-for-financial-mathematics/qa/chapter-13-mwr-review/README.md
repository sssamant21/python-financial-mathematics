# Section 13.10 — scoped MWR review

Reviewed [Money-Weighted Return](../../chapter-13/13.10-money-weighted-return.md) against main at `7610f56d32e5cf479d3651db5bf2024292f87958`. Run `python -B review.py` here to reproduce [results.json](results.json). The [baseline](baseline.json) retains 16 failed checks. Source and listing hashes, actual values, independent references, and command outputs are recorded.

The one standard-library lab saves the entire Python fence as `money_weighted_return.py`. Execution printed the demonstration and ran all twelve existing methods; compilation and isolated import also passed. The corrected rerun passed 36 additional checks. These predicates do not add historical unique methods.

| Local answer records | Review |
|---|---|
| 1–4 | Single-period cash receipts divided by outlay give gross factors 1.1, 0.9 and 1.0. For 121 after two years, the factor is the positive square root of 121/100. |
| 5–7 | Read the ledger from the investor perspective: −500 paid, +80 received, +300 imputed terminal proceeds. |
| 8–10 | Solve the positive gross root of 100g²+50g−E=0 with E=180 or 144. The periodic results are 11.47344064% and −2.42349328%. The separate cumulative TWR is 1.10×0.90−1=−1%; align horizons before comparing. |
| 11–14 | The annual fixture spans 365 days, so 110/100 gives 10% and discounts back to 100. The independent polynomial for the two-root case factors as −100(g−1.1)(g−1.2). |
| 15–18 | Same-sign endpoints do not exclude roots inside the bracket. The investment multiple is 120/100; a terminal valuation and sale for the same asset would duplicate proceeds. TWR removes the mechanical effects of external flows; it cannot by itself prove skill. |

The eight-task mini-project uses days 0, 90, 243 and 365 from the origin. [benchmark.py](benchmark.py) compounds each signed flow forward to the terminal date and solves that equation with high-precision Newton steps, independently of the manuscript's discounted NPV and bisection. The exact-source methods match the base and stressed XIRRs (10.594687% and −6.212551%); both absolute currency residuals are below 1e−7. Equal spacing gives 3.466088% per interval and 10.762842% annually under three intervals per year. Investing 12,000, receiving 500 and counting the 12,700 terminal valuation once gives 1.10×; stressed multiple is 0.94125×.

The source does not implement ledger export. Run `python -B export.py /path/to/output` for the separate supplemental exporter, which calls the exact listing. Two runs matched the retained [ledger](example-output/ledger.csv) and [calculation summary](example-output/summary.json) byte for byte. Project stress, ambiguity, and the reconciliation of signed flows were checked independently of the export format. Timestamp cutoffs, duplicate event identity, exhaustive root enumeration, and production reporting policies remain design topics.

**F104.** The original absolute currency stopping threshold returned false roots when amounts were small, and multiplying endpoint values could underflow and erase a sign distinction. XIRR also missed exact endpoint roots, accepted decreasing dates after the first date, and could return a rate when all net dated flows cancelled. The shared bisection now validates inputs, handles endpoint roots, compares signs directly, and uses rate width or an evaluated zero. Daily nets are checked for signs on distinct dates. Two printed answers were corrected. This float implementation was checked on Linux CPython with the recorded fixtures; extreme horizons, final independent acceptance, F28 and F32 are outside this scope.
