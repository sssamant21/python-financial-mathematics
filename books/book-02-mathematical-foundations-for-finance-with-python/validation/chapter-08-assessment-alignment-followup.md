# V-145 — Exact assessment runtime/input alignment

Candidate based on `2bd9edae71a0f1def7176b33ec516d3a798393af`. [Checker](../chapter-08/code/check_section_08_assessment_alignment.py) · [Runner](chapter-08-assessment-alignment-runner.txt) · [Actual results](chapter-08-assessment-alignment-results.json). No Book2 numerical implementation changed.

```sh
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-assessment-alignment-runner.txt .
```

The prior prepared[checkpoint runner](chapter-08-assessment-checkpoint/run_when_available.txt) was actually executed:[two compiled files,two commands and11 exact-source checks passed](chapter-08-assessment-checkpoint/python-runtime.json). Its source hashes still match the pinned earlier implementation,which is unchanged. Historical V-144 static/JavaScript and unavailable-runtime records are retained;they were not retroactively called Python passes.

The expanded checker passes48 source predicates and8 separately labelled supplemental expectations. Seven actual source/checker files compiled;three Python commands passed:assessment demo,unchanged existing checker,new alignment checker. Two are check/test scripts;one is the source demo. All seven source hashes matched before and after. The current Python/platform and actual stdout/stderr are retained.

## Exact prompt mapping

P1/P2 now use the named Section8.6 coefficient API for the exact assessment polynomials;limit proof remains manual. P8 uses125 stationary profit2525 and endpoints;uniqueness proof remains analytic. P10/P11 use independent100-digit Decimal complete PV/derivative/Taylor/exponential-gap expectations for the printed decimal model with declared ordinary-case tolerances. P12 uses the exact log input;simple.05 is supplemental. P14/P15 use the quoted break-even and bond-yield/inverse inputs;direct price derivative−1000/11 is supplemental because this lab has no direct function for it.

P16/P17 use exact polynomial derivative/sign/value APIs at the stated expressions and selected points;the all-neighborhood conclusions remain analytic. P18 explicitly executes earlier Section8.8 forward/backward APIs and the assessment centered API at x2,h.1,matching12.61/11.41/12.01. P19 uses the assessment square stencil. P20 calls the actual Richardson API for the exact cubic;formal order derivation remains manual. P21 executes−1/+1/0 kink stencils;nonexistence is justified by one-sided slopes,not by a centered pass.

P23 now executes the exact three-flow schedule[(100,1),(200,2),(300,3)] through Section8.6 at four signed/zero/positive rates,against independent100-digit Decimal term derivatives;selected signs are checked while the all-real sign claim is analytic positivity of each exponential contribution. P25 executes the actual comparator over.01/.001/.0001,records centered acceptance/forward disagreement and rejects a deliberately wrong analytic reference at all three steps. Agreement is still not independent acceptance.

Supplemental P9 accumulation,P12 simple return,P13 elasticity,P15 direct price derivative,P22 roots andP24 bp arithmetic are not invented assessment APIs. P3–P7 symbolic derivations,P20 proof,heuristic qualifications,units andprotocol governance retain the[25 static source/solution records](chapter-08-assessment-checkpoint/answer-map.json). No claim that every problem has a source implementation,or that a finite numerical grid proves a symbolic result.

Fresh inventory603 Python files/390 check-test scripts/604 required source-fixture blobs is not a full run. V-142 at `a847812cb63d75354199723e5489cd84a579988d` remains latest full601/388/602 evidence. Two small checkers added since that full pass have scoped execution;no Book2 numerical source changed. Thirty-five selected COV categories remain partial;none closed. Independent mathematical/editorial/platform/release/canonical approval remains pending. Next:Section8.10 copied numerical helpers' complete-range,log-return,bond and centered-preflight contracts;retain branch/conditioning/resource gaps.

Executable source/checker revision: `556f351206e6584cafa972dca5b3f1e919809fa3`. [Publication source manifest and pinned inventory](chapter-08-assessment-alignment-publication-verification.json).
