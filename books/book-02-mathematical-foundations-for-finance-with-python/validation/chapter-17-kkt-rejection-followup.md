# Chapter 17 — Independent KKT rejection follow-up

**Date:** 2026-10-28 (America/New_York)
**Scope:** Section 17.9 selected COV-76 obligations.
**Status:** Selected oracle/rejection checks passed; optimizer unchanged; independent review pending.

## Reference and cases

The checker now differentiates the explicit variance polynomial x^2/25+xy/50+9y^2/100 using rational coefficients and independently reconstructs equality/inequality residuals, stationarity, complementarity products, their violation norms and objective value. Fraction arithmetic uses decimal strings of supplied candidates; comparisons retain the existing 1e-9 absolute/1e-10 relative tolerance.

Four optimized regimes are checked: first-cap binding, budget-only optimum, second-cap binding and both caps fixing the allocation. The second-cap multiplier now has an explicit 0.016 benchmark in this project check; this does not fill every separate final-assessment obligation.

Four constructed candidates isolate individual rejection reasons, with the other three norm families zero to the stated tolerance:
- Zero weights: equality/primal violation one.
- Weights (0,1), lambda -0.18 and lower-bound multiplier -0.16: dual violation 0.16.
- Weights (0.5,0.5), zero lambda/multipliers: stationarity norm 0.1.
- Weights (0.5,0.5), zero lambda and lower multipliers (0.05,0.1): complementarity norm 0.05.

Each case is rejected by the existing verifier. Temporary in-memory variants omitting each corresponding norm from acceptance were all detected. No solver or mutation was published.

## Runtime and publication

Baseline tree: `2fc787d0b975cadc21fb0f1291d282f5b185cbc6`. All 20 Chapter 17 Python files were fetched at that revision; the snapshot replaced only the Section 17.9 checker. Python 3.12.14/Linux: 20/20 files compiled and 10/10 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-17/code/check_section_17_09.py): commit `f0a61c086bea4abd22b8c144c2a197033547079f`; blob `52fe40b6735c1b5a667cd86295b60742467d9c40`. The optimizer remains at blob `bb640f580fea304ef4710c02d0558854a1b9524d`.

COV-76 remains partially open for tolerance units/scales, adjacent active-set transitions, degenerate multiplier choices and independent review. These fixed-model KKT cases are not a generic optimality certificate or proof of all constraint qualifications. This scoped checker change follows the full-book runtime record.

[Chapter 17 map](coverage-chapter-17.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
