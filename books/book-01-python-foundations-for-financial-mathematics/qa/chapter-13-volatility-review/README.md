# Section 13.11 — scoped volatility review

Reviewed [Volatility](../../chapter-13/13.11-volatility.md) at main parent `a4d6415c16131f0c6ea43b00117712fb919a6ded`. Run `python -B review.py` here. It writes [results.json](results.json), with manuscript and lab hashes, observed outputs, reference values and tolerances. The [baseline](baseline.json) retains 11 manuscript failures. A preceding QA runner error assumed there was only one Python fence and stopped before executing either; the runner was corrected to map the data and lab fences separately before taking the baseline.

The standard-library workflow saves the exact lab fence as `volatility.py`, runs the demonstration and all 12 existing methods, and compiles the file. The isolated-import probe also passed. The separate exact data fence was executed and checked against the five-day fixture. All three command checks and 47 additional predicates passed on rerun; no historical unique methods were added.

| Local answer records | Independent review |
|---|---|
| 1–6 | Opposite 10% returns have zero mean and squared deviations totaling .02. Denominators two and one give .01 and .02. Constant returns have no dispersion. |
| 7–10 | Five returns sum to .03. The pairwise difference identity gives .00172 for the centered sum of squares; divide by 5 or 4 and take the square root. |
| 11–14 | For uncorrelated periods of equal variance, annual variance is 252 times daily variance. For downside, only the negative observation contributes .01 to the numerator; divide by two. Four-observation windows over ten observations end on days 4 through 10. |
| 15–18 | Each weighted exposure is .10. At zero correlation the variances add; at +1 exposures add before taking the magnitude, and at −1 equal exposures cancel. |

For the eight-task mini-project the independent reference calculates dispersion from pairwise squared differences, using rational arithmetic and then a decimal square root. The exact-source methods match the mean, both daily volatilities, annualization, all eight rolling windows, downside deviation, and stress. Full-sample volatility was 1.219517% daily, versus 1.069268% for the final three-day window; after appending +15% the corresponding values rose to 4.624500% and 8.638480%. The prose now includes these outputs and the audit row contract.

The [supplemental exporter](export.py) calls the exact listing for rolling volatility and adds a CSV view. Two runs matched the retained [ledger](example-ledger.csv) byte for byte; the first two of ten rows have blank volatility and the counts are 1, 2, then 3. Price adjustments, stale observations, independent data sourcing, and forecast calibration are design considerations.

**F105.** The original implementation could erase integer spreads and tiny volatility, overflow before forming a representable result, and treat a non-boolean downside switch as truthy. It also lost covariance precision near a hedge. The corrected listing uses fractions for intermediate values, takes roots before converting to float, and validates the downside option. This is a Linux CPython review of the recorded fixtures, without throughput or independent acceptance. F28 and F32 remain open.
