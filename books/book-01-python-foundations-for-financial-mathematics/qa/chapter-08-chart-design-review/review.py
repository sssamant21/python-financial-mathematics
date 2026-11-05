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
SOURCE = HERE.parents[1] / 'chapter-08/8.12-effective-financial-chart-design.md'
EXPECTED = """Observed: 4/5; unknown: 1
Displayed order: DELTA, ALPHA, GAMMA, BETA
Unknown and omitted: EPSILON
Saved output/financial_chart.png
Saved output/financial_chart.svg
Saved output/financial_chart_monochrome.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-812-') as tmp:
        lab = Path(tmp) / 'visualization_lab_812'
        lab.mkdir()
        for name, body in [('chart_design.py', program), ('test_chart_design.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['chart_design.py']),
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
        png = lab / 'output/financial_chart.png'
        if png.exists():
            (HERE / 'financial_chart.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
        from xml.etree import ElementTree
        svg=lab/'output/financial_chart.svg'
        mono=lab/'output/financial_chart_monochrome.png'
        check('SVG parses and monochrome PNG is distinct',
              ElementTree.parse(svg).getroot().tag.endswith('}svg') and
              mono.read_bytes().startswith(b'\x89PNG\r\n\x1a\n') and
              sha(mono.read_bytes())!=sha(png.read_bytes()))
        (HERE/'financial_chart_monochrome.png').write_bytes(mono.read_bytes())
    m=types.ModuleType('exact_chart_design')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    values,start,end=m.fixture()
    observed,missing,times=m.prepare(values,start,end)
    check('independent numeric descending order with labeled values',
          observed.asset.tolist()==['DELTA','ALPHA','GAMMA','BETA'] and
          observed['return'].tolist()==[.04,.025,0,-.01])
    check('missing retained as omission not numeric zero',missing==['EPSILON'] and len(observed)==4)
    ties=values.copy();ties.loc['ALPHA']=.04
    tied=m.prepare(ties,start,end)[0]
    check('controlled tie orders asset labels ascending',tied.asset.tolist()[:2]==['ALPHA','DELTA'])
    for mono in (False,True):
        fig,ax=m.build_figure(values,start,end,mono)
        try:
            check(str(mono)+' signed artist widths match fractions',
                  np.allclose([b.get_width() for b in ax.patches],
                              [float(Fraction(x,1000)) for x in [40,25,0,-10]],atol=1e-12,rtol=0))
            check(str(mono)+' direct signs and hatch preserved',
                  [t.get_text() for t in ax.texts]==['+4.0%','+2.5%','+0.0%','-1.0%'] and
                  [p.get_hatch() for p in ax.patches]==[None,None,None,'//'])
            check(str(mono)+' visible zero marker remains',ax.lines[0].get_xdata().tolist()==[0])
            check(str(mono)+' common UTC window and omission note',
                  '2026-01-01 00:00 to 2026-02-01 00:00 UTC' in ax.get_title(loc='left') and
                  'EPSILON' in fig.texts[0].get_text())
        finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'financial_chart.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
