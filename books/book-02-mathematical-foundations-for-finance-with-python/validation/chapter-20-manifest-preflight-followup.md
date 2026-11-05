# Section 20.7 manifest preflight and exclusive creation

Date: 2026-11-05. Baseline: `503edbdc3e622f98acabea861a53ac1581b9132f`. Corrected executable revision: `081a73dce77591e11377df37ff7b23c5d1836674`. Final combined Chapter 20 revision: `081a73dce77591e11377df37ff7b23c5d1836674`.

The writer validates bytes and serializes a complete strict JSON payload before opening the output path in exclusive-create mode. Invalid data or serialization no longer reserves an empty or partial path, and a valid retry can use the same destination. A valid collision still raises FileExistsError and leaves existing bytes intact. Invalid input takes precedence over opening, even at an existing path. These checks do not establish atomicity or cleanup after an actual write or filesystem failure.

Actual temporary-directory cases exercise invalid input and retry, injected serialization failures, a known digest and pending fields on disk, and collision protection. Seven of ten baseline rows failed; all ten corrected rows pass. The first baseline wrapper printed the counts then hit KeyError: 'helper' while formatting the already-saved rows; its checker exit and complete rows were retained, and the wrapper key was corrected separately. This is manifest behavior evidence, not completed execution provenance or evidence authenticity.

Final combined scope: 33 compiled files and 22 passing scripts, with matching Git blob hashes before and after. [Raw baseline, rerun and scoped hashes](chapter-20-manifest-preflight-followup.json) · [Runnable checker](../chapter-20/code/check_manifest_preflight.py).

Replay from Book 02's chapter-20/code at the corrected revision: run python check_manifest_preflight.py with assertions enabled. For the baseline, save the checker externally, check out the stated baseline and overlay only that checker. Compile each .py via py_compile.compile(path,doraise=True), run check_/test_ basenames in separate processes from their parent directories with a 60-second timeout, and verify raw Git blob hashes before and after. Successful stdout is omitted from the scope summary.

Selected assistant-run Linux evidence only. No independent sign-off, supported-platform validation, release acceptance or canonical approval.
