# V-116 — Section 8.5 complete rate shock

Executable revision `63ff224ef85691be6a513db55f27c3f567889f76`. [Raw baseline, identical replay, corrected observations and scoped Git manifest/results](chapter-08-rate-shock-range-followup.json).

All **57 checks pass**: 36 numerical observations, 20 invalid-input/validation-order checks and one new complete-change independence requirement. Original source blob `3c383e586995712a6342be44d43dbb2367c1ffb3` at `0e8bd0fcb5d2bd3e45262569342c152afbe44f52` has **14 mismatches**, replayed byte for byte. One mismatch enforces the new requirement to avoid a rounded PV helper; these are not fourteen distinct defects.

## Model and independent reference

The corrected helper evaluates C·[exp(-(r+h)·t)-exp(-r·t)] from complete represented inputs. For positive h, it factors -C·exp(-r·t)·[1-exp(-h·t)]; for negative h, it factors C·exp(-(r+h)·t)·[1-exp(h·t)]. Exact rational coefficients/exponents/gaps feed the existing Section 8.1 scaled evaluator. The mathematical shifted rate r+h is not rounded to a float, so even an out-of-range intermediate sum can yield a finite change.

The independent oracle subtracts two complete Decimal prices at 1600 and 2200 digits; references agree including zero signs. Selected min-subnormal/max-float, both shock signs, zero-factor, huge exponent, tiny-product, ordinary, true final-overflow and exact shifted-rate cancellation cases pass with 4e-15 relative tolerance and no absolute floor; zero signs/error types are exact. This is selected numerical evidence, not an exhaustive rounding proof.

The exponent shortcuts are conservative for this input domain: nonzero C is at least the minimum subnormal and a nonzero |t·h| is at least its square. These factors cannot offset a largest price exponent above 10000 into a finite binary64 change; an exponent below -10000 cannot be rescued by a coefficient at most the maximum float. Small positive gaps are formed without float underflow; the shared 1300-digit evaluator retains precision after cancellation for gaps as small as the product of two minimum subnormals.

Years/change prevalidation, then payment/rate/year validation and nonnegative payment/horizon domains remain. After validation, zero C, t or h returns the algebraic signed zero of -C·t·h without a large product. Nonfinite final changes raise ValueError; finite underflow remains allowed. This explicitly repairs intermediate exceptions, NaNs and lost finite changes, and may change ordinary finite rounding.

## Actual scope and inventory

All **eight scoped Python files compiled and six scripts passed**, with all eight Git blobs verified before/after. The scripts are the existing Section 8.5 suite plus exponential, logarithm, accumulation, PV and new rate-shock checkers. Exact environment, timeout, timings, stdout hashes and any failure stderr are retained. Pinned corrected observations match the local run; raw stdout hashes preserve original zero representations, alongside explicit input/output zero-sign fields.

Fresh pinned full-tree inventory is **582 Python files, 369 check/test scripts and 583 required source/fixture blobs**. These counts are inventory only. [V-115](runtime-refresh-2026-11-08.md) remains the latest full candidate Linux pass (581/368/582 at its earlier executable revision). This isolated helper/checker change received scoped regression validation; include it in the next accumulated full refresh.

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

## Reproduce from a Git checkout

At the executable revision, run `python check_rate_shock_range.py` from `chapter-08/code`. To reproduce all scoped checks and the failing original source, download the raw JSON beside this script and run from repository root with assertions enabled:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-rate-shock-range-followup.json").read_text())
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
    (root/"section_8_05.py").write_bytes(fetch(
        e["baseline_revision"], path, e["baseline_source_blob"]))
    for p in root.glob("__pycache__/section_8_05.*"):
        p.unlink()
    for attempt in range(2):
        r = subprocess.run([sys.executable, "check_rate_shock_range.py"],
                           cwd=root, env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Next: [log-return range baseline](chapter-08-log-return-range-baseline.md), with four actual finite-model failures and four retained controls. Stable exponential quotient, centered copy, resource limits and independent review remain open. Do not repeat completed rate-shock/PV/accumulation examples.

[Publication verification](chapter-08-rate-shock-publication-verification.json).
