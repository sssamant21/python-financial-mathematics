# Project 51 — fresh CI artifact inspection (2026-11-23)

## Provenance

Downloaded both ZIP artifacts from [successful GitHub Actions run 45086662829](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45086662829), tested commit `3938c931d4abccfc314e197e1ed2f75afe0acca4`, on 2026-11-23 UTC.

- [Synthetic benchmark artifact 14779227714](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45086662829/artifacts/14779227714), SHA-256 digest recorded by GitHub: `7e7940ba2dadb48d782aec7b9d1ed3ec25b8e39010e74553d6100b21d32700cd`; expires 2026-12-07.
- [Repeated/scaling artifact 14779402269](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45086662829/artifacts/14779402269), GitHub SHA-256: `e3a78e9f474540f6872b648f260df63d79263d5655c8640aae275707fc39cd68`; expires 2026-12-07.

Inspected `benchmark-evidence.json`, `repeated-benchmark-evidence.json` and `scaling-diagnostics.json` from the downloaded ZIPs. All three declare synthetic-only data; reported runtime is CPython 3.11.18 on Linux.

## Independent local checks against downloaded JSON

A separate Python standard-library script using 100-digit `decimal.Decimal` precision checked:

- **8/8** benchmark rows: support sizes `n+1` for equal severities and `2**n` for distinct powers-of-two severities, reported peak/final states, and exact event probability `1 - 0.75**n`; nonnegative traced memory with final allocations no larger than peak.
- **6/6** repeated rows: exact analytical event probability, expected support, and ordered minimum/median/maximum traced allocations.
- **6/6** scaling rows: agreement with repeated-benchmark state counts and median traced allocations; consecutive within-pattern state-growth ratios.

**20/20 row-level checks passed locally.** The CI job separately reported 100/100 Project 51 tests passing. These are distinct checks, not 120 independent test cases.

| Borrowers | Equal-severity states | Distinct-severity states | Equal median traced peak (bytes) | Distinct median traced peak (bytes) |
|---:|---:|---:|---:|---:|
| 4 | 5 | 16 | 3,120 | 5,120 |
| 8 | 9 | 256 | 5,008 | 56,112 |
| 12 | 13 | 4,096 | 7,264 | 986,092 |

The single benchmark reported batch elapsed time **0.1073 seconds**; the repeated benchmark reported median batch time **0.0996 seconds** across three repetitions. These are environment-specific batch measurements, not per-scenario latency or performance guarantees. Traced allocations are Python `tracemalloc` measurements, **not** process RSS, system-wide memory, or production sizing estimates.

## Limits and next milestone

This confirms synthetic numerical evidence for the tested revision, not market-data calibration, correlated-default validation, independent mathematical review, or production readiness. The GitHub Actions Node.js 20 deprecation warning associated with `actions/upload-artifact@v5` remains unresolved. Before extending Project 51 further, investigate action compatibility; then prioritize a **distinct Project 52** with a separate quantitative research question, reproducible synthetic fixtures, and clear train/test isolation. No broker connectivity, live trading, or licensed market-data redistribution.
