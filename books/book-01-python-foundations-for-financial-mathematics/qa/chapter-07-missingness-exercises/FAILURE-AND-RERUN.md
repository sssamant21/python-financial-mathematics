# F37 — QA regex-module name shadowing

Affected baseline main `8cbba0741fd27713b7cf67b2c5d97c558a1b6e04`; severity low; owner QA executor. This was a new harness error,not a manuscript defect.

The initial runner assigned the explicit-missing report to a local variable named re. Python therefore treated re as local throughout run(),and the earlier re.findall source extraction raised UnboundLocalError. The initial attempt aborted before any source file assembly,command execution or predicate results. It does not count as a failed manuscript test or reference-method invocation.

[Exact initial runner](review-initial.py) and [reproduced returncode/stdout/traceback](initial-failure.json) retain the original bytes and diagnosis. Run python3 -B on review-initial.py to reproduce the expected failure. The retained reproduction has exit1 and zero source commands executed. No past failure record was removed.

The corrected [runner](review.py) uses explicit_report for that local output. No manuscript code or numerical expectation changed. The [corrected rerun](results.json) passes3 command checks,24 predicates and8 existing methods. The initial runner's SHA256 is 7badb51eeec43f79168c6e33b971f8feae34c4bda0d6fa8978844ca7c745f437; corrected runner's SHA256 is 1c20d31625127c745e13bfcd2f878b6ad5436bd90ce7097fe7c4c6c9807deb43.

Status: RESOLVED QA HARNESS within this batch. Broader numerical,input/platform and independent acceptance remain open. Avoid module names for local result variables;syntax compilation alone cannot detect this runtime binding error.
