# V259 — Partial Section10.8 complete equal-payment PV

Baseline pin: `f19f4218adbf94b9e6c33e5b5e8ae2a1d3024e9d`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [retained continuous18](continuous-retention.json), [chapter runner](native-runtime.txt), [chapter execution](chapter-runtime.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-equal-payments-2026-11-22/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-equal-payments-2026-11-22/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-equal-payments-2026-11-22/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-equal-payments-2026-11-22/continuous-retention.txt candidate continuous-retention
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-equal-payments-2026-11-22/native-runtime.txt
```

Final baseline/replay **18 passes /21 failed contract predicates**;corrected **39 pass twice**,identical rows. Three baseline probes statically record absence of the newly declared integer-size budget rather than executing an unbounded integer case;these are policy probes,not numeric defects. Other failures include premature C*T or geometric/exponential overflow,step-resolution loss/huge-count conversion,and unreportable zero-rate totals leaking infinity. Counts are not independent defect totals. The initial33-probe runner/results and initial chapter execution are retained in interim33-* and interim-native.json;final39 adds single immediate-payment and zero-rate final-overflow cases. These are additional meaningful contracts,not new independent acceptance.

## Complete-expression method and references

Let z=rT,x=abs(z)/n,offset=0,.5,1. Normalize by the largest payment exponential. With phi(y)=(1−exp(−y))/y and phi(0)=1,the complete sum is
`c*T*phi(abs(z))/phi(x)*exp(dominant)`,where dominant=−x*offset for z>=0 and x*(n−1+offset) for z<0. This is an exact finite-sum rearrangement,not an integral approximation. The source keeps binary-input Fractions,uses800-digit Decimal scaling,a stable integrated exponential series for small y,and reports one final float. Near-zero steps no longer require conversion to a nonzero float. Zero c/T and zero rate preserve their validated contracts.

Independent1800-digit oracle sums every actual payment at its exact binary-input nominal time for the tested small schedules,using halving/Taylor/squaring exponentials. It does not use the geometric rearrangement or source phi helper. Tests cover all three timings,positive/negative cash flows,compensated growth,huge positive discount exponent,representable subnormal time steps,zero rate/amount/horizon,final overflow and n=10^400 approaching continuous PV below float resolution. Final float equality holds for explicit finite-sum probes;the huge-n comparison is a separately labelled near-continuous control with2e−15 relative tolerance. Retained V25818 independent continuous-PV predicates pass.

A single beginning payment at time0 remains c*T even when negative discount growth over the full horizon is enormous;mid/end cases appropriately reject if unreportable. For positive huge discount,an immediate first payment may remain finite while later payments underflow. The final-underflow-to0 convention is retained explicitly;this differs from some other section helpers' nonzero-underflow rejection policies.

## Declared support/resource limits

Equal-payment counts must be positive exact integers with bit_length<=4096. This new finite input-size policy applies to equal_payment_pv,not an acceptance claim for schedule/ratio functions. It is a teaching bound,not a measured optimal budget. Arbitrarily large counts do not cause a payment loop in the source;the oracle uses only small explicit sums. The source's phi series has a2000-term guard and800-digit context. For y>10000,phi(y) uses1/y;dominant>10000 rejects and dominant<−10000 returns0. With validated float c,T and n<2^4096<10^1234,an individual nonzero payment magnitude is bounded below by roughly10^−1881 and total undiscounted magnitude above by10^617;exp(±10000) exceeds the full compensation range. These cutoffs cannot hide a representable tested complete sum under the declared size envelope. No universal correct-rounding,performance or arbitrary resource proof.

Chapter10:21 files compile,11 checkers and10 CLIs pass;all21 code identities verify afterward. Full statuses/outputs/timings retained. Fresh pinned Book2 inventory642 Python files /429 check-test scripts /643 required blobs;only10.8 source/checker differ from V257. This is NOT a new full-book run. Native numerical regression includes immediate-payment/final-overflow cases and prior source checks.

**Next:**10.8 explicit schedule PV,ratio/range and complete comparison/report contracts,then timing-order/limit/units/14-exercise/applied-lab crosswalk and a full refresh when accumulated changes justify it. Equal-payment correction does not validate those still-unchanged functions. All38 selected COV categories partial,none closed;not defect counts/percentages. Book2 IN PROGRESS;broader numerical/resource/data/model/platform/reviewer/release/canonical acceptance open. Book1 separate.
