# Section5.2 — eight local exercise answers

Original-source execution, new callers/fixtures and conceptual reasoning are distinguished per record. No independent reviewer acceptance is implied.

## 5.2-E1 — SUPPLEMENT+SOURCE

**Prompt:** Add an explicit unaliased from-import in a fourth caller and verify its output matches the existing three bindings.

New fourth_caller uses from quantity_rules import checked_quantity without alias and delegates to it. For exact Decimal0 and12.5 it matches all three original bindings. Shared implementation means four equal values are not four independent financial policies.

## 5.2-E2 — SOURCE_EXPERIMENT

**Prompt:** Define a caller variable with the same name as an imported function. Explain why the module-qualified function remains accessible if the module name is preserved.

Caller-local checked_quantity can be rebound to text without modifying quantity_rules.checked_quantity. Preserve module binding quantity_rules and its qualified function remains callable; test returns2.5. Shadowing is a readability hazard, not code copying.

## 5.2-E3 — SOURCE_EXPERIMENT

**Prompt:** Add a fresh-process test showing that assigning a new local POLICY_LABEL name does not update quantity_rules.POLICY_LABEL.

Fresh child imports POLICY_LABEL then assigns local-only to that local name. Module attribute remains nonnegative-units-v1. No mutation survives child exit; from-import binds a reference at import time, not a live attribute link.

## 5.2-E4 — SOURCE_EXPERIMENT

**Prompt:** Explain why changing a mutable imported list can affect another module, while assigning a new list to the local name does not.

A module list referenced by imported rows is shared: rows.append(A) updates module.rows. Assigning rows=[local] rebinds only caller name and leaves module.rows=[A]. List mutation and name rebinding are distinct; only synthetic ephemeral state used.

## 5.2-E5 — SUPPLEMENT

**Prompt:** Create two modules exposing a same-named validator. Use descriptive aliases to make the call sites unambiguous.

New position_policy and order_policy both expose validate and delegate to the unchanged nonnegative-units rule. Import as validate_position_units and validate_order_units; module names distinguish call sites and wrappers, zero/fraction outputs tested. No separate order-specific financial contract is invented.

## 5.2-E6 — EXPECTED_FAILURE+DESIGN

**Prompt:** Explain why catching ImportError and returning an empty report conceals a broken application.

An existing synthetic application imports a missing transitive dependency. Unhandled import traceback identifies the missing name, whereas broad except ImportError produces misleading successful[] stdout. ModuleNotFoundError is an ImportError subclass, so broad catch also hides transitive failures. Preserve traceback and correct actual dependency/interpreter; do not fabricate a dependency or silently substitute empty financial input. No real missing dependency is repaired/approved here.

## 5.2-E7 — SOURCE_EXPERIMENT

**Prompt:** Inspect the loaded module path in your lab and compare it with the file you edited.

In the owned temporary quantity_rules file append a harmless saved comment, then fresh-import and compare resolved __file__ and SHA256 against exactly that saved file. Restore original bytes afterward. __file__ is useful for this source module but not guaranteed for every Python module.

## 5.2-E8 — DESIGN

**Prompt:** Explain the difference between importing a function and copying its source into another file.

Import binds an existing module/function object and keeps the implementation owned by quantity_rules. Copying source creates another maintained definition whose corrections/version can diverge. Imports still execute module initialization and use normal caching; they do not install dependencies, sandbox code or guarantee unchanged future behavior.
