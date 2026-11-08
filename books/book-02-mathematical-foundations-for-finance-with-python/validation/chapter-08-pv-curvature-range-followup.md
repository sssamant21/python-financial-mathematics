# V-120 — Section 8.6 PV rate-curvature range

Executable revision `274ce4598c7a97d25f996a33512c1d8f5e176048`. [Raw baseline, identical replay, corrected observations and scoped Git manifest/results](chapter-08-pv-curvature-range-followup.json).

All **49 checks pass**: 32 numerical triples, 16 invalid-input/validation-priority cases and one new independence requirement. Original source blob `cb05d8a24ea6c4d47d9d2a7503f2420af6c2451b` at `79a67421b80bb7393bdc86169cad62dffa33b79f` has **22 mismatches**, replayed byte for byte. This includes final-output policy differences and one new requirement to avoid a rounded local PV helper; it is not a distinct-defect count. The [earlier six-probe screen](chapter-08-pv-curvature-range-baseline.md) remains retained.

## Complete model and independent expectation

The corrected `pv_rate_second` combines exact represented coefficient C·t² and exponent -r·t before output conversion through the existing Section 8.1 scaled evaluator. It no longer squares a horizon in float arithmetic or multiplies a rounded local PV.

The independent oracle instead evaluates the log-amplitude ln(C)+2·ln(|t|)-r·t and exponentiates at Decimal precisions 1600/2200. Both references agree, including zero signs and range classifications. Selected min-subnormal/max-float values, squared-horizon overflow/underflow, premature exponential overflow/underflow, finite curvature beside zero/unrepresentable prices, ordinary rates, algebraic zeros and true final overflow pass with 4e-15 relative tolerance and no absolute floor. Zero signs and exception types are exact. This is selected numerical evidence, not an exhaustive correct-rounding proof.

Years-first validation and then payment/rate/year finite checks and nonnegative payment/horizon domains remain. Zero payment/horizon returns the signed algebraic zero of C·t² after validation; negative-zero payment retains its sign. Nonfinite final curvature raises ValueError; finite underflow is permitted. Ordinary finite rounding may change under complete-expression evaluation. The ±10000 shared exponent bounds are conservative: the coefficient contains at most three finite nonzero binary64 factors, whose total log magnitude cannot offset such exponents into another float-range classification.

## Actual scope and limits

All **four scoped Python files compiled and two scripts passed**, with four exact Git blobs verified before/after. Scope is Section 8.1 dependency, Section 8.6, its existing reference suite (including second-difference error/order examples), and the new curvature checker. Pinned corrected observations match local results; raw stdout hashes and explicit input/output zero-sign fields retain sign evidence. Python/platform, timings and timeout are in JSON.

Fresh full-tree inventory: **586 Python files, 373 check/test scripts and 587 required source/fixture blobs**. These are inventory counts, not a new full runtime pass. [V-119](runtime-refresh-2026-11-08-r3.md) remains the latest full candidate Linux pass (585/372/586 at its earlier executable revision). This isolated helper/checker change received scoped regression validation.

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending. Local PV/first-derivative, shock, cash-flow, polynomial and sampled-second-difference range contracts are separate obligations.

## Reproduce from a Git checkout

At the executable revision, run `python check_pv_curvature_range.py` from `chapter-08/code`. Download the raw JSON beside the script below and run from repository root with assertions enabled to repeat scoped checks and the original failing source:

```python
from pathlib import Path
import hashlib, json, os, py_compile, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-pv-curvature-range-followup.json").read_text())
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
        r = subprocess.run([sys.executable, "check_pv_curvature_range.py"],
                           cwd=root, env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Next: [local Section 8.6 PV/first-derivative baseline](chapter-08-section-06-pv-baseline.md), with four actual paired probes, independent complete references and pinned replay. Other local helpers, resource limits and independent review remain open.

[Publication verification](chapter-08-pv-curvature-publication-verification.json).
