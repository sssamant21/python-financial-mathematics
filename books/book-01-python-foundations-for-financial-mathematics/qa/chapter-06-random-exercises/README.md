# Chapter 6 — Section 6.13 random-generator exercises

Based on main `c42fb1965a8febe91dc9ed310b2db9b0d0cb9ca2`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [Saved innovations](innovations.json) · [Replay manifest](replay-manifest.json)

CPython 3.12.14, NumPy 2.3.5, Linux: **2 command checks and 23 predicates passed** on the first run. Eight original methods passed once. No unexpected failure or manuscript change. Exercise records, predicates, commands, formal workflows and historical unique methods remain separate; overlapping reruns add no historical methods or workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-random-exercises/review.py
```

The runner compiles/reconstructs both original listings unchanged, executes original discovery/main, compares full demonstration stdout and retains source/listing hashes and byte equality. Supplemental orchestration calls the original generator helpers and NumPy SeedSequence/PCG64. Local equality/state/hash checks establish deterministic mechanics, not independently derived population moments or statistical quality.

A saved innovation matrix round-trips exactly through the retained JSON representation. Two checkpoint restorations replay the same local continuation; three named child tasks preserve their mapping even when serial execution order is reversed. All child checkpoints and the saved matrix replay from the serialized manifest; transforms reuse saved draws without redrawing. Factory traps and original source guard review distinguish explicit invalid-argument failure from hidden replacement streams. No live parallel workers run.

The manifest records algorithm, seed/state, request method/dtype/shape/call order, task/progress, source/artifact hashes and environment/build. It is a generated local example, not a general trusted checkpoint loader, atomic storage workflow or cross-version stream guarantee. **E7 statistical checks and E8 financial price-path assumptions are conceptual proposals only; no larger-sample test or financial simulation is executed.** Shared draws couple assumptions; different child arrays do not prove independence.

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, static checking, live parallel execution, statistical/generator-quality certification, financial calibration and independent acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact. Following unnumbered navigation text was excluded only from E8's reviewed prompt; identity/count unchanged.

**104/128 local prompts reviewed; 24 remain.** All 16 core workflows and 20 chapter-wide answers remain separate. Next: Section 6.14 local exercises.
