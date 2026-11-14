# Section20.1 — Testing financial code (scoped)

Source based on `815dc77f8f5accf0166b6e4c107f5d861a86f8c2`. One formal workflow, [40 individual local-answer records](answer-records.json), [12 step contracts](lab-step-records.json). No chapter-wide answer or completion percentage is inferred.

Run from repository root:
```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-testing-review/review.py
```
Pass the baseline revision as an optional argument to replay the prior source. [Initial five failures](baseline.json), [identical predicate replay](baseline-replay.json), and [corrected actual output](results.json) are retained. Corrected source:31 predicates pass, four commands pass (demo/tests, compilation, quiet import, optimized demo/tests). Twelve existing unique methods ran normally and under optimization. These are24 invocations, not24 new methods.

F201: oversized integer finite checks leaked OverflowError, near-unity returns lost subtraction accuracy, and truly unrepresentable returns leaked infinity. Strict finite validation now normalizes oversized integers to ValueError; complete represented-input Fraction return is rounded once and rejects final overflow. Independent return/ordinary NPV expectations use rational arithmetic; 110/1.1=100, −100+100=0 and.01*1000000=10000. Original twelve tests passed even on the baseline, illustrating their limited scope.

A separate [deliberately faulty return implementation](faulty_variant.py.txt) makes an existing known-return test fail (exit1); unchanged source control passes (exit0). Both outputs are saved under supplemental_fault_detection. Those two selected-method invocations bring total invocations to26 of12 existing methods;zero new historical unique methods. This synthetic failure is not a published-source defect or independent test acceptance.

Prompt alignment: positive/negative payment monotonicity assumes a future payment (t>0); time-zero payments are constant. Positional append/insertion, generator/empty/invalid domains, zero terminal return and optimization contracts are checked. Definitions, model validation, integration, leakage, simulation, currency and production readiness records are conceptual/design review. No invented parser, simulation or dated API execution.

The NPV implementation remains the stated float/log/exp model with limited extreme-discount/summation/underflow behavior; complete-range NPV and universal financial conventions are not claimed. F28 notebook/platform, F32 shared-input integration, F165/F185 and wider source/resource/platform/independent acceptance remain open. This is one Linux runtime and assistant review, not certification. Next:Section20.2 Assertions and Known-Value Tests.

Executable source/runner revision:`489c46b92214906f22e642b199a8829909a64f00`. [Pinned source manifest](publication-verification.json).
