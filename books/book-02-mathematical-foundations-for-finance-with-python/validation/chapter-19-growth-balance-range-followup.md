# Section 19.8 — Continuous/discrete growth balance range

Date: 2026-11-05. Baseline: `4d803a09669ae4734a8970aabad623b346ea418f`. Corrected executable revision: `47511f620984be32b808cd5b50897fbf18eb9f19`.

The original balance helpers failed15 of31 checks. A factor could overflow or underflow before multiplication by the initial amount, and the discrete helper could lose its nominal-rate quotient or fail at a large integer frequency. Continuous growth now forms the complete integrated rate exactly. Discrete growth validates the exact periodic gross domain, retains nominal/frequency scaling through a bounded small-quotient logarithmic series or wide logarithm, and multiplies by the full integer period count before evaluation.

Both helpers delegate final scaled-exponential evaluation to the corrected Section19.2 routine. Two observed injected calls verify actual shared use. Valid zero-amount and zero-period identities occur only after domain validation; signed initial balances remain supported as before. Nonfinite final values or nonzero values rounding to zero raise ValueError.

[Runnable checker](../chapter-19/code/check_growth_balance_range.py) uses exact finite powers, independent high-precision integrated exponentials, and a justified high-frequency exponential limit for one selected1,001-digit frequency/period case. All25 numerical and six invalid-input checks pass. [Initial failures and rerun](chapter-19-growth-balance-range-followup.json) retain output, exits and scoped hashes. Run from chapter-19/code.

All33 Chapter19 files compiled and23 scripts passed. [V-65](runtime-refresh-2026-11-05-r7.md) includes this correction and the shared dependency's pinned source. These selected checks are not an all-input correctly rounded guarantee for the logarithm/exponential or financial-model approval.
