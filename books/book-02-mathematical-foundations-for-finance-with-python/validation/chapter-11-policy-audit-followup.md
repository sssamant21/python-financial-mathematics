# Chapter 11 — Exposure policy audit follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 11.9 portion of COV-59.
**Status:** Selected threshold/report gaps addressed; scoped runtime passed; independent review pending.

The policy report now records configured gross/name/NAV-gap limits and comparison tolerances. Existing decisions remain unchanged: breach requires measured value greater than cap plus 1e-10 for dimensionless exposures or 1e-8 USD for the NAV gap.

A one-asset unit-price/NAV example isolates each breach. Gross and absolute-name tests use a 0.5 cap and exercise the effective threshold and its neighboring representable values. A separately constructed NAV-gap cap makes its effective float threshold exactly one; zero holdings hit the boundary, and positive/negative 2^-52 holdings test either side without another breach. Reported limits, allowances, feasibility and exact breach lists are asserted. Reference defaults are retained and asserted.

Invalid Policy fields cover negative values, NaN and booleans for each setting; empty scenarios and wrong scenario units are also rejected. The tests document selected floating-point comparisons, not all possible cap-rounding or policy-scale behavior.

Baseline tree: `959285f8cb024e4ac418a2ff93adbf79d3b9d24f`. All 21 Chapter 11 Python files were fetched at that revision; the local snapshot replaced only Section 11.9 and its checker. Python 3.12.14/Linux: 21/21 sources compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_11_09.py](../chapter-11/code/section_11_09.py) | `08aa3c4cab45b877503377bfcfe40e7a4a66b01e` | `dd024e8c7094e7ce908beb62f8c1f834fec1887c` |
| [check_section_11_09.py](../chapter-11/code/check_section_11_09.py) | `803079a15c6968aae55fb564d0a6b744f2f04329` | `49895ab1076a48f0d2a3f753b79cbd03d4013a26` |
| [11.09-chapter-project-vectorized-portfolio-exposure-calculator.md](../chapter-11/11.09-chapter-project-vectorized-portfolio-exposure-calculator.md) | `25558c08d128e55d5d2ebe93242b764b1c996bc7` | `26ec00ccce4817bc38bebdb2f06d01ce3515d4f8` |

COV-59 remains partially open for Section 11.7's budget path, broader signed/sector policy scope, tolerance-unit review and independent review. Retained settings do not establish external policy authorization or NAV/data provenance. This scoped change follows the latest full-book run.

[Chapter 11 map](coverage-chapter-11.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
