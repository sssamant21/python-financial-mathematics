# Chapter 6 — Section 6.15 performance exercises

Based on main `0796d390e6a22c541143a3fb230c41614aff03a9`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Supplemental implementations](extensions.py) · [Results](results.json)

CPython 3.12.14, NumPy 2.3.5, Linux shared host: **2 command checks and 24 predicates passed** on the first run. Eight original Section 6.15 correctness methods passed once. No unexpected failure or manuscript change. Exercise records, predicates, commands, timing experiments, formal workflows and historical unique methods remain separate; overlapping reruns add no historical methods or workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-performance-exercises/review.py
```

The runner compiles/reconstructs the two original listings unchanged, runs original discovery and the unmodified benchmark main, and retains source/listing hashes and byte equality. [Original benchmark](original-benchmark.json) is measured JSON, not literal expected stdout or a reproduction of the historical manuscript timings. All three original sizes complete with correctness gates; raw sample/minimum/median/ratio consistency is checked without a speed threshold.

[Supplemental measurements](supplemental-measurements.json) retain an original benchmark call at size10000, three rotated same-process method sessions, a tiny-case20-call protocol, a matched validated array-to-three-array API comparison, and a separately named reused-output resident experiment. The latter changes allocation/ownership and is not presented as a drop-in independent-output optimization. Public NumPy function calls use the exact Section 6.5 listing; its hashes are separate and its suite is not rerun. Supplemental Python validation/arithmetic is labelled implementation evidence. Named failures are expected contract probes, not manuscript failures.

[Workflow input](workflow-fixture.json), [output](workflow-output.json) and [cProfile listing](workflow-profile.txt) retain a complete synthetic file-to-validated-API-to-report run with1000 positions, independently checked P&Ls and matching IDs. The public API accounted for approximately **9.46%** of this instrumented run, including validation/allocation. Pure arithmetic is a subset; this is a bounded Amdahl-style observation, not a measured achievable speedup or production workload claim.

All timing records preserve raw samples and their protocol. Fixed short batches, in-process rotation, shared-host load, profiler overhead and sparse hardware context limit interpretation. timeit disables cyclic GC in its timed loops; cProfile workflow timing is a separate mechanism. Replaying the runner produces new measurements/hashes and does not reproduce timings exactly. **E6 peak-memory experiment and E8 portability interpretation are conceptual records only; peak RSS, isolated hardware/cross-machine measurements and performance guarantees remain unexecuted.**

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, static checking, arbitrary-input API equivalence, live reporting/production, external financial validation and independent acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact. Following unnumbered navigation text was excluded only from E8's reviewed prompt; identity/count unchanged.

**120/128 local prompts reviewed; 8 remain.** All 16 core workflows and 20 chapter-wide answers remain separate. Next: Section 6.16 project extension exercises.
