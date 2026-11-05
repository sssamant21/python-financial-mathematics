# Section 19.2 — Integrated-rate and scaled growth range

Date: 2026-11-05. Baseline: `c040c2d5062be55b7d31fde5eedd6d17d4890496`. Corrected executable revision: `ea55f5efc6c94d8e8f64b791641c48e7a064947e`.

The original pure growth, affine-time-rate growth and proportional-withdrawal helpers failed18 of36 checks. Intermediate exponentials could overflow or underflow before multiplication by the initial amount, and large cancelling integrated-rate terms could produce NaN or a false zero exponent. A tiny initial amount times exp(1000), for example, has a finite result despite the exponential alone overflowing.

The helpers now form the complete integrated rate in exact rational arithmetic from represented inputs. A shared private routine evaluates the scaled exponential in a wide private decimal context. An exact zero integral preserves the initial value; zero initial amount is returned only after domain validation. A nonzero result rounding to zero or a nonfinite final value raises ValueError. The coarse magnitude guard is applied to the complete integral, beyond the recoverable combined binary64 input/result range. Signed initial amounts remain supported where the original growth helpers permitted them.

[Runnable checker](../chapter-19/code/check_integrated_growth_range.py) uses exact trapezoidal integration of an affine rate, separately integrated proportional rates and1600-digit scaled exponential references. All30 numerical cases and six invalid-input cases pass. [Raw evidence](chapter-19-integrated-growth-range-followup.json) retains the initial18 failures, an intermediate rerun with six remaining variable-growth failures, and the final pass. That intermediate implementation attempt had not yet replaced the affine-rate expression; it was corrected before publication.

Run the checker from chapter-19/code. All31 Chapter19 sources compiled and21 scripts passed at the pin. [V-63](runtime-refresh-2026-11-05-r5.md) includes the implementation and checker. These are selected range checks, not an all-input correct-rounding guarantee for transcendental values, independent mathematical sign-off or financial model approval.
