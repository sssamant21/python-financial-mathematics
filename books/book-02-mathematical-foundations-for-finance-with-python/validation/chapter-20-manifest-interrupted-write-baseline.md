# Section 20.7 interrupted manifest writes: baseline

[Execution provenance follow-up](chapter-20-execution-provenance-followup.md) covers the recording of an actual worker result. The separate COV-86 obligation concerns what the shared writer leaves behind when writing is interrupted.

Reproduced on [source `641c6ad0304d242fd3a780b12908726b4778d724`](https://github.com/sssamant21/python-financial-mathematics/blob/641c6ad0304d242fd3a780b12908726b4778d724/books/book-02-mathematical-foundations-for-finance-with-python/chapter-20/code/section_20_07.py) (module blob `09e7a7364b5b0013e93873c23b8b221e07f3037f`). In a temporary directory, a wrapper around the real file object wrote and flushed the first 12 characters of the payload and then raised `OSError("injected write interruption")`. The public `write_manifest` propagated the error, left the 12-byte prefix `7b0a20202261637475616c5f` at the final path, and the bytes failed JSON parsing. A normal retry hit `FileExistsError`. No process crash or durability failure was simulated.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import section_20_07 as lab

real_open = Path.open

class FailingFile:
    def __init__(self, handle):
        self.handle = handle
    def __enter__(self):
        self.handle.__enter__()
        return self
    def __exit__(self, *args):
        return self.handle.__exit__(*args)
    def write(self, text):
        self.handle.write(text[:12])
        self.handle.flush()
        raise OSError("injected write interruption")

with TemporaryDirectory() as d:
    path = Path(d) / "manifest.json"
    with patch.object(Path, "open", lambda p, *a, **k: FailingFile(real_open(p, *a, **k))):
        try:
            lab.write_manifest(path, b"abc")
        except OSError as exc:
            assert str(exc) == "injected write interruption"
        else:
            raise AssertionError("expected injected write error")
    assert path.read_bytes().hex() == "7b0a20202261637475616c5f"
    try:
        json.loads(path.read_bytes())
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("expected a partial document")
    try:
        lab.write_manifest(path, b"abc")
    except FileExistsError:
        pass
    else:
        raise AssertionError("partial artifact should block this baseline retry")
```

Next: preserve no-overwrite behavior while ensuring a failed write never exposes an incomplete final manifest. Exercise the shared publication path, write and close failures, retry, collisions and staging cleanup. Distinguish local visibility guarantees from crash durability and authenticity.
