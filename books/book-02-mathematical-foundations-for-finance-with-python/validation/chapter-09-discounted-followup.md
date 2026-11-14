# V-152 — Section9.1 complete discounted sensitivity/shocks and units

Based on `cc4c3de4d314d0bb569f78b8be94abe4c1d41c2e`. [Checker](../chapter-09/code/check_section_01_discounted_contracts.py),[observer](chapter-09-discounted-observer.txt),[scope runner](chapter-09-discounted-runner.txt),[actual scope results](chapter-09-discounted-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discounted-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discounted-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-discounted-runner.txt .
```

[Baseline](chapter-09-discounted-baseline.json):42 passes/31 failed source predicates,actual child exit1;[actual replay](chapter-09-discounted-baseline-replay.json) has identical observations. [Corrected](chapter-09-discounted-corrected.json):73 source predicates and5 separate exact-unit predicates pass/exit0. Observer exit0 means child output was captured,not that failing checks passed.

Independent1800/2400-digit Decimal references agree at float reporting precision for complete C*exp(−rT),−T*C*exp(−rT),analytic normalizedT/elasticity−rT,linear shock and the difference of two exponential levels. Nine value/sensitivity vectors cover45 field calls;eight shock reports cover16;three printed bp/relative-percent/percentage-point shocks cover6;invalid/priority controls cover6. Relative5e−14/zero absolute slack;zero signs follow explicit reporting conventions. Whole-report rejection applies if any requested field overflows. Small amounts/large horizons/small shocks rescue complete results without premature exponential,PV or derivative rounding. Final underflow may report signed zero;analytic positive model value is distinguished from a rounded zero report. Zero horizon/shock identities preserve strict validation priority.

The implementation now uses exact represented-input products and a private1300-digit scaled exponential/gap calculation,with conservative±10000 exponent cutoffs and explicit final finite reports. This resembles the reviewed Chapter8 numerical approach but is standalone standard-library code;it does not import sibling-directory modules or depend on sys.path mutation. Positive-C/nonnegative-T domains remain unchanged. At rate0,the algebraic elasticity0 has no implied relative-percent interpretation.

E10 is now explicit:1% relative of.04 is delta.0004/new rate.0404,whereas one percentage point is delta.01/new rate.05. E7 uses1bp=.0001. Actual source shock calls at all three deltas have independent complete expectations;five exact decimal unit calculations remain supplemental because no source conversion API exists. Broader symbolic exercise proofs and economic interpretations remain manual.

Three files compiled;three top-level commands passed (demo+two checker invocations);three hashes verified before-after. Existing Section9.1 checker passes unchanged. Fresh608 Python files/395 check-test scripts/609 required source-fixture blobs is inventory,not itself a full pass;the new full pinned refresh records execution separately.

[Executed open demand/portfolio probes](chapter-09-demand-portfolio-initial.json),[runnable probe](chapter-09-demand-portfolio-probes.txt) retain a finite demand quantity lost to power overflow,finite quantity lost to underflow/division by zero,and an inf/NaN portfolio report. They remain OPEN;no demand/portfolio source changed or acceptance claimed. The next coherent scope is those complete-range and normalization/report contracts. Broader COV-54 elasticity/near-zero obligations remain partial. This adds COV-54 to the selected register:36 selected categories partial,none closed;these are not defect counts or completion percentages. Independent mathematical/editorial/platform/release/canonical acceptance remains pending. Book1 tracked independently.

Executable source/checker/probe revision:`c0fd15b82b1122ee170bbe1b8709f2f05b8681e5`. [Pinned three-input manifest](chapter-09-discounted-publication-verification.json).

[Family scope comparison](chapter-09-family-scope-comparison.json) verifies finite/demand/portfolio function source remains byte-identical to the starting main revision;only the discounted public family changed.
