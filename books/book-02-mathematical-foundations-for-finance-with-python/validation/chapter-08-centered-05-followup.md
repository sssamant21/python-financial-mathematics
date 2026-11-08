# V-119 — Section 8.5 centered-difference copy

Executable revision `5b919e8b93caf2cd4d6f003b61f60d07bec4bd69`. [Raw baseline, identical replay, corrected observations and oracle crosschecks](chapter-08-centered-05-followup.json) · [full runtime](runtime-refresh-2026-11-08-r3.md).

All **47 checks pass**: 21 exact numerical/call-trace observations, eight perturbation-preflight observations, eight invalid callback-output checks, two original-exception-identity checks and eight input/validation-priority checks. Original source blob `21eda96c3f8b2f7cfd8488646ba2b16dec5db225` at `24957071300057f05fe26ed816c9135f906d3640` has **11 mismatches**, reproduced byte for byte. Six exercise strengthened finite/distinct-point preflight; five concern returned nonfinite estimates. These are not eleven distinct defects.

The wrapper now delegates to the existing guarded Section 8.1 helper, preserving callable-before-controls priority and default step 1e-4. Rounded perturbations must be finite and distinct from x before any callback. For valid samples, callbacks run once in x+h, then x-h order, including negative steps. Results must be finite; invalid first outputs short-circuit the second call. Original callback exceptions propagate as the same objects.

## Independently derived expectations

Numerical expectations are exact rational sampled-output differences divided by twice the represented step, followed by final float conversion. Twenty-one numerical oracles were separately crosschecked using direct Decimal subtraction/division at 1600/2200 digits, with agreeing float values, range classifications and zero signs. The JSON retains runnable crosscheck code. No expected value calls the implementation's internal helper.

The selected corpus includes max-float numerator/denominator overflow, minimum-subnormal steps, complete finite estimates, true final overflow, signed zeros/underflow, default-step identity samples, collapsed/nonfinite perturbations, output types/nonfinites, callback short circuit and exception identity. Final numeric expectations use exact float equality rather than a tolerance. The default identity estimate is the actual sampled quotient about 0.9999999999998899, not the analytic derivative 1.

Signed-zero policy follows the shared helper. A nonfinite final estimate raises ValueError. Input validation does not invoke callbacks. The explicitly strengthened preflight is distinguished from already-existing callback/input behavior in the retained observations.

The existing Section 8.5 suite passed before publication. All pinned checker observations match the local corrected run, including actual call traces and exception-identity flags. The [full runtime report](runtime-refresh-2026-11-08-r3.md) records the exact source/fixture manifest and broader regression scope. These are selected assistant checks, not independent mathematical/editorial review, supported-platform validation, release acceptance or canonical approval. Thirty-five selected COV categories remain partial; none is closed.

## Reproduce

At the executable revision, run `python check_centered_05.py` from `chapter-08/code`. Download the raw JSON beside this script and run from repository root with assertions enabled to reproduce the original failures and replay:

```python
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-centered-05-followup.json").read_text())
assert __debug__
env = dict(os.environ)
env.pop("PYTHONOPTIMIZE", None)
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name, rev, expected in e["baseline_reproduction_files"]:
        path = "books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/" + name
        b = subprocess.check_output(["git", "show", rev + ":" + path])
        assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == expected
        (root/name).write_bytes(b)
    for attempt in range(2):
        r = subprocess.run([sys.executable, "check_centered_05.py"], cwd=root,
                           env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Next: [distinct Section 8.6 PV-curvature baseline](chapter-08-pv-curvature-range-baseline.md), with six actual failures and independent complete three-factor/exponential references. Other Section 8.6 helpers, resource limits and independent review remain open. Do not repeat completed Section 8.5 examples.

[Publication verification](runtime-refresh-2026-11-08-r3-publication-verification.json).
