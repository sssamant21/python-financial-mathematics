# Book 1 — V04 syntax and dependency audit

**Result: PASS (scoped).** Recorded 2026-10-28 against manuscript revision `f0b203904b9ec3f1018d4ac7e192452e260172e7`. This checks compilation, import inventory and one clean dependency profile; it does not establish runtime compatibility for every advertised interpreter, package version or operating system.

## Results

| Check | Observed result |
|---|---|
| Manuscript inventory | 356 chapter/companion/index Markdown files; QA evidence excluded; 1,160 explicit Python fences |
| CPython 3.10.22, Linux | 1,158 fences compile; two intentional loop-context fragments; zero unexplained compilation failures |
| CPython 3.12.14, Linux | Same result |
| CPython 3.13.16, Linux | Same result |
| Dependency inventory | 129 static import roots: 40 standard-library, five third-party runtime libraries, 84 manuscript-local modules |
| Clean Python 3.12 virtual environment | Pinned direct requirements installed; `pip check` reports no broken requirements |
| Dependency smoke probes | Five passed: NumPy dot product, pandas UTC series, SciPy root solving, Matplotlib Agg PNG generation, openpyxl workbook/formula-cache behavior |

The two context fragments are Chapter 2.10's bare `break`/`continue` block and its `if balance >= target_balance: break` illustration. They are intentionally not standalone modules. `ast.parse` alone accepts them; actual compilation correctly rejects them outside a loop. Each also compiles when placed inside a loop. The earlier 1,152-block syntax screening and this 1,160-block compilation inventory use different snapshots/methods and are not execution totals.

The automatic candidate classification identifies 478 blocks containing functions/classes and 680 other compiling illustrative/context-dependent blocks. This is a triage aid, **not** a determination that 478 blocks are complete runnable files. Filename/import dependencies, companion blocks, expected exceptions and input data still matter. Existing chapter runtime reports identify previously executed assembled files. Static imports inside parsed ASTs are inventoried, including imports inside functions; dynamic imports and code stored in strings are not a complete dependency graph. Every local-module root has a filename/directory mention in the manuscript; that does not prove every assembly contract.

## Tested dependency profile and version boundaries

| Distribution | Installed version | Installed metadata: Requires-Python |
|---|---|---|
| NumPy | 2.3.5 | >=3.11 |
| pandas | 2.2.3 | >=3.9 |
| SciPy | 1.17.0 | >=3.11 |
| Matplotlib | 3.10.8 | >=3.10 |
| openpyxl | 3.1.5 | >=3.8 |

This exact scientific profile therefore requires Python **3.11 or later by metadata**, and its smoke probes were actually run only on **3.12.14**. Python 3.10 or later declarations in standard-library Chapter 5 labs are not a promise that this scientific profile installs on 3.10. Python 3.10/3.13 compilation does not establish API, numerical or runtime compatibility. Windows, macOS, Python 3.11, other library combinations, JupyterLab workflows and historical mypy claims remain unverified by this audit. Chapter 5's exact setuptools 84.0.0 build is covered separately by its [backend-resolution evidence](../chapter-05-runtime/backend-resolution/README.md); it is not a runtime dependency here. Moving documentation URLs in [V03](../external-references-2026-10-28/README.md) do not define installed versions.

The [direct requirements](requirements.txt) and [observed full freeze](environment-freeze.txt) describe this audit environment. The freeze is a version record, not a platform-independent or hash-verified supply-chain lock. Full supported-platform/runtime and notebook/tooling acceptance remains V05/V12 work. No code in manuscript fences was changed.

## Reproduction and evidence

Create a clean Python 3.12 virtual environment, install `requirements.txt`, then run from this evidence directory, substituting a fresh temporary output directory:

```bash
python audit_v04.py ../.. /tmp/book1-v04-reproduce
python compile_blocks.py /tmp/book1-v04-reproduce/blocks-for-compilation.json /tmp/book1-v04-reproduce/compile-312.json
python probe_dependencies.py
python -m pip check
```

Run `compile_blocks.py` with actual Python 3.10/3.13 interpreters for those compilation checks; it uses only the standard library. The extraction script needs markdown-it-py 4.0.0. Generated code payloads are temporary and are not duplicated in this evidence directory. Compilation never executes manuscript contents. Smoke probes execute only the provided bounded synthetic checks, with a headless renderer and in-memory workbook; the output image was not visually reviewed.

Evidence includes the [source hashes](source-manifest.json), [inventory summary](inventory-summary.json), [dependency register](dependency-register.json), per-block compilation outcomes ([3.10](compile-310.json), [3.12](compile-312.json), [3.13](compile-313.json)), [installed metadata and probe results](dependency-probes.json), and [pip check output](pip-check.log). Full numerical and financial correctness remains separate.
