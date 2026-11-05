# Section 19.8 — Nominal/continuous conversion range

Date: 2026-11-05. Baseline: `676bb1910d19f52632bb4b293533681fccb14a4e`. Corrected executable revision: `29e2c8fc93087cb58cf08f641f49c58e9ac33a05`.

The original rate converters failed24 of52 checks. Dividing tiny rates by frequency could produce a rounded zero before multiplication recovered the rate scale. Large positive integer frequencies could also fail conversion to binary float even when the final rate was finite.

The helpers now form the rate/frequency quotient exactly and keep the complete scaling. For absolute quotient at most2⁻²⁶, rational series evaluate log1p(q)/q or expm1(q)/q without forming 1+q or rounding the quotient. The logarithmic relative tail is below2⁻¹⁰³ in this region; this is an approximation bound, not an all-input correctly rounded guarantee. Other finite-range cases use a private wide decimal context; coarse exponential guards cover unavoidable overflow and negative saturation. Frequency remains a positive Python integer, including the selected 1,001-digit case.

[Runnable checker](../chapter-19/code/check_rate_conversion_range.py) independently forms gross factors and 2,200-digit logarithm/exponential references. All44 numerical and eight invalid-frequency checks pass, including subnormal rates, negative-domain boundaries and large inverse conversions. [Initial failures and rerun](chapter-19-rate-conversion-range-followup.json) retain outputs, exits and scoped hashes. Run from chapter-19/code.

A negative nominal rate can correctly round to minus the frequency after exponential saturation, even though the mathematical gross factor is positive. Such a rounded nominal value cannot be inverted through the positive-gross domain; round-trip recovery is not promised at that boundary.

All32 Chapter19 files compiled and22 scripts passed. [V-64](runtime-refresh-2026-11-05-r6.md) includes the correction. Independent review, supported platforms and release approval remain pending.
