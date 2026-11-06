# Section 19.5 — Euler complete updates and represented time grid

Baseline `144e4b3e60c7428e8490dd6937a67bb6c2f8b402` with only the new checker overlaid: 13 of 21 checks disagreed, including schema differences for the new grid diagnostics. Corrected executable revision `c7fb27159683d94cdf41aa1f6bd8a1cb6e5bd946`: all 21 passed. The [raw log](chapter-19-euler-range-grid-followup.json) retains the initial run, identical baseline replay and corrected rerun, with both Chapter 19 blob manifests. The [original probes](chapter-19-euler-range-grid-baseline.md) are retained.

The solver rounds each ideal grid endpoint once, uses the exact difference between successive represented endpoints, and rounds only the complete affine state update. It rejects a collapsed grid before calling the derivative. Zero horizon executes no steps. The existing `step_size` is the nominal width; the result now also reports `final_time` and the minimum and maximum actual interval widths rounded to float.

The checker uses exact constant-slope integrals, hand-derived subnormal tick grids and left-rectangle sums for time-dependent slopes. It observes callback times, actual balances, genuine overflow, collapsed-grid rejection and ordinary assessment convergence. The existing Section 19.5, decay stability and time-varying forcing scripts pass. [V-84](runtime-refresh-2026-11-06-r03.md) records the full candidate Linux run.

Run [the checker](../chapter-19/code/check_euler_range_grid.py) from the book root: `python chapter-19/code/check_euler_range_grid.py`. For the baseline, overlay only that checker on the named baseline revision. This is selected COV-84 evidence; general error bounds and independent review remain open.
