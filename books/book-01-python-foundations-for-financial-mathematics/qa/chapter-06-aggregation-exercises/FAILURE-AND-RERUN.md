# F36 — Section 6.7 QA variance constant

Severity: low QA harness error. Owner: QA executor. Baseline: `e2f090f789910a5dec18ffa72a7be615edbe0330`. Discovered 2026-10-30. Resolved in this scoped batch; no manuscript defect or source edit.

[Initial runner](initial-review.py) and [initial results](initial-results.json) preserve the actual first run. Both original source commands passed and all eight original methods passed. One of 27 supplemental predicates failed: the independently derived variance was Fraction(3616), while a manually entered expected constant was Fraction(4376). The other 26 predicates, including source standard deviation against a separately derived Decimal square root, passed.

Recalculation from totals [-60,0,60,120,40] and mean 32 gives deviations [-92,-32,28,88,8]. Their squared sum is 8464+1024+784+7744+64=18080; 18080/5=3616. The manuscript/source result is consistent with this derivation. Only the new QA expected constant changes from 4376 to 3616. [Corrected runner](review.py) and [final results](results.json) retain the rerun: 27/27 predicates, 2/2 commands and eight original methods pass. The initial/final runs invoke the same eight methods twice (16 invocations, eight unique existing methods), never 16 new tests.

To reproduce without replacing retained final results, run this from the repository root. It executes the unchanged initial runner with only its output directory redirected to an owned temporary directory; the original SOURCE/BOOK constants and extracted listings remain unchanged:

```python
import runpy
import tempfile
from pathlib import Path
namespace = runpy.run_path('books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-aggregation-exercises/initial-review.py')
with tempfile.TemporaryDirectory() as tmp:
    namespace['run'].__globals__['HERE'] = Path(tmp)
    failed = namespace['run']()
    assert failed is True
```

The reproduction recipe is supplied for future use; this batch retains the actual initial run and actual corrected run, not an additional claimed execution of the recipe. Expected source ValueError traces for missing inputs are intentional rejections and are not this QA failure.
