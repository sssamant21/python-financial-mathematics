# V-109 — full Book 02 runtime refresh

Executable source `a93acb89609087281b4e1872c6420313ddf7adca`. [Raw manifest, compilation inventory and per-script results](runtime-refresh-2026-11-07-r15.json).

Fresh pinned-tree counts: **575 Python files compiled, 362/362 discovered check/test scripts exited zero, and 576 required blobs verified before and after execution**. This adds the large-period-count checker to V-108's 574/361/575 inventory. Required blobs are every Book 02 Python source and the Section 1.14 JSON fixture.

Scripts execute separately from their containing directories with assertions enabled and a 60-second timeout each. Detailed Python/Linux environment and per-script timings are retained in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. [Scoped count evidence](chapter-08-large-period-count-followup.md) preserves forty-two baseline observations, exact-source replay and 78 final passing checks.

This is one candidate Linux run, not independent mathematical review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partial; none is closed. Next: [nested-power baseline](chapter-08-nested-power-range-baseline.md).

## Reproduce

Check out the executable source revision, download the raw JSON beside the following script, and run from the repository root with Python without optimization:

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys
root = Path(".")
data = json.loads(Path("runtime-refresh-2026-11-07-r15.json").read_text())
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

[Publication verification](runtime-refresh-2026-11-07-r15-publication-verification.json).
