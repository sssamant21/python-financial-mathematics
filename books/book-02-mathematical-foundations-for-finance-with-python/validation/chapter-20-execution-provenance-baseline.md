# Section 20.7 execution provenance: baseline and next checks

COV-86 remains partially addressed. The [manifest preflight checks](chapter-20-manifest-preflight-followup.md) covered validation and exclusive creation. This checkpoint starts the separate open obligation for actual source, environment and command provenance.

On [pinned source `b8d9ad694136393a36aca2c06d9c0798062cb21c`](https://github.com/sssamant21/python-financial-mathematics/blob/b8d9ad694136393a36aca2c06d9c0798062cb21c/books/book-02-mathematical-foundations-for-finance-with-python/chapter-20/code/section_20_07.py) (module blob `ba7b73820ac8503b4e284ebf40c3aa07c9e60a48`), the actual CLI succeeded in an isolated empty directory and wrote a strict JSON manifest. The digest matched an independently computed SHA-256 of the literal input bytes. As documented for the synthetic example, it recorded `source_commit`, `working_tree_dirty`, `command`, `exit_code` and `actual_result` as null, `execution_status` as `"not run"`, and review and approval as pending. These observations record the provenance feature boundary; they are not a failure of the synthetic template.

Replay with assertions enabled, using an absolute path to the pinned module:

```sh
module=/absolute/path/to/chapter-20/code/section_20_07.py
out=$(mktemp -d)
cd "$out"
python "$module"
python - <<'PY'
import hashlib
import json
from pathlib import Path

report = json.loads(Path("section_20_07_manifest.json").read_text())
assert report["input_sha256"] == hashlib.sha256(b'{"amount":100,"rate":0,"years":2}').hexdigest()
for key in ("source_commit", "working_tree_dirty", "command", "exit_code", "actual_result"):
    assert report[key] is None, (key, report[key])
assert report["execution_status"] == "not run"
assert report["review_status"] == report["approval_status"] == "pending"
PY
```

Next check a bounded local execution record against independently observed source state, interpreter, arguments, exit status and output, while preserving the synthetic example. Use a temporary Git fixture and deterministic success and failure commands. Keep operational provenance, evidence authenticity and approval distinct. Wider Chapter 19 capstone provenance and independent review remain open.
