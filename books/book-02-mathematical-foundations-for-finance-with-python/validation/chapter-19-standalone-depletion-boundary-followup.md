# Section 19.7 — Standalone depletion-time boundaries

Baseline `575f8e472cb8e5eb0d2c62d9487d3d9f75a61cbb` with only the new checker overlaid: five of 24 checks disagreed. Corrected executable revision `08e154d93ba1c3d413ab625a6680825f5121a3e0`: all 24 passed. The [raw log](chapter-19-standalone-depletion-boundary-followup.json) retains the initial run, identical baseline replay and corrected rerun, with both Chapter 19 blob manifests. The [original probes](chapter-19-standalone-depletion-boundary-baseline.md) are retained.

The standalone helper now uses the validated Section 19.8 withdrawal-time calculation. The exact represented equilibrium threshold decides no crossing. A zero initial balance returns zero, and a positive crossing that overflows or rounds to zero raises `ValueError`. A representable subnormal time remains valid. The simulator's separate ordering, time-zero and coincidence behavior is unchanged.

The checker solves the integrating-factor equation independently at high precision, and checks the actual assessment's four standalone time fields, terminal simulation time and unchanged review flags. Cases include equality and adjacent inputs, zero-rate overflow and underflow, tiny signed rates and a finite crossing whose naive intermediate product overflows. The ordinary Section 19.7 and 19.8 checks and the jump policy checks pass.

Run [the checker](../chapter-19/code/check_standalone_depletion_boundary.py) from the book root: `python chapter-19/code/check_standalone_depletion_boundary.py`. For baseline, overlay only that checker on the named baseline revision. [V-88](runtime-refresh-2026-11-06-r07.md) records the full candidate Linux run. This is selected COV-83 evidence; arbitrary correctly rounded outputs and independent review are not established.
