# Chapter 19 cumulative scope and lab command markup

Date: 2026-11-05. Inspected main: `6a393b6bb977938709ec0bd555c305b0d9d54414`. Corrected manuscript pin: `f4144ee674ed49fcbebb460426cc1986d24ba14d`.

## Confirmed manuscript changes

Section 19.10's lab previously promised Euler/RK4 diagnostics and terminal-event enforcement. Its source returns scalar terminal estimates from both steppers, calculates depletion time separately, and implements one signed jump through two analytical no-flow transitions. Its assessment supplies selected fixed-grid absolute errors; it is not the Section 19.9 simulator. The revised lab states those boundaries and links to the actual terminal-policy project. Signed balances/jumps remain permitted by the cumulative deposit helper. The Python implementation and checker are unchanged.

All ten numbered Chapter 19 manuscripts also escaped their inline working-directory backticks and bash fence delimiters. The initial static audit found no recognized bash block containing the expected two lab commands in any of the ten files. Removing those escapes yields ten recognized command blocks with twenty existing source/checker targets. A pinned re-fetch matched all ten published manuscripts. All 59 recognized local destinations in the corrected numbered manuscripts exist. This checks source markup and path existence; it does not claim rendered browser, anchor or external-link validation.

[Raw initial audit, rerun, exact blobs and runnable replay](chapter-19-cumulative-scope-command-followup.json). Save that JSON outside the checkout before selecting a historical revision. Run its `replay_javascript` text with Node.js from a clean repository root at the corrected manuscript pin. At the baseline pin it returns failure for the ten missing command fences; preserve those failures separately from numerical defects. For example, from a corrected checkout:

```bash
node -e 'const fs=require("fs");eval(JSON.parse(fs.readFileSync("books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-19-cumulative-scope-command-followup.json","utf8")).replay_javascript)'
```

To replay the baseline audit, retain the corrected JSON outside the checkout, select the inspected baseline revision, and evaluate the saved replay text there. The expected commands come from each section number and corresponding source/checker names; local targets are checked against actual paths.

## Execution blocker and numerical handoff

The command runner returned exactly: "No usable execution environment is available. Wait for an environment to become available before using this tool." Even `pwd` could not run. No new Python compilation, numerical script execution or full-book runtime is claimed. GitHub reading/writing and JavaScript static checks remained available, so the independent manuscript/navigation work proceeded. Treat the missing execution environment as a runtime blocker, not a numerical test failure.

Next: execute independent probes of the **actual Section 19.10 helpers** at the baseline before changing numerical source. The following runnable handoff is retained but **has not been executed in this batch**. Run it from `chapter-19/code` at the inspected revision and retain stdout, stderr and exit code. It derives zero-rate/equilibrium identities and separately compounds the initial/deposit contribution; it must not be reported as a completed 19.8/19.9 test. An ordinary signed-jump control verifies the documented nonterminal scope.

```python
import json, math, sys
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import section_19_10 as lab

big = sys.float_info.max
tiny = math.ulp(0.0)
rows = []
with localcontext() as ctx:
    ctx.prec = 1600
    fixtures = [
        (lab.exact_account, (big, 0, -big, 2), float(F(big)-2*F(big))),
        (lab.exact_account, (1, 1000, -1000, 1), 1.0),
        (lab.deposit_at, (tiny, 1000, 0, 0, 1), float(D(tiny)*D(1000).exp())),
        (lab.deposit_at, (big, -1000, 0, 0, 1), float(D(big)*D(-1000).exp())),
        (lab.deposit_at, (0, 0, -1, 0, 1), -1.0),
    ]
    for fn, args, expected in fixtures:
        try:
            actual = fn(*args)
            passed = math.isfinite(actual) and abs(actual-expected) <= 4*math.ulp(expected)
        except Exception as exc:
            actual = type(exc).__name__
            passed = False
        rows.append(dict(helper=fn.__name__, inputs=repr(args),
                         expected=repr(expected), actual=repr(actual), passed=passed))
print(json.dumps(rows, indent=2))
assert all(row["passed"] for row in rows)
```

Then extend to exact depletion-threshold/reciprocal references, step-range copies and observed shared-helper/report integration before any corrected pass. Establish whether jump-state representability is required separately from final-balance representability; do not silently change event/domain policy. Broader Section 19.8 end-period exponent evaluation beyond abs(rate*years)=4000 remains open.

## Coverage and runtime disposition

COV-84 receives a manuscript/source scope reconciliation, not closure or new numerical certification. COV-83's distinct project-event policy remains intact. Thirty-one selected COV categories remain partially addressed; none closed. Current pinned inventory: 522 Python files, 311 check/test scripts and 523 required source/fixture blobs. All Python blobs are unchanged from inspected main; no accumulated code change in this batch justifies another full run. V-68 remains the earlier full 521-file/310-script/522-hash result at `908a65f2cd68240d65ef70f8a86c63078660218e`; Section 19.8's later 38-file/28-script scope stays separate.

Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.
