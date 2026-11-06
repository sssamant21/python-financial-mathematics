"""Run the Section 20.7 example in an isolated Git fixture and compare records."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


SOURCE = "section_20_07.py"
DATA = b'{"amount":100,"rate":0,"years":2}'
INVALID = b'{"amount":100,"rate":0.01,"years":2}'


def run(source):
    rows = []

    def check(name, expected, operation):
        try:
            actual = operation()
        except Exception as exc:
            actual = {"exception": type(exc).__name__}
        rows.append(dict(case=name, expected=expected, actual=actual, passed=actual == expected))

    def command(*args, **kwargs):
        return subprocess.run(args, cwd=root, capture_output=True, timeout=15, **kwargs)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target = root / SOURCE
        shutil.copyfile(source, target)
        command("git", "init", "-q", check=True)
        command("git", "add", SOURCE, check=True)
        command("git", "-c", "user.name=Lab", "-c", "user.email=lab@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-qm", "fixture", check=True)
        commit = command("git", "rev-parse", "HEAD", check=True).stdout.decode().strip()
        version = command(sys.executable, "-I", "--version", check=True).stdout.decode().strip().split()[-1]

        def cli(*args):
            return command(sys.executable, "-I", "-B", SOURCE, *args)

        synthetic = cli()
        placeholder = root / "section_20_07_manifest.json"
        p = json.loads(placeholder.read_bytes())
        check("default remains synthetic", [0, "not run", None, None, "pending", "pending"],
              lambda: [synthetic.returncode, p["execution_status"], p["source_commit"],
                       p["actual_result"], p["review_status"], p["approval_status"]])
        placeholder.unlink()

        argv = [sys.executable, "-I", "-B", SOURCE, "--worker"]
        for case, data, dirty, code, out, err, actual in (
            ("clean success", DATA, False, 0, b'{"present_value":100.0}\n', b"", {"present_value": 100.0}),
            ("dirty failure", INVALID, True, 2, b"", b"invalid zero-rate scenario\n", None),
            ("tracked edit success", b'{"amount":-17.5,"rate":0,"years":0}', True, 0,
             b'{"present_value":-17.5}\n', b"", {"present_value": -17.5}),
        ):
            if case == "dirty failure":
                (root / "untracked.txt").write_text("known dirt", encoding="utf-8")
            if case == "tracked edit success":
                (root / "untracked.txt").unlink()
                target.write_bytes(target.read_bytes() + b"\n# known tracked change\n")
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            report_path = root / "run.json"
            # Independent child run supplies raw streams and exit; fixed literals
            # also check that the child itself performs the advertised computation.
            child = command(*argv, input=data)
            check(case+" child exit and streams", [code, out.decode(), err.decode()],
                  lambda: [child.returncode, child.stdout.decode(), child.stderr.decode()])
            driver = command(
                sys.executable, "-I", "-B", SOURCE, "--run", str(report_path), input=data)
            check(case+" CLI exit", code, lambda: driver.returncode)
            def fields(*keys):
                payload = json.loads(report_path.read_bytes())
                return [payload[key] for key in keys]
            state = {"commit": commit, "dirty": dirty, "script_sha256": digest}
            check(case+" source snapshots", [state, state, False],
                  lambda: fields("source_before", "source_after", "source_observation_changed"))
            check(case+" command and interpreter", [argv, version, SOURCE],
                  lambda: fields("command", "python_version_at_manifest_creation", "source_path"))
            check(case+" input and outcome", [hashlib.sha256(data).hexdigest(), code,
                  "succeeded" if code == 0 else "failed", actual],
                  lambda: fields("input_sha256", "exit_code", "execution_status", "actual_result"))
            check(case+" exact output and review state",
                  [out.decode(), err.decode(), "pending", "pending"],
                  lambda: fields("stdout", "stderr", "review_status", "approval_status"))
            if report_path.exists():
                report_path.unlink()
        oversized = command(sys.executable, "-I", "-B", SOURCE, "--run", "large.json",
                            input=b" " * 4097)
        check("oversized input rejected before publication", [1, False, True],
              lambda: [oversized.returncode, (root/"large.json").exists(),
                       b"input exceeds 4096 bytes" in oversized.stderr])
        command("git", "rm", "--cached", "-q", SOURCE, check=True)
        result = command(sys.executable, "-I", "-B", SOURCE, "--run", "untracked.json", input=DATA)
        check("untracked recorder refuses attribution", [1, False, True],
              lambda: [result.returncode, (root/"untracked.json").exists(),
                       b"runner must be tracked" in result.stderr])
    print(json.dumps(rows, allow_nan=False))
    return all(row["passed"] for row in rows)


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name(SOURCE)
    raise SystemExit(0 if run(target) else 1)
