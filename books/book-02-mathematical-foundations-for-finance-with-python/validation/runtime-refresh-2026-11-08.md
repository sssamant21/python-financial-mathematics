# V-115 — full Book 02 runtime refresh

Executable revision `536dc531ca19a913507977f63df20d2cefd1f90b`. [Raw source/fixture manifest, compilation inventory and per-script results](runtime-refresh-2026-11-08.json).

Fresh pinned-tree counts: **581 Python files compiled, 368/368 discovered check/test scripts exited zero, and 582 required source/fixture Git blobs verified before and after execution**. This includes the V-114 accumulation checker and V-115 PV checker after V-113's 579/366/580 inventory. Required blobs are every Book 02 Python file and the Section 1.14 JSON fixture.

Each script ran separately from its containing directory with assertions enabled and a 60-second timeout. PYTHONOPTIMIZE was removed from subprocess environments. Actual Python/platform and timings are in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. The PV checker's complete pinned observations and raw-stdout hash are retained separately in the [93-check follow-up](chapter-08-pv-range-followup.json), matching local corrected observations. [PV report](chapter-08-pv-range-followup.md) preserves 26 baseline mismatches, an identical replay, source revisions and runnable reproduction.

All files were staged via repository reads and checked against exact Git blob hashes; a transport-added final newline was removed only when the resulting bytes matched the pinned hash. No source/fixture changed during execution. This is one candidate Linux pass, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partial; none is closed.

## Reproduce

Check out the executable revision, download the raw JSON beside this script, and run from repository root with Python without optimization:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys
e = json.loads(Path("runtime-refresh-2026-11-08.json").read_text())
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

Next: [Section 8.5 rate-shock baseline](chapter-08-rate-shock-range-baseline.md), with four independent finite/zero price-change references and pinned actual failures. Log-return, stable quotient, centered-copy, resource limits and independent-review obligations remain open.

[Publication verification](runtime-refresh-2026-11-08-publication-verification.json).
