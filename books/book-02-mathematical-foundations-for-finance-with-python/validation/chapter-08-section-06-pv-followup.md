# V-121 — Local Section 8.6 PV and first-sensitivity range

Executable revision `5eeda11e6454396ad61cd0ea69e19ebc7c5fc38b`. [Raw baseline, identical replay and corrected observations](chapter-08-section-06-pv-followup.json) · [full runtime](runtime-refresh-2026-11-08-r4.md).

All **93 checks pass**: 64 numerical observations from 32 triples, 26 invalid-input checks, two competing-invalid-input priority checks and one new independent-sensitivity requirement. Original source blob `39268cf39d2ad15549b98a5bb6b3bb1698e2c329` at `35be44f1096e4da87ba2b75c8f87a9e903cc230a` has **31 mismatches**, reproduced byte for byte. This includes final-output policy differences and one requirement to avoid a rounded local PV helper; it is not a distinct-defect count. The [earlier four paired probes](chapter-08-section-06-pv-baseline.md) remain retained.

The local value and first derivative now combine exact represented coefficients C and -C·t with exponent -r·t through the existing Section 8.1 scaled evaluator. The independent oracle instead computes log-amplitudes and exponentiates at Decimal precisions 1600/2200; references agree including zero signs and range classifications. Selected extreme/subnormal inputs, finite sensitivity beside zero/unrepresentable PV, true final overflow, zero identities, ordinary rates and guards pass at 4e-15 relative tolerance with no absolute floor. Zero signs/error types are exact. This is selected numerical evidence, not an exhaustive rounding proof.

Value validation remains payment/rate/years; the derivative retains years-first validation followed by payment/rate/years. Payment/horizon remain nonnegative finite built-in numeric values, with signed-zero compatibility. After validation, zero factors use signed algebraic identities. Nonfinite final values/sensitivities raise ValueError; finite underflow is allowed. Ordinary finite rounding can change under complete-expression evaluation. The shared ±10000 exponent shortcut is conservative for a coefficient containing at most two finite binary64 factors.

The existing Section 8.6 reference/order suite passed before publication. The new checker ran against exact pinned source/dependency during the full refresh and all observations match the local corrected run; raw stdout hashes and explicit input/output sign fields retain zero details. The prior curvature helper/checker is also included in the full refresh. This local contract does not certify Taylor/exact shocks, signed cash-flow derivatives, polynomials or sampled-second-difference range.

## Reproduce

At the executable revision, run `python check_section_06_pv_range.py` from `chapter-08/code`. Download the raw JSON beside this script and run from repository root with assertions enabled to reproduce baseline and replay:

```python
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile
e = json.loads(Path("chapter-08-section-06-pv-followup.json").read_text())
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
        r = subprocess.run([sys.executable, "check_section_06_pv_range.py"], cwd=root,
                           env=env, timeout=60, text=True, capture_output=True)
        assert r.returncode == 1 and json.loads(r.stdout) == e["baseline"]
```

Thirty-five selected COV categories remain partially addressed; none is closed. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.

Next: [local Taylor/exact-shock baseline](chapter-08-section-06-shock-baseline.md), with four pinned probe triples, working controls and independent complete references. Product/sum, zero-sign and final-output policies require explicit reconciliation. Cash-flow, polynomial, sampled-second-difference, resource and independent-review obligations remain separate.

[Publication verification](runtime-refresh-2026-11-08-r4-publication-verification.json).
