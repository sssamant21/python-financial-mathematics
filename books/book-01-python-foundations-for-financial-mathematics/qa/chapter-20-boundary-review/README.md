# Section20.4 — Boundary and edge cases (scoped)

Based on `04aba8a51eb7b2ddf3208bb1ed045888704e18c2`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-boundary-review/review.py
```

Optional revision argument replays prior source. [Initial13 failed source-call predicates](baseline.json),[identical actual replay](baseline-replay.json),[50 corrected source-call predicates and five passing source commands](results.json) retained. Two supplemental math.isclose semantics controls pass separately. Fourteen existing unique methods run normally,through module unittest and optimized source:42 invocations,zero new historical methods. Source fence compilation and quiet import also pass;compilation is not financial correctness.

F204: finite checks leaked oversized-int OverflowError;zero PV identities entered overflowing discount/period arithmetic;simple return lost cancellation accuracy or leaked infinity;mean failed on finite-result intermediate sums. Strict finite checks normalize invalid oversized integers toValueError. Validated PV n0/r0/C0 identities returnC. Complete represented-input Fraction return/mean round once at final float reporting;true final return overflow rejects. Collections still materialize fully without a resource cap. No claim of complete-range nonzero PV or universal financial conventions.

Independent ordinary PV oracles use rational represented-rate powers. Return/mean references use1600/2000-digit Decimal arithmetic and agree at float reporting precision,including ordinary.015,near-unity,huge sums/cancellation,subnormal mean and true overflow. Rate nextafter cases distinguish just-above/below−1. Invalid types/nonfinite and invalid-before-identity checks,zero end,empty/singleton/generator and iterator-failure propagation are explicit. The same14 original methods passed on the baseline despite13 external failing predicates.

The two separate comparison controls show math.isclose(abs_tol=...) retains its default relative tolerance,while rel_tol=0 can reject the same difference. Those are semantic demonstrations,not extra financial source cases. Date/calendar/DST,variance/outlier/model/currency/integration statements are conceptual/design reviews;no missing API execution is invented.

Broader nonzero PV discount/underflow,collection/input resources,F28 notebook/platform,F32 shared-input integration,F165/F185 and independent/source/model/platform/release acceptance remain open. Chapter20 now4 scoped workflows/160 local answers. Next:Section20.5 Testing Floating-Point Results.
