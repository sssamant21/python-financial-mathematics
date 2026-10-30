# Chapter5 — Section5.8 hash/dependency-closure exercises

Based on main `28af429b` with manuscript/code hashes retained. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results/raw failures and retries](results.json) · [Concrete evidence manifest](evidence-bundle/manifest.json)

CPython3.12.14 Linux: **18 command expectations and16 predicates passed**. No unittest methods occur in these workflows; historical unique methods/workflow totals unchanged. Initial run met all expectations; no unexpected failures or manuscript corrections. Deliberate incomplete-closure and incorrect-report-hash installation errors are retained as raw nonzero records, with absent-import checks and successful complete approved-specification retries. Neither failure is misrepresented as a successful installation.

Reproduce using standard library and venv/ensurepip:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-hash-exercises/review.py
```

Original Section5.6 wheel/command helpers and Section5.8 install_arguments/BEHAVIOR are compiled unchanged with explicit helper assembly, without running original main workflows. New exercise orchestration creates two fresh runtimes with pip; local no-index/no-cache/only-binary/hash-mode options retained, dependencies enabled. Unchanged original source behavior verifies installed origins, exact quantity contract and unsupported inputs independently in both. Supplemental file-bound caller replaces only input acquisition and adds digest output; no fixture financial validation implementation changed.

The retained [application](evidence-bundle/application_probe.py) consumes [input bytes](evidence-bundle/input.txt)12.50, reports input/application digests and known output. [Complete spec](evidence-bundle/complete.txt), [omitted transitive-hash spec](evidence-bundle/missing-transitive.txt) and [wrong report-hash spec](evidence-bundle/wrong-report-hash.txt) retained. Approved wheel files are beneath evidence-bundle/approved-wheels, with exact names/digests in manifest; retained bytes checked equal those supplied to pip. These original synthetic fixture wheels are QA evidence, not a package-index release or recommended production artifact.

Manifest design concretely links application/source/input/spec/wheel hashes and selected runtime results. Known expectation is representation instrument_units/12.50, including exact zero and invalid cases in original probe, not a money calculation. Both independent known results and consumed-source/input digest checks pass. Selected invariants agree while runtime prefixes and pip location strings differ as intended; full evidence object equality is not required.

Runner reruns regenerate synthetic wheels (timestamps may differ) and replace its generated bundle/results; preserve past versions in Git before comparing. Hashes identify selected bytes, not trust/authenticity or correctness. No external download, source build/backend, compiled dependency, OS/Python matrix, candidate dependency update, registry, notebook, production or independent reviewer/financial acceptance. F28/F32 remain open and prior F33 observer history retained.

66 of96 local prompts now reviewed;30 remain. All12 core workflows and20 chapter-wide answers remain separate. Next: Section5.9 layout/output-file/discovery exercises, then queue order; skip completed5.12-E2/E3 unless sources change.
