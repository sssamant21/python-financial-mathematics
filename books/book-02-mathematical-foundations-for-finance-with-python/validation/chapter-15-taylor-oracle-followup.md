# Chapter 15 — Independent Taylor path and portfolio error follow-up

**Date:** 2026-10-29
**Scope:** Section 15.9 portion of COV-70.
**Status:** Selected oracle and report-contract gaps addressed; independent review pending.

## Independent reference derivation

For either output write \(V=cP\exp(srt)\), with \((c,s)=(1,1)\) or \((0.5,-1)\). Along the shocked-input path, use a scalar \(u\):

\[
V(u)=c(P+u\Delta P)\exp\{s(r+u\Delta r)(t+u\Delta t)\}.
\]

Let \(q=t\Delta r+r\Delta t\) and \(z=\Delta r\Delta t\). Expanding in \(u\), the first-order change at \(u=1\) is

\[
c e^{srt}(\Delta P+sPq),
\]

and the quadratic correction is

\[
c e^{srt}\left(sPz+\frac{Pq^2}{2}+s\Delta Pq\right).
\]

This path expansion avoids the engine's Jacobian, Hessians, dot product and quadratic-form helper. The checker evaluates its reference coefficients and exponential revaluation in a 60-digit Decimal context, then compares converted expected values against float results using the existing 1e-7 relative/absolute tolerance. This is an independently structured numerical oracle, not review by an independent person.

For the reference shock, \(q=0.045\) and \(z=0.005\). The first output's quadratic coefficient is \(5+1.0125+4.5=10.5125\); its second-order change is \(155.5125e^{0.1}\). The second output's correction is \(-4.24375e^{-0.1}\), giving a second-order change of \(23.25625e^{-0.1}\). Both are now directly asserted.

## Report contract and selected cases

The engine now includes signed and absolute first-/second-order portfolio errors. Portfolio signed error sums signed output errors. Portfolio absolute error takes the absolute value of that sum, so offsetting instrument errors can cancel. It does not sum absolute output errors. The manuscript now states this distinction and the four field names.

Nine scenarios check output exact/first-/second-order changes, signed and absolute output errors, portfolio Taylor changes and signed/absolute portfolio errors:
- Reference full shock and a second signed full shock at a negative base rate.
- Each of the three isolated mixed-input pairs.
- Each of the three individual input axes.
- Zero shock.

These selected cases cover contraction cross terms; they do not prove all finite inputs, convergence rates or universal approximation bounds.

## Runtime evidence

Baseline: `0c805403aa4cf7d9bbed552a151b0d5f1c51a163`. All 21 Chapter 15 Python files were fetched at that revision; the local snapshot replaced only the engine and its Section 15.9 checker.

Python 3.12.14/Linux: 21/21 files compiled with py_compile; all 11 check scripts exited zero from the chapter code directory, with assertions enabled and a 15-second per-script timeout. This includes the nine-method finite-difference boundary suite.

Three temporary in-memory mutations of the engine's quadratic-form function were each detected by the new path checks: diagonal-only contraction, doubled contraction, and omitted principal–rate pair. The original function was restored after the experiment; no mutant was published.

## Publication

| File | Commit | Blob |
|---|---|---|
| [section_15_09.py](../chapter-15/code/section_15_09.py) | `37bcbeb147694c6fece2e7b47ad677073f87b96b` | `a0349a78638e6e0d47a82766f257a8ed890d3e46` |
| [check_section_15_09.py](../chapter-15/code/check_section_15_09.py) | `b520fc74f77c2164724668ea4146046981be75bc` | `730b067eb1ae6b2cc19b552823e8f6e52c0d5089` |
| [15.09-chapter-project-multi-input-valuation-sensitivity-engine.md](../chapter-15/15.09-chapter-project-multi-input-valuation-sensitivity-engine.md) | `1d7b8df4e514d049a483e9fde7050981be4a7898` | `a6ed63338c1a7189a2e98ba12fa24e2f51241fd3` |

## Remaining disposition

The Section 15.9 nonzero contraction and portfolio error-field gaps are addressed for the stated cases. COV-70 remains partially open because final-assessment coverage and shared dependencies still need review. No independent mathematical/editorial review or canonical approval is granted. This scoped run does not replace the historical full-book runtime result.

[Chapter 15 map](coverage-chapter-15.md) · [Remediation queue](substantive-coverage-index.md) · [Progress tracker](PROGRESS.md).
