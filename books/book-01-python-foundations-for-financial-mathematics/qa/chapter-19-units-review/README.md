# Section 19.10 — Currency and unit normalization scoped review

Baseline `2b521783ba191220b3f1f3318ad4d94575e68c4b`. [Manuscript](../../chapter-19/19.10-currency-and-unit-normalization.md) · [40 answer records](answer-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-units-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-units-review/review.py 2b521783ba191220b3f1f3318ad4d94575e68c4b
```

The baseline intentionally exits1. [Initial results](baseline.json) retain three failed predicates and [identical replay](baseline-replay.json). [Corrected results](results.json) retain42 passing predicates,three source commands (demo with12 existing tests,compile,quiet import),and one separately counted supplemental half-up comparison. One workflow,12 lab-step records and40 local worked answers were reviewed;zero new historical unique methods are claimed.

## F197 — fresh decimal arithmetic context

Although helpers set precision28,the original localcontext copied caller rounding,exponent limits and traps. A FLOOR caller changed the reciprocal's final digit; Emax2 made an ordinary1000×1.10 raise Overflow; disabling that trap returned Infinity. These three initial failures are retained. Each arithmetic helper now uses a fresh Context(prec=28,rounding=ROUND_HALF_EVEN),including standard exponent bounds and traps. USD cent quantization remains explicitly HALF_EVEN; no unrequested cash rounding is added to FX multiplication. Decimal text parsing still preserves supplied coefficient/scale. Extreme coefficients/exponents,arbitrary resources,currency-specific cash rules and final underflow guarantees remain outside the example.

Independent unit identities:10000/100=100;5/100=.05;1/10000=.0001;100/10000=.01. A5%→6% move is1percentage point=100bp,but(6−5)/5=.2 relative increase. At1.10 target USD/source EUR,100×1.10=110;1/1.10=10/11 gives the 28-digit reciprocal. USD110 multiplied by the rounded reciprocal returns approximately EUR100 under the stated finite context; exact inversion is not promised for arbitrary amounts. Constant EUR100 at1.05 becomesUSD105;105−110=−5USD before fees/other changes. Negative amounts are allowed;zero/negative FX rates reject. Units,quote direction,source and timestamp truth are caller prerequisites,not verified labels.

Half-even ties1.005→1.00,1.015→1.02 and−1.005→−1.00 execute the source boundary. The lab8 explicitly chosen alternative HALF_UP maps1.005→1.01 in a separate supplemental Decimal calculation. It is not a replacement settlement rule. The context correction makes results reproducible under tested caller contexts; it is not independent library certification or financial acceptance.

## Twelve lab-step records

| Step | Review / evidence |
|---|---|
| 1 | Caller must supply currencies and target-per-source quote direction; source does not validate labels. |
| 2 |10000 cents→100 dollars executed and independently derived. |
| 3 |5%→.05;100bp→.01;1bp→.0001 executed. |
| 4 |+1 percentage point,+100bp and20% relative increase derived separately. |
| 5 |EUR100×1.10USD/EUR=USD110;negative and zero amounts also checked. |
| 6 |10/11 reciprocal report and rounded reverse conversion executed;28-digit policy documented. |
| 7 |EUR asset held constant;USD105−110=−5;no asset move/fees/source reconciliation inferred. |
| 8 | Source half-even tie cases executed;one separate half-up policy comparison. |
| 9 | Zero/negative FX,missing/wrong types,empty/malformed/NaN/infinities rejected. |
| 10 | Quote timestamps,rate type,bid/ask,provider and availability absent:conceptual review only. |
| 11 |12 unchanged reference methods and three actual commands executed;predicate counts remain separate. |
| 12 | Python/platform,source hashes,actual results,context and caller policies retained. No live FX or settlement approval. |

## Forty prompt-to-answer records

| Exercise | Topic | Worked answer | Scope |
|---|---|---|---|
| 1 | Cents: | USD 100. | Actual source calls and independent unit arithmetic |
| 2 | Percent: | .05 decimal. | Actual source calls and independent unit arithmetic |
| 3 | Basis point: | .0001 decimal. | Actual source calls and independent unit arithmetic |
| 4 | 100 bp: | .01. | Actual source calls and independent unit arithmetic |
| 5 | Rate move: | +1 percentage point. | Actual source calls and independent unit arithmetic |
| 6 | Rate move: | +100 bp. | Actual source calls and independent unit arithmetic |
| 7 | Rate move: | 20%. | Actual source calls and independent unit arithmetic |
| 8 | FX: | USD 110. | Actual source calls and independent unit arithmetic |
| 9 | Reciprocal: | Approximately .9090909 EUR/USD. | Actual source calls and independent unit arithmetic |
| 10 | Reverse conversion: | Approximately EUR 100. | Actual source calls and independent unit arithmetic |
| 11 | FX shift: | USD 105. | Actual source calls and independent unit arithmetic |
| 12 | P&L: | −USD 5. | Actual source calls and independent unit arithmetic |
| 13 | Quote direction: | It determines multiplication or inversion. | Conceptual/design/source-contract review only |
| 14 | Bid/ask: | No. | Conceptual/design/source-contract review only |
| 15 | Timestamp: | They describe values at particular times. | Conceptual/design/source-contract review only |
| 16 | Stale rate: | Yes. | Conceptual/design/source-contract review only |
| 17 | Missing rate: | No. | Conceptual/design/source-contract review only |
| 18 | Zero FX rate: | No. | Actual source calls and independent unit arithmetic |
| 19 | Negative amount: | Yes; it may represent a liability. | Actual source calls and independent unit arithmetic |
| 20 | NaN: | No. | Actual source calls and independent unit arithmetic |
| 21 | Decimal: | No. | Conceptual/design/source-contract review only |
| 22 | Precision: | Decimal arithmetic can round under finite precision. | Conceptual/design/source-contract review only |
| 23 | Reciprocal: | Yes. | Conceptual/design/source-contract review only |
| 24 | Rounding: | No. | Supplemental alternative rounding comparison plus conceptual review |
| 25 | Half-even: | 1.00 under this example. | Actual source calls and independent unit arithmetic |
| 26 | Minor units: | No. | Conceptual/design/source-contract review only |
| 27 | Price per share: | No. | Conceptual/design/source-contract review only |
| 28 | Contract size: | To convert per-unit price to position value. | Conceptual/design/source-contract review only |
| 29 | Currency code: | No. | Conceptual/design/source-contract review only |
| 30 | Observation time: | Not necessarily. | Conceptual/design/source-contract review only |
| 31 | Revision: | Yes, if used before availability. | Conceptual/design/source-contract review only |
| 32 | Hash: | Hashed bytes. | Conceptual/design/source-contract review only |
| 33 | Hash: | No. | Conceptual/design/source-contract review only |
| 34 | Quote inversion: | No. | Conceptual/design/source-contract review only |
| 35 | Fees: | No. | Conceptual/design/source-contract review only |
| 36 | Live rate: | No. | Conceptual/design/source-contract review only |
| 37 | Unit label: | No. | Conceptual/design/source-contract review only |
| 38 | Reconciliation: | To detect conversion or unit errors. | Conceptual/design/source-contract review only |
| 39 | Tests: | No. | Conceptual/design/source-contract review only |
| 40 | Production: | No. | Conceptual/design/source-contract review only |

F28 notebook/platform,F32 shared-input integration,F165 tails,F185 signed-normal-terminal integration and independent acceptance remain open. No currency-label/calendar/point-in-time/source-quality/bid-ask/settlement/resource acceptance is inferred. Next:Section19.11 Data Quality Checks formal workflow/local-answer review.

Executable source revision: `309316221a32aaeed52cc896675c3a78dfee8cdd`. [Publication source manifest](publication-verification.json). Tested manuscript/observer blobs match this revision; metadata pins do not alter executable inputs.
