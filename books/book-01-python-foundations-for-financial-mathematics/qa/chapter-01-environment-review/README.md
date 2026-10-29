# V06/V12 — Chapter 1 environment-step review

Date: 2026-10-29. Source revision: `6d4d9828224dbd056da729644acb050ff690ce30`.

**PARTIAL — 14 checks passed; one notebook check blocked by this runtime; one server/UI validation unit not executed.** There are no failed numerical checks in the completed batch. The initial notebook attempt exited 1 and remains an unresolved environment result, not a passing run. Chapter 1 platform acceptance remains open.

| Evidence | Scope |
|---|---|
| [Step register](STEPS.md), [JSON](step-register.json) | All 22 numbered Section 1.5 subsections reviewed with explicit dispositions; not all executable |
| [Checks and actual outputs](results.json) | Venv isolation, version/pip identity, pip check/list/freeze, bash activation, all six exact Python fences, JupyterLab CLI, Git ignore probe |
| [Initial failure record](initial-attempt.json), [initial harness](initial-review.py) | Actual kernel attempt failed: socket/interface Operation not permitted; kernel died before kernel_info reply |
| [Current runnable review](review.py) | Non-network checks plus explicit unresolved dispositions; it does not retry or conceal the blocked kernel attempt |
| [Resolved requirements](requirements-resolved.txt), [recreation evidence](recreation.json) | Actual install profile and clean second-environment recreation; not a cross-platform lockfile |
| [Open platform checklist](PLATFORM-CHECKLIST.md) | Concrete Windows/macOS/Jupyter and troubleshooting follow-ups |

A new CPython 3.12.14 venv was created with `python -m venv /tmp/book1_setup_runtime`, then `python -m pip install numpy pandas matplotlib jupyterlab nbclient` using its interpreter. The first four packages match the manuscript's unpinned stack; nbclient is an extra QA dependency for real notebook execution. Versions are captured in results.json; they differ from the earlier V04 profile and do not replace its evidence. The shell activation was tested in a child bash; direct interpreter execution was tested separately. Package import/version checks and FV/NumPy examples execute the exact source fences, not retyped substitutes.

The initial notebook used nbclient and the environment's kernel. It failed before executing cells with `Operation not permitted (src/ip_resolver.cpp:542)` and `Kernel died before replying to kernel_info`. The observed errors support a runtime restriction diagnosis; they do not establish that the manuscript or all Jupyter versions are defective. No executed notebook artifact, HTTP response, browser screenshot or kernel-identity success is claimed. JupyterLab CLI version availability does not substitute for those checks. A local server/browser launch was not attempted after this failure.

Run the current review with the isolated environment's Python. It writes results and resolved requirements; its zero exit means the non-network checks passed, while JSON still explicitly reports blocked/not-executed items. The initial harness remains available for a capable host; do not treat it as current successful evidence.

No manuscript source or Python fence changed. Existing Chapter 1 core answers, short exercises and integrated challenges retain their separate evidence. The remaining platform, notebook and injected troubleshooting items are retained under V12; Chapter 1 is PARTIAL, not certified. Next executable review: Chapter 2 formal lab-step and answer review. Independent mathematical/editorial/model/copyright and cross-book acceptance remain separate.
