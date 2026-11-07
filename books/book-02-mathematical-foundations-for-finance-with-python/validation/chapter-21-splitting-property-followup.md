# CF-04 cash-flow splitting acceptance

[Baseline](chapter-21-splitting-property-baseline.md) · [Exact failures, replay, checker correction and rerun](chapter-21-splitting-property-followup.json) · [Pinned source](https://github.com/sssamant21/python-financial-mathematics/blob/12de5ae82ef9155593bf2b97ebfd034524bef0b5/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_08.py).

CF-04 now distinguishes mathematical linearity from the actual per-term float rounding policy. Its declared domain requires exact equality of the normalized split-amount sum and merged amount, with finite discounted terms and final values. The property comparison uses an absolute rounding allowance, not bit equality or an unconditional fixed tolerance. The valuation calculation is unchanged.

All 23 final checks pass. The expanded baseline had two missing acceptance-policy observations and its replay produced identical rows. Initial runs also retained a failed checker assumption: a symmetric large positive/negative pair cancels exactly in the rational accumulator. Replacing it with unequal large terms that sum exactly to one exposed the intended cancellation case. This correction is test development, not a valuation defect.

The independent oracle evaluates discounted terms with 1000-digit Decimal arithmetic, rounds terms separately and sums represented terms exactly with Fraction. The allowance is one-half ULP per split term, one-half ULP for the merged discounted value, and one-half ULP for the final split value. The triangle-inequality explanation is conditional on correct term rounding, which the selected fixtures check against the independent oracle; no exhaustive rounding proof is claimed.

Fixtures cover continuous and effective rates, subnormals, cancellation, signed and fractional amounts, zero rate and zero date. They retain the case where individual-term overflow prevents comparison despite a finite merged value. A deliberately altered result fails the same bound. Pending plan status is preserved.

Run `python check_splitting_property.py` from `chapter-21/code` at revision `12de5ae82ef9155593bf2b97ebfd034524bef0b5`. For baseline replay, pass the baseline checkout's absolute `chapter-21/code` path to that checker. [Full candidate run](runtime-refresh-2026-11-07-r03.md). Selected COV-88 evidence only; independent review, supported platforms, release acceptance and canonical approval remain pending.
