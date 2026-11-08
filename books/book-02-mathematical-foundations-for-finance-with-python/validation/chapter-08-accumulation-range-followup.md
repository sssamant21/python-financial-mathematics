# V-114 — Section 8.5 accumulation scaling

Executable revision `a2de6dbfdacb2ef34d30674ee51b5509a8dc4f35`. [Raw baseline, replay, corrected observations, scoped manifest and actual script results](chapter-08-accumulation-range-followup.json).

All **137 checks pass**: 93 formula observations from 31 principal/rate/horizon triples, 39 invalid-input checks, three competing-invalid-input priority checks and two no-rounded-value-delegation checks. The original Section 8.5 blob `1ba84903bf0647de9691a329b1ba4a151601423d` at `473cfcd129fe042c9f1ddcde4a8f81c869609add` has **37 mismatches**, reproduced byte for byte. Two mismatches enforce the new direct-sensitivity implementation requirement; the total is not a count of distinct defects.

## Numerical contract and independent expectations

The three public functions now combine complete represented coefficients and exponents. Sensitivities no longer depend on a rounded accumulated value. Finite complete results survive premature exp/coefficient overflow or underflow; signed algebraic zero identities are applied after validation. A nonfinite final result raises ValueError. The principal/horizon nonnegative domains and built-in numeric/finite guards remain; rate-first/time-sensitivity and years-first/rate-sensitivity validation priorities are retained.

The implementation uses the existing Section 8.1 rational-coefficient/direct-Decimal-exp helper. The independent oracle uses log(P)+log(abs(multiplier))+r·t, then exponentiates at 1600 and 2200 digits; both references agree including zero signs. The corpus covers min-subnormal/max-float inputs, huge signed exponents, ordinary represented rates, zero horizons/rates/principals, finite derivatives beside zero or unrepresentable values, true final overflow and guards. Relative tolerance is 4e-15 with no absolute floor, plus exact zero signs/error types. This is selected numerical evidence, not an exhaustive correct-rounding proof. The shared helper's conservative exponent cutoff is valid here: a nonzero coefficient contains at most two finite binary64 factors, so its magnitude cannot offset an exponent outside ±10000.

Initial and cached-oracle outputs are byte-identical. Raw stdout SHA-256 values retain signed-zero serialization evidence. The cached checker completed locally in 15.6 seconds; each pinned scoped script has a 60-second timeout. An early report-assembly attempt ran before the scoped result file existed; assembly was rerun after the runner completed. Actual failure tracebacks and successful reruns are retained separately.

## Actual scope and fresh inventory

All **six scoped files compiled and four scripts passed**, with six exact Git blobs verified before/after: Section 8.1, Section 8.5, the existing Section 8.5 suite, exponential/logarithm range regressions and the new accumulation checker. Python/platform and per-script timings are in raw evidence. The pin's full tree contains **580 Python files, 367 check/test scripts and 581 required source/fixture blobs**. These fresh inventory counts are not a new full runtime result. [V-113](runtime-refresh-2026-11-07-r19.md) remains the latest full candidate Linux run at its earlier executable revision (579/366/580); a subsequent full refresh must include this new checker. This isolated change received scoped regression validation.

Thirty-five selected COV categories remain partial; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

## Reproduce from a repository checkout

Download the raw JSON beside this script and run from the repository root with Python assertions enabled. This stages only the six scoped Git blobs, verifies their hashes, compiles them and runs the four scripts. It then substitutes the exact original source and verifies its failing observations with the same checker.

```python
from pathlib import Path
import hashlib, json, py_compile, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-accumulation-range-followup.json").read_text())
assert __debug__
def blob(rev, path):
    return subprocess.check_output(["git", "show", rev + ":" + path])
def digest(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for entry in e["scoped"]["scope_manifest"]:
        b = blob(e["executable_source_revision"], entry["path"])
        assert digest(b) == entry["sha"]
        (root / Path(entry["path"]).name).write_bytes(b)
    def verify():
        for entry in e["scoped"]["scope_manifest"]:
            assert digest((root / Path(entry["path"]).name).read_bytes()) == entry["sha"]
    verify()
    for p in sorted(root.glob("*.py")):
        py_compile.compile(str(p), doraise=True)
        if p.name.startswith("check_"):
            subprocess.run([sys.executable, p.name], cwd=root, timeout=60, check=True)
    verify()
    source = "books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/section_8_05.py"
    original = blob(e["baseline_revision"], source)
    assert digest(original) == e["baseline_source_blob"]
    (root / "section_8_05.py").write_bytes(original)
    for p in root.glob("__pycache__/section_8_05.*"):
        p.unlink()
    result = subprocess.run([sys.executable, "check_accumulation_range.py"],
                            cwd=root, timeout=60, text=True, capture_output=True)
    assert result.returncode == 1
    assert json.loads(result.stdout) == e["baseline"]
```

Next: [PV and rate-sensitivity baseline](chapter-08-pv-range-baseline.md), with four pinned actual probe pairs and independent complete references. Rate-shock, log-return, stable quotient and centered-copy obligations remain open. Do not repeat the completed accumulation/exponential/logarithm corpus.

[Publication verification](chapter-08-accumulation-publication-verification.json).
