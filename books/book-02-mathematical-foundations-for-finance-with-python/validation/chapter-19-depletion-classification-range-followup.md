# Section 19.8 — Depletion classification and result range

Date: 2026-11-05. Baseline: `4c35f8d4eb841aa374a17f3b6ca9de9d01a4cda0`. Corrected executable revision: `175c27e55a4eb0d48011937661f3295363d2c890`.

Seven of24 checks failed initially. A product just below the nondepletion threshold rounded to one and incorrectly returned None; extreme negative-rate products lost finite depletion times; zero-rate division could silently return zero or infinity.

The helper now classifies the complete represented-input ratio r*A/w exactly. For a valid crossing, it evaluates the exact positive logarithmic margin in wider arithmetic, or uses a bounded small-ratio series with the full A/w scaling. Zero-rate quotients have the same final-range guard. Initial-zero and no-withdrawal meanings are preserved after validation. Nonfinite times or nonzero times rounding to zero raise ValueError.

[Runnable checker](../chapter-19/code/check_depletion_classification_range.py) independently uses the reciprocal logarithmic formula log(w/(w−r*A))/r with1600-digit references, exact threshold sides and selected extreme quotients. All20 numerical and four invalid-input checks pass. [Initial failures and rerun](chapter-19-depletion-classification-range-followup.json) retain output, exits and source hashes. Run from chapter-19/code. The scope compiled35 chapter files and passed25 scripts. [V-67](runtime-refresh-2026-11-05-r9.md) includes the correction.

These are selected numerical-contract checks, not all-input correct rounding or independent mathematical sign-off. Other depletion copies retain separate domains and require their own reconciliation.
