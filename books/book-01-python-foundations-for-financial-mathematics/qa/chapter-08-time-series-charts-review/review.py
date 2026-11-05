"""Section 8.4: exact lab, rational base ratios and DST artist checks."""
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
from importlib.metadata import version
from zoneinfo import TZPATH

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'chapter-08/8.04-financial-time-series-charts.md'
EXPECTED = """Expected instants: 6; source rows: 5
Absent rows: 1; observed price cells: 9/12
2026-11-01 01:30 EDT -0400
2026-11-01 01:30 EST -0500
Saved output/financial_time_series.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-84-') as tmp:
        lab = Path(tmp) / 'visualization_lab_84'
        lab.mkdir()
        for name, body in [('time_series_charts.py', program), ('test_time_series_charts.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['time_series_charts.py']),
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
        png = lab / 'output/financial_time_series.png'
        if png.exists():
            (HERE / 'financial_time_series.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m = types.ModuleType('exact_time_series')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    source, grid=m.fixture()
    aligned,indexed,present=m.prepare(source,grid)
    check('observed cell counts per instant',aligned.notna().sum(axis=1).tolist()==[2,2,0,1,2,2])
    check('presence distinct from cell counts',present.tolist()==[True,True,False,True,True,True])
    values=[[100,200],[101,202],[None,None],[103,None],[102,204],[104,206]]
    oracle=np.array([[float(100*Fraction(v,base)) if v is not None else np.nan
                     for v,base in zip(row,[100,200])] for row in values])
    check('independent base ratios for every observed price',
          np.allclose(indexed.to_numpy(),oracle,rtol=0,atol=1e-12,equal_nan=True),expected=repr(oracle))
    converted=source.copy()
    converted.index=converted.index.tz_convert('Asia/Tokyo')
    check('different aware timezone yields identical aligned values and flags',
          all(a.equals(b) for a,b in zip(m.prepare(converted,grid),(aligned,indexed,present))))
    missing=source.copy();missing.iloc[0,1]=np.nan
    try: m.prepare(missing,grid)
    except ValueError as error: check('missing common baseline rejected','starting prices' in str(error))
    else: check('missing common baseline rejected',False)
    empty=source.copy();empty.iloc[2]=np.nan
    ea,_,ep=m.prepare(empty,grid)
    check('present all-missing row and absent row both zero but flags differ',
          ea.iloc[2:4].notna().sum(axis=1).tolist()==[0,0] and ep.iloc[2:4].tolist()==[False,True])
    fig,(top,bottom)=m.build_figure(source,grid)
    try:
        x=top.lines[0].get_xdata()
        formatter=bottom.xaxis.get_major_formatter()
        check('artist UTC spacing is one hour across clock rollback',
              np.allclose(np.diff(x)*24,[1]*5,rtol=0,atol=1e-8))
        check('repeated local labels differ by offset',
              [formatter(y) for y in x[1:3]]==['01:30\nEDT -0400','01:30\nEST -0500'])
        check('absence marker shown only at the missing row',
              np.array_equal(bottom.lines[1].get_xdata(),x[2:3]))
    finally:
        m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
             matplotlib=m.matplotlib.__version__,tzdata_package=version('tzdata'),zoneinfo_search=list(TZPATH),
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'financial_time_series.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
