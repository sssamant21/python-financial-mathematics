# Section 19.4 — Equilibrium transition range

Baseline `7610f56d32e5cf479d3651db5bf2024292f87958` with only the new checker overlaid: nine of 22 checks disagreed. Corrected executable revision `2dccee14e57ace03c2fc58a3226ff7d4d19fc7d5`: all 22 passed. The [raw log](chapter-19-equilibrium-transition-range-followup.json) retains the initial run, identical baseline replay and corrected rerun, with both Chapter 19 blob manifests. The [original probes](chapter-19-equilibrium-transition-range-baseline.md) are retained.

Mean reversion now retains the complete balance, including zero-time and equilibrium identities, scaled decay, and a tiny drift that would otherwise round away in the exponent. A genuinely negligible signed balance may round to signed zero. Half-life rejects a result outside finite float range. The Section 19.4 logistic entry point uses the shared Section 19.2 evaluator, which avoids overflowing a capacity-to-initial ratio and preserves the zero-time and equilibrium identities.

The checker uses independent high-precision weighted balances and the reciprocal logistic solution. It also exercises the actual assessment's three fields and unchanged validation flags. The ordinary Section 19.2 and 19.4 scripts pass. [V-89](runtime-refresh-2026-11-06-r08.md) records the full candidate Linux run.

Run [the checker](../chapter-19/code/check_equilibrium_transition_range.py) from the book root: `python chapter-19/code/check_equilibrium_transition_range.py`. For baseline, overlay only that checker on the named baseline revision. This is selected COV-84 evidence; general correctly rounded output and independent review remain open.
