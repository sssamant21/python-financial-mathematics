# Section 19.2 — Logistic trajectories around capacity

Date: 2026-11-05. Unchanged implementation inspected at `288d63964ef328d68d8634ea8b3ecc4cda4afdc5`. Final executable pin: `9f66a3c24a0c66a7afc6605a6ccd0b04ac334b0c`.

[Runnable checker](../chapter-19/code/check_logistic_trajectories.py) derives the solution through the reciprocal coordinate: 1/A(t)=1/K+(1/A0−1/K)exp(−r*t). Six initial states, including zero, capacity, below-capacity and above-capacity values, provide54 independently referenced trajectory points. Direction, bounds and decreasing distance to capacity are asserted, allowing equality once floating-point saturation occurs. Five split-time consistency checks and three wrong branch/frozen-state variants also pass.

The first audit passed without a helper change. [Raw evidence](chapter-19-logistic-trajectory-followup.json) retains 100-digit reference values and scoped source hashes. Run from chapter-19/code. Final Chapter19 scope compiled28 files and passed18 scripts. This is selected trajectory evidence, not all-range input/result validation or independent mathematical review.
