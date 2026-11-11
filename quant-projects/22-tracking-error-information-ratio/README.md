# Project 22 — Tracking Error and Information Ratio

**Business question:** How consistently does a portfolio differ from its benchmark? A positive average active return does not by itself establish stable outperformance.

This reproducible, standard-library Python 3.11+ lab uses **invented aligned monthly simple returns**; it never downloads or republishes market data. It is not financial advice.

## Mathematics

For matched observations, active return is `a_t = portfolio_t - benchmark_t`. The sample tracking error is `TE = sqrt(periods_per_year) * stdev_sample(a_t)`. Annualized arithmetic active return is `A = periods_per_year * mean(a_t)`; information ratio is `IR = A / TE` when TE is nonzero. This is an **ex-post arithmetic approximation**, not compounded excess wealth, a forward risk estimate, or a statistically validated skill measure.

The rolling diagnostic uses only observations inside each trailing window, with no forward observations. Its end-of-window result is descriptive, not an out-of-sample prediction. A zero-TE series reports `None` for IR rather than infinity.

## Reproduce

```bash
cd quant-projects/22-tracking-error-information-ratio
python -m unittest -v test_tracking_error.py
python -m compileall -q tracking_error.py test_tracking_error.py
python tracking_error.py
```

No third-party dependencies, market data, credentials, or trading connections.

## Guardrails and model limitations

Inputs require at least three same-frequency aligned observations, finite simple returns >= -100%, and 1–366 periods/year. Matching array lengths **does not prove timestamp alignment**: users must align by date, currency, corporate-action treatment, benchmark membership, and observation cutoffs before using real data. Missing returns must not be silently forward-filled. Ex-post tracking error is sample-sensitive; overlapping rolling windows are dependent. Arithmetic annualization is not compounded performance. Survivorship, selection bias, stale prices, fees, and changing benchmarks are outside scope.

## Validation status

Nine deterministic synthetic unit tests authored, covering zero variance, a known numerical example, negative information ratio, rolling future-mutation isolation, and invalid inputs. Hosted CI, independently reproduced runtime results, real-market calibration, and independent review remain **unverified** until executed and recorded.
