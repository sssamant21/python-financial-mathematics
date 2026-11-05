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
SOURCE = HERE.parents[1] / 'chapter-08/8.07-scatter-plots-and-relationships.md'
EXPECTED = """Expected: 8; complete pairs: 6; excluded: 2
Benchmark absent endpoints: 1
Asset explicit missing cells: 1
Paired sample Pearson r: 0.9388
Saved output/scatter_relationships.png
"""

def main():
    manuscript = SOURCE.read_bytes()
    program, tests = re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60', manuscript, re.M | re.S)[-2:]
    commands, checks = [], []
    sha = lambda b: hashlib.sha256(b).hexdigest()

    def check(label, condition, **detail):
        checks.append(dict(label=label, passed=bool(condition), **detail))

    with tempfile.TemporaryDirectory(prefix='chapter08-87-') as tmp:
        lab = Path(tmp) / 'visualization_lab_87'
        lab.mkdir()
        for name, body in [('scatter_relationships.py', program), ('test_scatter_relationships.py', tests)]:
            (lab / name).write_bytes(body)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME')}
        env['MPLCONFIGDIR'] = str(Path(tmp) / 'mpl')
        for label, args in [
            ('test discovery', ['-m', 'unittest', '-v']),
            ('demonstration', ['scatter_relationships.py']),
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
        png = lab / 'output/scatter_relationships.png'
        if png.exists():
            (HERE / 'scatter_relationships.png').write_bytes(png.read_bytes())
        check('PNG produced at documented relative path', png.exists() and png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    m=types.ModuleType('exact_scatter')
    exec(compile(program,str(SOURCE),'exec'),m.__dict__)
    benchmark,asset,grid=m.fixture()
    aligned,pairs,report=m.prepare(benchmark,asset,grid)
    check('matched pair date identifies 2%,1% point',
          pairs.loc[pd.Timestamp('2026-01-07T00:00:00Z')].tolist()==[.02,.01])
    check('explicit missing and absent rows are distinct',
          (aligned.loc[grid[2],['asset_present','complete']].tolist()==[True,False]) and
          (aligned.loc[grid[7],['benchmark_present','complete']].tolist()==[False,False]))
    check('zero pair retained',pairs.loc[grid[3]].tolist()==[0,0])
    check('supplemental vertical difference is half a percentage point',
          Fraction(15,1000)-Fraction(1,100)==Fraction(5,1000))
    # Independent centered integer sums; units here are half-percentage-points.
    xs=[-6,-4,0,2,4,6];ys=[-4,-2,0,3,2,8]
    n=len(xs);sx=sum(xs);sy=sum(ys)
    numerator=n*sum(x*y for x,y in zip(xs,ys))-sx*sy
    denominator=((n*sum(x*x for x in xs)-sx*sx)*(n*sum(y*y for y in ys)-sy*sy))**.5
    check('independent centered-sum correlation',
          abs(report['correlation']-numerator/denominator)<1e-12,
          numerator=numerator,denominator_squared=(n*sum(x*x for x in xs)-sx*sx)*(n*sum(y*y for y in ys)-sy*sy))
    linear=benchmark*2+.01
    _,_,linear_report=m.prepare(benchmark,linear,grid)
    check('controlled affine relation has unit correlation but slope two',
          abs(linear_report['correlation']-1)<1e-12)
    zero=benchmark*0
    _,zero_pairs,zero_report=m.prepare(zero,asset,grid)
    check('constant input still displays pairs but withholds coefficient',
          len(zero_pairs)==6 and zero_report['correlation'] is None)
    rev=m.prepare(benchmark.iloc[::-1],asset.iloc[::-1],grid)
    check('source reversal preserves aligned frames and report',
          rev[0].equals(aligned) and rev[1].equals(pairs) and rev[2]==report)
    fig,ax=m.build_figure(benchmark,asset,grid)
    try:
        check('artist coordinates are exact matched pairs',
              np.array_equal(ax.collections[0].get_offsets(),pairs.to_numpy()))
        check('reference is equality with common bounds and aspect',
              np.array_equal(ax.lines[0].get_xdata(),ax.lines[0].get_ydata())
              and ax.get_xlim()==ax.get_ylim() and ax.get_aspect()==1)
    finally:m.plt.close(fig)
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
             matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(manuscript),program_sha256=sha(program),
             tests_sha256=sha(tests),png_sha256=sha((HERE/'scatter_relationships.png').read_bytes()),
             commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)


if __name__ == '__main__':
    raise SystemExit(main())
