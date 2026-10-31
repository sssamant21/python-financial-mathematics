# Chapter 18 — Observed local Newton order and hybrid safeguards

**Date:** 2026-10-31  
**Checker revision:** `51abbe74562487aed5b14fb4fc84ee4f0b6dc30c`  
**Unchanged implementation inspected at:** `148ea600804bd4c3ce69699862e6f2cd7eac7c61`

[Runnable checker](../chapter-18/code/check_newton_order.py) records actual function and derivative callbacks for x²-c with c=2,3,5. Exact rational objective callbacks and 100-digit Decimal square roots avoid using the helper's arithmetic as the root oracle. Twenty-four isolated accepted Newton proposals use the independent identity n=(x+c/x)/2 and e_next=e²/(2x), with a two-ulp proposal allowance. Twenty-one observed log-error ratios lie between1.9401965979712923 and1.9993703406822696; the final error coefficients approach1/(2sqrt(c)) within relative0.001.

Each isolated trial starts a fresh bracket around its requested center and stops after one proposal. These are local step-size ladders, not a claim that the full hybrid has quadratic convergence. In three full hybrid solves, each run accepts one Newton proposal and then34 midpoint fallbacks. Actual proposal/interior decisions, retained brackets, terminal residuals, counts and the width criterion are checked. The safeguard deliberately interrupts the local Newton sequence.

The [raw record](chapter-18-newton-order-followup.json) retains the initial harness failure: rounded bracket endpoints did not always preserve the requested center as the initial midpoint. The checker was corrected to use the observed iterate in its reference; the implementation was unchanged. The first corrected rerun and full scoped rerun passed. Three altered proposal/count/status records are detected.

All36 Chapter18 Python files compiled and26 scripts passed; scoped hashes match the executable revision and remain unchanged after execution. Run `python check_newton_order.py` from chapter-18/code; the raw record lists all scoped commands. Inventory497 Python files/286 scripts is scoped evidence after V-53, not a new full-book runtime result.

The manuscript now separates unrestricted Newton's local quadratic theorem from this hybrid's observed behavior and states the implemented derivative policy. COV-79 remains partially addressed. These are selected assistant checks, not independent mathematical reviewer sign-off, supported-platform validation or release acceptance.
