# Section 18.13 — scoped formal performance review

Baseline `5ad0dc3066bfcca85a3c50d1aac8a538c6459851`. One workflow, forty local-answer records and twelve lab-step records reviewed. [Source](../../chapter-18/18.13-computational-performance.md) · [baseline](baseline.json) · [baseline replay](baseline-replay.json) · [corrected results](results.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-performance-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-performance-review/review.py 5ad0dc3066bfcca85a3c50d1aac8a538c6459851
```

Baseline command intentionally exits1. Three failed predicates replay identically; corrected candidate has39 passing supplemental predicates, four exact-source command records and twelve existing unique unittest methods (zero new historical methods). Commands are reference script/test suite, compile, quiet import and optional NumPy fence; supplemental predicates and workflow/answer/step records are separate. Earlier [execution checkpoint](../chapter-18-performance-checkpoint/README.md) remains historical.

## F186 — scoped validation/state correction

Initial update overflow rejected only after mutating count/mean/M2. Rejected accumulators could be left with infinities. Oversized integer observations leaked OverflowError through math.isfinite. The finite predicate now returnsFalse for oversized integers and update computes candidate state locally, committing only after finite checks. Baseline failures are two state-preservation checks and one exception-normalization check. Rejection itself for extreme finite inputs remains intentional: this float Welford example does not support arbitrary magnitudes or protect externally mutated dataclass fields. All12 existing methods unchanged. F186 resolved only for these scoped validation/transactional-update contracts; F28/F32/F165/F185 stay open.

## Independent arithmetic and performance limits

Direct Fraction sums and centered squares derive expectations independently of Welford. Model population variance200 differs from sample variance400 for [80,100,120]. Reconstructed source samples share Python RNG draws by design; this verifies arithmetic/replay, not RNG independence or nominal confidence coverage. Five supplemental timing repetitions include RNG/accumulator setup, exclude imports and retain actual median/range. These shared-environment timings establish no scalar/vectorized/GPU speedup. Three tracemalloc measurements record peak Python allocations; they exclude native arrays, RSS and other processes and do not prove general asymptotic storage. Hardware/thread control and broader statistical/platform/independent acceptance remain open. No unexecuted profiler, parallel simulation, float32 accuracy or continuous barrier claim.

## Twelve lab-step contracts

| Step | Prompt | Evidence / scoped limit |
|---|---|---|
| 1 | Payoff/target | Three-state IID payoff; E=100, population variance200; fixed N10000 source run |
| 2 | Storage | 202400000 element bytes independently computed; excludes metadata/temporaries |
| 3 | Save/environment | Reference fence extracted verbatim; Python/platform/NumPy/config retained; CPU details incomplete |
| 4 | Streaming/output | Exact source command stdout and12 methods retained |
| 5 | Partial batch | Supplemental source calls count101,batch10; last remainder1 |
| 6 | Draw-order comparison | Exact dataclass equality for four partitions, same generator and scalar order |
| 7 | Estimate/SE | Actual sample reconstructed by shared draws; independent direct centered-sum variance; z deviation descriptive only |
| 8 | Repeated timing | Five actual repetitions; median/range; fresh RNG/setup included; no representative speedup claim |
| 9 | Optional NumPy | Exact second fence executed; version/config recorded; no SE calculated by fence |
| 10 | Statistical/shared comparison | Python batched equality uses shared draws; NumPy same seed not a cross-generator sequence contract; full statistical calibration remains open |
| 11 | Reference suite | 12 existing unique methods executed, unchanged; no new historical methods |
| 12 | Limits/memory | tracemalloc observed1000/10000/100000 draws; measures Python allocations only; no total-RSS/native-NumPy or peak-all-path memory claim |

## Forty prompt-to-answer records

| Exercise | Prompt | Reviewed answer / evidence boundary |
|---|---|---|
| 1 | Work N,T | O(NT) under per-step constant work; conceptual complexity, not timing proof |
| 2 | Full storage | O(NT) elements; excludes temporaries |
| 3 | Bytes | 202400000, exact integer predicate |
| 4 | MiB | 193.023681640625; rounds193.0 |
| 5 | Overhead | Excluded; no array/native/RSS claim |
| 6 | Binary32 | 4 bytes per element; conceptual dtype size |
| 7 | Binary64 | 8 bytes per element; matches byte calculation |
| 8 | Batch count | 10 full batches for100000/10000 |
| 9 | Partial batch | 101=10*10+1; source replay covers partial last batch |
| 10 | Terminal payoff | Only current/terminal value may suffice; payoff dependent |
| 11 | Average payoff | Running sum/count suffices for specified discrete average |
| 12 | Barrier state | Running hit flag on discrete grid |
| 13 | Continuous crossings | Discrete flag can miss intra-step crossings |
| 14 | Mean | 100 for [80,100,120], exact sum oracle |
| 15 | Sample variance | 400, direct centered-square oracle |
| 16 | SE | 20/sqrt(3), not population200/3 |
| 17 | Fourfold N | IID finite-variance SE halves; formula predicate |
| 18 | Bias | More paths does not remove bias |
| 19 | Vectorization speed | Workload must be measured; no universal speedup |
| 20 | Temporary arrays | NumPy where allocates; native memory not measured here |
| 21 | Cross-library seeds | Same seed does not assert same sequence |
| 22 | Duplicate workers | Same seed/state can duplicate paths; design review only |
| 23 | Different seeds | Not proof of non-overlap/independence |
| 24 | Threads | Affect timing/reduction; NumPy config retained, no controlled thread experiment |
| 25 | Clock | Source uses perf_counter |
| 26 | Single timing | Insufficient; five supplemental repetitions retained |
| 27 | Warm-up | Initialization matters; no warm-up speed claim |
| 28 | Precision | float32 accuracy depends on tolerance; no float32 validation |
| 29 | Quantiles | Two moments do not identify quantiles: symmetric +/-1 with equal mass and {-sqrt(2),0,+sqrt(2)} with masses{1/4,1/2,1/4} both mean0/variance1; conceptual counterexample |
| 30 | M2 | Sum squared deviations; direct sample oracle confirms |
| 31 | Denominator | n-1 for sample variance |
| 32 | N=1 | Source raises ValueError; existing test covers short sample |
| 33 | Reduction order | May change low bits; shared draw replay only |
| 34 | GPU | Transfer/workload dependent; no GPU execution |
| 35 | Profiling | Find actual bottleneck; no profiler run or bottleneck claim |
| 36 | SE meaning | Sampling deviation of mean, not outcome SD |
| 37 | Variance reduction | Use independent pair/cluster units; no implementation here |
| 38 | Optional stopping | Fixed-N nominal coverage not automatic |
| 39 | Benchmark equivalence | Same output/accuracy/workload/environment criteria reviewed |
| 40 | Illustrative timing | Execution now recorded; illustration alone was not evidence |

All listed prompts have scoped records; design/conceptual reviews are not claimed as executed software. Next: Section18.14 chapter project, including shared-input integration contracts; broader acceptance remains open.
