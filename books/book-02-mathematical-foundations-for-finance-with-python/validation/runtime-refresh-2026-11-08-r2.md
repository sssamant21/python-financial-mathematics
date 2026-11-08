# V-117 — full Book 02 runtime refresh

Executable revision `31c777e7b1e41eaa3913a5144a69c6cb56cf914a`. [Raw source/fixture manifest, compilation inventory and per-script results](runtime-refresh-2026-11-08-r2.json).

Fresh pinned-tree counts: **583 Python files compiled, 370/370 discovered check/test scripts exited zero, and 584 required source/fixture Git blobs verified before and after execution**. This includes V-116 rate-shock and V-117 log-return changes and checkers after V-115's 581/368/582 inventory. Required blobs are every Book 02 Python source and the Section 1.14 JSON fixture.

Each script ran separately from its containing directory with assertions enabled and a 60-second timeout. PYTHONOPTIMIZE was removed from subprocess environments. Actual Python/platform and timings are in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. The log-return checker's complete pinned observations and raw stdout hash are retained separately in the [95-check follow-up](chapter-08-log-return-range-followup.json), matching local corrected observations. [Log-return report](chapter-08-log-return-range-followup.md) preserves 20 baseline failures, an identical replay, source revisions and runnable reproduction.

All files were staged from repository reads and verified against exact Git blob hashes. A transport-added final newline was removed only when the resulting bytes matched the pinned hash. No required source/fixture changed during execution.

This is one candidate Linux run, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none is closed.

## Reproduce

Check out the executable revision, download the raw JSON beside this script, and run from repository root with Python assertions enabled:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys
e = json.loads(Path("runtime-refresh-2026-11-08-r2.json").read_text())
assert __debug__
def verify():
    for item in e["manifest"]:
        b = Path(item["path"]).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert actual == item["sha"], item["path"]
verify()
env = dict(os.environ)
env.pop("PYTHONOPTIMIZE", None)
for item in e["manifest"]:
    p = Path(item["path"])
    if p.suffix == ".py":
        py_compile.compile(str(p), doraise=True)
        if p.name.startswith(("check_", "test_")):
            subprocess.run([sys.executable, p.name], cwd=p.parent,
                           env=env, timeout=60, check=True)
verify()
```

Next: [stable exponential quotient baseline](chapter-08-stable-exponential-quotient-baseline.md), with four finite-result failures, two working controls, independent references and pinned actual replay. Centered-copy, resource-limit and independent-review obligations remain open.

[Publication verification](runtime-refresh-2026-11-08-r2-publication-verification.json).
