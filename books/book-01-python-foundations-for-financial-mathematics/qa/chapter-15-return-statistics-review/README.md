# Section 15.11 — scoped financial-return lab and answer review

Baseline manuscript: `86882ad58864ee685bd2e9b55bac7ee902c75e34`. One core workflow, 24 local answer records and one ten-task project reviewed. These counts are distinct from supplemental predicates and historical unique test methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-return-statistics-review/review.py
```

The observer extracts the single source fence unchanged, executes the printed demonstration and twelve existing unittest methods, imports silently and runs the printed compilation command in isolation. Three commands and 46 supplemental predicates pass in `results.json`; no historical unique methods added. Python/platform, raw command outputs, hashes, independent expectations and tolerances are retained. `baseline.json` retains twelve failed predicates against the unchanged baseline source above, reproducible with this runner and that source. All twelve existing methods already passed on baseline.

F137 corrects erased integer price increments/spread, nonfinite log returns caused by intermediate price-ratio overflow, mean/volatility/ES overflow or underflow, decimal tail-rank off-by-one errors, positive wealth falsely rounded to −100% loss and unreportable annual volatility. Integer and displayed-decimal float inputs use rational intermediate arithmetic. Near-unit gross logs use log1p; other logs and roots use 80-digit Decimal. Geometric growth near one uses log1p/expm1, while other products use Decimal log/exp before reporting. The maximum finite float geometric-mean fixture is also checked. Nonzero unreportable outputs raise ValueError, as does positive gross wealth rounding to a −100% simple/cumulative return. True observed −100% loss still locks cumulative wealth at zero; geometric mean deliberately rejects it under this section's positive-wealth domain. Educational conventions only, not binary-float compatibility or performance certification.

## Independent numerical expectations and all local answers

Simple return expectations use rational price differences; log expectations use 80-digit Decimal ln of exact rational gross ratios. Geometric mean for [.1,−.1] is independently Decimal sqrt(.99)−1, and cumulative return is exactly −.01. Volatility references use pairwise variance Σ(i<j)(ri−rj)²/[n(n−1)] instead of source centered squares. Tail expectations use explicitly ordered observations and integer counts; alpha=.14 with n=100 selects rank 14, not 15.

| Prompts | Review and execution boundary |
|---|---|
| 1–4 | Source returns for 100→110→99 are .1/−.1; log values checked individually and summed against independent ln(.99). |
| 5–8 | Source arithmetic mean 0, geometric≈−.0050125629 and cumulative −.01 checked. Volatility drag is an explanatory comparison, not a forecast claim. |
| 9–11 | Independent sample variance .0001, source volatility .01 and source annualized volatility √(.0252)≈.1587450787 checked. |
| 12–13 | Linear annual mean .252 versus compounded (1.001)^252−1 explicitly derived supplementally. The source has no exported annualized-mean/growth function; these are not falsely counted as source calls. |
| 14–16 | Long-only simple-return floor, positive-price log domain and total-return adjustment conventions reviewed. Nonpositive price and bankruptcy domains executed; no dividend/corporate-action feed supplied. |
| 17–18 | Source declared left-return nearest-rank VaR .10 at alpha=.25; ceil-count ES .075 at alpha=.5. These different alpha settings are preserved, not silently compared as the same tail. |
| 19–20 | Signed VaR may be negative; source positive-return example −.01 checked. n=10, alpha=.05 uses one worst observation. No zero flooring or fractional-tail ES claimed. |
| 21–22 | Excess return .012−.002=.01 and Sharpe .01/.02=.5 independently derived; project supplements excess differences and uses exact source means/volatility. No Sharpe function exists in the listing. |
| 23–24 | Stale prices may suppress volatility; cross-asset calendars require alignment. Conceptual/data-contract review only; actual quote freshness and date joins unexecuted. |

The declared VaR is negative nearest-rank left-return quantile, which is not generally the nearest-rank (1−alpha) quantile of losses. With [−.10,−.05,.01,.02], alpha=.25, these would give .10 and .05 respectively. The manuscript now explicitly states the distinction rather than changing its declared estimator. ES averages the ceil(alpha*n) worst returns and differs from fractional-tail/interpolated estimators. Neither tail statistic establishes future coverage.

## Project step and prerequisite contracts

| Task | Executed result and scoped limit |
|---|---|
| 1 | Synthetic prices [100,110,99], fictional USD, daily labels 0–2; real dates unspecified and no dividends/splits/cash flows. |
| 2 | Source simple/log returns and log additivity checked against rational/Decimal references. |
| 3–4 | Source arithmetic/geometric/cumulative summaries retained; .1/−.1 gives mean zero but −1% compound return. |
| 5 | Separate longer synthetic returns [−.04,−.01,0,.02,.08,.01] now specified; they are not derived from the three-price fixture. Source mean .01, sample variance reference .0016, source SD .04. |
| 6 | Source annualized volatility .04√252≈.6349803147, with periods_per_year=252 recorded. Stationary uncorrelated-increment interpretation is conditional and unvalidated for real data. |
| 7 | Hypothetical same-period risk-free .001 each of six days. Supplemental arithmetic excess differences give source mean excess .009 and per-period Sharpe .225 from source mean/SD. No actual risk-free feed or benchmark alignment accepted. |
| 8 | alpha=.05 yields one-observation tail: source signed VaR=.04 and ES=.04. Extremely unstable with n=6; no flooring or robust tail-model claim. |
| 9 | Real corporate actions, quote staleness, delistings and missing dates unavailable. Manuscript now requires recording this limitation and proposing actual source checks, rather than claiming a synthetic-data audit validates real feeds. |
| 10 | Inputs, fixture hash, source/listing hashes, runtime, units, periods/year, tail convention, outputs and baseline failures retained. Corrected revision is the containing commit. |

Prerequisites: Python sequences/functions, return conventions, sample moments, quantile ranks and calendar/currency alignment. Source uses the standard library only. The project report assembly and excess-return/Sharpe arithmetic are supplemental; source functions provide the underlying metrics. Exact source execution, independent rational/Decimal benchmarks, supplemental assembly and conceptual data/model review remain separate. No bank/model approval or investment recommendation is implied.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform and F32 broader shared-input integration remain open, as do other unresolved findings. No Windows/macOS/notebook execution, exhaustive branch proof, real-data provenance, independent acceptance, tail calibration or certification. Chapter 15 now records eleven workflows and 264 local answer records reviewed. Next: Section 15.12 — Rolling Statistics.
