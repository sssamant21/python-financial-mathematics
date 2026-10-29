# Chapter 11 — Final-assessment nonfinite follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 11.10 final-input portion of COV-60.
**Status:** Selected missing direct rejection cases passed; implementation unchanged; independent review pending.

The final checker now directly tests its own Vector constructor with NaN,+infinity,-infinity at both coordinates for USD/share, shares and simple_return records (18 selected cases). Nonfinite vector records reject at construction; they are not passed through a bypassed constructor.

The portfolio entry point is tested with nonfinite, negative and boolean NAV, mismatched price currency, and valid finite records causing position-product, scenario-P&L or weight-normalization overflow. The existing local validators reject these cases with ValueError (TypeError for boolean NAV). The successful assessment report also serializes with nonfinite JSON values disabled and round-trips the expected scenario P&L.

This closes the selected missing direct-final-module nonfinite assertions, not all COV-60 obligations. No implementation change or test of bypassed object invariants is claimed.

Baseline tree: `7b9ee5df7c2f091b3bf260e185189b5e839de5ec`. All 21 Chapter 11 Python files were fetched at that revision; only the final checker was replaced locally. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

Published [checker](../chapter-11/code/check_section_11_10.py): commit `0b55edd9559a9250b67feced33e292e43bdf253d`; blob `b2b09746387cd48d6e5cebff56e9e0c406b9af4a`. Implementation blob remains `c3514616378f2f2cff9212ad7f5abe5037153019`.

COV-60 remains partially open for omitted exercise computations, report/rubric/manual review and broader numerical scope. This scoped checker change follows the recorded full-book run; no final grade or independent approval is granted.

[Chapter 11 map](coverage-chapter-11.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
