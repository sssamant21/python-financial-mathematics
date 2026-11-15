# Section20.6 — Decimal calculation contracts (scoped)

Based on `ba6d48c308ad25aa6c2d0cfd17f73ac11afa0599`. One formal workflow,[40 answer records](answer-records.json),[12 lab-step contracts](lab-step-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-decimal-review/review.py
```

Optional source revision replays baseline. [Nine failed source predicates](baseline.json),[identical actual replay](baseline-replay.json),[43 corrected source predicates/six source commands](results.json) retained. Both exact Python fences execute/compile;quiet import passes. Fourteen existing unique methods run direct/module/optimized suites:42 invocations,zero new historical methods. Three separate Decimal construction/equality/precision demonstrations pass;they are not extra financial implementations.

F206: four return precision/cancellation failures;unsupported quantize leaked InvalidOperation;caller traps/bounds leaked exceptions/infinity;malformed parser changed caller flags. Financial helper parsing/arithmetic now use fresh Context(prec28,HALF_EVEN),not inherited caller traps/bounds/flags. Complete Fraction return receives one28-digit report. Unsupported arithmetic/quantize ranges and nonzero interest/return rounded to zero reject withValueError;cent rounding intentionally allows zero and exponent−2. Caller configuration/preexisting flags remain intact.

Independent160-digit Decimal difference/quotient then28-digit reporting checks return expectations;fixed exact products/ties/scale and negative domain examples are separate. Actual source helper calls demonstrate per-line versus final rounding. Raw Decimal1/3 under two precisions is supplemental because the financial helper intentionally fixes28 digits. The same14 source methods passed on baseline despite nine additional failing predicates.

Decimal lexical length,coefficient/exponent size and Fraction conversion have no ingestion resource cap. All magnitude/platform/accounting/model/currency/date/fee policies are not accepted by this teaching example. F28 notebook/platform,F32 shared-input integration,F165/F185 and independent/source/resource/release acceptance remain open. Chapter20 now6 scoped workflows/240 local answers. Next:Section20.7 Financial Invariants.
