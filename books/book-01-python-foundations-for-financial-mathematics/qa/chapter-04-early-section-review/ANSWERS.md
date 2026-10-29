# Sections4.1–4.3 —27 scoped exercise answers

Reviewed2026-10-29. Runtime evidence and conceptual/proposed contracts are separate. No schema proposal is applied silently to canonical validators.

## 4.1-E1

Proposed source_record_id is a nonempty exact identifier scoped by source_system and source_dataset/version; document whether it names a raw observation or a corrected logical event. A correction needs explicit revision/lineage, not silent overwrite. Adding it requires coordinated schema, validator, fixture, copy/report and test changes. The existing strict five-field validator is not silently extended.

## 4.1-E2

Zero is a known signed-currency amount; missing is unavailable/absent and violates the required amount field. Do not default missing to zero. Empty collections require their own completeness statement.

## 4.1-E3

The executed pair copies the valid payment fixture, changes only payment_id, and validates both. Equal dates/amounts do not establish event identity or duplication.

## 4.1-E4

Proposed collection rule: unique (source_system,source_record_id,revision) with explicit policy for active logical-event revisions. Reject conflicting duplicates; retain correction linkage and audit history. This is a design, not implemented collection/concurrency validation.

## 4.1-E5

A date identifies a calendar day, not intraday ordering, timezone, cut-off or settlement instant. Add explicit timestamp/timezone/source sequence under a reviewed contract if those distinctions matter.

## 4.1-E6

The exact source validate_payment rejects Decimal Infinity with ValueError. The observed exception is retained; no arithmetic is attempted.

## 4.1-E7

A nested list would remain shared by a shallow dictionary copy. Validate/reconstruct owned nested contents or choose a documented deep-copy/frozen representation; preserve immutable-scalar assumptions only for the current schema.

## 4.1-E8

A signed payment may be negative from the investor perspective; a nonnegative-only valuation API rejects that domain. Choose an explicitly signed valuation or a documented sign/magnitude adapter without changing cash-flow direction silently.

## 4.1-E9

Before combining currencies require compatible sign/time semantics, currency/amount scale, chosen base currency, rate convention, FX source/version/as-of basis, rounding stage and completeness policy. Do not sum unlike currency amounts merely because Decimal addition is possible.

## 4.2-E1

The executed list[-1000,100,150,200,300] maps index0 to initial outflow and1–4 to later receipts under declared equal model-period units. Index alone does not define annual/monthly timing.

## 4.2-E2

Slice[1:3] returns100,150: indices1 and2 are included, stop3 excluded. These are the first two future observations in the stated receipt fixture.

## 4.2-E3

append([x,y]) adds one nested-list element, while extend([x,y]) adds two elements. The executed shapes are[[1,2]] versus[1,2]; choose the intended schema deliberately.

## 4.2-E4

remove(Decimal(100)) removes the first equal amount, not an identified payment. Equal amounts can belong to different events/dates; use explicit event identity before removal.

## 4.2-E5

pop on[] raises IndexError. An application must explicitly choose whether empty is normal absence or an invalid operation rather than invent a payment.

## 4.2-E6

An alias points to the same list, so append changes both names. A shallow copy has an independent outer list and does not receive later appends to the original; scalar inputs remain immutable.

## 4.2-E7

A shallow copy of record lists retains dictionary identities. Editing a copied record changes the original dictionary; fresh validated record reconstruction is needed for independent mutable views.

## 4.2-E8

The supplemental indexed_positive validates an entire list of exact finite Decimal amounts before returning enumerate-derived original(index,amount) pairs. The separate[-1000,100,0,200,300] fixture returns(1,100),(3,200),(4,300). Empty gives[]; wrong/nonfinite later inputs reject. No periods are invented or renumbered.

## 4.2-E9

Filtering and restarting indices at0 shifts future receipts to earlier/incorrect periods and changes any later discount exponents. Preserve original indices or explicit dated event records and their time-unit metadata.

## 4.3-E1

Empty tuple is(); singleton is(Decimal(1),). The comma creates the singleton tuple; parentheses alone group an expression.

## 4.3-E2

Unpacking(3,Decimal(200)) binds period3 and amount200. Declare period0 origin and the period unit separately; this pair is not automatically dated or annual.

## 4.3-E3

The temporary three-value unpack into two names raises ValueError. The fixture is isolated and does not change canonical source.

## 4.3-E4

Rebinding a tuple variable selects another object; assigning one of its items raises TypeError. Neither operation proves arbitrary descendants are immutable.

## 4.3-E5

The exact source positive_period_flows accepts(1000,Decimal(1)) and preserves it, confirming the supported upper boundary with a positive receipt.

## 4.3-E6

Equal period/amount pairs can represent distinct legitimate payments. Define an event key, identity scope and duplicate/correction policy before removal; value equality alone is insufficient.

## 4.3-E7

A tuple of Decimal scalars has immutable supported descendants; a tuple containing a dictionary permits dictionary mutation. The executed example changes the dictionary quantity while scalar tuple remains unchanged.

## 4.3-E8

When two fields expand to six, propose a named frozen dataclass or NamedTuple with documented field meanings and runtime validation. Frozen wrappers do not recursively freeze arbitrary mutable descendants; use validated immutable field types.

## 4.3-E9

The exact source period-preserving selector retains(2,100),(5,200) from an initial outflow and later receipts. Amount-only selection discards where those payments occur, preventing justified time-value calculations without recovering metadata.

