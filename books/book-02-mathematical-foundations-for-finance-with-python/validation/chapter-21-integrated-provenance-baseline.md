# Chapter 21 integrated report: execution evidence baseline

This starts the separate COV-88 obligation for the actual capstone report. On [pinned source `7b2430e2a88336993306dd6b1394ee250cb357e2`](https://github.com/sssamant21/python-financial-mathematics/blob/7b2430e2a88336993306dd6b1394ee250cb357e2/books/book-02-mathematical-foundations-for-finance-with-python/chapter-21/code/section_21_09.py) (entry point blob `ca2ff456691be2946163995558ecca4518b37f95`), two independent CLI processes produced byte-identical strict JSON under the observed Linux runtime. SHA-256: `e80374afef36633e76c1c3535f8a9434b2df1ae297bcfbdfe8e5cc725884f91e`. The payload intentionally reports `validation_execution: "not run"`, `independent_review: "pending"` and `approval: "pending"`. It is a teaching payload with no run receipt.

The observed examples agree with simple independent references: PV (100/2=50); first and second derivatives (-2(100)=-200) and (2^2(100)=400); replication by subtracting equations gives weights (1,2); the allocation shifts both targets by (0.05) to sum to one; the account ends at (1000+3(200)=1600). These observations identify the output to bind to an execution record. They do not replace existing numerical coverage or constitute a new sign-off.

From `chapter-21/code` at the pinned revision, run:

```sh
out=$(mktemp -d)
python section_21_09.py > "$out/first.json"
python section_21_09.py > "$out/second.json"
cmp "$out/first.json" "$out/second.json"
python -m json.tool "$out/first.json"
```

Next: retain an external run record that binds the actual capstone command and stdout to its entry point and imported source bytes, and check that a changed dependency or altered output is detected. Keep the run receipt separate from the report's pending validation/review/approval fields. See the [requirements map](chapter-21-capstone-requirements-evidence-map.md).
