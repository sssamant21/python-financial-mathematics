# Section20.9 — Exception handling (scoped)

Based on `14675f3f86154c3cdc5438c2808287592342eca8`. One formal workflow,[40 worked-answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-exceptions-review/review.py
```

[Three failed baseline source predicates](baseline.json),[identical actual replay](baseline-replay.json),[actual failing replay exit/output](baseline-run.json),[39 corrected source predicates/five commands](results.json) retained. F210 fixes two oversized finite-input classification leaks and late iterator TypeError misclassification. TypeError while obtaining iter(cashflows) becomes FinancialInputError with its cause;errors during consumption propagate. Input and numerical categories remain distinct. Exponential and fsum overflow causes are inspected;messages omit tested raw sentinels,but causes/tracebacks are not redacted.

Exact source fence executed direct,module unittest,compilation,quiet import and optimized. Fourteen existing unique methods ran42 invocations;zero new historical methods. Five independent represented-rate Fraction references use full rational discount sums,not the production exponential formula. Printed ordinary examples agree within absolute1e−10. Fresh tuple/list/generator inputs,caller immutability,materialization before invalid-rate rejection and actual consumption are checked.

Retry,idempotence,external writes,batch quarantine,access/retention and secret-safe logging are conceptual/design reviews only. No external operation performed. All-range NPV,underflow,cancellation,resources,shape/order(F209),F28 notebook/platform,F32 shared-input integration,F165 tail limits,F185 integration and independent/platform/release acceptance remain open. Chapter20 now9 scoped workflows/360 local answers. Next:Section20.10 Logging.

Executable source/checker bytes verified against `ded1212c249a58c750f6218214754d86a77ac178`;[source manifest](publication-verification.json).
