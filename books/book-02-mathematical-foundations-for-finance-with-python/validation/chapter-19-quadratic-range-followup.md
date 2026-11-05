# Section 19.2 — Quadratic growth singularity and range

Date: 2026-11-05. Baseline: `55750b5ea8864ce5e9587eb7eb2d567ed4afa79a`. Corrected executable revision: `9b4ae81bb9d057d7a904083f34f7586dcf3ec301`.

Two of22 checks failed initially. The original 1/(k*a) singularity calculation could overflow or underflow in its intermediate product, rejecting a valid time-zero balance or dividing by zero. The helper now tests 1−k*a*t exactly for the represented inputs using rational arithmetic. It rejects at/beyond the singularity and rounds the complete rational value once; an unrepresentable positive result raises ValueError.

[Runnable checker](../chapter-19/code/check_quadratic_growth_range.py) independently uses the reciprocal state 1/A(t)=1/A0−k*t, with exact rational references. Eighteen numerical cases and four invalid-input cases pass, including adjacent represented times around a singularity and extreme coefficients. [Raw evidence](chapter-19-quadratic-range-followup.json) preserves both failures and rerun. Run from chapter-19/code. All30 chapter files compiled and20 scripts passed. Independent review remains pending.
