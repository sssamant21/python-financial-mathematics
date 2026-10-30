# Chapter 6 — Section 6.1 local exercises

Based on main `981cca1ad232323aa43a1ff003cc35ab346dfb0f`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Four-asset caller](four_assets.py) · [Results](results.json)

CPython 3.12.14, NumPy 2.3.5, Linux: **3 command checks and 23 predicates passed**. The eight original methods passed once in the final run; earlier unchanged-source reruns overlap and do not add unique methods. Counts for eight exercise records, commands, predicates, core workflows and historical methods remain separate. No new unittest methods or historical workflow cases are claimed. Initial execution passed; a guard was added to the new caller and the same checks rerun successfully. No unexpected failures or manuscript changes.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-motivation-exercises/review.py
```

The runner reconstructs the two original source/test listings unchanged, runs the original suite/main and checks a separate four-asset caller's exact stdout. It hashes source/listings/caller and verifies original files remain byte-identical. Source API probes compare aligned and swapped prices against independent Fraction ratios and retain expected rank/missing/dtype rejection tracebacks. List repetition and ndarray multiplication are separate representation demonstrations.

Executed examples distinguish unavailable prices from genuine zero quotes, rank-zero arrays from supported vectors, and valid numeric pairing from correct instrument identity. A limited near-zero example illustrates an explicitly proposed tolerance policy; no financial materiality threshold or universal error guarantee follows. Float32 narrowing/widening probes demonstrate lost information while the source continues to reject float32 inputs. Supporting a new dtype requires a separate reviewed contract and regression evidence, not a silent cast.

The fair-benchmark and float32-support answers are designs only. This batch times no price-return implementation and cannot reuse the earlier Section 6.15 P&L ranking as evidence for it. Fresh installation, Windows/macOS, notebook/server, static checking, production and independent acceptance remain unexecuted. F28/F32 and F33–F35 history remain intact. E8's discovery record was trimmed to exclude its following unnumbered navigation sentence; its identity and the 128-prompt count are unchanged.

**8/128 local prompts reviewed; 120 remain.** All 16 core workflows and the 20 chapter-wide answers remain separate scoped records. Next: Section 6.2's eight local exercises, continuing through the existing queue. Project extensions remain separate from the completed core project checklist.
