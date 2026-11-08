# V-110 — full Book 02 runtime refresh

Executable source `76208b8f944cf6ab706ae75f94cc0329d1f3dbfe`. [Raw manifest, compilation inventory and per-script results](runtime-refresh-2026-11-07-r16.json).

Fresh pinned-tree counts: **576 Python files compiled, 363/363 discovered check/test scripts exited zero, and 577 required blobs verified before and after execution**. This adds the nested-power checker to V-109's 575/362/576 inventory. Required blobs are every Book 02 Python source and the Section 1.14 JSON fixture.

Scripts execute separately from their containing directories with assertions enabled and a 60-second timeout each. Detailed Python/Linux environment and per-script timings are retained in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. [Scoped nested-power evidence](chapter-08-nested-power-range-followup.md) preserves seventeen baseline mismatches, exact-source replay and 45 final passing checks.

This is one candidate Linux run, not independent mathematical review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partial; none is closed. Next: [price/log-growth baseline](chapter-08-price-log-growth-baseline.md).

## Reproduce

Check out the executable source revision, download the raw JSON beside the following script, and run from the repository root with Python without optimization:

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys
root = Path(".")
data = json.loads(Path("runtime-refresh-2026-11-07-r16.json").read_text())
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

[Publication verification](runtime-refresh-2026-11-07-r16-publication-verification.json).
