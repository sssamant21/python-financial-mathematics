# Chapter 3 formal lab-step review

Ten labs: nine standalone programs (3.4–3.12) and the Section3.13 testing lab. Six derived review units per lab make prerequisites, source, contracts, commands, outputs and limits reviewable; these are not 60 runtime cases.

## Section 3.4 — return_values_lab.py

Return versus print semantics; zero/nonfinite/type/bool/horizon guards and known values are checked by the source assertions. Arithmetic remains ambient-context dependent.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — return_values_lab.py; code hash retained in results.json
- **Review model/interface contract** — Return versus print semantics; zero/nonfinite/type/bool/horizon guards and known values are checked by the source assertions. Arithmetic remains ambient-context dependent.
- **Run documented command** — 3.4 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.5 — default_keyword_arguments_lab.py

Default contribution timing is end; source prints/checks no, end and beginning contribution outcomes 1050/1150/1155. None/default binding and timing validation remain part of the interface.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — default_keyword_arguments_lab.py; code hash retained in results.json
- **Review model/interface contract** — Default contribution timing is end; source prints/checks no, end and beginning contribution outcomes 1050/1150/1155. None/default binding and timing validation remain part of the interface.
- **Run documented command** — 3.5 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.6 — variable_scope_lab.py

Scenario state is independent; unchanged principal and two captured rates are checked. Deliberate local-binding failure is handled by the source. This does not prove concurrency safety.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — variable_scope_lab.py; code hash retained in results.json
- **Review model/interface contract** — Scenario state is independent; unchanged principal and two captured rates are checked. Deliberate local-binding failure is handled by the source. This does not prove concurrency safety.
- **Run documented command** — 3.6 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.7 — type_hints_lab.py

Type hints accompany runtime guards; full sequence validation precedes early search. Static negative fixture is checked only and never executed as a financial program.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — type_hints_lab.py; code hash retained in results.json
- **Review model/interface contract** — Type hints accompany runtime guards; full sequence validation precedes early search. Static negative fixture is checked only and never executed as a financial program.
- **Run documented command** — 3.7 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.8 — docstrings_lab.py

Doctests and explicit contract checks are different commands. A changed expected Boolean fails doctest; unsupported contribution prose still passes examples and is rejected by contract/interface review.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — docstrings_lab.py; code hash retained in results.json
- **Review model/interface contract** — Doctests and explicit contract checks are different commands. A changed expected Boolean fails doctest; unsupported contribution prose still passes examples and is rejected by contract/interface review.
- **Run documented command** — 3.8 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.9 — pv_fv_lab.py

Source checks paired PV/FV and input domains; four doctests run separately. Matching rate/period units are contractual metadata rather than encoded currency/time types.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — pv_fv_lab.py; code hash retained in results.json
- **Review model/interface contract** — Source checks paired PV/FV and input domains; four doctests run separately. Matching rate/period units are contractual metadata rather than encoded currency/time types.
- **Run documented command** — 3.9 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.10 — rate_discounting_lab.py

Nominal conversion, effective annual and discount factor are checked; six doctests run. A nominal quotation is not treated as an effective annual rate.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — rate_discounting_lab.py; code hash retained in results.json
- **Review model/interface contract** — Nominal conversion, effective annual and discount factor are checked; six doctests run. A nominal quotation is not treated as an effective annual rate.
- **Run documented command** — 3.10 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.11 — composition_lab.py

Staged rate-to-valuation composition preserves explicit period units; four doctests pass. Earlier ambient-policy implementations are not silently replaced.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — composition_lab.py; code hash retained in results.json
- **Review model/interface contract** — Staged rate-to-valuation composition preserves explicit period units; four doctests pass. Earlier ambient-policy implementations are not silently replaced.
- **Run documented command** — 3.11 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.12 — reproducibility_lab.py

A fresh fixed Decimal context isolates caller settings/flags/traps; two doctests and source reproducibility checks pass. Rounding/underflow/error-bound limitations remain.

- **Prerequisites and file layout** — Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12
- **Extract/save exact complete file** — reproducibility_lab.py; code hash retained in results.json
- **Review model/interface contract** — A fresh fixed Decimal context isolates caller settings/flags/traps; two doctests and source reproducibility checks pass. Rounding/underflow/error-bound limitations remain.
- **Run documented command** — 3.12 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — Exact complete source stdout compared, not only a PASS substring
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

## Section 3.13 — test_financial_functions.py

Requires the exact Section3.12 module beside the suite. Twelve methods pass; targeted valuation defect causes known-value failure; restored suite and isolated known-value method pass. Method count is not subcase count.

- **Prerequisites and file layout** — Section3.12 reproducibility_lab.py beside test module
- **Extract/save exact complete file** — test_financial_functions.py; code hash retained in results.json
- **Review model/interface contract** — Requires the exact Section3.12 module beside the suite. Twelve methods pass; targeted valuation defect causes known-value failure; restored suite and isolated known-value method pass. Method count is not subcase count.
- **Run documented command** — 3.13 direct command record; same Linux interpreter invoked explicitly; Windows/macOS unexecuted
- **Compare expected output** — 12-method unittest summary; elapsed time variable
- **Interpret limits and cleanup** — Temporary working directories removed; manuscript unchanged; no -O/-OO; assertions are educational checks, not external validation

