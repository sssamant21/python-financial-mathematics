# Section 15.1 — scoped descriptive statistics review

Reviewed [Descriptive Statistics](../../chapter-15/15.01-descriptive-statistics.md) at `5cf0fa7533f199c91b7f8edd89f49e31a172df99`. Run `python -B review.py`. The [baseline](baseline.json) retains five failures; the [rerun](results.json) records the source hashes, exact command output and independent expectations. Three command checks, twelve existing methods and 32 additional predicates passed. The exact standard-library listing ran under the required filename, compiled and imported in isolation. No historical unique methods were added.

| Answers | Independent review |
|---|---|
| 1–7 | Sum .04 over four observations gives .01; central values 0 and .02 average to .01. Extrema are −.01 and .03, with range .04 and count four. |
| 8–14 | Pairwise squared differences sum to .004; divide by four for centered square sum .001, then by four or three for population/sample variance. Multiplying returns by 100 scales variance by 10,000. Counts are one negative, two positive and one zero. |
| 15–18 | Opposing 10% returns compound to .99 and geometric mean √.99−1. The outlier sample sums to .26 and has central values .02 and .03. Removing the extreme ends leaves those same central values. |
| 19–24 | Missing values must not become zero. A singleton has zero population variance but undefined sample variance. Scale/shift identities apply to SD; observation units and annualization interpretation must be explicit. |

All six mini-project deliverables were reviewed. The exact report matches independent rational sums and pairwise variance. Exact gross products give cumulative .040094 and geometric .00987622458. The structured supplemental audit retains inputs, report, runtime and source hashes, and explicitly marks absent dates and currency unspecified. The alternative outlier series was executed. A four-observation sample cannot support reliable tail calibration. Actual market-data adjustments, date lineage and independent acceptance remain outside scope.

**F127.** The original report could lose small integer spread or overflow before averaging, and cumulative returns could erase tiny gains or misreport positive remaining gross as complete loss. Exact intermediates and explicit range checks now govern the tested calculations. Reporting a variance beyond float range rejects the report; it does not certify arbitrarily large data. F28 and F32 remain open.
