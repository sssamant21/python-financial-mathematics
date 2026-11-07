# V-104 — full Book 02 runtime refresh

Executable source `78b09101177563c3511c1932f6a4e7469567e7bc`. [Raw manifest, compilation inventory and per-script results](runtime-refresh-2026-11-07-r10.json).

Fresh pinned tree counts: **570 Python files compiled; all 357 check/test scripts exited zero; 571 required blobs matched before and after execution**. This adds the Section 8.2 checker to V-103's 569/356/570 inventory. The manifest includes every Book 02 Python source and the Chapter 1 Section 1.14 JSON fixture.

Each script runs separately from its containing directory with assertions enabled and a 60-second timeout. This candidate Linux execution is not independent mathematical review, supported-platform validation, release acceptance or canonical approval. Detailed environment and timings are retained in JSON. Successful output is omitted; failure output would be retained. [Scoped polynomial evidence](chapter-08-polynomial-range-followup.md) retains baseline, replay and corrected observations, including the initial checker serialization failure.

## Reproduce

At the executable source revision, download the raw JSON and run the following with Python without optimization from the repository root:

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys
root = Path(".")
data = json.loads(Path("runtime-refresh-2026-11-07-r10.json").read_text())
assert __debug__
def verify():
    for entry in data["manifest"]:
        value = (root / entry["path"]).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(value)).encode() + b"\0" + value).hexdigest()
        assert actual == entry["sha"], entry["path"]
verify()
for entry in data["manifest"]:
    source = root / entry["path"]
    if source.suffix == ".py":
        py_compile.compile(str(source), doraise=True)
        if source.name.startswith(("check_", "test_")):
            subprocess.run([sys.executable, source.name], cwd=source.parent,
                           timeout=60, check=True)
verify()
```

Thirty-five selected COV categories remain partial; none is closed. Next: [financial cost output baseline](chapter-08-cost-output-baseline.md). [Publication verification](runtime-refresh-2026-11-07-r10-publication-verification.json).
