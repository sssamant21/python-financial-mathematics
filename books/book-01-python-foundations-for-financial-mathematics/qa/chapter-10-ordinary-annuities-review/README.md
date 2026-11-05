# Section10.4 — Ordinary-annuity lab and twelve local answers

Baseline `40095cc4c4e8e8aa1d27dc5f88f134b3dcc07d58`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Twelve answer records](ANSWERS.md).

One core workflow and twelve local prompts scoped. Two documented commands,29 supplemental predicates and twelve existing methods passed after F54 follow-up and F55/F56 fixes. The exact single Python listing was reconstructed as ordinary_annuities.py, executed and compiled in isolation. Prepared Linux CPython3.12.14, standard library only; no previous module import, external data or network. Save/run/compile prerequisites and exact filename hold; no demonstration output is expected from this suite. Eleven original failures remain retained; original twelve source methods passed even then.

- F54 follow-up: tiny-rate PV/FV returned0 for a representable .1 payment (two cases); zero-rate PV/FV and positive-rate PV returned infinity unchecked (three). Factors now precede multiplication, and all result branches share finite/nonzero-output checks.
- F55: inverse payment accepted bool,NaN and infinity targets, then returned infinity or zero after output overflow/underflow (five cases). Target/rate/count validation and explicit result range checks now cover the inverse. Legitimate zero targets and signed targets remain supported.
- F56: FV(100,−.9,1000) failed while computing an overflowing PV intermediate, although the final finite-series sum is approximately111.1111111111. Direct FV-factor computation removes that unnecessary intermediate. One original exception and corrected finite result are retained; the reference is the exact rational sum1000/9×(1−10^(−1000)).

All eleven regression cases were added within the existing invalid-rate test method; no new historical unique methods. Reproduce initial failures by running this runner at the same relative path against baseline source. F54 remains scoped to recorded cases, not an arbitrary-range promise.

Independent Fractions sum dated payments and accumulated terms, including signed payments and finite empty schedules. Decimal at precision100 derives a monthly effective conversion and an inverse payment from a direct finite discount sum; it does not reuse the source geometric formula. Prompts5/6 rate conversions are supplemental mathematical derivations because no source conversion API is supplied. Prompt1's payment dates are a conceptual timing review; no schedule-generation API is supplied in this module. Source inverse reconstruction and PV/FV reconciliation pass with unrounded values. Prompt7 has a positive count and includes the zero-rate P/n branch in the review record.

No loan amortization/cent rounding, fees, credit calendar, fresh installation, Windows or notebook validation ran. A nonrepresentable factor can still be rejected even if a differently arranged final result might be representable; exhaustive input/domain/branch support is not implied. The source remains an instructional constant-period model. F28/F32, platform and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-ordinary-annuities-review/review.py
```

Next: Section10.5 formal lab and local answers.
