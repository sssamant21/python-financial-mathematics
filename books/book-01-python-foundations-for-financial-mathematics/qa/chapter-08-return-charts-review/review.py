"""Section 8.5: exact lab and independent return-path checks."""
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
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'chapter-08/8.05-return-charts.md'
EXPECTED = """Known adjacent intervals: 3/5
Endpoint-only price change: 8.00%
Last finite linked value: -1.00%
Final linked value unknown: True
Saved output/return_charts.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-85-') as tmp:
        lab = Path(tmp) / 'visualization_lab_85'
        lab.mkdir()
        for name, body in [('return_charts.py', program), ('test_return_charts.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['return_charts.py']),
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
        png = lab / 'output/return_charts.png'
        if png.exists():
            (HERE / 'return_charts.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_return_charts')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    p=m.fixture()
    data,endpoint=m.calculate(p)
    check('supplemental exact compounding gives -4 percent',
          Fraction(6,5)*Fraction(4,5)-1==Fraction(-1,25))
    check('baseline adjacent undefined and linked baseline zero',
          np.isnan(data.simple.iloc[0]) and data.linked.iloc[0]==0)
    check('known simple returns match independent fractions',
          np.allclose(data.simple,[np.nan,float(Fraction(1,10)),float(Fraction(-1,10)),
                      np.nan,np.nan,0],atol=1e-12,rtol=0,equal_nan=True))
    check('last zero observed while strict path stays unknown',
          data.simple.iloc[-1]==0 and np.allclose(data.linked,[0,.1,-.01,np.nan,np.nan,np.nan],
                      atol=1e-12,rtol=0,equal_nan=True))
    check('independent endpoint comparison',abs(endpoint-float(Fraction(108,100)-1))<1e-12)
    gap=p.dropna()
    try: m.calculate(gap)
    except ValueError as error: check('exact source rejects a deleted expected day','consecutive' in str(error))
    else: check('exact source rejects a deleted expected day',False)
    check('supplemental Jan 3 to Jan 5 ratio is 1/11 over 48 hours',
          (gap.index[3]-gap.index[2])==pd.Timedelta(days=2) and Fraction(108,99)-1==Fraction(1,11))
    full=p.copy();full.iloc[3]=105
    linked,complete_endpoint=m.calculate(full)
    exact_prices=[100,110,99,105,108,108]
    from math import prod
    rational=prod(Fraction(b,a) for a,b in zip(exact_prices,exact_prices[1:]))-1
    check('full synthetic path telescopes',abs(linked.linked.iloc[-1]-float(rational))<1e-12
          and abs(complete_endpoint-float(rational))<1e-12 and rational==Fraction(2,25))
    fig,(bars,missing,cumulative)=m.build_figure(p)
    try:
        formatter=bars.yaxis.get_major_formatter()
        check('source percent scale uses one as 100%',
              formatter.xmax==1 and formatter.convert_to_pct(-.025)==-2.5)
        check('missing markers and observed zero are separate',
              len(missing.lines[0].get_xdata())==2 and len(bars.lines[0].get_xdata())==1
              and bars.lines[0].get_ydata().tolist()==[0])
        check('source linked artist stops after first missing interval',
              np.isnan(cumulative.lines[0].get_ydata()).tolist()==[False,False,False,True,True,True])
    finally:
        m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'return_charts.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
