# Book 02 — Runtime failure follow-up

**Scope:** Targeted fixes and local rerun; independent mathematical and editorial review remain pending.

The local snapshot began from revision `a20484672beae64e7c61037af0b11baba2fd7e54`, with the seven files below modified. The changes were published through commit `deac1e6b9d447322b71cdda751fb04197e497b57`. Other concurrent repository changes were not included in the local snapshot; this is not a claim that the whole current branch was tested.

| Finding | Change |
|---|---|
| Chapter 08 | Use a smaller finite-difference step justified by the exponential's truncation term; check required report keys rather than an incorrect fixed count. |
| Chapter 10 | Reject non-integer interval counts, including bool, with TypeError; retain ValueError for nonpositive integers. |
| Chapter 11 | Compute angle using normalized-vector sums and differences with atan2, improving behavior near 0 and 180 degrees. |
| Chapter 16 | Compare a local polynomial objective change to avoid cancellation near a stationary point; retain a no-descent status if the step cannot move. |
| Chapter 18 | Use an explicit left-to-right addition loop for the naive summation demonstration, rather than relying on version-dependent sum behavior. |
| Chapter 20 | Evaluate the documented asymmetric tolerance rule exactly for represented binary floats using Fraction; add adjacent-value and large-magnitude cases. This is an educational, potentially slower comparison. |

## Results

- Python 3.12.14 on the local Linux runtime.
- All 427 Python files in the snapshot compiled.
- All 216 check/test scripts exited zero when invoked individually from their directories with a 15-second timeout.
- The count is script executions, not independent tests or coverage. Chapter-level checks can invoke section checks.
- The initial failed pass remains documented in [the initial inventory](initial-runtime-inventory.md). No claim is made that the original revision passed.

## Remaining work

Audit mathematical derivations, numerical edge cases, links, documentation, test coverage and companion solutions. Independently review the fixes, especially numerical behavior and applicability across Python versions and platforms. Verify the final repository revision after any further changes. Runtime success is not independent mathematical review, model certification or production approval.
