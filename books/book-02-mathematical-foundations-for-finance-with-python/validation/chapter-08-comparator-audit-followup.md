# Chapter 8 — Derivative comparator audit follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 8.9 portion of COV-50.
**Status:** Selected error/acceptance gaps and nonfinite false-pass defect addressed; scoped runtime passed; independent review pending.

## Exact references and decisions

For f(x)=x^3 at x=2,h=0.25, expected first-derivative estimates are forward 13.5625, backward 10.5625, centered 12.0625 and Richardson 12; signed errors against 12 are 1.5625,-1.4375,0.0625,0. The centered second derivative is exactly 12. These dyadic cases directly assert estimates, signed/absolute errors and inclusive acceptance decisions for absolute-only, mixed and zero tolerances.

An absolute threshold of exactly 0.0625 accepts the centered estimate; nextafter(0.0625,0) rejects it. A zero analytic first derivative at the quadratic origin tests absolute-scale behavior without division by zero. Wrong analytic first/second callbacks returning zero are explicitly rejected for the cubic benchmark. Omitting the second derivative leaves its field absent.

The report now retains both tolerance settings and its asymmetric sum-rule description.

## Confirmed range defect

Finite callback values can overflow a stencil or error subtraction. Previously, a resulting infinite error could compare true against an infinite tolerance threshold. Every numerical estimate and signed error is now validated through the module's finite check; nonfinite results raise ValueError before a plausible acceptance report is returned. Tests cover overflowing first-derivative/error and second-derivative calculations. Floating-point rounding, cancellation and underflow remain outside this guard's accuracy guarantee.

## Runtime and publication

Baseline tree: `e82f7f4c018e18c81d748bbcf84c9609e836bfb6`. All 21 Chapter 8 Python files were fetched at that revision; the local snapshot replaced only Section 8.9 and its checker. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero, with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_8_09.py](../chapter-08/code/section_8_09.py) | `ef63d76915a50cc5e088afcbc830553d6350293b` | `b5d6a113fcd98ebf63a2bf0b0e08e79bdb100ce3` |
| [check_section_8_09.py](../chapter-08/code/check_section_8_09.py) | `ccadf00526e6b434fafef643c4580f4fc278b59e` | `ac89ea5c048645f83fc8d7f439b53482e30c2478` |
| [8.09-analytic-and-numerical-derivative-comparator.md](../chapter-08/8.09-analytic-and-numerical-derivative-comparator.md) | `486c3ef5988f68c0c8606c0ada8d3917b25cc638` | `bc204fd2fca0004622dbe10cb4b10c9a1dc71029` |

COV-50 remains partially open for broader model/error/tolerance cases and independent review. The comparison validates agreement with supplied callbacks, not their general correctness or differentiability. This scoped change follows the latest full-book run.

[Chapter 8 map](coverage-chapter-08.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
