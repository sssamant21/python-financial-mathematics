"""Synthetic evidence manifest example. No validation is performed."""
import hashlib
import json
import platform
from pathlib import Path

def input_digest(data):
    """Hash exact bytes, not a mutable or implicitly serialized object."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return hashlib.sha256(data).hexdigest()

def make_manifest(data):
    return {
        "schema_version": 1,
        "scenario": "synthetic zero-rate present value",
        "formula": "PV = amount * exp(-rate * years)",
        "units": {"amount": "currency units", "rate": "per year", "years": "years"},
        "input_sha256": input_digest(data),
        "python_version_at_manifest_creation": platform.python_version(),
        "source_commit": None,
        "working_tree_dirty": None,
        "command": None,
        "execution_status": "not run",
        "exit_code": None,
        "actual_result": None,
        "expected_result": 100.0,
        "tolerance": None,
        "review_status": "pending",
        "approval_status": "pending",
    }

def write_manifest(path, data):
    path = Path(path)
    # Exclusive creation protects existing evidence from accidental replacement.
    with path.open("x", encoding="utf-8") as handle:
        json.dump(make_manifest(data), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")

if __name__ == "__main__":
    synthetic = b'{"amount":100,"rate":0,"years":2}'
    write_manifest("section_20_07_manifest.json", synthetic)
    print("Synthetic manifest created; execution and review remain pending.")
