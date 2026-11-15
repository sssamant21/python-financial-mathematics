# V-176 — Section9.4 complete single-flow shock reports

Baseline `eb336b137d85b7920ebf1da6cf68db4f398a59a6`. [Scope proof](chapter-09-single-shock-scope.json):only single_shock body changes;single/aggregate/Taylor helper/portfolio wrapper function text unchanged. [Independent checker](../chapter-09/code/check_section_04_single_shocks.py) uses direct C exp(-T(R+H))-C exp(-TR),latent -TBH and -TBH+T²BH²/2,and direct error differences at1800/2400digits;both references must agree. It separately computes baseline five-field eligibility,never calls implementation to generate expected values. Relative5e-14,absolute0;zero signs compare numerically. Twenty vectors times six fields plus ten domain/priority checks and one context observation =131predicates,not131unique methods or defects.

## Actual initial failures and rerun

[Initial118pass/13failed](chapter-09-single-shock-baseline.json),[identical replay](chapter-09-single-shock-baseline-replay.json),[actual baseline command](chapter-09-single-shock-baseline-run.json),[actual replay command](chapter-09-single-shock-baseline-replay-run.json). Six failed fields arise from one saved OverflowError (1e-308,2,.5,-355),including the entire rejected report's metadata. Seven more fields expose loss of complete mathematical error terms in ordinary/tiny-shock/tiny-time cases. These are13failed predicates,not13unique mathematical bugs. Error fields now have an explicit latent-difference contract;earlier float-subtraction arithmetic is retained in initial evidence.

[Corrected131/131](chapter-09-single-shock-corrected.json),[actual corrected command](chapter-09-single-shock-corrected-run.json),[six-file/six-command scoped run](chapter-09-single-shock-results.json). Run `python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-09-single-shock-observer.txt . baseline-replay` to restage baseline source with new checker;corrected uses working source. Observer retains stdout/stderr,exit,source blob and full predicate detail. [Scoped runner](chapter-09-single-shock-runner.txt) compiles six sources/checkers and runs demo plus fivecheckers. Fresh620Python/407check-test/621required blobs is inventory only until separately pinned full refresh.

## Retained prerequisites and limitations

Existing complete baseline eligibility is deliberately retained:baseline value must round positive and all five baseline fields finite. The saved underflowed-baseline observation therefore still returns ValueError;its mathematical finite change is not an accepted input under this policy. This is a documented retained range/design limit,not a repaired numerical case or independent policy approval. The saved expm1 overflow case is scoped resolved. Historical initial/resume records remain unchanged.

Each output is rounded from complete latent expressions in a private1300-digit context. The endpoint can exceed float range while its difference remains finite;conversion occurs after subtraction. Scalar finite/domain/priority behavior and ambient Decimal state are checked. Exponent guard10000 is beyond binary64 input/output rescue range under retained eligible-baseline assumptions;negative endpoints below-10000 round away. Selected reference agreement is not proof of universal transcendental correct rounding or resource guarantees.

Next:portfolio_shock complete collection/aggregate/endpoint/Taylor/error contracts. It still requests unused per-leg normalized fields and uses rounded single-flow values/expm1 products;passing old examples or full runtime does not settle that scope. All36selected COV categories remain partial,noneclosed. Independent mathematical/editorial/model/platform/release/canonical acceptance remains pending. Book1 independent.


### Section9.4 portfolio_shock resume — OPEN

[Fresh initial observations](chapter-09-portfolio-shock-resume-r7-initial.json),[actual identical replay](chapter-09-portfolio-shock-resume-r7-replay.json),[runner](chapter-09-portfolio-shock-resume-r7-probes.txt) pinb5808b7f52ce3ecec42e99a091e240bf29d5aa11. An eligible aggregate still fails zero-shock unused per-leg normalization;finite aggregate exactchange rescue still overflows expm1;an underflowed leg accepted by aggregate is rejected by child-report eligibility. Three diagnostic observations,not passing predicates or settled parent/child policy. Next complete portfolio exact/linear/quadratic/error reports,collection/priority and aggregate eligibility integration. Historical records unchanged.

Executed source pin`b5808b7f52ce3ecec42e99a091e240bf29d5aa11`;[source verification](chapter-09-single-shock-publication-verification.json).

Checker naming qualification:the case named "report overflow" at cash1e308,h=-1 actually has a finite complete change about1.718e308 and is expected to pass;the expected JSON/reference value governs. Actual whole-report overflow is covered by other vectors,including the huge positive shock.
