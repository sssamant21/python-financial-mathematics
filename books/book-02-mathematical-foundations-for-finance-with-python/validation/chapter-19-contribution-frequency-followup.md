# Section 19.8 — Contribution frequency convergence

Date: 2026-11-05. Unchanged implementation inspected at `91fc2035f500543aac8695628b8dba68db3ec475`. Checker revision: `b02cce8e82873fa6601ba7e098b5d8de1ef25340`; final scoped revision: `36006c921c0c005f2812e0589f2b68e64dfc17b4`.

[Runnable checker](../chapter-19/code/check_contribution_frequency.py) compares 20 actual end-period contribution balances with independent 100-digit sums of separately accumulated payments. Four signed-rate/flow families use 4, 8, 16, 32 and 64 payments. Six zero-rate/horizon controls also pass. Sixteen observed and reference error ratios approach two, confirming selected first-order convergence. With h=T/n, the leading continuous-minus-discrete gap is u*T*(exp(r*T)−1)/(2*n); both its sign and magnitude are checked. Three wrong timing/sign/limit variants are detected.

The first checker failed because its allowance was based on the small total after large signed components cancelled. The corrected allowance is 12 times the sum of component ulps, with twice that budget for differences. This is a disclosed selected-case allowance, not a general proved error bound. The numerical helper was unchanged. [Raw evidence](chapter-19-contribution-frequency-followup.json) retains the initial harness failure, corrected runs, commands and scoped source hashes. Run the checker from chapter-19/code.

The final Chapter 19 scope compiled 24 files and passed 14 scripts. [V-59](runtime-refresh-2026-11-05.md) includes these checks and the earlier applied cases. COV-84 remains partially addressed; independent review, supported platforms and release acceptance remain open.
