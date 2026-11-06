"""Synthetic evidence template and a bounded local execution example."""
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
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

def _write_payload(path, manifest):
    payload = json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n"
    destination = Path(path)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
            prefix=".evidence-", suffix=".tmp", delete=False,
        ) as handle:
            staged = Path(handle.name)
            handle.write(payload)
        # Publish only a closed file. Linking fails if the name already exists,
        # including when another writer wins between staging and publication.
        os.link(staged, destination)
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def write_manifest(path, data):
    _write_payload(path, make_manifest(data))


_MAX_INPUT = 4096
_TIMEOUT = 5
_SYNTHETIC = b'{"amount":100,"rate":0,"years":2}'


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          check=True, timeout=_TIMEOUT).stdout


def _observe(root, source):
    return {
        "commit": _git(root, "rev-parse", "--verify", "HEAD").decode("ascii").strip(),
        "dirty": bool(_git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")),
        "script_sha256": input_digest(source.read_bytes()),
    }


def record_execution(path, data):
    """Execute the fixed zero-rate worker and write its observed provenance."""
    manifest = make_manifest(data)
    if len(data) > _MAX_INPUT:
        raise ValueError("scenario input exceeds 4096 bytes")
    source = Path(__file__).resolve()
    try:
        raw_root = _git(source.parent, "rev-parse", "--show-toplevel")
        root = Path(raw_root.decode(sys.getfilesystemencoding()).rstrip("\n")).resolve()
        relative = source.relative_to(root).as_posix()
        _git(root, "ls-files", "--error-unmatch", "--", relative)
        before = _observe(root, source)
    except subprocess.CalledProcessError as exc:
        raise ValueError("runner must be tracked in a Git checkout with a commit") from exc

    argv = [sys.executable, "-I", "-B", relative, "--worker"]
    child = subprocess.run(argv, cwd=root, input=data, capture_output=True, timeout=_TIMEOUT)
    after = _observe(root, source)
    stdout, stderr = child.stdout.decode("utf-8"), child.stderr.decode("utf-8")
    manifest.update(
        source_commit=before["commit"], working_tree_dirty=before["dirty"],
        source_before=before, source_after=after, source_observation_changed=before != after,
        source_path=relative, command=argv, command_cwd="repository root",
        python_implementation=platform.python_implementation(), platform=platform.platform(),
        execution_status="succeeded" if child.returncode == 0 else "failed",
        exit_code=child.returncode, stdout=stdout, stderr=stderr,
        actual_result=json.loads(stdout) if child.returncode == 0 else None,
        expected_result=None,
    )
    _write_payload(path, manifest)
    return manifest


def _worker():
    try:
        data = sys.stdin.buffer.read(_MAX_INPUT + 1)
        if len(data) > _MAX_INPUT:
            raise ValueError("oversized scenario")
        scenario = json.loads(data)
        if type(scenario) is not dict or set(scenario) != {"amount", "rate", "years"}:
            raise ValueError("invalid keys")
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in scenario.values()):
            raise ValueError("nonfinite or nonnumeric input")
        if scenario["rate"] != 0 or scenario["years"] < 0:
            raise ValueError("not a zero-rate scenario")
    except (ValueError, OverflowError, RecursionError):
        sys.stderr.buffer.write(b"invalid zero-rate scenario\n")
        return 2
    payload = json.dumps({"present_value": float(scenario["amount"])},
                         separators=(",", ":"), allow_nan=False) + "\n"
    sys.stdout.buffer.write(payload.encode("utf-8"))
    return 0


def main():
    if sys.argv[1:] == ["--worker"]:
        return _worker()
    if len(sys.argv) == 3 and sys.argv[1] == "--run":
        try:
            record = record_execution(sys.argv[2], sys.stdin.buffer.read(_MAX_INPUT + 1))
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        return record["exit_code"]
    if len(sys.argv) != 1:
        print("usage: section_20_07.py [--run OUTPUT]", file=sys.stderr)
        return 1
    write_manifest("section_20_07_manifest.json", _SYNTHETIC)
    print("Synthetic manifest created; execution and review remain pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
