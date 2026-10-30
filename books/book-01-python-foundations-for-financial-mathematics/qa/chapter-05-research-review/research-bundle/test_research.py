from decimal import Inexact, ROUND_DOWN, localcontext
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from research import analyze, bundle, digest

ROOT = Path(__file__).resolve().parent
DATA = (ROOT / 'inflows.json').read_bytes()
CONFIG = (ROOT / 'settings.json').read_bytes()
SOURCE = (ROOT / 'research.py').read_bytes()

class ResearchTests(unittest.TestCase):
    def test_known_answer_and_policy(self):
        result = analyze(DATA, CONFIG)
        self.assertEqual(result['total'], '30.01')
        self.assertEqual(result['count'], 2)
        self.assertEqual(result['method'], 'sum_then_round')
        # Rounding each 10.005 and 20.005 first would instead yield 30.00.

    def test_context_isolation(self):
        expected = analyze(DATA, CONFIG)
        with localcontext() as context:
            context.prec = 2
            context.rounding = ROUND_DOWN
            context.traps[Inexact] = True
            self.assertEqual(analyze(DATA, CONFIG), expected)
            self.assertEqual(context.prec, 2)
            self.assertTrue(context.traps[Inexact])

    def test_repeat_bundle(self):
        self.assertEqual(bundle(DATA, CONFIG, SOURCE), bundle(DATA, CONFIG, SOURCE))

    def test_byte_identity_versus_result(self):
        changed = DATA + b'\n'
        self.assertNotEqual(digest(DATA), digest(changed))
        self.assertEqual(analyze(DATA, CONFIG), analyze(changed, CONFIG))

    def test_changed_data_and_source(self):
        changed = DATA.replace(b'10.005', b'11.005')
        self.assertEqual(analyze(changed, CONFIG)['total'], '31.01')
        self.assertNotEqual(bundle(DATA, CONFIG, SOURCE)['evidence']['source_sha256'],
                            bundle(DATA, CONFIG, SOURCE+b'\n')['evidence']['source_sha256'])

    def test_invalid_records(self):
        baseline = json.loads(DATA)
        for amount in ('NaN', '-1', '1e2', ' 1', '1000001', '1.00001', 1, None):
            rows = [dict(baseline[0], amount=amount)]
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                analyze(json.dumps(rows).encode(), CONFIG)
        for rows in ([], baseline*2, [dict(baseline[0], currency='EUR')], [{}]):
            with self.assertRaises(ValueError):
                analyze(json.dumps(rows).encode(), CONFIG)

    def test_config_and_duplicate_members(self):
        with self.assertRaises(ValueError):
            analyze(DATA, CONFIG.replace(b'ROUND_HALF_EVEN', b'ROUND_DOWN'))
        with self.assertRaises(ValueError):
            analyze(b'[{"id":"A","id":"B"}]', CONFIG)

    def test_cli_rerun_and_no_overwrite(self):
        with TemporaryDirectory() as directory:
            paths = [Path(directory)/name for name in ('a.json', 'b.json')]
            for path in paths:
                result = subprocess.run([sys.executable, str(ROOT/'research.py'),
                    '--input', str(ROOT/'inflows.json'), '--config', str(ROOT/'settings.json'),
                    '--output', str(path)], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())
            before = paths[0].read_bytes()
            failed = subprocess.run([sys.executable, str(ROOT/'research.py'),
                '--input', str(ROOT/'inflows.json'), '--config', str(ROOT/'settings.json'),
                '--output', str(paths[0])], capture_output=True, text=True, timeout=10)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(paths[0].read_bytes(), before)

    def test_invalid_input_creates_no_report(self):
        with TemporaryDirectory() as directory:
            bad, output = Path(directory)/'bad.json', Path(directory)/'out.json'
            bad.write_text('[]', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'research.py'),
                '--input', str(bad), '--config', str(ROOT/'settings.json'), '--output', str(output)],
                capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

if __name__ == '__main__':
    unittest.main(verbosity=2)
