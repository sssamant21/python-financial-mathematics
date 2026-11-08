# V-119 — full Book 02 runtime refresh

Executable revision `5b919e8b93caf2cd4d6f003b61f60d07bec4bd69`. [Raw source/fixture manifest, compilation inventory and per-script results](runtime-refresh-2026-11-08-r3.json).

Fresh pinned-tree counts: **585 Python files compiled, 372/372 discovered check/test scripts exited zero, and 586 required source/fixture Git blobs verified before and after execution**. This includes V-118 stable exponential quotient and V-119 centered-copy changes/checkers after V-117's 583/370/584 inventory. Required blobs are every Book 02 Python source and the Section 1.14 JSON fixture.

Each script ran separately from its containing directory with assertions enabled and a 60-second timeout. PYTHONOPTIMIZE was removed from subprocess environments. Actual Python/platform and timings are in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. The centered-copy checker's complete pinned observations and raw stdout hash are retained separately in the [47-check follow-up](chapter-08-centered-05-followup.json), matching local corrected observations. [Report](chapter-08-centered-05-followup.md) preserves 11 baseline mismatches, an identical replay, callback traces, exact source revisions and runnable reproduction. Twenty-one numerical expectations also match independent Decimal references at 1600/2200 digits; these are crosschecks of the same numerical cases.

All files were staged from repository reads and verified against exact Git blob hashes. A transport-added final newline was removed only when the resulting bytes matched the pinned hash. No required source/fixture changed during execution.

This is one candidate Linux run, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none is closed.

## Reproduce

Check out the executable revision, download the raw JSON beside this script, and run from repository root with Python assertions enabled:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys
e = json.loads(Path("runtime-refresh-2026-11-08-r3.json").read_text())
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

Next: [Section 8.6 PV-curvature baseline](chapter-08-pv-curvature-range-baseline.md), with six actual failures and independent complete second-derivative references, replayed at the executable pin. Other Section 8.6 helpers, resource limits and independent review remain open.

[Publication verification](runtime-refresh-2026-11-08-r3-publication-verification.json).
