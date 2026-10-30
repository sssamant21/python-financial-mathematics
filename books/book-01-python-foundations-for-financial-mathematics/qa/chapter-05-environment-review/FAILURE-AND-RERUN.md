# Observer failure, expected negatives and corrected rerun

The first new QA observer used runpy.run_path without restoring the direct-script sibling import path. Section5.6 and5.7 completed, but5.8 could not import its present sibling pip_dependency_lab.py. The aggregation harness then attempted to decode absent evidence stdout and raised JSONDecodeError. No manuscript defect was inferred.

Initial observer/runner snapshots and raw child traces are retained under initial-attempt. [Reproduced original import failure](initial-attempt/failure.json) records actual nonzero exit and ModuleNotFoundError; [initial child records](initial-attempt/5-8-children.json) are empty because import failed before any child launch. The failed outer attempt did not produce final results.json; no missing result is represented as a pass. Nested initial Python files are historical snapshots, not standalone reproduction entry points.

Correction: observer sets sys.path[0] to the extracted script's directory and argv to that script, matching normal direct-file semantics. Published source remains unchanged. Final runner records a failed source before trying to decode its evidence. Final three workflows, quiet imports and supported manual setup pass27 predicates in results.json. No tests or source guards were weakened.

Separately, final traces retain intentional nonzero child operations:5.6 pip check after deliberate dependency removal, then approved repair;5.8 hash rejection of changed wheel, then approved original installation. These expected failures are requirements of the workflow. Their raw diagnostics/returncodes remain visible rather than folded into a claim that every child command returned zero. No original source unit-test methods are added by these workflows.
