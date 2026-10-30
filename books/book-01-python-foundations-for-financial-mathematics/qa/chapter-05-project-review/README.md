# Chapter5 — formal project/checklist and retained-wheel review

Based on main `099d3350022df7e636be435a96a96aa18c1eca31`; concurrent Book2 changes are preserved on publication. [Formal review](REVIEW.md) · [29 review records](review-register.json) · [Two exercise records](exercise-register.json) · [Runner](review.py) · [Results](results.json) · [Builder provenance](builder-evidence.json)

CPython3.12.14 Linux passed **23 command records** and **14 separate predicates**. Exact original verifier ran8 installed methods, then two fresh runtimes each ran the same8 source methods against one retained wheel:24 invocations of8 existing unique methods. None is added to historical unique-method/workflow totals. All12 core Chapter5 workflows now have scoped formal records. Only2 of96 local exercises (5.12-E2/E3) are completed here;94 remain.

Reproduce after preparing the exact builder with the [existing provenance-checked instructions](../chapter-05-runtime/backend-resolution/README.md):

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-project-review/review.py --builder /path/to/builder/bin/python
```

Initial run passed; no unexpected failure or manuscript correction. Raw expected nonzero missing-argument and malformed-JSON diagnostics are retained with subsequent successful commands; passing rejection checks do not mean those application invocations succeeded. Original source listings/verifier unchanged; all11 extracted file hashes bound to source SHA256. Source tests/fixtures remain caller-side assets. Original verifier is distinguished from supplemental retained-build/two-runtime orchestration.

Retained artifact: [book1_financial_inflows-0.1.0-py3-none-any.whl](artifacts/book1_financial_inflows-0.1.0-py3-none-any.whl) (3836 bytes), SHA256 `2ad393c4bd77a1d73c5165c1859ea527d615c3b6cb575a98984e611a362a91f1`. Both follow-up installations used these exact unchanged bytes. The original verifier's temporary wheel has its own digest; separate builds need not be byte-identical. This is a synthetic local teaching artifact, not a registry publication, supported release or signed provenance record. Runner reruns rebuild output and replace its generated evidence/artifact; retain earlier versions through Git history before comparing builds.

Numerical expected value independently derived using Fraction/integer ties-to-even: (10005+20005)/1000USD→3001 cents=30.01. Full expected output schema compared with both module and console CLIs. Existing installed bound/context/invalid-input methods rerun; no valuation/FX/outflow economics inferred.

Builder was recreated after the old scratch environment was absent, using exact setuptools84.0.0 artifact checked against PyPI metadata. Builder pip25.0.1, Python3.12.14; provenance/install transcript retained. Backend preparation used network; all project builds/installs used declared local offline options. F13 guard respected. No system interpreter modification.

Scoped limits: same base runtime/Linux, no Windows/macOS/version matrix, source-distribution rebuild, static checker, remote IAM, package-index upload, production, independent human recipient/reviewer or financial certification. Quiet imports demonstrate no output; proving the requested application-file-access boundary remains pending exercise5.12-E4. F28 notebook/platform and F32 shared-input integration remain open; F33 original QA observer failure/corrected rerun remains retained.

Next: Section5.1 local exercises, then remaining local queue in order. Core workflow review is recorded but94 optional local prompts and broader Book1 validation/independent acceptance are unfinished.
