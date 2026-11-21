# V10 — Section 18.13 streaming and batch-order assumptions

Source pin: `477083a59f74be60e5e5766f4cd9ec5c8b1656b9`. [Runnable review](review.py), [first run](first.json), [replay](replay.json), [source identity](identity.json).

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-performance-order/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-performance-order/review.py replay
```

Both runs pass **1,465 predicates** with identical rows. Five native fields (count, mean, M2, sample variance, standard error) are compared against exact rational raw-sum/centered-moment references across all 243 ordered length-five paths from {80,100,120}: 1,215 fields. Another 30 fields cover six fixed-seed streaming counts; 180 fields cover six batch sizes at each count. Thirty-six exact dataclass-state comparisons confirm the selected same-generator/draw-order batch contract. Four storage/unit/partial-batch checks complete the total. Standard-error comparisons use the square root of the independent exact variance/count, with rtol 5e-14 and atol 1e-12.

The 243 paths are deterministic arithmetic cases, not equally likely observations under the native generator: the stated payoff probabilities are 1/4,1/2,1/4, so mean is 100 and variance is 200. The seeded reference separately reproduces the documented Python draw mapping and evaluates exact moments of those realized payoffs; it is not an independent RNG implementation or independence/coverage test. Counts 2,3,10,11,101,1003 and batch sizes 1,2,10,11,100,2000 cover one-element, partial, exact-divisor and oversized batches. Agreement requires the explicit serial draw and reduction order; it does not establish parallel or NumPy replay.

Each run executes the complete exact-source reference demo, its twelve existing unittest methods and compilation. Across both runs: four command records and 24 invocations of twelve existing methods. The single printed elapsed time is an actual illustrative observation, not a repeated benchmark or speedup claim. No optional NumPy, native peak-memory, parallel stream, resource-bound or supported-platform validation is newly claimed.

The entire source manuscript matches the earlier F186 review. Its three initial failed predicates, 39 corrected predicates, timing/traced-allocation observations and state/range limitations remain at their original scope. An initial observer identity assertion compared whole-source and listing hashes incorrectly; the retained identity note corrects the comparison without changing execution. No financial source change or new implementation defect is found here. Forty local answers, twelve lab steps, existing workflows and historical unique methods are not recounted.

Next: **18.14 chapter-project assumptions/integration**. V10 and Book 1 remain in progress. F28/F32/F209/F165/F185 and broader model, resource, platform, release, independent and canonical acceptance remain open.
