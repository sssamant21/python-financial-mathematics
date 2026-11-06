"""Capture and check a Section 21.9 receipt in an isolated source-only directory."""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ENTRY = "section_21_09.py"
FILES = (ENTRY, *(f"section_21_{i:02}.py" for i in range(3, 8)))
BOOTSTRAP = "import runpy,sys; sys.path.insert(0,'.'); runpy.run_path(sys.argv[1],run_name='__main__')"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_hashes(sources):
    return {name: sha(data) for name, data in sorted(sources.items())}


def read_sources(directory):
    # Scope is the fixed report and its current explicit chapter-local imports.
    sources = {name: (directory / name).read_bytes() for name in FILES}
    pending, seen = [ENTRY], set()
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        for node in ast.walk(ast.parse(sources[name], filename=name)):
            if isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:
                continue
            for module in modules:
                if module.startswith("section_21_"):
                    target = module + ".py"
                    if target not in sources:
                        raise ValueError(f"unexpected local dependency: {target}")
                    pending.append(target)
    if seen != set(sources):
        raise ValueError("fixed source inventory no longer matches the report")
    return sources


def execute(sources):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, data in sources.items():
            (root / name).write_bytes(data)
        argv = [sys.executable, "-I", "-B", "-c", BOOTSTRAP, ENTRY]
        result = subprocess.run(argv, cwd=root, capture_output=True, timeout=15)
        if source_hashes(read_sources(root)) != source_hashes(sources):
            raise ValueError("isolated sources changed during execution")
    return {
        "source_sha256": source_hashes(sources),
        "command": argv, "cwd": "temporary source-only directory",
        "environment": {"python": sys.version, "platform": platform.platform()},
        "exit_code": result.returncode,
        "stdout": result.stdout.decode("utf-8"), "stdout_sha256": sha(result.stdout),
        "stderr": result.stderr.decode("utf-8"), "stderr_sha256": sha(result.stderr),
    }


def differences(reference, observed):
    reasons = []
    for stream in ("stdout", "stderr"):
        for label, record in (("reference", reference), ("observed", observed)):
            if sha(record[stream].encode("utf-8")) != record[stream + "_sha256"]:
                reasons.append(f"{label} {stream} hash inconsistent")
    for key in ("source_sha256", "command", "cwd", "environment", "exit_code",
                "stdout_sha256", "stderr_sha256"):
        if reference[key] != observed[key]:
            reasons.append(key + " differs")
    return reasons


def reject_constant(value):
    raise ValueError(f"nonfinite JSON value: {value}")


def verify(directory):
    sources = read_sources(directory)
    first, second = execute(sources), execute(sources)
    report = json.loads(first["stdout"], parse_constant=reject_constant)
    dep = "section_21_03.py"
    changed = execute({**sources, dep: sources[dep] + b"\n# changed bytes, same calculation\n"})
    wrong_output = first["stdout"].replace('"value": 50.0', '"value": 51.0', 1)
    assert wrong_output != first["stdout"]
    altered = {**first, "stdout": wrong_output}
    rehashed = {**altered, "stdout_sha256": sha(wrong_output.encode("utf-8"))}
    failed = execute({**sources, dep: b'raise RuntimeError("injected dependency failure")\n' +
                      sources[dep]})
    def one(case, expected, actual):
        return dict(case=case, expected=expected, actual=actual, passed=expected == actual)
    rows = [
        one("two isolated runs agree", [], differences(first, second)),
        one("actual command completes cleanly", [0, ""], [first["exit_code"], first["stderr"]]),
        one("byte hash of actual stdout", first["stdout_sha256"], sha(first["stdout"].encode())),
        one("present value, analytic derivatives, replication and account",
            [50.0, [-200.0, 400.0], [1.0, 2.0], 1600.0],
            [report["cash_flow"]["value"], report["sensitivity"]["first_second"],
             report["replication"]["solution"], report["account"]["ending_balance"]]),
        one("allocation projection within tolerance", True,
            all(math.isclose(got, expected, rel_tol=0, abs_tol=1e-14)
                for got, expected in zip(report["allocation"]["weights"], (.75, .25), strict=True))),
        one("teaching status untouched", ["not run", "pending", "pending"],
            [report[k] for k in ("validation_execution", "independent_review", "approval")]),
        one("dependency change detected even when output matches", ["source_sha256 differs"],
            differences(first, changed)),
        one("altered output without changed hash", ["observed stdout hash inconsistent"],
            differences(first, altered)),
        one("altered output with changed hash", ["stdout_sha256 differs"],
            differences(first, rehashed)),
        one("real import failure is retained", [1, "", True],
            [failed["exit_code"], failed["stdout"], "injected dependency failure" in failed["stderr"]]),
    ]
    return {"receipt": first, "negative_receipt": failed, "checks": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("code", nargs="?", type=Path,
                        default=Path(__file__).resolve().parent.parent / "chapter-21" / "code")
    args = parser.parse_args()
    evidence = verify(args.code)
    print(json.dumps(evidence, indent=2, allow_nan=False))
    raise SystemExit(0 if all(r["passed"] for r in evidence["checks"]) else 1)
