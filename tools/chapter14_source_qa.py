#!/usr/bin/env python3
"""Chapter 14 source-fidelity Python QA: extract and run exact Markdown code fences."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

BASE = pathlib.Path("books/book-01-python-foundations-for-financial-mathematics/chapter-14")
FENCE = re.compile(r"^\x60{3}python[^\n]*\n(.*?)^\x60{3}[ \t]*$", re.MULTILINE | re.DOTALL)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", default="all", help="14.01, 14.02, or all")
    parser.add_argument("--output", default="chapter14-qa-results.json")
    args = parser.parse_args()
    files = sorted(BASE.glob("14.*.md"))
    if args.section != "all":
        files = [p for p in files if p.name.startswith(args.section + "-")]
    if not files:
        raise SystemExit("No matching section files")
    records = []
    with tempfile.TemporaryDirectory(prefix="chapter14_qa_") as td:
        for source in files:
            data = source.read_text(encoding="utf-8")
            blocks = FENCE.findall(data)
            test_blocks = [code for code in blocks if "unittest" in code and "def test_" in code]
            record = {"section": source.name, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                      "python_fences": len(blocks), "test_blocks": len(test_blocks), "blocks": []}
            if len(test_blocks) != 1:
                record["error"] = "Expected exactly one unittest reference block"
            for index, code in enumerate(test_blocks, 1):
                dest = pathlib.Path(td) / (source.stem + f"-{index}.py")
                dest.write_text(code, encoding="utf-8")
                compilation = subprocess.run([sys.executable, "-m", "py_compile", str(dest)],
                                             capture_output=True, text=True, timeout=30)
                execution = None
                if compilation.returncode == 0:
                    try:
                        execution = subprocess.run([sys.executable, str(dest)], capture_output=True,
                                                   text=True, timeout=120)
                    except subprocess.TimeoutExpired:
                        record["error"] = "Runtime timeout"
                record["blocks"].append({
                    "code_sha256": hashlib.sha256(code.encode()).hexdigest(),
                    "compile_exit": compilation.returncode,
                    "compile_stderr": compilation.stderr[-4000:],
                    "run_exit": None if execution is None else execution.returncode,
                    "stdout": "" if execution is None else execution.stdout[-5000:],
                    "stderr": "" if execution is None else execution.stderr[-8000:],
                    "tests_reported": None if execution is None else
                        (re.findall(r"Ran (\d+) tests?", execution.stderr) or [None])[-1]
                })
            record["pass"] = not record.get("error") and len(record["blocks"]) == 1 and all(
                b["compile_exit"] == 0 and b["run_exit"] == 0 and b["tests_reported"] == "12"
                for b in record["blocks"])
            records.append(record)
            print(f"{'PASS' if record['pass'] else 'FAIL'} {source.name}")
    report = {"python": sys.version, "sections": len(records), "passed": sum(r["pass"] for r in records),
              "results": records}
    pathlib.Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"QA RESULT: {report['passed']}/{report['sections']} sections passed")
    return 0 if report["passed"] == report["sections"] else 1

if __name__ == "__main__":
    sys.exit(main())
