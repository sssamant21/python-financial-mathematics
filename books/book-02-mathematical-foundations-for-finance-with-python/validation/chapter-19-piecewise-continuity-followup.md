# Section 19.3 — Piecewise transition continuity

Date: 2026-11-05. Unchanged implementation inspected at `288d63964ef328d68d8634ea8b3ecc4cda4afdc5`. Final executable pin: `9f66a3c24a0c66a7afc6605a6ccd0b04ac334b0c`.

[Runnable checker](../chapter-19/code/check_piecewise_continuity.py) independently integrates each scheduled flow against the global integrating factor, rather than composing the implementation's account primitive. Positive, zero and negative rates cover nine prefix balances, eighteen zero-duration/split-segment controls and an empty schedule. Eighteen two-sided boundary probes check independently integrated values, shrinking deviations and a declared derivative bound. The state remains continuous when the contribution rate changes; no lump-sum jump is inserted.

Three wrong schedule/timing/jump variants are rejected. The first audit passed and the numerical helper was unchanged. [Raw evidence](chapter-19-piecewise-continuity-followup.json) retains observations, exact source hashes and scoped exits. Run from chapter-19/code. Final Chapter19 scope compiled28 files and passed18 scripts. [V-61](runtime-refresh-2026-11-05-r3.md) includes this evidence. The selected 2e-11 absolute allowance and finite boundary probes are not a universal conditioning or continuity proof.
