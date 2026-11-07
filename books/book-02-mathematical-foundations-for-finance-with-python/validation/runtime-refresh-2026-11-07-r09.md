# V-103 — full Book 02 runtime refresh

Executable source: `a6441d707337946a76e059c6cf53a5b05291afa0`. [Raw evidence, complete manifest and per-script exits/timings](runtime-refresh-2026-11-07-r09.json).

Actual fresh-tree counts: **569/569 Python files compiled; 356/356 discovered check/test scripts exited zero; 570/570 required blobs verified before and after execution**. No failed run or timeout in this refresh. Required blobs comprise every Book 02 Python source plus the Chapter 1 Section 1.14 JSON fixture. Compared with V-102, this includes two additional checkers, both corrected financial/wrapper sources and the existing regression suite.

Environment: Python 3.12.14, Linux x86_64/glibc 2.41, assertions enabled. Each script ran separately from its containing directory with a 60-second timeout. Successful stdout is omitted in raw evidence; failures would retain stdout/stderr. This is one candidate Linux environment, not a supported-platform matrix or independent mathematical review.

Selected scoped evidence: [Section 8.1 financial range](chapter-08-initial-pv-range-followup.md) (40 checks; seventeen retained baseline mismatches) and [Section 8.3 centered wrapper](chapter-08-centered-copy-followup.md) (eight checks; six baseline observations). These are separate checks and not coverage percentages or category closures. Thirty-five selected COV categories remain partially addressed; none is closed by the register.

## Reproduce

Check out the executable source revision above. Save the raw evidence JSON alongside the following script, set `root` to that checkout, and execute with Python without optimization. This reproduces the discovery, blob verification, compilation and script execution policy:

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys
root = Path(".")
data = json.loads(Path("runtime-refresh-2026-11-07-r09.json").read_text())
def verify():
    for item in data["manifest"]:
        value = (root / item["path"]).read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(value)).encode() + b"\0" + value).hexdigest()
        assert digest == item["sha"], item["path"]
assert __debug__
verify()
for item in data["manifest"]:
    source = root / item["path"]
    if source.suffix != ".py":
        continue
    py_compile.compile(str(source), doraise=True)
    if source.name.startswith(("check_", "test_")):
        subprocess.run([sys.executable, source.name], cwd=source.parent,
                       timeout=60, check=True)
verify()
```

[Next Section 8.2 baseline](chapter-08-polynomial-range-baseline.md) retains two actual failures with finite exact expectations. External reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending. [Publication verification](runtime-refresh-2026-11-07-r09-publication-verification.json).
