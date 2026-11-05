"""Section 8.3: exact lab and independent gap and step checks."""
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
SOURCE = HERE.parents[1] / 'chapter-08/8.03-line-charts.md'
EXPECTED = """Source observations: 6; plotted rows: 7
Observed account values: 11/12
Inserted gap-separator rows: 1
Saved output/line_charts.png
"""

def main():
    source = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', source, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-83-') as tmp:
        lab = Path(tmp) / 'visualization_lab_83'
        lab.mkdir()
        for name, body in [('line_charts.py', program), ('test_line_charts.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['line_charts.py']),
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
        png = lab / 'output/line_charts.png'
        if png.exists():
            (HERE / 'line_charts.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m = types.ModuleType('exact_lines')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    d,v,q=m.fixture()
    x, observed, shares, plot_x, plot_y=m.prepare(d,v,q)
    check('supplemental linear midpoint is 1015 and is absent from source',
          Fraction(1020+1010,2)==1015 and 2 not in x)
    check('duration equal to threshold keeps day 1 to 3 adjacent',
          plot_x.tolist()[:3]==[0,1,3] and np.isfinite(plot_y[1:3]).all())
    check('one rendering separator before day 7, not a source row',
          plot_x.tolist()==[0,1,3,4,7,7,8] and np.isnan(plot_y[4]).all() and len(x)==6)
    check('observed source count is 11 and source missing value persists',
          int(np.isfinite(observed).sum())==11 and np.isnan(observed[3,0]))
    _,_,_,wide_x,wide_y=m.prepare(d,v,q,max_gap=3)
    check('threshold three reconnects Account B across day 4 to 7',
          wide_x.tolist()==d.tolist() and wide_y[3:5,1].tolist()==[1015,1030])
    check('threshold three preserves source missing Account A at day 4',
          np.isnan(wide_y[3,0]))
    check('supplemental lookup gives 12 shares at day 2',
          shares[np.searchsorted(x,2,side='right')-1]==12)
    check('repeated day 4 state remains eight',shares[2:4].tolist()==[8,8])
    fig,(upper,lower)=m.build_figure(d,v,q)
    try:
        check('exact artists retain separate account and ledger contracts',
              np.isnan(upper.lines[0].get_ydata()[3]) and
              lower.lines[0].get_drawstyle()=='steps-post' and
              np.array_equal(lower.lines[0].get_ydata(),q))
    finally:
        m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(source),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'line_charts.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
