# Section 13.15 — scoped chapter assessment review

Reviewed [Exercises and Applied Problems](../../chapter-13/13.15-exercises-and-applied-problems.md) at parent `f381485739a47b54c7dfa687e99fbff5bc24059e`. Run `python -B review.py` here. The [baseline](baseline.json) retains 12 failures. The [corrected rerun](results.json) records source hashes, exact output, independent expectations, and scope counters. The single standard-library workflow runs the unchanged extraction of the published fence as `chapter13_exercises.py`, compiles it, and checks isolated import. Three commands, twelve existing methods, and 60 additional predicates passed after correction. No historical unique methods were added.

| Chapter-wide answers | Prompt alignment and independent checks |
|---|---|
| 1–6 | Price gain is 12/80; loss of .12 leaves .88; ln(1.10) and its inverse are consistent; linked factors are .99 and 1.05987. |
| 7–12 | Annual factor is √1.21; cash held yields 8/100; arithmetic is .05 and geometric is √1.08−1. AM–GM holds for positive factors with equality only for identical factors; TWR is 110/100 × 144/160 − 1. |
| 13–18 | One annual receipt yields .10; the positive gross quadratic root for the larger ledger gives −2.423493%. The stated dates are 365 days apart. Opposite .10 moves give variance .01 or .02 depending on the divisor; .01√252 gives annual volatility. |
| 19–24 | Downside uses one squared shortfall divided by two. Peak 120 to 90 loses .25, and a 40% loss needs .40/.60 gain. Monthly Sharpe is .008/.02, annualized by √12; Sortino is zero for the opposing moves; Calmar is .12/.20. |
| 25–30 | Opposite active moves imply zero mean and nonzero tracking error. The benchmark slope is two; the polynomial has distinct roots 10% and 20%. Total loss fixes gross wealth at zero and has no finite log return. Contributions belong outside investment gains; constant returns make Sharpe undefined. |

| Applied problem | Review |
|---|---|
| A — Price and dividend | Exact ledger: price gain 4/100, total gain 6/100, second price move −3/104. Holding the dividend leaves $103; reinvesting gives $102.9423077. The retained 3% account return uses −3/106 in month 2. |
| B — Cash flows | Verified +10%, −10%, −1% cumulative TWR and −2.423493% periodic IRR by a quadratic root; the source reprices the unrounded rate. |
| C — Drawdown | Ordered-pair enumeration independently gives the 112→91 episode (3→5), −18.75% depth, recovery at 7, and required gain 21/91. The final high-water mark is 118. Each source drawdown was compared to the ledger. |
| D — Strategy metrics | The source methods match the return, volatility, drawdown and Sharpe outputs on both paths. [scorecard.py](scorecard.py) separately computes downside, Sortino and information ratio using rational downside and pairwise variances; those metrics are not implemented in this listing. The worked table now reports all requested outputs with scale conventions. |
| E — Ambiguous IRR | The terminal-value polynomial factors as −100(g−1.1)(g−1.2). Both brackets recover the respective roots, and the wide same-sign bracket rejects. |

The twelve project deliverables, troubleshooting table, and seven conceptual knowledge checks were reviewed as a rubric. The supplied fixtures exercise return and flow reconciliation, drawdown, ambiguity and undefined denominators; a dated end-to-end reporting pipeline, operational runbook execution, and independent acceptance are outside this scope.

**F109.** The original chapter lab inherited range and scale failures and accepted some boolean or string inputs. It now uses the same arithmetic and root conventions as the preceding analyzer, keeping the listing self-contained. The assessment corrects two IRR statements and distinguishes the final high-water mark from the worst episode's peak. These are Linux CPython results for the recorded fixtures; F28 and F32 remain open.
