# Section 20.5 vector norm and scaled-residual design

Date: 2026-11-05. Inspected main: `58301a4e13b618a3340b31524af89d92354c2b27`. Runnable evidence pin: `e1364e25cf09cadb7210372c24d2cf8ef4ab0f67`.

Lab step 11 asks the reader to design a vector norm and scaled-residual check. The companion implements scalar errors and an asymmetric scalar comparator; it has no general vector or matrix residual API. This follow-up supplies a worked design with fixed exact counterexamples and exercises the actual scalar functions without implying a new general solver feature. The scalar implementation is unchanged. No numerical defect was found in these selected cases; the initial audit passed.

For n components each differing from zero by 1/8, every scalar comparison passes at atol=1/8, rtol=0. The Euclidean norm is sqrt(n)/8. At n=4 it is 1/4, and at n=64 it is 1, so both fail the same absolute norm threshold. Exact rational sums of squared components independently establish those norms; math.hypot and the actual scalar comparator agree with the expected decisions. Component tolerances cannot be reused as a norm guarantee without accounting for dimensionality and the chosen error budget.

For A=diag(1,epsilon), b=(1,epsilon), exact x=(1,1) and candidate xhat=(1,0), the residual is (0,-epsilon). With infinity norms, beta=||A*xhat-b||/(||A||*||xhat||+||b||)=epsilon/2, while relative solution error is 1. The infinity-norm condition number is 1/epsilon. Four exact rational cases use epsilon=2^-10,2^-20,2^-40,2^-100; each small residual passes a declared atol=epsilon comparison while the actual errors helper reports solution-component errors (1,1). This demonstrates the need to distinguish residual size from forward accuracy; it does not turn that tolerance into an application recommendation.

All six design cases pass. All 21 chapter sources compiled and 12 scripts passed with matching before/after hashes. [Raw arithmetic/results and scoped manifest](chapter-20-vector-residual-design-followup.json) · [Runnable checker](../chapter-20/code/check_vector_residual_design.py).

Replay from a clean checkout at the evidence pin: change to Book 02's chapter-20/code and run python check_vector_residual_design.py with assertions enabled. For the scope, compile all chapter-20/code/*.py, then run every check_/test_ basename in its parent directory in fresh Python subprocesses with timeout=60; compare raw Git blob hashes before/after.

The manuscript now separates this selected design exercise from the scalar companion and the later human provenance/error-budget/review work. COV-85 remains partial for general matrix/vector/unit and variable-rate obligations; 32 selected categories remain partial and none closed. Selected assistant-derived expectations and Python 3.12.14/Linux checks only; no independent reviewer sign-off, supported-platform validation, release acceptance, canonical approval or general numerical accuracy/model suitability certification.
