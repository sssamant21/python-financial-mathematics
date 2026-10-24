"""Run the fifteen Chapter 01 reference-check scripts and optionally save evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


def run_chapter():
    chapter = Path(__file__).resolve().parents[1]
    results = []
    for number in range(1, 16):
        relative = f"code/check_section_1_{number:02}.py"
        script = chapter / relative
        if script.is_file():
            completed = subprocess.run([sys.executable, relative], cwd=chapter,
                                       capture_output=True, text=True)
            result = {"command": f"python {relative}", "return_code": completed.returncode,
                      "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip()}
        else:
            result = {"command": f"python {relative}", "return_code": None,
                      "stdout": "", "stderr": "required check script is missing"}
        results.append(result)
    files = sorted((chapter / "code").glob("*.py")) + sorted((chapter / "data").glob("*.json"))
    return {"python_version": platform.python_version(), "platform": platform.platform(),
            "scope": "fifteen section reference-check scripts; written reasoning and canonical review separate",
            "passed": sum(row["return_code"] == 0 for row in results), "required": 15,
            "success": all(row["return_code"] == 0 for row in results), "commands": results,
            "sha256": {str(p.relative_to(chapter)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional evidence JSON path")
    args = parser.parse_args()
    report = run_chapter()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for number, row in enumerate(report["commands"], start=1):
        print(f"Section 1.{number:02}: {'PASS' if row['return_code'] == 0 else 'FAIL'}")
    print(f"Chapter reference checks: {report['passed']}/{report['required']} passed")
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
