# V-135 — Independent suggested-step references

Candidate based on `f46c548b68ff7426d6d86effc462e352d77ccb35`. No source helper was changed. [Results](chapter-08-suggested-step-results.json) retain 77 passing predicates, four compiled files, two passed scripts, actual stdout/stderr and four before/after Git source hashes. [Runnable checker](../chapter-08/code/check_section_08_suggested_step.py) · [Scoped runner](chapter-08-suggested-step-runner.txt).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-suggested-step-runner.txt .
```

## Numerical derivation and actual contract

The source suggests `s*epsilon**(1/3)` for first derivatives and `s*epsilon**(1/4)` for second derivatives, with epsilon=2^-52 and s=max(1,abs(x)) unless the caller supplies a positive finite scale. This balances a simplified centered truncation/roundoff model; it is a heuristic seed, not an optimal-step guarantee, error bound, noise model or proof of derivative accuracy.

The checker derives exact epsilon as 1/2^52 in a private 160-digit context. Newton's iteration `z_next=((n-1)z+epsilon/z**(n-1))/n` solves the cube/fourth-root equations independently of the source floating fractional-power operation. Complete scaled references at 100 and 160 digits agree after binary reporting. Tolerance is relative 4e-15 with no absolute floor: first-order source exponent 1/3 is itself a represented binary approximation, and the source rounds its root before scaling. No bit-identical real-root claim is made.

Sixteen default/explicit-scale vectors for each order yield 32 numerical root predicates and 32 independent finite/distinct represented-grid predicates. Cases include signed zero, tiny positive/negative x, ±1, ±2, ±1e100, ±1e300, explicit tiny/huge scales and scaled ordinary points. Thirteen additional predicates cover x-before-order-before-scale error priority, bool/float/out-of-range derivative orders, scale types/domain/nonfinite/conversion range, subnormal step underflow, a scale too small to perturb a large x, and a maximum finite x with an overflowing represented perturbation. The helper deliberately uses the same symmetric finite/distinct gate even when a consumer might later request a one-sided derivative.

## Observer correction and scope

[Initial observer output](chapter-08-suggested-step-observer-initial.txt) retained 77 passing predicates. Its epsilon construction initially used ambient 28-digit Decimal precision; that was corrected to exact 2^-52 before the accepted evidence, even though the tested tolerance did not expose a source failure. [Initial scoped metadata](chapter-08-suggested-step-observer-initial-results.json) separately retains the observer's incomplete required-blob inventory: it omitted the one Chapter 1 data fixture because it searched only a fixtures-directory spelling. The corrected runner explicitly verifies `chapter-01/data/section-1.14-cases.json` belongs to the inventory. Neither observer correction is a source defect or a claimed source failed test.

Fresh current inventory is 597 Python files,384 check/test scripts,598 required Python/fixture blobs. Only four selected Python files were compiled and two selected scripts executed in this batch; inventory is not a full execution result. V-134's 54/44 Chapter 8 financial scope and V-133's full 595/382/596 candidate Linux execution remain separate historical evidence. Thirty-five selected COV categories remain partially addressed; none closed. Independent mathematical/editorial/platform/release/canonical acceptance remains pending.

Next substantive COV-51 obligation: demonstrate and document conditioning/noise limits for suggested-step use and finite-difference derivative estimates with independently known noisy/quantized callback references; retain the represented-grid contract and keep arithmetic/reporting success separate from derivative accuracy. Broader resource guarantees remain open. Book 1 has independent progression and trackers.
