# Section10.6 — Deferred-annuity lab and twelve local answers

Baseline `916d1f123dd29ad5815e17e8ce2551a9ca97c030`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Twelve answer records](ANSWERS.md).

One workflow and twelve local prompts scoped. Two documented commands,28 supplemental predicates and twelve existing methods passed after F54/F55/F56 follow-up. The single Python listing was extracted verbatim as deferred_annuities.py, executed and compiled in isolation. Printed PV deferred:205.52 matches source formatting, with spaces retained in results.json. Prepared Linux CPython3.12.14, standard library only; no earlier module, data or network needed. Save/run/compile steps, exact filename and standalone imports hold.

Nine original failures remain retained; the original two commands and twelve embedded methods passed. F54 recurred in two tiny-rate PV cases, unchecked zero-rate ordinary overflow, zero deferral factor/nonzero final PV and two timeline losses (seven probes). Factors now precede monetary multiplication, and finite/nonzero checks cover ordinary, deferred, timeline and zero-rate branches. F55 recurred in a nonzero inverse payment lost to zero; the result is now rejected. F56 recurred for a large ordinary monetary PV that overflowed before a deferral discount made the final value finite. Unit annuity and deferral factors are now combined before monetary scaling; an independent exact rational sum verifies the supported final value. All nine regression cases were added within the existing invalid-input method. No historical unique methods were added. To reproduce baseline failures, place this runner at the same relative path against baseline source.

Independent Fractions sum dated payments over d+1…d+n; these verify ordinary-at-zero-delay, positive and negative delays' valuation effects, signs and explicit timeline calculations. Decimal at precision100 derives the inverse payment from a direct ten-term discounted sum over periods4…13. Source reconstruction and genuine zero-target behavior pass. These are QA oracles, not substitute implementations. Prompt1's explicit date list is a conceptual timing review supported by the original embedded timing method; this module supplies no schedule-generation API. Prompt9's monthly quote is supplemental exact rational conversion; no conversion API is present. Empty schedules remain valid, while zero-count inverse problems are rejected.

The bounded float policy rejects an unsupported individual factor even if an alternative log-space arrangement could represent the final result. Full arbitrary-domain/branch support, input-size/performance limits and arbitrary precision are not claimed. No dates/day-count/settlement calendar, contractual ledger rounding, production/investment approval, fresh installation, Windows or notebook workflow ran. F28/F32, platform and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-deferred-annuities-review/review.py
```

Next: Section10.7 formal lab and local answers.
