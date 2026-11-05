# Section10.5 — Annuities-due lab and twelve local answers

Baseline `3fbb5be6d8e2e06c5bace03036048998a688abb3`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Twelve answer records](ANSWERS.md).

One workflow and twelve local prompts scoped. Two documented commands,30 supplemental predicates and twelve existing methods passed after F54/F55/F56 follow-up. The exact single listing was reconstructed as annuities_due.py, executed and compiled in isolation. Console output PV due:273.55 and FV due:364.10 matches source formatting (spaces retained in raw results). Prepared Linux CPython3.12.14, standard library only. Save/run/compile, filename and self-contained-import contracts hold; no earlier module, data or network needed.

Ten baseline failures are retained; both original commands and all twelve reference methods passed even then. F54 recurred in tiny-rate ordinary PV/due PV/due FV (three), unchecked ordinary PV/due FV zero-rate overflow (two), and timeline factor/payment underflow (two). Factors now precede payment multiplication and finite/nonzero range checks cover result branches and individual timeline terms. F55 recurred when a nonzero tiny inverse-payment target divided to zero; output range validation now rejects it. F56 recurred through an overflowing ordinary PV for a single huge time-zero payment, and an overflowing monetary intermediate before the due FV shift. Direct due PV uses payment×[1+ordinary factor(n−1)]; due FV incorporates the shift into the factor before monetary multiplication. Both finite cases now pass independent benchmarks. All ten regressions are within the existing invalid-input method; no historical unique methods were added. Reproduce failures by running the same runner against baseline source at the same relative path.

Independent exact finite rational sums check beginning-of-period PV and terminal-period FV, ordinary/due identities, negative/signed payments, long negative-rate FV and empty streams. Decimal at precision100 derives the inverse from a direct sum of ten individual discounts and an effective-monthly conversion. These are QA oracles, not replacement source implementations. Prompts1/2 are conceptual timing reviews; the source's timeline sum uses periods0…n−1 and is checked separately. Prompts8/9 conversions are supplemental derivations; no conversion API exists here. Source inverse reconstruction and genuine zero-target behavior pass.

A factor-first float implementation can still reject a factor whose monetary scaling would be representable under another arrangement; exhaustive range/branch support is not claimed. The timeline policy rejects unsupported individual factor/payment loss even if the final rounded sum might be finite. No calendar, production rounding, real contract acceptance, fresh install, Windows or notebook workflow ran. F28/F32, platform and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-annuities-due-review/review.py
```

Next: Section10.6 formal lab and local answers.
