# Chapter5 — Section5.5 local package exercises

Based on main `88f8f44bd7305872df77706842eff53e82c43d58`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results/source and extension snapshots](results.json)

CPython3.12.14 Linux: **eight command records satisfied expectations**, **19 predicates passed**, and **24 invocations of8 existing original methods** passed (baseline, extended relative package, extended absolute-import variant). Counts are separate; no historical unique methods/workflows added. Initial run passed; no unexpected failures or manuscript corrections. Two deliberate wrong-context child errors are retained with raw tracebacks and checked against specific diagnostics; these are satisfied negative checks, not successful imports.

Reproduce using standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-package-exercises/review.py
```

All original package/test listings are reconstructed unchanged for baseline, hashed and recorded. New temporary-copy code adds count view/facade export, extracts display formatting, and creates regular nested reports package. Extended source snapshots and alternate absolute-view hash retained; original core validation unchanged, relative variant restored after comparison. These are supplemental exercise implementations, not published manuscript/package API changes.

count_holdings and nested holding_count are cardinalities including zero, not quantities or values. Explicit zero/fraction input expectations, object-identity checks between implementation/facade, original behaviors, source ownership, full validation, wildcard names, lazy display initialization, nested module names and empty views checked. Old __all__ deliberately remains stable while the new view is explicitly re-exported, so original wildcard contract/tests need no weakening. __all__ does not hide explicit implementation modules.

Both internal import forms work in package-aware launch with discoverable parent. Relative plain-file views.py has no known parent package; absolute plain-file variant cannot discover finance_lab under this local, noninstalled layout. The latter is a path/distribution condition, not a universal statement that absolute imports need relative context. No sys.path repair or installed-finance_lab claim. Existing -m package output remains exact after display extraction.

All eight prompts have scoped answers. Import/distribution naming and release/recreation requirements are conceptual reviews, not a wheel build or certified handoff for this extended package. Nested subpackage is regular with its own __init__, explicit internal dependency direction and no application startup work. No static checker, Windows/macOS, notebook/kernel, registry, external data, valuation or independent acceptance executed. F28/F32 remain open and prior F33 history retained.

42 of96 local prompts now reviewed;54 remain. Next: Section5.6 dependency exercises, then queue order; skip already completed5.12-E2/E3 unless source changes.
