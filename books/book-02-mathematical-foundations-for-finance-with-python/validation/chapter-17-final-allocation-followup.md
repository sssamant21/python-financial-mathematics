# Chapter 17 — Final allocation assessment follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 17.10 portion of COV-78, plus its empty-cap-interval boundary.
**Status:** Selected executable gaps addressed; scoped runtime passed; independent review pending.

The two-sided final example now returns its equality and four inequality multipliers. At caps (0.9,0.2), the independent reference is weights (0.8,0.2), variance 0.0324, lambda -0.068 and second-cap multiplier 0.016, with other inequality multipliers zero.

The checker validates the returned certificate using Section 17.9's verifier. Omitting the second-cap multiplier fails with stationarity norm 0.016. A feasible candidate (0.9,0.1) with zero multipliers has variance 0.0351, above 0.0324, and fails stationarity. First-cap, unconstrained and both-cap regimes are also checked. The checker now depends on Section 17.9; this dependency is documented and does not create an independent generic solver.

A separate confirmed boundary defect used rounded a+b<1 to determine feasibility. With cap1=nextafter(0.5,0) and cap2=0.5, that sum rounds to one although lo=0.5 exceeds hi=cap1. The final example now rejects lo>hi before clipping. Exact caps (0.5,0.5) remain accepted.

Baseline tree: `4002ed47e19a235d0da3832b22102b572109c97f`. All 20 Chapter 17 Python files were fetched at that revision; the local snapshot replaced only Section 17.10 and its checker. Python 3.12.14/Linux: 20/20 files compiled; 10/10 check scripts exited zero with assertions enabled, code-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_17_10.py](../chapter-17/code/section_17_10.py) | `d8ea7467b09f787f12e2009137047281e77c02c0` | `137c8f83c1991c708739695b6341363b25c9e25b` |
| [check_section_17_10.py](../chapter-17/code/check_section_17_10.py) | `5aa9bd0216e57ebfd222f8d2524fe6624ca3a9ee` | `acfbc0d3ea3fd37283dbcf1147d95abe14fb748e` |
| [17.10-exercises-and-applied-problems.md](../chapter-17/17.10-exercises-and-applied-problems.md) | `f96b8e896600b85bc5d79ae92a4d914a521a2f00` | `d88fce43ca6ea343a5604565a378aa45bcc59637` |

COV-78 remains partially open for broader final LP/QP coverage and manual convexity, qualification and duality proofs. This scoped change follows the recorded full-book runtime pass. No independent approval is implied.

[Chapter 17 map](coverage-chapter-17.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
