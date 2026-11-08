# V-118 — Section 8.5 stable exponential quotient

Executable revision `67cfc7f76615c8144d200c0b9478547b894fe506`. [Raw baseline, identical replay, corrected observations and scoped Git manifest/results](chapter-08-stable-exponential-quotient-followup.json).

All **66 checks pass**: 54 numerical observations and 12 invalid-input/validation-priority checks. Original source blob `25628c7427517aabaf3dc5968f4171971be6b21d` at `216d807a39ae1aa90a1ededeb376a3b20b26940c` has **23 mismatches**, replayed byte for byte. The total includes final-overflow exception-policy differences and is not a distinct-defect count.

## Model and independent reference

For nonzero h, the complete model quotient is [exp(x+h)-exp(x)]/h. The corrected helper factors exp(max(x,x+h))·[1-exp(-|h|)]/|h| and combines exact rational coefficient, exponent and gap before final conversion. The represented-input sum x+h is exact; it need not be a distinct or finite float perturbation.

The independent oracle subtracts two complete Decimal exponentials and divides by the represented step at 1600/2200 digits. References agree including positive-zero underflow. Selected tiny steps of both signs, max/min-subnormal inputs, large/cancelled exponents, finite complete results despite overflowing numerator/exponential, and genuine final overflow pass with relative tolerance 4e-15 and no absolute floor. Zero signs/error types are exact. These are selected numerical checks, not an exhaustive rounding proof.

Conservative exponent shortcuts avoid attempting enormous Decimal exponentials. A nonzero step has magnitude between the minimum subnormal and maximum float. The coefficient 1/|h| and gap factor cannot offset an exponent above 10000 into a finite binary64 quotient; below -10000 even the largest coefficient cannot rescue a nonzero output. Very negative terms below -20000 are omitted only in the independently evaluated reference where they cannot affect these selected binary64 results. The shared 1300-digit implementation retains ample precision after cancellation for a minimum-subnormal gap.

X-before-step numeric/finite validation and rejection of either signed-zero step remain. Model quotients are positive; finite underflow returns positive zero and a nonfinite final output raises ValueError. This reconciles old intermediate OverflowErrors, returned infinity and lost finite values. Ordinary finite rounding may change under complete-expression evaluation.

## Actual scope and fresh inventory

All **ten scoped Python files compiled and eight scripts passed**, with ten exact Git blobs verified before/after. The scripts are the existing Section 8.5 suite plus exponential, logarithm, accumulation, PV, rate-shock, log-return and new quotient checkers. Actual Python/platform, timings, timeout, stdout hashes and failure stderr are retained. Pinned corrected observations match the local run.

Fresh full-tree inventory is **584 Python files, 371 check/test scripts and 585 required source/fixture blobs**. These are inventory counts. [V-117](runtime-refresh-2026-11-08-r2.md) remains the latest full candidate Linux pass (583/370/584 at its earlier executable revision). This isolated helper/checker change received scoped regression validation; include it in the next accumulated full refresh.

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

## Reproduce from a Git checkout

At the executable revision, run `python check_stable_exponential_quotient.py` from `chapter-08/code`. Download the raw JSON beside the script below and run from repository root with assertions enabled to repeat all scoped checks and the failing original source:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-stable-exponential-quotient-followup.json").read_text())
assert __debug__
def fetch(rev, path, expected):
    b = subprocess.check_output(["git", "show", rev + ":" + path])
    assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == expected
    return b
env = dict(os.environ)
env.pop("PYTHONOPTIMIZE", None)
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for item in e["scoped"]["scope_manifest"]:
        (root/Path(item["path"]).name).write_bytes(
            fetch(e["executable_source_revision"], item["path"], item["sha"]))
    def verify():
        for item in e["scoped"]["scope_manifest"]:
            b = (root/Path(item["path"]).name).read_bytes()
            assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == item["sha"]
    verify()
    for p in sorted(root.glob("*.py")):
        py_compile.compile(str(p), doraise=True)
        if p.name.startswith("check_"):
            subprocess.run([sys.executable, p.name], cwd=root, env=env, timeout=60, check=True)
    verify()
    path = "books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_05.py"
    (root/"section_8_05.py").write_bytes(fetch(e["baseline_revision"], path, e["baseline_source_blob"]))
    for p in root.glob("__pycache__/section_8_05.*"):
        p.unlink()
    for attempt in range(2):
        r = subprocess.run([sys.executable, "check_stable_exponential_quotient.py"],
                           cwd=root, env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Next: [Section 8.5 centered-copy baseline](chapter-08-centered-05-baseline.md), with two actual numerical failures, two explicitly identified preflight requirements and a default-step control. Resource limits and independent review remain open. Do not repeat completed analytic Section 8.5 helpers.

[Publication verification](chapter-08-stable-exponential-quotient-publication-verification.json).
