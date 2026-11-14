# Section20.3 — Unit testing (scoped)

Based on `fb5b9d7482605ae671893f70a2af6649db9ae9da`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-unit-review/review.py
```

Optional revision argument replays prior source. [Five failed baseline predicates](baseline.json),[identical actual replay](baseline-replay.json),[29 corrected predicates/five passing source commands](results.json) retained. Exact source fence compiled and imported quietly. Twelve existing unique methods passed as direct suite,module suite and optimized suite:36 invocations. Separate selected faulty/control probes add2 invocations of those same methods,38 total;zero new historical unique methods. Compilation is not finance correctness.

F203: oversized integer cashflow/rate finite checks leaked OverflowError;zero amount/zero rate identities wrongly entered overflowing discount/period arithmetic. All inputs now validate before exact n0/r0/C0 identities return C;oversized inputs consistently reject with ValueError. Broader nonzero extreme-discount/large-period scaling,underflow and resource policy remain unreviewed;this is not complete-range PV certification.

Independent normal expectations use Fraction powers of the represented rate:110/1.1=100,95/.95=100,−110/1.1=−100;selected additional periods/negative rates use narrow declared tolerances. Linearity,positive/negative future-payment direction and time-zero constancy are separate relationship checks. API/calendar/date/currency/fee/mock/model statements are conceptual/design reviews;no invented integration execution.

The [deliberate supplemental sign-defect copy](faulty_variant.py.txt) fails the existing negative-cashflow method (exit1),while unchanged source control passes (exit0). Actual outputs are retained;the faulty copy never mutates the reference source and is not a published-source defect. The same12 original methods passed even on the baseline,illustrating finite coverage limits.

F28 notebook/platform,F32 shared-input integration,F165/F185 and broader source/model/resource/platform/independent acceptance remain open. Chapter20 now3 scoped workflows/120 local answers. Next:Section20.4 Boundary and Edge Cases.
