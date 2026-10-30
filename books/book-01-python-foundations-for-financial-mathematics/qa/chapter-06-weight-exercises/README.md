# Chapter 6 — Section 6.10 weight exercises

Based on main `e01d6e04e6324746c2c6b6e5dc6af00b117ce39d`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Results](results.json)

CPython 3.12.14, NumPy 2.3.5, Linux: **2 command checks and 32 predicates passed** on the first run. Eight original methods passed once. No unexpected failure or manuscript change. Exercise records, predicates, commands, formal workflows and historical unique methods remain separate; overlapping reruns add no historical methods or workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-weight-exercises/review.py
```

The runner reconstructs and compiles both original listings unchanged, executes original discovery/main and compares complete application stdout. Source/listing hashes and byte equality are retained. Supplemental probes exercise the original functions; independent Fraction arithmetic derives weights, cash contribution, closing-weight and subset-denominator examples, plus controlled fixed-holding/rebalanced ending values. Fixture comparisons use rtol=0, atol=1e−14 with NaNs disallowed.

Aligned permutations preserve the scalar within tolerance; mismatched identity order fails. Invalid returns on a newly added zero-value position still fail with unchanged inputs. Closing weights give a different valid numerical hypothetical, not the original interval return. The two-interval illustration calls the original one-interval function separately; signed-account, financing and holdings/rebalancing APIs remain designs only. All eight prompt scopes and prerequisites are recorded.

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, static checking, live return alignment, leveraged/financed accounts, transaction execution, general multi-interval integration, extreme-magnitude accuracy and independent acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact. Following unnumbered navigation text was excluded only from E8's reviewed prompt; identity/count unchanged.

**80/128 local prompts reviewed; 48 remain.** All 16 core workflows and 20 chapter-wide answers remain separate. Next: Section 6.11 local exercises.
