# Chapter 17 — Financial-report range follow-up

**Date:** 2026-10-28 (America/New_York)
**Scope:** Section 17.9 financial arithmetic portion of COV-77.
**Status:** Selected range defects corrected; scoped runtime passed; independent review pending.

## Changes and reference behavior

The prior cost expression gross*cost_bps/10000 could overflow its product although the final quotient was representable. With capital 1e308, weights (1,0), current weights (0.5,0.5), and cost 10 basis points, gross is 1e308 and cost should be approximately 1e305. The report now forms the product/quotient as an exact Fraction of the represented gross and cost floats before returning a float.

Signed trades and gross traded notional are checked for finiteness; unrepresentable reported values or final cost raise OverflowError. Gross turnover now sums absolute weight changes directly, avoiding division by a possibly underflowed gross. Expected return and the fixed financial model are unchanged.

Tests cover ordinary/huge/small/subnormal capital, a large multiplier with a tiny nonzero gross, zero trades with huge capital/cost, true notional/cost overflow, and boolean capital/cost rejection. The existing independent KKT checks remain.

## Limits

The exact cost arithmetic begins with the reported rounded gross, not ideal exact trades. Individual subnormal trades can underflow to zero while dimensionless turnover remains nonzero. Float conversion can underflow a final cost. This is documented, not claimed to be exact currency accounting or an arbitrary-range ledger. The covariance/return assumptions, cost policy, capital provenance, taxes and market impact remain outside numerical validation.

## Runtime and publication

Baseline tree: `22b42b4180b864949c67384c58fb64d12218c8b9`. All 20 Chapter 17 Python files were fetched at that revision; the local snapshot replaced only the project and checker. Python 3.12.14/Linux: 20/20 sources compiled and 10/10 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_17_09.py](../chapter-17/code/section_17_09.py) | `b476d4aed70c202482e4891d9ffa821e80e478ee` | `d25f60e48864952911b7b75c142b37203181d2bb` |
| [check_section_17_09.py](../chapter-17/code/check_section_17_09.py) | `7737a7673d26c78afdd662a2be0ca40c96efbce5` | `770f5f10f71be8e0c5bc044469a8ec6255e7969f` |
| [17.09-chapter-project-constrained-allocation-decision-engine.md](../chapter-17/17.09-chapter-project-constrained-allocation-decision-engine.md) | `bbd2315c79289af04cfe8debc50962868817620e` | `17a25d42aca91ab8fdcf898062e8c9032e3eaf4b` |

This scoped change follows the recorded full-book run. COV-77 remains partially open for broader report/input/audit scope, underflow policy and independent review.

[KKT follow-up](chapter-17-kkt-rejection-followup.md) · [Chapter 17 map](coverage-chapter-17.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
