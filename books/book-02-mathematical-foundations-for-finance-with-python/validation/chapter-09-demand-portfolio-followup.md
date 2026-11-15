# V-154 — Section9.1 demand/portfolio complete range and normalization

Based on `ba6d48c308ad25aa6c2d0cfd17f73ac11afa0599`. [Checker](../chapter-09/code/check_section_01_demand_portfolio.py),[observer](chapter-09-demand-portfolio-observer.txt),[scope runner](chapter-09-demand-portfolio-runner.txt),[actual scope results](chapter-09-demand-portfolio-results.json).

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-demand-portfolio-observer.txt . baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-demand-portfolio-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-demand-portfolio-runner.txt .
```

[Baseline](chapter-09-demand-portfolio-baseline.json):46 passes/34 failed source predicates,actual child exit1;[actual replay](chapter-09-demand-portfolio-baseline-replay.json) has identical predicates. [Corrected](chapter-09-demand-portfolio-corrected.json):80/80 pass/exit0. Observer exit0 records actual child output,not a numerical pass by itself.

Independent1800/2400-digit Decimal direct powers/products/quotients agree at float reporting precision. Ten demand vectors cover quantity and three report fields (40 predicates);ten portfolio vectors cover30 field calls;ten invalid/priority cases complete80. Relative5e−14/zero absolute slack;zero signs follow explicit reporting policy. Includes ordinary elasticity−1.5,complete power rescues,quantity underflow with derivative rescue,analytic elasticity for positive exact models despite zero float reports,zero exponents,signed zeros,true final overflow,exact zero portfolio rejection and input priority. Whole dictionaries reject if any requested field cannot be finitely reported.

Demand now uses a private1300-digit log-amplitude calculation with exact represented coefficient/exponent products and conservative±10000 output-amplitude guards;portfolio uses exact Fraction position/value/elasticity before float reporting. Fixed domains and sensitivity validation priority retained. Quantity/portfolio displayed zero from underflow is distinguished from an exact model-zero baseline. This is selected complete-expression/report evidence,not a universal power-conditioning proof.

The three[original OPEN probes](chapter-09-demand-portfolio-initial.json) and[actual before-fix replay](chapter-09-demand-portfolio-before-fix-replay.json) are preserved as historical evidence. [Explicit dispositions](chapter-09-demand-portfolio-probe-disposition.json) map them to passing corrected predicates:finite low-price demand quantity rescued;high-price quantity/derivative/elasticity report rescued;unrepresentable portfolio total now raisesValueError instead of inf/NaN. Only these selected probe contracts are RESOLVED (scoped). COV-54 remains partial;36 selected categories partial,none closed.

Four files compiled,four commands passed (demo+three checker invocations),four input hashes verified before-after. Existing Section9.1 and discounted73+5 checker pass unchanged. [Function source comparison](chapter-09-demand-portfolio-scope-comparison.json) confirms finite/discounted/helper functions unchanged. Fresh609 Python files/396 check-test scripts/610 required source-fixture blobs is inventory,not full execution;full pinned refresh records actual full outcomes separately.

Broader conditioning/resources/financial interpretations,independent mathematical/editorial/platform/release/canonical acceptance remain pending. Next:Section9.2 elasticity helpers and near-zero denominator/arc-elasticity contracts from the existing Chapter9 coverage queue. Book1 tracked independently.
