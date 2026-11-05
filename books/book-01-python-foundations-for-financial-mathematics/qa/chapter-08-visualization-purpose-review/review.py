"""Section 8.1: exact lab and independent rational checks."""
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import types
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'chapter-08/8.01-why-visualization-matters.md'
EXPECTED = """CALM: endpoint=20.00%; known intervals=4/4
DIP: endpoint=20.00%; known intervals=4/4
GAP: endpoint=20.00%; known intervals=2/4
Saved output/why_visualization.png
"""


def main():
    source = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', source, re.M | re.S)
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-81-') as tmp:
        lab = Path(tmp) / 'visualization_lab_81'
        lab.mkdir()
        for name, body in [('visualization_purpose.py', program), ('test_visualization_purpose.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['visualization_purpose.py']),
            ('compilation', ['-m', 'compileall', '-q', '.']),
        ]:
            p = subprocess.run([sys.executable, '-B', '-W', 'error::FutureWarning', *args],
                               env=env, cwd=lab, capture_output=True, text=True, timeout=60)
            count = re.search(r'Ran (\d+) tests?', p.stderr)
            methods = int(count[1]) if count else None
            if label == 'test discovery':
                ok = methods == 8 and bool(re.search(r'^OK\s*$', p.stderr, re.M))
            elif label == 'demonstration':
                ok = p.stdout == EXPECTED and not p.stderr
            else:
                ok = not (p.stdout or p.stderr)
            commands.append(dict(label=label, args=args, returncode=p.returncode, stdout=p.stdout,
                                 stderr=p.stderr, methods=methods, passed=ok and p.returncode == 0))
        png = lab / 'output/why_visualization.png'
        if png.exists():
            (HERE / 'why_visualization.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))

    module = types.ModuleType('exact_purpose')
    exec(compile(program, str(SOURCE), 'exec'), module.__dict__)
    days, prices, names = module.fixture()
    _, indexed, returns = module.prepare(days, prices, names)
    rows = [[100, 105, 110, 115, 120], [200, 160, 180, 210, 240], [50, 49, None, 56, 60]]
    exp_idx = np.array([[100 * float(Fraction(x, col[0])) if x is not None else np.nan
                         for x in col] for col in rows]).T
    exp_r = np.array([[float(Fraction(b, a) - 1) if a is not None and b is not None else np.nan
                       for a, b in zip(col, col[1:])] for col in rows]).T
    check('all indexed values match rational reference',
          np.allclose(indexed, exp_idx, atol=1e-12, rtol=0, equal_nan=True), expected=repr(exp_idx))
    check('all adjacent returns match rational reference',
          np.allclose(returns, exp_r, atol=1e-12, rtol=0, equal_nan=True), expected=repr(exp_r))
    check('80 to 92 gives index 115 and return 15%',
          np.allclose([100 * float(Fraction(92,80)), float(Fraction(92,80)-1)], [115, .15]))
    scaled = prices.copy()
    scaled[:, 1] *= 7
    _, scaled_idx, scaled_r = module.prepare(days, scaled, names)
    check('DIP scale by seven leaves transformed arrays unchanged',
          np.allclose(indexed, scaled_idx, atol=1e-12, rtol=0, equal_nan=True) and
          np.allclose(returns, scaled_r, atol=1e-12, rtol=0, equal_nan=True))
    mask = days != 4
    x, _, dropped = module.prepare(days[mask], prices[mask], names)
    check('dropping day 4 makes a distinct four-day GAP interval',
          x[2]-x[1] == 4 and abs(dropped[1,2]-float(Fraction(56,49)-1)) < 1e-12)
    fig, (upper, lower) = module.build_figure(days, prices, names)
    try:
        check('artists preserve irregular elapsed-day coordinates',
              np.array_equal(upper.lines[0].get_xdata(), [0,1,4,5,8]) and
              np.array_equal(lower.lines[0].get_xdata(), [1,4,5,8]))
        check('GAP artists preserve price and return omissions',
              np.isnan(upper.lines[2].get_ydata()).tolist() == [False,False,True,False,False] and
              np.isnan(lower.lines[2].get_ydata()).tolist() == [False,True,True,False])
        check('DIP first plotted return expressed in percent',
              abs(lower.lines[1].get_ydata()[0] - (-20)) < 1e-12)
    finally:
        module.plt.close(fig)
    import warnings
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always')
        try:
            extreme_fig, extreme_axes = module.build_figure(
                np.array([0, 1, 2]), np.array([[1.], [1e-308], [1.]]), ('A',))
        except ValueError as error:
            check('unsupported percentage is rejected before rendering',
                  'percentage' in str(error), actual=str(error))
        else:
            check('unsupported percentage is rejected before rendering', False,
                  actual=repr(extreme_axes[1].lines[0].get_ydata()))
            module.plt.close(extreme_fig)
    checks[-1]['warnings'] = [str(w.message) for w in observed]
    out = dict(python=platform.python_version(), numpy=np.__version__,
               matplotlib=module.matplotlib.__version__, platform=platform.platform(),
               png_sha256=sha((HERE / "why_visualization.png").read_bytes()),
               source_sha256=sha(source), program_sha256=sha(program), tests_sha256=sha(tests),
               commands=commands, checks=checks)
    (HERE/'results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(len(commands), len(checks), sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
