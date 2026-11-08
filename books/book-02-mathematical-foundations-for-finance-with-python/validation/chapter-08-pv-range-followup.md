# V-115 — Section 8.5 PV and rate-sensitivity scaling

Executable revision `536dc531ca19a913507977f63df20d2cefd1f90b`. [Raw observations, baseline replay and source references](chapter-08-pv-range-followup.json) · [full-book runtime](runtime-refresh-2026-11-08.md).

All **93 checks pass**: 64 formula observations from 32 payment/rate/horizon triples, 26 invalid-input checks, two competing-invalid-input priority checks and one direct-sensitivity requirement. Original source blob `cf3f9e07225d4b87f2b33c43bd8ab300ce40aec3` at `e7fabf3bcb43a6956461213703eb842e839d700d` has **26 mismatches**, replayed byte for byte. One enforces the new requirement to avoid multiplying an already rounded PV; the total is not a distinct defect count.

Complete represented-input formulas C·exp(-r·t) and -C·t·exp(-r·t) now combine coefficient and exponent before output conversion using the existing Section 8.1 helper. The independent oracle instead uses log(C)+log(abs(multiplier))-r·t and exponentiates at 1600/2200 digits. Both references agree, including zero signs. Selected min-subnormal/max-float, large positive/negative exponent, zero, ordinary-rate and true final-overflow cases use relative tolerance 4e-15 with no absolute floor; zero signs/error types are exact. Signed zero inputs are preserved in the runnable checker and explicit output signs/raw stdout hashes in JSON.

Finite sensitivities survive a zero or unrepresentable PV. Algebraic zero identities apply only after validation. ValueError now denotes nonfinite final outputs, replacing intermediate OverflowErrors and returned infinities/NaNs; ordinary finite rounding can also change. Finite underflow remains allowed. Payment/horizon remain nonnegative finite built-in numbers; signed rates remain accepted. Payment/rate/years priority is retained for values and years-first priority for derivatives. Zero payment does not bypass bad rate/horizon guards.

The existing Section 8.5 suite passed before publication. The new checker also ran beside the exact pinned source/dependency during the full refresh; observations match the local corrected run. The shared helper's ±10000 exponent shortcut remains conservative here because the nonzero coefficient contains at most two finite binary64 factors. This selected evidence is not an exhaustive correct-rounding proof.

## Reproduce

At the executable revision, run `python check_pv_range.py` from `chapter-08/code`. To reproduce the initial failure from a Git checkout, the following stages the exact original source/dependency and published checker, verifies Git blob hashes and compares all observations to the retained baseline. Download the raw JSON beside the script and run from repository root with assertions enabled.

```python
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-pv-range-followup.json").read_text())
assert __debug__
def git_blob(rev, path, expected):
    b = subprocess.check_output(["git", "show", rev + ":" + path])
    actual = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
    assert actual == expected
    return b
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name, ref, sha in e["baseline_reproduction_files"]:
        path = "books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/" + name
        (root/name).write_bytes(git_blob(ref, path, sha))
    for attempt in range(2):
        r = subprocess.run([sys.executable, "check_pv_range.py"], cwd=root,
                           text=True, capture_output=True, timeout=60)
        assert r.returncode == 1
        assert json.loads(r.stdout) == e["baseline"]
```

Thirty-five selected COV categories remain partially addressed; none is closed. This is assistant evidence in one candidate Linux environment, not independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval.

Next: [rate-shock baseline](chapter-08-rate-shock-range-baseline.md) with four independent complete-price-difference probes, replayed at the same executable pin. Log-return, stable quotient, centered-copy, resource-limit and independent-review obligations remain open. Do not repeat completed PV/sensitivity or accumulation examples.

[Publication verification](runtime-refresh-2026-11-08-publication-verification.json).
