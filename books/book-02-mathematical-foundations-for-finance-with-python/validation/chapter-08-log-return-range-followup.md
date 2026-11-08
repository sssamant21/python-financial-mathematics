# V-117 — Section 8.5 log-return range and near-unity accuracy

Executable revision `31c777e7b1e41eaa3913a5144a69c6cb56cf914a`. [Raw baseline, identical replay and corrected observations](chapter-08-log-return-range-followup.json) · [full runtime](runtime-refresh-2026-11-08-r2.md).

All **95 checks pass**: 81 numerical price pairs and 14 invalid-input/validation-priority checks. Original source blob `49ab0874ff725e3138c4e36d6dd4f66663d9341c` at `a029e1d587ac54836bdcc639905cdbcdab1fb2ed` has **20 mismatches**, reproduced byte for byte. These are selected observed failures, not twenty distinct defects.

## Contract and independent references

The model return is ln(end/start) for positive finite represented prices. Near unity (end between half and twice start), the existing log1p((end-start)/start) arithmetic is retained. For distant prices, frexp normalizes each input and the return is log(end_mantissa/start_mantissa)+(end_exponent-start_exponent)·ln(2). The normalized ratio stays bounded, so full ratio overflow and relative-change rounding to -1 are avoided.

The independent oracle takes the Decimal logarithm of a complete price ratio at 200/400 digits. References agree including equal-price positive zero. Extreme max/min-subnormal ratios, branch boundaries at three scales, adjacent prices around normal/subnormal/power-of-two boundaries and 24 seeded positive binary64 pairs pass at 4e-15 relative tolerance with no absolute floor. Four original range failures and their four working controls are included. This is selected numerical evidence, not an exhaustive correct-rounding proof.

Under binary64/math-library assumptions, accepted results are finite: mantissas lie in [0.5,1), their ratio is bounded by 0.5 and 2, and exponent differences are bounded by 2097. The near-unity relative change stays away from -1 and infinity. Start-before-end finite/type validation and subsequent positive-price domains remain; equal prices return positive zero. Guard tests retain validation precedence even when an earlier price violates the later positivity gate.

The existing Section 8.5 suite passed before publication. The new checker then ran against exact pinned source/dependency during the full refresh; all corrected observations match the local run. Raw stdout hashes and explicit zero-sign fields preserve sign evidence. A completed-process session-ID bookkeeping error in the first wrapper is recorded separately from actual numerical failures and reruns.

## Reproduce

At the executable revision, run `python check_log_return_range.py` from `chapter-08/code`. To reproduce the baseline and its replay, download the raw JSON beside this script and run from repository root with assertions enabled:

```python
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-log-return-range-followup.json").read_text())
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
        r = subprocess.run([sys.executable, "check_log_return_range.py"], cwd=root,
                           env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

Next: [stable exponential quotient baseline](chapter-08-stable-exponential-quotient-baseline.md), with four finite-model range failures and two working controls, independent 1600/2200-digit references and pinned actual replay. Centered-copy, resource-limit and independent-review obligations remain open. Do not repeat completed log-return/rate-shock/PV/accumulation examples.

[Publication verification](runtime-refresh-2026-11-08-r2-publication-verification.json).
