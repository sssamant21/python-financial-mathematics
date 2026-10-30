# Section 6.15 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; bounded deterministic inputs and declared prevalidated kernel boundaries. Public-API experiments include comparable checks explicitly. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.15-E1

Add an intermediate size while preserving the existing correctness gate and output-boundary definitions.

**EXACT SOURCE BENCHMARK CALL**. Add size10000 by calling original benchmark(10000), retaining prepare, verify, all three boundaries, one untimed warm-up and five samples of three calls. The original unchanged main also runs sizes3,1000,100000 and is retained separately in original-benchmark.json. The intermediate case has three float64 input payloads totaling240000 bytes and one output payload80000 bytes; these are not peak RSS. All original correctness gates pass before timers. Raw samples/minima/medians and list-boundary ratio are retained; no timing value is an acceptance predicate.

## 6.15-E2

Rotate method order between experimental sessions and compare the retained samples.

**SUPPLEMENTAL ROTATED DRIVER USING ORIGINAL KERNELS/GATE**. extensions.rotated_sessions calls the original prepare/verify and kernels at size1000 in three sequential experimental sessions. Method orders are [python_lists,numpy_lists,numpy_resident], [numpy_lists,numpy_resident,python_lists], and [numpy_resident,python_lists,numpy_lists]. Every session runs the original gate first and one warm-up per method, then five samples of three calls per method. Raw samples and ratios are retained by session. These are same-process sessions, not isolated hardware runs; order rotation reduces one fixed-order bias but does not eliminate scheduling/cache/allocator/thermal effects or establish statistical significance.

## 6.15-E3

Increase calls per sample for tiny cases and report the changed protocol explicitly.

**EXACT SOURCE CHANGED-PROTOCOL BENCHMARK**. Call original benchmark(3,repeat=5,number=20), increasing calls per sample from3 to20 within the supported limit. Each retained sample remains seconds per call after dividing total by20. Compare with the unchanged original main size3 case only as separately labelled local protocols; setup timing, host interference and warmup conditions can differ. Do not merge the raw samples or interpret batch-average call times as request latency/confidence intervals. A larger calls-per-sample value beyond20 would require a deliberately changed driver, which is not introduced here.

## 6.15-E4

Add a validated public-API benchmark that charges comparable input checks to every implementation.

**EXACT SECTION 6.5 PUBLIC API + SUPPLEMENTAL VALIDATED PYTHON IMPLEMENTATION**. Benchmark an explicitly separate array-to-dictionary public boundary: three preexisting exact float64 vectors enter, and three independent arrays named opening/closing/pnl return. The original Section6.5 position_changes is loaded unchanged with file/listing hashes. Supplemental validated_python applies the same exact dtype/rank/nonempty/finiteness/equal-shape/nonnegative-price checks, strict local arithmetic signals and final finite-output checks, then scalar NumPy arithmetic and array construction. Validation and output allocation occur inside every timed call for both implementations; this avoids comparing a validated API against an unchecked P&L-only kernel. Pre-timing agreement checks every output and independent known marks/changes. Both routes reject shape mismatch, nonfinite end at zero quantity and overflow. Five samples of three calls at1000 entries are retained. This is a supplemental implementation, not manuscript replacement or a general proof of identical behavior on every extreme input; Section6.5 unittest methods are not rerun/count-added here.

## 6.15-E5

Measure a separately named resident-array implementation with a reused output buffer and state its ownership differences.

**SUPPLEMENTAL REUSED-BUFFER IMPLEMENTATION + MEASUREMENT**. resident_reused_out uses subtract(end,start,out=out) then multiply(q,out,out=out). Before timing, the controlled caller verifies writable exact float64 equal-shape out with no input alias, and gates numerical agreement. Measure it separately from original allocating numpy_resident at1000 entries with the same prevalidated resident inputs, five samples of three calls. Source inputs remain unchanged. The reused case excludes output allocation because its named boundary changes ownership/lifecycle: every call returns the same out reference and a later call overwrites earlier results held by reference. The runner explicitly demonstrates that overwrite and retains a copy when preservation is required. Do not use aliased buffers or claim drop-in independent results; wrapper overhead, temporary allocation differences and retention semantics remain visible. No speed ranking is asserted.

## 6.15-E6

Design a peak-memory experiment without interpreting element payload as whole-process memory.

**PEAK-MEMORY EXPERIMENT DESIGN ONLY — NOT EXECUTED**. Define separate isolated child-process runs per implementation and size, with a consistent lifecycle: imports/baseline, input construction, conversion if in scope, repeated eager calculation, required output retention and cleanup. Record OS/runtime/library versions, measurement provider and units, baseline and absolute peak resident memory, sampling cadence/limitations, raw samples, list/object storage, temporaries, allocator reuse and garbage-collection settings. Use fresh processes because process high-water marks cannot be reset by subtracting arbitrary later readings. Compare allocating and reused-output semantics separately. An external RSS sampler may miss brief peaks; Python allocation tracing alone does not cover all native array/backend memory. Repeat under a documented workload/retention policy and do not infer whole-process memory from nbytes, input+output sums or this timing report. This batch designs the experiment but does not measure RSS/peak allocation.

## 6.15-E7

Profile a complete local reporting workflow and estimate which fraction a kernel optimization could affect.

**SUPPLEMENTAL COMPLETE LOCAL WORKFLOW PROFILE + ORIGINAL PUBLIC API**. Generate and retain a1000-position synthetic JSON fixture with integer-valued q,start,end and stable IDs. Profile one complete local workflow: read/parse file, construct arrays, call original Section6.5 validated API, convert all outputs to lists, serialize and write the JSON report. Correct P&Ls are independently derived with Fraction arithmetic; output-file equality/IDs are checked after profiling. Retain workflow-fixture.json, workflow-output.json, full cProfile cumulative listing and measurement metadata/digests. In this single instrumented run the public API consumed about9.46% of total profile time, including its checks/allocation, not just arithmetic. That fraction is an upper bound on the fraction pure kernel optimization could affect in this observed workflow if everything else were fixed; eliminating all API time is itself unrealistic. Amdahl reasoning uses Tnew/Told=(1−f)+f/s only under the stated fixed-work assumptions. cProfile overhead, tiny durations, caches, filesystem and shared host affect this estimate; it is not a production fraction or a guaranteed end-to-end speedup. Fixture generation and independent answer validation are outside the profiled workflow; input parsing and report writing are inside.

## 6.15-E8

Explain why the measured list-boundary ratios cannot be promised to another machine or dataset.

**PERFORMANCE INTERPRETATION REVIEW ONLY**. A list-boundary ratio is Python-list median divided by NumPy-list median for this local measured workload, while the resident-array and reused-buffer cases have different representation/ownership boundaries. Another machine, interpreter/NumPy build, input size/layout/dtype, conversion policy, validation, allocation/retention, workload mix, cache/CPU/load, GC/thread settings or I/O profile can change timings and ranking. Even order-rotated local sessions do not create a universal speed promise. Keep raw evidence and correctness contracts, profile the intended application, repeat on supported target environments, report variability and avoid asserting benchmark speed thresholds in tests. No cross-machine or dataset performance guarantee is made.
