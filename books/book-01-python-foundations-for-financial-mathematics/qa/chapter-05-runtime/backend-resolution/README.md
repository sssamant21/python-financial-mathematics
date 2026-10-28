# Chapter 5 — Pinned backend resolution and installed-package checks

**Date:** 2026-10-27. **Reviewer / execution owner:** Codex. **Finding:** F13 RESOLVED. **Source:** Chapter 5 manuscripts unchanged through `840bd6d123258a0dfbff4967765f38536d37e17e`; the comparison from initial evidence commit `516de89a0f14772a6b4a7e2539ac1763874ca5f6` returned no changed Book 1 files. Source SHA-256 values are recorded in [results.json](results.json).

## Result

The exact declared backend, setuptools 84.0.0, was prepared in a dedicated builder. Both published verification workflows passed without loosening the version guard or changing the package implementation:

| Run | Installed tests | Additional verifier checks | Compilation |
|---|---:|---|---|
| Section 5.12 base project | 8 passed | Regular wheel build/install, external isolated import origin, module/console CLI parity, invalid arguments, pip check and temporary runtime cleanup passed | Passed |
| Section 5.13 extended companion | 12 passed | The same checks, including the four companion acceptance methods, passed | Passed |

The companion copy contains exactly the documented extension insertion and success-message update. Actual unittest counts and zero exit codes were checked by the [driver](run_package_checks.py), rather than accepting the verifier's printed success message alone. Detailed outputs: [base.log](base.log), [extended.log](extended.log), [base compilation](base-compile.log), [extended compilation](extended-compile.log).

The twelve extended methods include the eight base methods. Across these two runs there were twenty test invocations, representing twelve distinct installed methods. Together with the earlier 68 methods, Chapter 5 contributes **80 distinct passing reference test methods** to the tracker, avoiding double-counting the base rerun. Earlier demonstrations, environment workflows and initial failures remain in the [initial evidence](../README.md).

## Builder provenance

The dedicated builder used Python 3.12.14, pip 25.0.1 and setuptools 84.0.0 on Linux x86_64. The downloaded wheel was `setuptools-84.0.0-py3-none-any.whl`, 818216 bytes.

SHA-256: `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`.

The digest matched the version-specific PyPI JSON metadata fetched over HTTPS. [builder-evidence.json](builder-evidence.json) records the metadata URL, artifact URL, hashes and tool versions; [builder-install.log](builder-install.log) records installation from the local wheel. The shared interpreter's setuptools was not replaced. The initial lack of an exact cached artifact was resolved by downloading the declared version.

Backend preparation involved an external PyPI download and metadata lookup. After preparation, the project verifiers built wheels with `--no-index --no-deps --no-build-isolation` and installed them in fresh temporary runtimes with no package-index access.

## Reproduction

Use new output and builder directories. From the repository root, on Linux:

```sh
python -m pip download --no-deps --only-binary=:all: --dest /tmp/ch05-backend setuptools==84.0.0
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-runtime/backend-resolution/prepare_builder.py /tmp/ch05-backend
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-runtime/backend-resolution/run_package_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-05 /tmp/ch05-packages-new /tmp/ch05-backend/builder/bin/python
```

The preparation script verifies the downloaded artifact against PyPI metadata and installs it locally in a dedicated venv. The package driver reconstructs fresh base and extended projects from the manuscripts, invokes their verifiers, checks actual test counts (8 and 12), and compiles both projects. The output directory must not already exist. Windows commands and execution remain unverified.

## Artifact and acceptance limits

The verifiers reported these actual built wheel hashes:

- Base: `204618198eca44dbfb50c6fa111d4462bac02219ce15b173bb6d071c760ae26e`.
- Extended-run build: `a2215c43044796bdc252cd13c05ca28bd42f6ce7174a51583e85c372f1d6e883`.

Temporary project wheels and runtime environments were removed by the published verifiers. Wheel equality across rebuilds was not asserted; ZIP/build metadata can differ. These records establish the scoped regular-wheel checks, not bit-for-bit reproducible builds, cross-platform acceptance, package-index publication, security certification or independent financial validation.

**Disposition:** F13 is resolved for this environment and source scope. Continue with Chapter 4 runtime evidence reconciliation.
