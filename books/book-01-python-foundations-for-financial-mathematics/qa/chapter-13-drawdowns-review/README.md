# Section 13.12 — scoped drawdown review

Reviewed [Drawdowns](../../chapter-13/13.12-drawdowns.md) at main parent `e73a812aace959f9f9296f60a545cfe6deb0d079`. Run `python -B review.py` here; it writes [results.json](results.json), including source and listing hashes, command results, tolerances, and individual observations. The [baseline](baseline.json) retains six failed predicates from the original listing.

The workflow saves the verbatim standard-library fence as `drawdowns.py`, runs the example and twelve existing methods, and compiles the listing. The isolated import also passed. After correction, all three commands and 49 additional predicates passed. No historical unique methods were added.

| Local answer records | Review and independent expectations |
|---|---|
| 1–5 | Prior maxima are 100, 120, 120. Losses of 30 and 15 relative to 120 give −25% and −12.5%; at 120 there is no remaining loss. |
| 6–11 | Divide each shortfall by the capital left: 10/90, 20/80, 25/75, 50/50 and 80/20. With zero capital there is no finite recovery multiplier. |
| 12–16 | 100 × 1.20 × .75 = 90; a tenth of 90 adds 9, leaving a 21/120 shortfall. Two observations sit below 120 before recovery. With zero-based indexing the shorter fixture has peak 1 and trough 2. |
| 17–18 | A contribution changes the account balance without changing the performance index. Rearranging +25%, −20%, −20% preserves terminal wealth at 80; clustering the losses gives a 36% decline from 125 versus 20% when separated. |

The eight-task project checked all nine observations against an independent enumeration of ordered wealth pairs. The lowest ratio is 91/112 at observations 3→5; the 18.75% drawdown needs a gain of 21/91 to recover. Observations 4–6 remain underwater and 7 recovers. The exact listing rejects a missing valuation; the artificial forward-filled run reports only −12.50%. The [supplemental dashboard](project.py) combines source drawdowns with independently compared running peaks, exact threshold states, and a CSV output checked by parsing it back. The exact source does not implement alerts or a production dashboard. Sampling, data feeds, cutoff policies, and incident actions remain design considerations.

**F106.** The original listing could erase small drawdowns and recovery gains, report zero or infinity for an unrepresentable wealth path, report complete loss with positive wealth, and assign a later drawdown to a peak before an already recovered episode. The corrected listing keeps exact fractions until reporting, and it associates a decline with the latest equal peak preceding it. This Linux CPython evidence does not establish platform coverage or independent acceptance. F28 and F32 remain open.
