# Section 19.9 — Project depletion event range

Date: 2026-11-05. Baseline implementation: `175c27e55a4eb0d48011937661f3295363d2c890`. Corrected executable revision: `95dcc535a881a90fad323f8a2528cd2caf7f0fff`.

Four actual simulator scenarios failed initially: two near-threshold paths missed the independently known depletion time, and two extreme negative-rate paths raised before recording their finite crossing. The signed-flow project adapter now delegates withdrawal depletion to the corrected Section19.8 helper, preserving zero-balance, nonnegative-flow and future-jump precedence policies.

[Runnable checker](../chapter-19/code/check_project_depletion_range.py) derives crossing times independently and checks final status/time/balance, exact one-event depletion logs and unapplied future jumps. All four scenarios pass. An injected helper call verifies the signed-flow-to-withdrawal mapping and actual use in simulate. [Initial failures and rerun](chapter-19-project-depletion-range-followup.json) retain observations and source hashes. Run from chapter-19/code.

All36 Chapter19 files compiled and26 scripts passed at the corrected pin. [V-67](runtime-refresh-2026-11-05-r9.md) is the preceding519-file/308-script full run; the project adapter/checker are subsequent scoped evidence. Current inventory520 Python files/309 scripts is not a new full execution. Transition arithmetic, other event-range cases, independent review and release approval remain open.
