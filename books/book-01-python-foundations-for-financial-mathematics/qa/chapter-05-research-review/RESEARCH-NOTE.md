# Research note — synthetic USD inflow aggregation

Question: do unchanged supplied files under this recorded runtime produce identical artifacts and the declared bounded sum-then-round result?

Run: exact extracted Section5.11 research.py, two fresh output names, CPython3.12.14 Linux. Commands and actual stdout/stderr are in results.json. Both successful commands produce no stdout; comparison prints Identical run artifacts. Existing-name rerun and invalid-input attempt return nonzero as required; original output preserved and no invalid-output file created.

Independent expected total: (10005+20005)/1000=30.010USD, once rounded half-even to cents30.01. Fraction/integer-cent oracle separately checks even/odd ties and maximum total1000000000.00. Local repeat supports identical artifact bytes for these source/data/config/runtime fields, not independent reproduction or economic robustness.

The retained research-bundle contains the exact source, test, input/config snapshots and both actual output artifacts. Its source/input/config digests can be recomputed and compared with output evidence; current manuscript/code hashes are in the review results. No wheel/backend/runtime was required here. Relevant limitations include missing interpreter binary identity, test/full-repository digest within the source program's own artifact, crash-atomic write, other-platform/kernel execution, authentic/historically available market inputs and independent reviewer acceptance. F28 notebook/platform remains open. Do not treat mere file presence or digest equality as successful/approved financial research.
