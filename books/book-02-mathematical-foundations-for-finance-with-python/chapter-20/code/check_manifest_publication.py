"""Check final-path visibility, no-overwrite and retry on the real filesystem."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from threading import Barrier
from unittest.mock import patch

path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name("section_20_07.py")
spec = importlib.util.spec_from_file_location("evidence_lab", path)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def check():
    rows = []
    real_open = Path.open
    real_temp = tempfile.NamedTemporaryFile

    def record(case, expected, actual):
        rows.append(dict(case=case, expected=expected, actual=actual, passed=expected == actual))

    def attempt(dest, data):
        try:
            lab.write_manifest(dest, data)
        except OSError as exc:
            return type(exc).__name__
        return "published"

    def digest(data):
        return hashlib.sha256(data).hexdigest()

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for fault in ("write", "close", "none"):
            folder = root / fault
            folder.mkdir()
            dest = folder / "manifest.json"
            seen = []

            class ObservedFile:
                def __init__(self, handle):
                    self.handle = handle
                def __enter__(self):
                    self.handle.__enter__()
                    return self
                def __getattr__(self, name):
                    return getattr(self.handle, name)
                def __exit__(self, *args):
                    result = self.handle.__exit__(*args)
                    seen.append(dest.exists())
                    if fault == "close":
                        raise OSError("injected close error")
                    return result
                def write(self, text):
                    seen.append(dest.exists())
                    if fault == "write":
                        self.handle.write(text[:12])
                        self.handle.flush()
                        raise OSError("injected write error")
                    return self.handle.write(text)

            def open_final(p, *args, **kwargs):
                return ObservedFile(real_open(p, *args, **kwargs))

            def open_stage(*args, **kwargs):
                return ObservedFile(real_temp(*args, **kwargs))

            with patch.object(Path, "open", open_final), patch.object(
                    tempfile, "NamedTemporaryFile", open_stage):
                result = attempt(dest, b"abc")
            record(fault+" hidden through close", [False, False], seen)
            if fault != "none":
                files = sorted(p.name for p in folder.iterdir())
                leftover = dest.read_bytes().hex() if dest.exists() else None
                record(fault+" propagated without final or staging file",
                       ["OSError", [], None], [result, files, leftover])
                result = attempt(dest, b"abc")
            parsed = json.loads(dest.read_bytes()) if result == "published" else None
            record(fault+" complete artifact and no staging file",
                   ["published", ["manifest.json"], digest(b"abc"), "pending"],
                   [result, sorted(p.name for p in folder.iterdir()),
                    parsed and parsed["input_sha256"], parsed and parsed["approval_status"]])

        folder = root / "race"
        folder.mkdir()
        dest = folder / "manifest.json"
        gate = Barrier(2, timeout=5)
        def compete(data):
            gate.wait()
            return attempt(dest, data)
        inputs = (b"first", b"second")
        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(compete, inputs))
        winner = inputs[statuses.index("published")]
        complete = json.loads(dest.read_bytes())["input_sha256"]
        record("competing writers leave exactly the winner's document",
               [["FileExistsError", "published"], digest(winner), ["manifest.json"]],
               [sorted(statuses), complete, sorted(p.name for p in folder.iterdir())])
        original = dest.read_bytes()
        record("separate collision preserves exact bytes",
               ["FileExistsError", True, ["manifest.json"]],
               [attempt(dest, b"third"), original == dest.read_bytes(),
                sorted(p.name for p in folder.iterdir())])
    print(json.dumps(rows, allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__ == "__main__":
    raise SystemExit(0 if check() else 1)
