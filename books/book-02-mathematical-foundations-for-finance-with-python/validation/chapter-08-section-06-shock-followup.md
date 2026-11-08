# V-122 — Local Section 8.6 Taylor and exact shocks

Executable revision `37b29e56354a02fbccb747ff0c77bbd45cd67edd`. [Raw baseline, identical replay, corrected observations and scoped manifest/results](chapter-08-section-06-shock-followup.json).

All **163 checks pass**: 93 numerical observations from 31 triples, 57 input/priority observations, ten order/control-priority checks and three complete-shock independence checks. Original source blob `e0b2bbb8f5020e687d4fa59cce25390dd66b088a` at `84edbf7fcbe0766189e06159b700d9315d4a4bfa` has **24 mismatches**, replayed byte for byte. Three enforce the new requirement to avoid separately rounded value/derivative helpers; the total also includes final-range exception-policy changes. It is not a distinct-defect count. The [earlier four-probe screen](chapter-08-section-06-shock-baseline.md) remains retained.

## Models and independent expectations

For exact represented g=t·h, the Taylor coefficients are -C·g and C·g·(g/2-1), scaled by exp(-r·t). The implementation combines these rational coefficients before final output conversion. Independently, the oracle expands the two Decimal Taylor terms, combines them and uses a log-amplitude to evaluate complete scaling at 1600/2200 digits.

The exact model change is C·[exp(-(r+h)·t)-exp(-r·t)]. Implementation factors the larger price and an exponent gap; the independent oracle subtracts two complete Decimal prices. The shifted rate and products are exact functions of represented inputs. They are not separately rounded to finite float intermediates.

Both oracle precisions agree, including zero signs. Selected cancellation at and adjacent to g=2, finite changes beside unrepresentable base values, zero factors, tiny products, extreme/shifted exponents, ordinary shocks and true final overflow pass at 4e-15 relative tolerance with no absolute floor. Zero signs/error types are exact. The exact g=2 Taylor cancellation returns positive zero; numerical stability of that approximation does not establish its accuracy for a large shock.

The nonzero second-order rational coefficient is bounded below in magnitude by 2^-5371 and above by 2^5120 for finite binary64 inputs. The lower bound follows denominator bounds for C, g and g/2-1; the upper bound follows finite input magnitudes. These bounds make the shared ±10000 exponent shortcuts conservative. This is selected numerical evidence, not an exhaustive correct-rounding proof.

## Validation, zeros and final range

Shock-before-years prevalidation is retained. Taylor order must be a built-in integer 1 or 2 and is checked before payment/rate/year validation and nonnegative payment/horizon domains. Zero factors are handled only after validation. First-order and exact zero-factor results retain the sign of -C·t·h; the second-order zero-factor result adds that signed zero to a zero with C's sign. This explicitly reconciles the earlier direct-Decimal zero-sign observations with the API's existing expm1/IEEE zero behavior.

Finite underflow is allowed; nonfinite final outputs raise ValueError. Ordinary finite roundings can change under complete-expression evaluation. The existing Section 8.6 reference/order suite passed before publication. Pinned curvature, local PV, reference/order and new shock scripts all pass. The independent-helper discriminator replaces local PV/first/second helpers with actual raising functions; corrected shocks bypass them and baseline calls are retained.

## Actual scope and inventory

All **six scoped Python files compiled and four scripts passed**, with six exact Git blobs verified before/after. Exact Python/platform, timeout, timings and stdout hashes are in JSON. Corrected pinned observations match the local run.

Fresh full-tree inventory: **588 Python files, 375 check/test scripts and 589 required source/fixture blobs**. These are inventory counts. [V-121](runtime-refresh-2026-11-08-r4.md) remains the latest full candidate Linux pass (587/374/588 at its earlier executable revision). Include this isolated helper/checker change in the next accumulated full refresh.

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

## Reproduce from a Git checkout

At the executable revision, run `python check_section_06_shocks.py` from `chapter-08/code`. Download the raw JSON beside the script below and run from repository root with assertions enabled to repeat scoped checks and baseline/replay:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-section-06-shock-followup.json").read_text())
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
    path = "books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_06.py"
    (root/"section_8_06.py").write_bytes(fetch(e["baseline_revision"], path, e["baseline_source_blob"]))
    for p in root.glob("__pycache__/section_8_06.*"):
        p.unlink()
    for attempt in range(2):
        r = subprocess.run([sys.executable, "check_section_06_shocks.py"],
                           cwd=root, env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Next: [signed cash-flow derivative baseline](chapter-08-cash-flow-derivatives-baseline.md), with five actual aggregate probes including a reordered control, independent signed references and pinned replay. Polynomial, sampled-second-difference, resource-limit and independent-review obligations remain open.

[Publication verification](chapter-08-section-06-shock-publication-verification.json).
