# Editor/notebook runtime and origin checklist — design only

**Status: NOT RUN here.** Owner: QA executor on a capable approved host. F28 kernel/platform gap remains open. Successful CLI venv probes do not mark any item below complete.

| Item | Evidence to retain | Status |
|---|---|---|
| Choose supported project interpreter and kernel/editor configuration | Explicit desired interpreter path, approved Python/platform and project revision | NOT RUN |
| Inspect inside actual running editor/notebook process | sys.executable, sys.prefix, sys.base_prefix, platform.python_version/implementation | NOT RUN |
| Check selected import origin | Required project module __file__ where supplied, distribution metadata and expected installed/source location | NOT RUN |
| Bind pip to that exact executable | Interpreter -m pip --version and runtime requirements/artifact records, no bare shell pip assumption | NOT RUN |
| Restart after selection or source/module rename | Kernel identity before/after, no reliance on normal re-import for cached code edits | NOT RUN |
| Fresh-kernel run in documented order | Restart/clear state, run all cells without hidden variables, capture every cell error/output and source order | NOT RUN |
| Preserve consumed inputs/settings | Synthetic immutable snapshots, source/data/config hashes, numeric policies and exact commands/kernel spec | NOT RUN |
| Verify independent expected output and invalid-input cases | Comparison rule/derivation, actual outputs and failures, editor versus terminal differences | NOT RUN |
| Record limits/platform differences | Windows/macOS/Linux versions actually exercised, unexecuted items, owner/next action | NOT RUN |

Do not change shell execution policy or access production to complete this plan. An environment label is not authorization; use explicit interpreter/runtime evidence and approved synthetic resources. Complete actual notebook/platform evidence before resolving F28, not merely this design response.
