# Section 14.2 — scoped sample space and event review

Reviewed [Sample Spaces and Events](../../chapter-14/14.02-sample-spaces-and-events.md) at `b8d5590794bdf2b32c4979081ca2887bdaed4fdf`. Run `python -B review.py` here. The [baseline](baseline.json) retains five failures; the [rerun](results.json) records the source and listing hashes, exact command output and expectations. The exact Python fence was run under the specified filename, compiled, and imported in isolation. All three command checks, twelve existing test methods and 34 additional predicates passed on rerun. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–8 | The three listed market outcomes cover the toy model. Two ordered three-state assets give nine pairs; a fair coin gives two equal weights. Excluding down leaves up and flat; the empty, certain, and singleton sets have the stated meanings. |
| 9–16 | Set membership gives the stated union, intersection and disjointness. Summing the .50 and .20 atoms gives .70, complementing .30. For Exercise 16 the four disjoint atoms are .40 A-only, .30 B-only, .20 both and .10 neither, so the union is .90. |
| 17–24 | .40+.40+.40 is invalid. Listing the four ordered loan states gives two exactly-one and three at-least-one outcomes. Product cardinality does not imply independence. The three singletons partition the market model. Continuous returns cannot be enumerated as a short list; omitting flat from the toy market requires justification. |

The ten-step mini-project was reviewed using integer probability points (72, 8, 15, 5) independently of the source implementation. Summing atoms gives stress 20%, default 13%, both 5% and either 28%; conditioning on the 20% stress event gives 25%. Independence would give only 2.6% joint probability. All 16 subsets matched, and an undeclared event state was rejected. The runner combines the exact functions into a supplemental JSON event report with event definitions and hypothetical weights. Real-world calibration and continuous sample spaces were reviewed conceptually; they were not executed.

**F111.** Empty iterators and duplicate or unhashable labels could yield an invalid Cartesian space. Enormous invalid integer weights raised overflow, and near-unit accepted totals could give a whole-space probability above one. The corrected code validates axes and normalizes accepted probability mass before summing. Cross-platform coverage, F28, F32 and independent acceptance remain open.
