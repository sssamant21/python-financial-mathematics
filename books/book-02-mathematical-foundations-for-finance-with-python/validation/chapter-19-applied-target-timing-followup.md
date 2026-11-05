# Section 19.10 — Applied target adjustment and deposit timing

Baseline: `46aa9c5a32f9a3293bcd7926efa4c04c984a3258`. Corrected executable revision: `62691beb94b8747787990a187ea5925eaeb9208d`.

The cumulative report now executes the two outstanding applied examples. The target adjustment uses speed 0.6, equilibrium 5,000 and initial balance 3,000. The deposit comparison fixes initial balance 1,000, continuous rate 0.05 and horizon five years; only the time of the 500 deposit changes.

[Runnable checker](../chapter-19/code/check_applied_target_and_timing.py) independently derives the target deviation path, half-life, and discounted timing comparison using 80-digit Decimal references. It compares terminal balances with separately compounded deposit contributions. All 11 observations were missing or failed initially and passed after integration. [Raw evidence](chapter-19-applied-target-timing-followup.json) retains both runs and scoped hashes. Run from chapter-19/code. All 22 Chapter 19 files compiled and 12 scripts passed; no general ODE or event-range guarantee follows.
