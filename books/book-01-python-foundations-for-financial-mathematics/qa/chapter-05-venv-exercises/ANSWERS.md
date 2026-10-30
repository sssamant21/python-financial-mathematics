# Section5.7 — eight environment exercise answers

Exact source probes/recipe, new orchestration, expected shadowing error and design-only records are distinguished per prompt.

## 5.7-E1 — SOURCE_PROBES

**Prompt:** Print the five inspected runtime fields for both environments and explain which establish environment identity.

Both child INFO_CODE outputs retain executable,prefix,base_prefix,purelib,isolated. Executable is the actual selected path; prefix identifies environment, purelib its import/install target; base_prefix identifies shared base and differs from each venv. isolated1 is mode, not unique identity. Config system-site=false checked. Do not resolve executable symlink alone and mistake shared binary for shared environment.

## 5.7-E2 — SOURCE_PROBES

**Prompt:** Add a check that the two purelib paths differ.

Explicit resolved purelib paths for A/B differ and each lies under its owned prefix. Same base runtime/library availability does not collapse their separate local site-packages.

## 5.7-E3 — EXPECTED_SHADOW_FAILURE+SOURCE

**Prompt:** Repeat the marker probe without -I from a directory containing a same-named source file. Explain why source shadowing is different from package isolation.

Use exact original marker recipe in A/B purelib, plus same-named synthetic SHADOW file in working directory. Original BEHAVIOR_CODE without-I fails its origin assertion before quantities; diagnostic and separately inspected shadow origin retained. -I imports intended A marker and original behavior passes again. Environment prefix staysA while source lookup can be shadowed; normal CWD lookup is not loss of site-packages isolation. PYTHONPATH/PYTHONHOME/PYTHONSAFEPATH controlled for this experiment, no sys.path repair.

## 5.7-E4 — SUPPLEMENTAL_SETUP

**Prompt:** Add pip to a separate disposable environment using normal supported venv creation and inspect its version through the explicit interpreter.

Separate disposable normal venv creation includes ensurepip. Explicit environment interpreter -m pip --version succeeds and path is beneath that venv. Automated original marker lab still uses no-pip environments; no downloaded package or activation required.

## 5.7-E5 — SOURCE_RUNTIME

**Prompt:** Explain why setting VIRTUAL_ENV alone does not select an interpreter.

Compare all five runtime fields before/after setting only child VIRTUAL_ENV to A while invoking same current interpreter. Fields unchanged: variable can label shell state but cannot select an executable, change prefix or move a running kernel. Explicit path/actual runtime metadata determine selection. Parent environment is never modified.

## 5.7-E6 — DESIGN

**Prompt:** Design an editor/notebook checklist that records the runtime executable and import origin.

Retained EDITOR-NOTEBOOK-CHECKLIST lists interpreter/kernel selection, executable/prefix/base identity, import origin, pip binding, fresh-kernel ordered rerun, immutable inputs and captured outputs/errors. All checklist execution items NOT_RUN here: this is a requested plan, not actual editor/notebook validation. F28 remains open.

## 5.7-E7 — DESIGN

**Prompt:** Define the minimum source and dependency records needed to recreate a real financial project's environment.

Retain reviewed source/test revision and hashes, public contracts, creation/run instructions, Python implementation/version/platform target, exact direct/transitive requirements plus approved artifacts/hashes and build backend when relevant, input/config/reference-data snapshots and numeric/model policies, interpreter/import-origin evidence, known/invalid cases and result-comparison criteria. Exclude disposable venv directory. These are minimum categories for an actual project, not a claim that this marker fixture reproduces a real financial workload.

## 5.7-E8 — DESIGN+BENIGN_PROBE

**Prompt:** Explain why venv should not be used as a sandbox for untrusted programs.

A venv separates Python install paths, not OS permissions, files, network or credentials. Selected child successfully reads an owned synthetic file outside its venv under normal process permissions, demonstrating no filesystem jail without probing unrelated user/production data. Untrusted-code isolation needs an appropriate reviewed OS/container/VM/resource/identity/network boundary; no security sandbox certification, remote access or untrusted program execution is claimed.
