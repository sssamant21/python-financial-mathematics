"""Reference checks for manifest behavior; runtime validation pending."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from section_20_07 import input_digest, make_manifest, write_manifest

class EvidenceChecks(unittest.TestCase):
    def test_known_hash(self):
        self.assertEqual(input_digest(b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    def test_bytes_required(self):
        with self.assertRaises(TypeError): input_digest("abc")
    def test_hash_changes(self): self.assertNotEqual(input_digest(b"a"), input_digest(b"b"))
    def test_empty_hash(self): self.assertEqual(input_digest(b""), hashlib.sha256(b"").hexdigest())
    def test_pending_execution(self): self.assertEqual(make_manifest(b"x")["execution_status"], "not run")
    def test_pending_review(self): self.assertEqual(make_manifest(b"x")["review_status"], "pending")
    def test_pending_approval(self): self.assertEqual(make_manifest(b"x")["approval_status"], "pending")
    def test_no_result_claim(self): self.assertIsNone(make_manifest(b"x")["actual_result"])
    def test_no_commit_claim(self): self.assertIsNone(make_manifest(b"x")["source_commit"])
    def test_expected_value(self): self.assertEqual(make_manifest(b"x")["expected_result"], 100)
    def test_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "evidence.json"
            write_manifest(p, b"sample")
            self.assertEqual(json.loads(p.read_text(encoding="utf-8"))["input_sha256"], input_digest(b"sample"))
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "evidence.json"
            p.write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError): write_manifest(p, b"sample")
            self.assertEqual(p.read_text(encoding="utf-8"), "existing")

if __name__ == "__main__": unittest.main()
