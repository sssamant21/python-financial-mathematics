# Project 05 — Validation record (2026-11-08)

An initial locally authored prototype failed four of seven tests due to unsupported pandas `DatetimeIndex.dayofweek.ne` usage. After replacing it with an array comparison, **7/7 local prototype tests passed**. The prototype's synthetic CLI completed 364 scored weeks and six scenarios, with illustrative wealth per $1: baseline 1.1762, zero cost 1.1851, 25-bps cost 1.1631, 50% shrinkage 1.1343.

The published implementation was streamlined from the locally tested prototype; its exact GitHub revision has **not yet been executed or independently verified**. A dedicated GitHub Actions job is the next acceptance gate. No real market data was fetched or redistributed; no production certification.

## Forecast-risk calibration extension (2026-11-08)

Added `risk_calibration.py` and `test_risk_calibration.py` with a 13-week forward realized-volatility diagnostic. **Six of six local synthetic-fixture tests passed** in Python pytest, including manual variance oracle, no-future-leakage, incomplete-tail exclusion, RMSE identity, invalid inputs and scenario separation. The published GitHub revision has not yet been independently executed; full Project 05 CI remains unconfirmed. This follow-up does not claim market-data validation or statistical independence of overlapping windows.
