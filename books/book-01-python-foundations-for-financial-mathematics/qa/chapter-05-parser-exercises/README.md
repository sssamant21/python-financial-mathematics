# Chapter5 — Section5.3 parser/file/round-trip exercises

Based on main `983e04ba6a0dfb9b97c22af6c4b87b923ecc5680`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner and supplement interfaces](review.py) · [Results/hashes/transcripts](results.json)

CPython3.12.14 Linux: **52 source/supplement predicates passed**, **two original-source command records passed**, including **nine existing test methods** and the three introductory blocks executed in order as one program. These counts are separate, not new unique methods/workflows. Initial run passed; no unexpected failures or manuscript changes. Expected schema/lexical/domain/resource/file/calendar/export rejections retain actual exception class versus expected class in results; original suite transcript retained separately.

Reproduce with standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-parser-exercises/review.py
```

Original complete parser fence is compiled unchanged for direct function probes and separately run as the original test script in a temporary directory. Three original introductory fences are concatenated in documented order. All selected code/manuscript SHA256 retained. Supplements are new finite_amount, strict_amount, limited_parse and export_schedule functions in the QA runner; original parsing/lexical policy is not modified.

Independent expectations follow explicit contracts: zero/negative/fractional Decimal values retain tuples/text without binary floats; signed zero/long fractional scale and exponent round trips are checked, not only numeric equality. Impossible2027-02-29 rejects while2028-02-29 is preserved. Strict lexical spelling and finite numeric domain have separate tests, including wrong types and nonfinite direct Decimal probes. Original exponent acceptance is separately verified to prevent accidental narrowing of the published parser. Schema extras, duplicate identities, datetime/float fields and unsupported nonfinite export values reject.

Payload limit is on already-decoded string characters before JSON parsing, proved by delegated-call observation on oversized invalid JSON. It is not a file/network byte cap or complete resource defense. Unicode byte-count distinction explicitly checked. Valid-UTF8 malformed JSON file fails with JSONDecodeError, file bytes unchanged; invalid later date returns no partial result and earlier source record remains intact.

Exporter explicitly validates known canonical schema and emits amount/date strings, checks full original parser round trip and preserves same-day events, order and empty identity. Unknown fields are rejected rather than dropped. The exporter uses the original broad Decimal grammar; strict_amount is a separate scalar teaching interface, not an undisclosed change to original parser. No value arithmetic, currency conversion, ledger reconciliation or settlement implementation is inferred. Event-count/balance distinction and proposed planned/settled fields are design responses.

Limits: no hostile-input load/resource guarantee, static checker, Windows/macOS, notebook/kernel, external payment/market data or independent reviewer acceptance. F28/F32 remain open; F33 observer failure/rerun history retained. All12 core workflows and20 chapter-wide answer reviews remain separate from optional local prompts.

26 of96 local prompts now have scoped records;70 remain. Next: Section5.4 local utility exercises, then queue order; skip already completed5.12-E2/E3 unless sources change.
