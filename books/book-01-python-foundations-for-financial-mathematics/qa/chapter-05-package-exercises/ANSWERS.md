# Section5.5 — eight local package exercises

Original package tests, explicit temporary package extensions, import variants and design-only distribution proposals are distinguished per record.

## 5.5-E1 — SUPPLEMENT

**Prompt:** Add a second public view function and test both its implementation path and facade behavior.

Append count_holdings to views, delegating complete validation to original capture_holdings then len(snapshot). Re-export explicitly from facade; implementation and facade are the same function object. Count includes zero (2 for B0,A12.5), empty0; invalid later row rejects. Original wildcard __all__ deliberately stays stable at two original names; new explicit public import is available without changing wildcard contract.

## 5.5-E2 — SUPPLEMENT

**Prompt:** Move a display-only helper into a new module and keep it out of __init__.py until explicitly needed.

Move entry-point display expression into finance_lab/display.py format_active_ids; returns text without printing and is not re-exported in __init__.py. Extended __main__ prints that helper result; facade-only import does not initialize display. Formatter delegates original active_ids and keeps package output unchanged.

## 5.5-E3 — SOURCE

**Prompt:** Add a test rejecting numeric security IDs and extra holding fields.

Numeric security_id raises TypeError; extra holding field raises ValueError through original capture_holdings exposed on facade. Original core source remains byte-identical in every variant.

## 5.5-E4 — SOURCE_VARIANTS

**Prompt:** Compare an internal absolute import with the current explicit relative import. Explain what package context each requires.

Relative from .holdings needs package context. Absolute from finance_lab.holdings requires finance_lab discoverable on import path but not that relative context. Both pass normal -m launch from local package parent and all8 unchanged original methods. Direct local views.py fails relative import in relative variant, and absolute variant fails because local parent is not discoverable in this plain-file configuration. An installed/discoverable package could change the latter outcome; no sys.path patch or installation is claimed.

## 5.5-E5 — SOURCE+REVIEW

**Prompt:** Explain why __all__ does not prevent importing finance_lab.holdings.

__all__ selects wildcard export names, not access control. Explicit finance_lab.holdings import works and capture identity matches facade despite not listing module in __all__. New count_holdings is explicitly importable while absent from stable wildcard set, demonstrating that distinction. Internal modules remain Python-accessible.

## 5.5-E6 — DESIGN

**Prompt:** Describe the difference between the directory name used by import and a future distribution name used for installation.

Directory finance_lab is a regular import package namespace, not an installation record. A future distribution metadata name may differ, contain hyphens, or provide multiple import packages; choose it explicitly and declare metadata/entry points rather than infer it from folder. No registry ownership or installed finance_lab distribution claimed.

## 5.5-E7 — SUPPLEMENT

**Prompt:** Add a nested regular subpackage with its own __init__.py and test its fully qualified name.

Add finance_lab/reports/__init__.py with explicit count_report export and reports/summary.py using from ..views import count_holdings. Fully qualified names finance_lab.reports and finance_lab.reports.summary verified; report returns holding_count2 or0 without money aggregation. Parent package modules do not depend on nested reporting facade.

## 5.5-E8 — DESIGN

**Prompt:** Explain what additional work is needed to distribute this package to another environment reliably.

Reliable distribution requires declared project/build metadata, package discovery including nested package, supported Python/runtime/development requirements, reviewed backend/artifact sources, regular wheel build and retained digest, fresh install outside checkout with origin/version/CLI/API/error tests, fixtures/resource policy and documented recreation. Review supported platform/version behavior, license/provenance/security and compatibility policy before sharing/release; installation alone cannot validate financial semantics. No wheel of this extended finance_lab or public upload tested here.
