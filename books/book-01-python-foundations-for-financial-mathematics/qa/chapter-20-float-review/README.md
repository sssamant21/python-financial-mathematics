# Section20.5 — Floating-point acceptance gates (scoped)

Based on `cc4c3de4d314d0bb569f78b8be94abe4c1d41c2e`. One formal workflow,[40 answers](answer-records.json),[12 lab-step records](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-float-review/review.py
```

Optional source revision replays baseline. [Seven initial source failures](baseline.json),[identical actual replay](baseline-replay.json),[64 corrected source predicates/five source commands](results.json) retained. Six supplemental arithmetic/primitive predicates pass separately. Fourteen existing unique methods run direct,module and optimized suites:42 invocations,zero new historical methods. Compilation and quiet import pass;no claim that syntax acceptance validates finance.

F205: three finite-input gates falsely accepted because error/tolerance intermediates overflowed or subnormal products rounded across the exact decision boundary. Four oversized integer comparator/NPV inputs leaked OverflowError. The comparator now evaluates |a−b|≤atol+rtol*|b| exactly for represented finite built-in inputs using Fraction;strict finite checks normalize oversized inputs toValueError. Existing financial tolerances were not widened. Future-payment/time-zero and naive-float overflow answer qualifications corrected.

Independent1800/2400-digit Decimal decisions agree for42 named/seeded gates,including asymmetry,near-zero,subnormal,true equality and large finite products. Ten invalid-input checks plus12 ordinary NPV/domain/invariant checks complete64 source predicates. Normal NPV expectations use independent rational discount powers. Separate binary.1+.2,infinity/max-rule,log1p/expm1 vs100-digit references and exact-money controls are supplemental primitives,not invented financial APIs.

All14 original methods passed even on the baseline;the external boundary predicates found seven failures beyond that suite. This establishes the stated represented-input gate,not appropriate financial tolerances,original-decimal data truth or numerical/model acceptance for every workflow. The NPV log/exp implementation retains broader discount/sum/underflow/resource limits. F28 notebook/platform,F32 shared-input integration,F165/F185 and independent/source/model/platform/release acceptance remain open. Chapter20 now5 scoped workflows/200 local answers. Next:Section20.6 Testing Decimal Calculations.

Executable source/runner revision:`c0fd15b82b1122ee170bbe1b8709f2f05b8681e5`. [Pinned input manifest](publication-verification.json).
