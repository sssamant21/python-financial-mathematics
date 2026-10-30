# Chapter 6 — Section 6.12 linear-algebra exercises

Based on main `dac1146409e3a8f4cefcb1bd63de93d9d0dabcf9`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Results](results.json)

CPython 3.12.14, NumPy 2.3.5, Linux: final retained run **2 command checks and 29 predicates passed**; eight original methods passed in that run. No unexpected failure or manuscript change. An earlier passing development run preceded strengthening the normalized-formula predicate; these are overlapping reruns, not new unique methods. Exercise records, predicates, commands, formal workflows and historical unique methods remain separate.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-linear-exercises/review.py
```

The runner compiles/reconstructs the two original listings unchanged, executes discovery/main, compares full demonstration stdout and retains source/listing hashes and byte equality. Supplemental calls check manual/three-dimensional solutions, paired row and column permutations, and nonfinite coefficients. Unequal solved units make the column-order test informative. Ordinary solution comparisons use rtol/atol 1e−12 for these small fixtures; normalized formula agreement uses rtol 1e−14 and zero atol.

Rescaling records retain absolute residuals, normalization scales, normalized residuals and conditioning separately. Additional Fraction reconstruction from represented inputs/returned units distinguishes exact arithmetic residuals from the API's floating reconstruction. Zero displayed residual is not exact equation proof. Decimal-intent versus binary scaling differences are explicit. The least-squares toy is rational supplemental arithmetic plus original rectangular-input rejection; least-squares/constrained/pricing/trade models remain designs only.

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, static checking, numerical backend portability, financial scaling/materiality acceptance, least-squares/feasibility/execution integration and independent acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact. Following unnumbered navigation text was excluded only from E8's reviewed prompt; identity/count unchanged.

**96/128 local prompts reviewed; 32 remain.** All 16 core workflows and 20 chapter-wide answers remain separate. Next: Section 6.13 local exercises.
