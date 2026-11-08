# V-121 — full Book 02 runtime refresh

Executable revision `5eeda11e6454396ad61cd0ea69e19ebc7c5fc38b`. [Raw source/fixture manifest, compilation inventory and per-script results](runtime-refresh-2026-11-08-r4.json).

Fresh pinned-tree counts: **587 Python files compiled, 374/374 discovered check/test scripts exited zero, and 588 required source/fixture Git blobs verified before and after execution**. This includes V-120 curvature and V-121 local PV-copy changes/checkers after V-119's 585/372/586 inventory. Required blobs are every Book 02 Python source and the Section 1.14 JSON fixture.

Each script ran separately from its containing directory with assertions enabled and a 60-second timeout. PYTHONOPTIMIZE was removed from subprocess environments. Actual Python/platform and timings are in JSON. Successful stdout is omitted; failure stdout/stderr would be retained. The local PV checker's complete pinned observations and raw stdout hash are retained separately in the [93-check follow-up](chapter-08-section-06-pv-followup.json), matching local corrected observations. [Report](chapter-08-section-06-pv-followup.md) preserves 31 baseline mismatches, an identical replay, source revisions and runnable reproduction.

All files were staged from repository reads and verified against exact Git blob hashes. A transport-added final newline was removed only when the resulting bytes matched the pinned hash. No required source/fixture changed during execution.

This is one candidate Linux run, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partially addressed; none is closed.

## Reproduce

Check out the executable revision, download the raw JSON beside this script, and run from repository root with Python assertions enabled:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys
e = json.loads(Path("runtime-refresh-2026-11-08-r4.json").read_text())
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

Next: [local Section 8.6 Taylor/exact-shock baseline](chapter-08-section-06-shock-baseline.md), with four actual probe triples and independent complete references. Product/sum, zero-sign and final-output policies remain to be reconciled. Cash-flow, polynomial, sampled-second-difference, resource and independent-review obligations remain separate.

[Publication verification](runtime-refresh-2026-11-08-r4-publication-verification.json).
