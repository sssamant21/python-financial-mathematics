# Section 20.3 invariant lab scope follow-up

Date: 2026-11-05. Inspected main: `a269480a0cf03aeb5829b218bd3cfd7600b99204`. Corrected manuscript revision: `281fc1a142978bcd1f23af9384173945bb844b84`.

The lab promised covariance symmetry checks and an evidence manifest. The actual companion evaluates a scalar 2×2 quadratic form without checking symmetry, and emits a fixed-scenario assessment with false certification/review flags. It does not implement a covariance validator, general PSD test, orthogonality test, variable-rate curve, or a source/command/exit provenance manifest. The manuscript now states that executable subset and the remaining manual/extensions work. Its escaped command fence and working-directory markup were also corrected. Source and checker are unchanged.

An independent counterexample separates quadratic-form positivity from the missing symmetry obligation. For A=[[2,3],[-1,2]] and S=[[2,1],[1,2]], direct matrix-vector multiplication yields the same quadratic form, 2*x²+2*x*y+2*y² = x²+y²+(x+y)². S is symmetric and this expression is positive for all nonzero real vectors. A is nonsymmetric and therefore is not a real covariance matrix, despite having that same positive quadratic form. Algebraically the skew-symmetric part vanishes in xᵀAx. Thus even all quadratic-form values cannot establish symmetry. This is a source-scope finding, not a new numerical implementation failure.

Exact integer checks ran in JavaScript using BigInt for six vectors: (1,0), (0,1), (1,-1), (2,3), (-4,5), (0,0). Matrix-vector products for both matrices matched the independent sum-of-squares values 2,2,2,38,42,0. Separate symmetry controls distinguished A and S; the existing Applied D matrix [[1,2],[2,1]] gave -2 at (1,-1). The polynomial identity provides the general reasoning; six samples alone would not prove it. The [raw record](chapter-20-invariant-scope-followup.json) retains exact source blobs, original promises, observed integer results and executable JavaScript.

Replay the arithmetic independently of the checkout with Node.js:

```bash
node -e 'const fs=require("fs");const r=JSON.parse(fs.readFileSync("books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-20-invariant-scope-followup.json","utf8"));console.log(JSON.stringify(eval(r.replay_javascript),null,2))'
```

These are exact integer arithmetic checks, not Python runtime checks of covariance_quadratic_2x2. The execution environment remains unavailable: "No usable execution environment is available. Wait for an environment to become available before using this tool." No new Python compilation, script execution or full-book runtime refresh occurred.

COV-85 is newly partially addressed for this selected scope reconciliation and independently derived counterexample. Variable-rate composition, general matrix/unit checks, other lab promises and independent review remain open. The remediation register now has 32 selected categories partially addressed; none closed. Category disposition is not a defect count or completion percentage. Historical coverage-map statements remain at their original revisions.

Next numerical work remains the retained Section 19.10 baseline range/integration probes when Python execution is available. If it remains blocked, the next independent manuscript obligation is Section 20.5's promised vector/scaled-residual lab scope, using its source and actual checks. Do not repeat this Section 20.3 counterexample as a new runtime result. Independent reviewer sign-off, supported-platform validation, release acceptance and canonical approval remain pending.
