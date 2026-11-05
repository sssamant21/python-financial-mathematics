# Sections 19.5–19.6 — Time-varying forcing references

Date: 2026-11-05. Unchanged Euler/RK4 implementation inspected at `e5cfc81a96ea8a64bdec3adedab1f11086ee753a`. Checker revision: `52dc87eab3d4c7c6c0e2d00bce344259af8af85f`. Final scoped revision: `9f2f2ae7297b44fa443a0fe70a5e2616a74a4536`.

[Runnable checker](../chapter-19/code/check_time_varying_forcing.py) runs 20 polynomial-forcing grids (t^p, p=0 through4; 1,2,4,8 steps), each with Euler and fixed RK4. Closed-form power sums independently verify Euler outputs and callback times. Exact integrals verify RK4 through cubic forcing. For quartic forcing, the signed RK4 error is h^4/120 on the unit horizon, as independently obtained from the Simpson quadrature identity. Six observed error ratios verify selected first/fourth order.

A coupled manufactured equation y'=y−t²+2t−1, y(0)=1 has solution y=1+t². At h=1/2, the checker observes all four stage states against explicit rational references and verifies the numerical result 1919/1536, rather than assuming exact integration. Three altered stage/state records are detected.

The first checker failed because it allowed ulps of the small error after subtracting rounded final values. The corrected check allows 32 ulps of the solution scale for that difference; state comparisons use16 ulps. [Raw evidence](chapter-19-time-varying-forcing-followup.json) retains the failure and rerun. The numerical helpers were unchanged. Final Chapter 19 scope compiled26 files and passed16 scripts; [V-60](runtime-refresh-2026-11-05-r2.md) includes the checker. Run from chapter-19/code. This is selected polynomial/coupled evidence, not general ODE or financial-model validation.
