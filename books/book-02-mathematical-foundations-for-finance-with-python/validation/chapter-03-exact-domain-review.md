# Book 02 — Chapter 3 Exact-Domain Boundary Review

**Date:** 2026-10-28  
**Status:** Focused source review and runtime checks passed; independent review pending.

## Scope and revision

Reviewed the nine Chapter 3 implementation modules and selected existing assertions at repository revision `695f393a6c14d37973bdd0644fc5a062df6f9af7`. The runtime snapshot used the 19 Chapter 3 Python files from that revision plus the new [boundary check](../chapter-03/code/check_exact_domain_boundaries.py). No implementation changes were required by the cases examined.

## Focused cases

Six unittest cases add exact expected-value checks for:

- Discount rates arbitrarily close to -1, using a rational denominator of 10^100, and rejection at -1.
- Decreasing-profit inverse solutions: valid whole units, negative algebraic quantity and a fractional quantity outside the whole-unit range.
- Piecewise fee values at and within 1/10^100 of the threshold; the flat fee jumps while the marginal fee follows its exact segment.
- Large rational perfect-square inversion and the zero endpoint.
- Empty iterator rejection and singleton monotonicity. Both strict order conditions are vacuously true on a singleton; this is a finite-domain statement.
- Expansion cost applied only after its quantity threshold, and a zero-capacity explorer domain.

## Runtime evidence

Environment: Python 3.12.14 on Linux. Each Python file was compiled with `py_compile.compile(path, doraise=True)`. Each `check*.py` script was invoked with the same interpreter from the code directory, with captured output and a 15-second timeout.

- Compilation: 20/20 Python files passed (nine implementation modules and eleven checks).
- Script execution: 11/11 exited zero, comprising the ten numbered section checks and the new boundary script.
- New boundary suite: six unittest cases passed.

Counts describe this snapshot and these scripts, not substantive section coverage or a current book-wide run.

## Remaining work

Review manuscript derivations, exercise solutions and domain wording independently. In particular, verify that users understand whole-unit versus continuous inverse domains, singleton ordering, equally spaced grids for second differences, and finite enumeration costs for very large capacities. Exhaustive coverage, editorial/source review, cross-platform behavior and final-revision validation remain pending.

The chapter remains not certified.
