# V-105 — full Book 02 runtime refresh

Executable source `7db1525c2f390b0eb9afa431c08648b6450737d3`. [Raw manifest and per-script results](runtime-refresh-2026-11-07-r11.json).

Fresh pinned-tree counts: **571 Python files compiled, 358/358 discovered check/test scripts exited zero, and 572 required blobs verified before and after execution**. This adds the cost-output checker to V-104's 570/357/571 inventory. Required blobs are all Book 02 Python sources and the Section 1.14 JSON fixture. All code and fixture counts derive from the pinned tree.

Scripts execute separately from their containing directories, with assertions enabled and a 60-second timeout each. Detailed Python/Linux environment and per-script timings are in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. [Scoped cost evidence](chapter-08-cost-output-followup.md) preserves four baseline mismatches, exact-source replay and all 50 corrected observations.

This is one candidate Linux run, not independent mathematical review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partial; none is closed. Next: [Section 8.4 callback baseline](chapter-08-chain-callback-baseline.md).

## Reproduce

Check out the executable source revision, download the raw JSON beside the following script and run from the repository root with Python without optimization:

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys
root = Path(".")
data = json.loads(Path("runtime-refresh-2026-11-07-r11.json").read_text())
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

[Publication verification](runtime-refresh-2026-11-07-r11-publication-verification.json).
