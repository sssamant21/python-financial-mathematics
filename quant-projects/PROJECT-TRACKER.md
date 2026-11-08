# Quant Projects — Progress Tracker

| Project | Stage | Acceptance |
|---|---|---|
| 01 — Single-stock Monte Carlo | Source + initial checks published | Local numerical test review required |
| 02 — Two-stock Monte Carlo and correlation | Previously built source published | Re-run and inspect plots locally |
| 03 — Five-stock portfolio optimization | Previously tested source and checks published | Tests pass in prior local context; verify after GitHub publication |
| 04 — Historical portfolio backtesting | Code, validation, downloadable-data workflow published | Synthetic-fixture tests; live provider refresh and point-in-time market-data review outstanding |

| 05 — Regime stress and parameter stability | Synthetic-first source, tests, and documentation published | Prototype 7/7 local tests passed; follow-up risk-calibration module 6/6 local tests passed; exact GitHub revision CI and independent review pending |

| 06 — Tail risk and bootstrap uncertainty | Synthetic-first source, tests, docs and runnable CLI published | 7/7 local tests on prepared source; exact-revision CI and independent review pending |

| 07 — Multi-horizon portfolio risk | Synthetic-first implementation, documentation, and tests published | Local prototype 12/12 tests passed; published revision CI and independent review pending |

Next: verify exact published Project 05 revision in CI, assess non-overlapping calibration and licensed 2020/2022 data provenance. Project 06 block bootstrap and conditional coverage extension authored; local prototype 7/7 tests passed, exact published revision CI pending. Project 07 extension: circular moving-block horizon bootstrap helper and 10 local deterministic tests added; exact published-revision CI and integration into forecast CSV remain pending. Point-in-time provenance checklist documented. Next: integrate bootstrap forecasts with walk-forward scoring and test exact published revision, then Project 08.

Do **not** label production-certified; this is an educational research series. No live trading or broker integration.
