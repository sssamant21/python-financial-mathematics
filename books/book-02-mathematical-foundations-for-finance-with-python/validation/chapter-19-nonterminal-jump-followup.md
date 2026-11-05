# Section 19.7 — Explicit nonterminal jump continuation

Date: 2026-11-05. Baseline: `e5cfc81a96ea8a64bdec3adedab1f11086ee753a`. Corrected executable revision: `9f2f2ae7297b44fa443a0fe70a5e2616a74a4536`.

Two of eight zero-rate policy fixtures failed initially: a negative intermediate balance was passed to the public account helper, which rejects negative initial balances. A private transition now supports signed continuation only for the simulator's explicit stop_at_depletion=False path. Terminal policy and public account input validation are unchanged.

[Runnable checker](../chapter-19/code/check_nonterminal_jump_policy.py) uses exact conservation, initial minus withdrawals plus applied jumps, for selected negative-jump, rescue and horizon paths. It distinguishes terminal clamping from nonterminal continuation and verifies the public helper's domain. All eight policy cases and the domain check pass. [Raw evidence](chapter-19-nonterminal-jump-followup.json) preserves the original failures and rerun.

Nonterminal mode is an illustrative extension of the same constant-rate linear equation, not an approved overdraft/borrowing model. It returns terminal balance and event_time=None without a separate threshold-crossing log. Real credit policy needs separate assumptions. Final Chapter 19 scope compiled26 files and passed16 scripts; [V-60](runtime-refresh-2026-11-05-r2.md) records candidate Linux execution.
