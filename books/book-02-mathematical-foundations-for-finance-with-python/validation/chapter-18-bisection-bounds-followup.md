# Chapter 18 — Bisection halving, error-bound and iteration-count references

**Date:** 2026-10-31  
**Checker revision:** `aa176cb320bc21daf02b18bafa4fde1ec93bbfba`  
**Unchanged implementation revision:** `4d90b8d6a3fdd397c7d071582829d5384fa410ab`

[Runnable checker](../chapter-18/code/check_bisection_bounds.py) observes actual Section18.3 objective callback points for five continuous affine objectives with independently known rational roots. Three dyadic convergence cases and one exhausted budget check every exact midpoint, width W/2^k, root containment and half-width error bound. The decimal-width case verifies Exercise10: eighteen reductions from0.2 to width at most1e-6. Its rounded endpoints use explicit one-half-ulp midpoint and two-endpoint-ulp width allowances rather than asserting exact binary halving of decimal quantities.

The count oracle independently brackets the tolerance between W/2^N and W/2^(N-1), including the exact decimal 1/5 exercise. All five paths check returned fields and exact objective-call count N+3 (two endpoints and N+1 midpoints); exhaustion is distinguished from convergence. Five altered count, width, root, status or callback records are detected. [Raw evidence](chapter-18-bisection-bounds-followup.json) retains the initial successful audit, current observed points/results, exact reference roots, command outputs, environment and source manifest. No implementation defect or initial numerical failure was found.

All **35 Chapter18 Python files compiled and25 scripts passed** at the checker revision, with scoped hashes matching the pinned tree and unchanged after execution. Run `python check_bisection_bounds.py` from chapter-18/code; raw evidence lists other commands. Current inventory is496 Python files/285 scripts; this is scoped evidence after [V-53](runtime-refresh-2026-10-31-r2.md)'s495-file/284-script full run, not a new full-book execution.

COV-79 remains partially addressed. The test uses continuous affine functions known analytically; it does not prove continuity/uniqueness for arbitrary callbacks or universal convergence in floating-point arithmetic. Independent reviewer, supported-platform and release approvals remain pending.
