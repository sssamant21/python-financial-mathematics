# Project 51 — inspected GitHub Actions synthetic evidence (2026-11-22)

Source: [successful workflow run 45058104641](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45058104641), tested commit `3c23b8721b0e2fa5a936438fd9cb0fa1aa4e0fbe`, Python 3.11.18 on Linux. The artifacts were downloaded and their ZIP JSON payloads actually inspected on 2026-11-22:

- [Synthetic benchmark artifact 14767933779](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45058104641/artifacts/14767933779): `benchmark-evidence.json`, 8 cases.
- [Repeated benchmark artifact 14767983612](https://github.com/sssamant21/python-financial-mathematics/actions/runs/45058104641/artifacts/14767983612): `repeated-benchmark-evidence.json` and `scaling-diagnostics.json`, 6 matched cases each, 3 repetitions.

## Independently recalculated invariants

Using Python standard-library `decimal.Decimal` with **100-digit precision**, independently recalculated the exact synthetic probability `1 - Decimal('0.75') ** n` for every row; checked the expected support counts `n + 1` (equal severity) and `2 ** n` (distinct powers-of-two severity). All 8 single-benchmark rows reconciled with `expected_states`, `peak_states`, `final_states` and `tail_probability`. All 6 repeated rows reconciled with their `analytical_tail` and expected support, and satisfied minimum ≤ median ≤ maximum traced bytes. All 6 scaling rows matched the corresponding repeated rows' states and median traced bytes. **These 20 row-level checks passed locally against the downloaded artifact payloads**; this is not an independent external audit.

| Borrowers | Equal states | Distinct states | Equal median traced peak | Distinct median traced peak |
|---:|---:|---:|---:|---:|
| 4 | 5 | 16 | 3,120 bytes | 5,120 bytes |
| 8 | 9 | 256 | 5,008 bytes | 56,112 bytes |
| 12 | 13 | 4,096 | 7,264 bytes | 986,092 bytes |

For 12 borrowers, the common event probability `P(at least one default)` was `0.968323647975921630859375`. The change in severity pattern changes support growth, not this event probability. These allocations are `tracemalloc` observations, **not RSS, a memory cap, cross-machine performance guarantee, or a production capacity estimate**.

## Validation limits

This is **historical CI artifact inspection**, not a rerun on current `main`. The 98-test current revision, upgraded Node.js 24 GitHub Actions, and new exact-revision CI are still unverified. No real default data, correlated-default calibration, licensed market data, external mathematical review, or production certification is established. The artifacts have retention deadlines (2026-12-06); this Markdown records the observed numbers without redistributing market data.

To reproduce: download the two linked ZIP artifacts before expiry, inspect their JSON, and compare against `1 - 0.75 ** n` and the stated support-count formulas at adequate Decimal precision.
